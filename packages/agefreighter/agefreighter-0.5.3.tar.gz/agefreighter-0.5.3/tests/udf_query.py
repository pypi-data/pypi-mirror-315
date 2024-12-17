udf_query = """CREATE OR REPLACE FUNCTION {func_name}()
RETURNS VOID AS $$
DECLARE
    chunk RECORD;
    chunk_size BIGINT := {chunk_size * chunk_multiplier};
    num_offset BIGINT := 0;
    total_rows BIGINT;

    ENTRY_ID_BITS INTEGER := 32 + 16;
    ENTRY_ID_MASK BIGINT := 0x0000FFFFFFFFFFFF;
    oid BIGINT;
    first_id_s BIGINT;
    first_id_e BIGINT;
BEGIN
    -- bulk load from the Azure Storage into the temporary table
    INSERT INTO temp_from_azure_storage
    SELECT *
    FROM azure_storage.blob_get(
        '{self.storage_account_name}',
        '{self.blob_container_name}',
        '{os.path.basename(csv)}',
        options := azure_storage.options_csv_get(header := 'true'))
    AS res ({columns_in_temp_table});

    SELECT COUNT(*) INTO total_rows FROM temp_from_azure_storage;

    WHILE num_offset < total_rows LOOP
        -- bulk insert the start vertices
        INSERT INTO "{graph_name}"."{start_v_label}" (properties)
        SELECT format('{{"id":"%s", {start_props_formatted}}}', {start_id}, {','.join([f'"{start_prop}"' for start_prop in start_props])})::agtype
        FROM (
            SELECT DISTINCT {','.join([f'"{item}"' for item in [start_id] + start_props])}
            FROM temp_from_azure_storage
            OFFSET num_offset LIMIT chunk_size
        ) AS distinct_s;

        -- bulk insert the mapping between the entryID and the id
        INSERT INTO temp_id_map (entryID, id)
        SELECT distinct_s.{start_id}, first_id_s + ROW_NUMBER() OVER () - 1
        FROM (
            SELECT DISTINCT {start_id}
            FROM temp_from_azure_storage
            OFFSET num_offset LIMIT chunk_size
        ) AS distinct_s;

        -- bulk insert the end vertices
        INSERT INTO "{graph_name}"."{end_v_label}" (properties)
        SELECT format('{{"id":"%s", {end_props_formatted}}}', {end_id}, {','.join([f'"{end_prop}"' for end_prop in end_props])})::agtype
        FROM (
            SELECT DISTINCT {','.join([f'"{item}"' for item in [end_id] + end_props])}
            FROM temp_from_azure_storage
            OFFSET num_offset LIMIT chunk_size
        ) AS distinct_e;

        -- bulk insert the mapping between the entryID and the id
        INSERT INTO temp_id_map (entryID, id)
        SELECT distinct_e.{end_id}, first_id_e + ROW_NUMBER() OVER () - 1
        FROM (
            SELECT DISTINCT {end_id}
            FROM temp_from_azure_storage
            OFFSET num_offset LIMIT chunk_size
        ) AS distinct_e;

        -- bulk insert the edge data
        INSERT INTO "{graph_name}"."{edge_type}" (start_id, end_id)
        SELECT s_map.id::agtype::graphid, e_map.id::agtype::graphid
        FROM (
            SELECT DISTINCT {start_id}, {end_id}
            FROM temp_from_azure_storage
            OFFSET num_offset LIMIT chunk_size
        ) AS af
        JOIN temp_id_map AS s_map ON af.{start_id} = s_map.entryID
        JOIN temp_id_map AS e_map ON af.{end_id} = e_map.entryID;

        num_offset := num_offset + chunk_size;
    END LOOP;

    CREATE INDEX ON "{graph_name}"."{start_v_label}" USING GIN (properties);
    CREATE INDEX ON "{graph_name}"."{start_v_label}" USING BTREE (id);

    CREATE INDEX ON "{graph_name}"."{end_v_label}" USING GIN (properties);
    CREATE INDEX ON "{graph_name}"."{end_v_label}" USING BTREE (id);

    CREATE INDEX ON "{graph_name}"."{edge_type}" USING BTREE (start_id);
    CREATE INDEX ON "{graph_name}"."{edge_type}" USING BTREE (end_id);

END;
$$ LANGUAGE plpgsql;
"""
