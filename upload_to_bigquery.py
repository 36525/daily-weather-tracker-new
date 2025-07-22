import pandas as pd
from google.cloud import bigquery

def upload_to_bigquery():
    # Kelias iki CSV failo
    csv_file = 'daily_weather.csv'

    # Tavo projekto informacija
    project_id = "optical-wall-447816-m1"
    dataset_id = "weather_data"
    table_id = "daily_weather"

    # Inicializuojame BigQuery klientą
    client = bigquery.Client()

    # Nuskaitome CSV
    df = pd.read_csv(csv_file)

    # Lentelės nuoroda
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Įkėlimo konfiguracija
    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",  # prideda naujas eilutes
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV
        )
    )

    job.result()
    print(f"✅ Įkelta {len(df)} eilučių į {table_ref}")

if __name__ == "__main__":
    upload_to_bigquery()
