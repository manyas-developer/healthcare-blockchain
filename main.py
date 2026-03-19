from stream import stream_data, buffer_records
from blockchain import Blockchain
from pbft import pbft_consensus
from metrics import measure, report
import time

bc = Blockchain()

print("System started...\n")

for batch in buffer_records(stream_data(), batch_size=5):

    start = time.time()

    print("\nBatch received:", len(batch))

    if pbft_consensus(batch):
        bc.add_block(batch)

    measure(start)

    time.sleep(0.5)

report()