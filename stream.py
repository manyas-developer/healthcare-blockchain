import pandas as pd
import time

data = pd.read_csv("heart_disease_uci.csv")

def stream_data():
    for _, row in data.iterrows():
        record = {
            "patient_id": row["id"],
            "heart_rate": row["thalch"],
            "bp": row["trestbps"],
            "chol": row["chol"],
            "timestamp": time.time()
        }
        yield record


def buffer_records(generator, batch_size=5):
    buffer = []
    for rec in generator:
        buffer.append(rec)
        if len(buffer) == batch_size:
            yield buffer
            buffer = []