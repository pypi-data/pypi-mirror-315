import os
import re
import json
from .mappers import map_oracle_to_avro

def generate_avro_and_mapping(sql_file_path, avro_output_path, json_output_path, sql_output_path, date_format):
    with open(sql_file_path, 'r') as sql_file:
        sql_content = sql_file.read()

    # Extraer nombre de la tabla
    table_name_match = re.search(r'CREATE TABLE\s+"[^"]+"\."([^"]+)"', sql_content, re.IGNORECASE)
    table_name = table_name_match.group(1).lower() if table_name_match else "unknown_table"

    # Extraer columnas
    columns = re.findall(r'"([^"]+)"\s+([A-Z0-9\(\),\s]+)', sql_content, re.IGNORECASE)

    # Crear esquema Avro
    avro_schema = {
        "type": "record",
        "name": table_name,
        "fields": []
    }

    # Mapeo JSON
    field_mappings = []
    column_names_types = []

    for column_name, column_type in columns:
        if column_name.lower() == table_name:
            continue  # Evitar campo si coincide con nombre de tabla

        # Mapeo Avro
        avro_type = map_oracle_to_avro(column_type)

        # Ajustar tipo para el JSON
        if isinstance(avro_type, dict) and avro_type.get("logicalType") == "decimal":
            json_type = "numeric"
        elif avro_type == "long":
            json_type = "int"
        else:
            json_type = avro_type

        # Añadir al esquema Avro
        avro_schema["fields"].append({
            "name": column_name,
            "type": ["null", avro_type] if isinstance(avro_type, str) else ["null", avro_type]
        })

        # Añadir al mapeo JSON
        field_mappings.append((column_name.upper(), json_type))

        # Mantener el nombre y tipo original para SQL
        column_names_types.append((column_name, column_type.strip().upper()))

    # Guardar esquema Avro
    if not os.path.isdir(avro_output_path):
        os.makedirs(avro_output_path)
    avro_file_path = os.path.join(avro_output_path, f"{table_name}.avsc")
    with open(avro_file_path, 'w') as avro_file:
        json.dump(avro_schema, avro_file, indent=4)

    # Guardar mapeo JSON (como dict)
    if not os.path.isdir(json_output_path):
        os.makedirs(json_output_path)
    json_file_path = os.path.join(json_output_path, f"{table_name}.json")
    with open(json_file_path, 'w') as json_file:
        # Convertir la lista a dict
        json.dump(dict(field_mappings), json_file, indent=4)

    # Generar consulta SQL
    select_columns = []
    for col_name, col_type in column_names_types:
        if col_name.lower() == table_name:
            continue
        if col_type.startswith("DATE"):
            format_string = 'YYYY-MM-DD HH24:MI:SS' if date_format == 'datetime' else 'YYYY-MM-DD'
            select_columns.append(f"TO_CHAR({col_name}, '{format_string}') AS {col_name}")
        else:
            select_columns.append(col_name)

    select_columns_str = ",\n    ".join(select_columns)
    sql_query = f"SELECT\n    {select_columns_str}\nFROM\n    {table_name.upper()}\nWHERE\n    ROWNUM <= 100"

    if not os.path.isdir(sql_output_path):
        os.makedirs(sql_output_path)
    sql_query_file_path = os.path.join(sql_output_path, f"{table_name}.sql")
    with open(sql_query_file_path, 'w') as query_file:
        query_file.write(sql_query)

    print(f"Generado Avro: {avro_file_path}")
    print(f"Generado JSON: {json_file_path}")
    print(f"Generado SQL: {sql_query_file_path}")

def process_multiple_sql_files(input_folder, avro_output_folder, json_output_folder, sql_output_folder, date_format='datetime'):
    if not os.path.isdir(input_folder):
        raise ValueError("La carpeta de entrada no existe.")

    sql_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.sql')]
    if not sql_files:
        raise ValueError("No se encontraron archivos SQL en la carpeta de entrada.")

    for sql_file in sql_files:
        sql_file_path = os.path.join(input_folder, sql_file)
        generate_avro_and_mapping(sql_file_path, avro_output_folder, json_output_folder, sql_output_folder, date_format)

    print("Proceso finalizado. Todos los archivos generados correctamente.")


def generate_bigquery_table_scripts(config_folder, config_file=None, output_folder="sql/bigquery/scripts/"):
    """
    Genera scripts de creación de tablas en BigQuery con base en un archivo de configuración y esquemas Oracle.
    """
    # Verificar si existe la carpeta de configuración
    if not os.path.isdir(config_folder):
        raise ValueError(f"La carpeta de configuración no existe: {config_folder}")
    
    # Archivos de configuración a procesar
    config_files = []
    if config_file:
        config_files.append(config_file)
    else:
        config_files = [
            os.path.join(config_folder, f) for f in os.listdir(config_folder)
            if f.endswith(".json")
        ]

    if not config_files:
        raise ValueError("No se encontraron archivos de configuración en la carpeta especificada.")

    # Crear carpeta de salida si no existe
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for file in config_files:
        with open(file, 'r') as f:
            config = json.load(f)

        table_name = config.get("table_name")
        zones = config.get("zone", [])  # Acepta una lista o un string
        if isinstance(zones, str):  # Convertir string a lista si es necesario
            zones = [zones]
        partition_field = config.get("partition_field")
        clustering_fields = config.get("clustering_fields", [])
        partition_type = config.get("partition_type", "DAY")
        partition_data_type = config.get("partition_data_type", "DATE")
        date_field_type = config.get("date_field_type", "DATE")
        dataset = config.get("dataset")
        labels = config.get("labels", [])  # Nuevo campo tags

        if not table_name:
            raise ValueError(f"El archivo de configuración {file} no contiene el campo obligatorio 'table_name'.")
        if not dataset:
            raise ValueError(f"El archivo de configuración {file} no contiene el campo obligatorio 'dataset'.")
        if not labels:
            raise ValueError(f"El archivo de configuración {file} no contiene el campo obligatorio 'labels'.")
        if not zones:
            raise ValueError(f"El archivo de configuración {file} no contiene el campo obligatorio 'zone'.")
        
        # Generar el script de creación
        for zone in zones:
            zone_dataset = "staging_dataset" if zone == "stg" else dataset
            bq_table_name = f"{zone}_{table_name.lower()}"
            script_lines = [f"CREATE TABLE `${{PROJECT_NAME}}.{zone_dataset}.{bq_table_name}` ("]
            schema_path = f"schemas/oracle/{table_name}.sql"
            
            if not os.path.exists(schema_path):
                raise FileNotFoundError(f"No se encontró el esquema Oracle para la tabla: {table_name}")

            # Leer esquema Oracle y convertir los tipos
            with open(schema_path, 'r') as schema_file:
                schema_content = schema_file.readlines()
                for line in schema_content:
                    column_match = re.match(r'^\s*"([^"]+)"\s+([A-Z0-9\(\),\s]+)', line)
                    if column_match:
                        column_name, column_type = column_match.groups()
                        column_name = column_name.lower()  # Nombres en minúsculas
                        column_type = column_type.strip().upper()

                        # Mapear tipos de datos
                        if column_type.startswith("DATE"):
                            column_type = date_field_type  # Convertir tipo de fecha
                        elif column_type.startswith("VARCHAR2") or column_type.startswith("CHAR"):
                            column_type = "STRING"
                        elif column_type.startswith("NUMBER"):
                            if "," in column_type:  # NUMBER(p, s)
                                match = re.match(r"NUMBER\((\d+),\s*(\d+)\)", column_type)
                                if match:
                                    precision, scale = map(int, match.groups())
                                    if precision > 38:  # Precisión grande → BIGNUMERIC
                                        column_type = "BIGNUMERIC"
                                    else:
                                        column_type = "NUMERIC"
                                else:
                                    column_type = "NUMERIC"
                            else:  # NUMBER(p) o NUMBER sin escala
                                column_type = "INT64"
                        elif column_type.startswith("RAW"):
                            column_type = "BYTES"
                        elif column_type in ["CLOB", "NCLOB"]:
                            column_type = "STRING"
                        elif column_type == "BLOB":
                            column_type = "BYTES"
                        else:
                            column_type = "STRING"  # Tipo por defecto

                        script_lines.append(f"  {column_name} {column_type},")
            
            # Agregar campos por defecto
            script_lines.append("  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),")
            script_lines.append("  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()")

            # Remover la última coma
            if script_lines[-1].endswith(","):
                script_lines[-1] = script_lines[-1][:-1]

            script_lines.append(")")

            # Añadir configuración de partición (opcional)
            if partition_field:
                if partition_data_type == "TIMESTAMP":
                    if partition_type in ["DAY", "MONTH", "YEAR"]:
                        trunc_expression = f"TIMESTAMP_TRUNC({partition_field.lower()}, {partition_type})"
                        partition_config = f"PARTITION BY {trunc_expression}"
                    else:
                        raise ValueError(f"Tipo de partición inválido para TIMESTAMP: {partition_type}")
                elif partition_data_type == "DATE":
                    if partition_type == "DAY":
                        partition_config = f"PARTITION BY {partition_field.lower()}"
                    else:
                        raise ValueError(f"Tipo de partición inválido para DATE: {partition_type}")
                elif partition_data_type == "DATETIME":
                    if partition_type in ["DAY", "MONTH", "YEAR"]:
                        trunc_expression = f"DATETIME_TRUNC({partition_field.lower()}, {partition_type})"
                        partition_config = f"PARTITION BY {trunc_expression}"
                    else:
                        raise ValueError(f"Tipo de partición inválido para DATETIME: {partition_type}")
                else:
                    raise ValueError(f"Tipo de partición inválido: {partition_data_type}")
                script_lines.append(partition_config)


          

            # Añadir clustering (opcional)
            if clustering_fields:
                clustering_config = f"CLUSTER BY {', '.join([field.lower() for field in clustering_fields])}"
                script_lines.append(clustering_config)
            
            # Añadir tags (Requerido)
            if labels:
                label_list = ", ".join([f"('{label['key']}', '{label['value']}')" if isinstance(label, dict) else f"('{label}', '{label}')" for label in labels])
                script_lines.append(f"OPTIONS(labels=[{label_list}])")

            # Finalizar el script
            script = "\n".join(script_lines)

            # Guardar el script en la carpeta de salida
            output_file = os.path.join(output_folder, f"{zone}_{table_name.lower()}.sql")
            with open(output_file, 'w') as output:
                output.write(script)

            print(f"Script generado: {output_file}")
import re

def parse_oracle_schema(schema_file):
    """
    Analiza un archivo SQL con una definición de tabla Oracle (CREATE TABLE) y extrae los campos y tipos.
    """
    with open(schema_file, 'r') as file:
        content = file.read()

    # Extraer columnas del esquema
    columns = re.findall(r'"([^"]+)"\s+([A-Z0-9\(\),\s]+)', content, re.IGNORECASE)
    fields = []
    for column_name, column_type in columns:
        column_name = column_name.lower()  # Convertir a minúsculas
        column_type = column_type.strip().upper()

        # Mapear tipos de datos Oracle a BigQuery
        if column_type.startswith("NUMBER"):
            if "," in column_type:  # NUMBER(p, s)
                match = re.match(r"NUMBER\((\d+),\s*(\d+)\)", column_type)
                if match:
                    precision, scale = map(int, match.groups())
                    column_type = "NUMERIC" if precision <= 38 else "BIGNUMERIC"
            else:
                column_type = "INT64"
        elif column_type.startswith("VARCHAR2") or column_type.startswith("CHAR"):
            column_type = "STRING"
        elif column_type.startswith("DATE"):
            column_type = "DATETIME"
        elif column_type.startswith("RAW"):
            column_type = "BYTES"
        elif column_type in ["CLOB", "NCLOB"]:
            column_type = "STRING"
        elif column_type == "BLOB":
            column_type = "BYTES"
        else:
            column_type = "STRING"  # Tipo por defecto

        fields.append(column_name)

    return fields


def generate_bigquery_store_procedures(config_folder, schema_folder, output_folder):
    """
    Genera procedimientos almacenados para MERGE en BigQuery a partir de configuraciones y esquemas Oracle.
    """
    # Verificar existencia de carpetas
    if not os.path.isdir(config_folder):
        raise ValueError(f"La carpeta de configuración no existe: {config_folder}")
    if not os.path.isdir(schema_folder):
        raise ValueError(f"La carpeta de esquemas no existe: {schema_folder}")
    
    # Crear carpeta de salida si no existe
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    # Procesar cada archivo JSON de configuración
    config_files = [
        os.path.join(config_folder, f) for f in os.listdir(config_folder)
        if f.endswith(".json")
    ]

    if not config_files:
        raise ValueError("No se encontraron archivos de configuración en la carpeta especificada.")

    for config_file in config_files:
        with open(config_file, 'r') as f:
            config = json.load(f)

        table_name = config.get("table_name")
        merge_fields = config.get("merge_fields")
        dataset = config.get("dataset", "dep")  # Por defecto, 'dep'

        if not table_name or not merge_fields:
            print(f"Saltando {config_file}. 'table_name' o 'merge_fields' faltantes.")
            continue

        # Leer el esquema desde el archivo .sql
        schema_file = os.path.join(schema_folder, f"{table_name.lower()}.sql")
        if not os.path.isfile(schema_file):
            print(f"Esquema no encontrado: {schema_file}. Saltando {table_name}.")
            continue

        all_fields = parse_oracle_schema(schema_file)

        if not all_fields:
            print(f"No se encontraron campos en el esquema de {table_name}. Saltando.")
            continue

        # Preparar nombres de tabla y procedimiento
        target_table = f"{dataset}.dep_{table_name.lower()}"
        source_table = f"staging_dataset.stg_{table_name.lower()}"
        procedure_name = f"{dataset}.sp_merge_{table_name.lower()}"

        # Crear las cláusulas ON, UPDATE y INSERT
        on_clause = " AND ".join([f"T.{field} = S.{field}" for field in merge_fields])
        update_clause = ",\n      ".join([f"T.{field} = S.{field}" for field in all_fields])
        insert_fields = ",\n      ".join(all_fields)
        insert_values = ",\n      ".join([f"S.{field}" for field in all_fields])

        # Generar el procedimiento almacenado
        procedure_script = f"""
CREATE PROCEDURE `${{PROJECT_NAME}}.{procedure_name}`()
BEGIN
  MERGE `{target_table}` T
  USING `{source_table}` S
  ON {on_clause}
  WHEN MATCHED THEN
    UPDATE SET
      {update_clause}
  WHEN NOT MATCHED THEN
    INSERT (
      {insert_fields}
    )
    VALUES (
      {insert_values}
    );
END;
"""
        # Guardar el archivo
        output_file = os.path.join(output_folder, f"sp_merge_dep_{table_name.lower()}.sql")
        with open(output_file, 'w') as output:
            output.write(procedure_script)

        print(f"Procedimiento almacenado generado: {output_file}")

