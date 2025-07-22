import pandas as pd
import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account

def upload_to_bigquery():
    # Kelias iki CSV failo
    csv_file = 'daily_weather.csv'

    # Google Cloud informacija
    project_id = "optical-wall-447816-m1"
    dataset_id = "weather_data"
    table_id = "daily_weather"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # ✅ Gauti raktą iš GitHub Secret kaip JSON
    keyfile_dict = json.loads(os.environ["BIGQUERY_KEY_JSON"])

    # ✅ Autentifikacija su raktu
    credentials = service_account.Credentials.from_service_account_info(keyfile_dict)

    # ✅ Inicializuoti BigQuery klientą su autentifikacija
    client = bigquery.Client(credentials=credentials, project=project_id)

    # Nuskaitome CSV failą
    df = pd.read_csv(csv_file)

    # ✅ Įkelti į BigQuery
    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV
        )
    )

    job.result()
    print(f"✅ Įkelta {len(df)} eilučių į {table_ref}")

if __name__ == "__main__":
    upload_to_bigquery()
