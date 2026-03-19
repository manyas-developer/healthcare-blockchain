from flask import Flask, render_template, request
from blockchain import Blockchain
from stream import stream_data
from pbft import pbft_consensus, get_nodes, get_node_status
import itertools
import time
import random

app = Flask(__name__, static_folder="static")

bc = Blockchain()
data_stream = stream_data()

BATCH_SIZE = 5

latest_records = []
latest_latency = 0
latest_throughput = 0
block_count = 0


# =============================
# Dashboard
# =============================
@app.route("/")
def index():
    failed_nodes, malicious_nodes = get_node_status()

    return render_template(
        "index.html",
        blocks=len(bc.chain),
        records=latest_records,
        latency=round(latest_latency, 4),
        throughput=round(latest_throughput, 4),
        total_blocks=block_count,
        node_count=len(get_nodes()),
        chain_valid=bc.is_chain_valid(),
        failed_nodes=failed_nodes,
        malicious_nodes=malicious_nodes
    )


# =============================
# Run Streaming
# =============================
@app.route("/run", methods=["POST"])
def run_system():
    global latest_records, latest_latency, latest_throughput
    global block_count, BATCH_SIZE

    batch_from_ui = request.form.get("batch_size")
    if batch_from_ui:
        BATCH_SIZE = int(batch_from_ui)

    start = time.time()

    records = list(itertools.islice(data_stream, BATCH_SIZE))

    if not records:
        return index()

    latest_records = records

    if pbft_consensus(records):
        bc.add_block(records)
        block_count += 1

    end = time.time()

    latest_latency = end - start
    latest_throughput = 1 / latest_latency if latest_latency > 0 else 0

    return index()


# =============================
# Tamper Simulation
# =============================
@app.route("/tamper", methods=["POST"])
def tamper_block():
    tamper_type = request.form.get("tamper_type")
    block_number = request.form.get("block_number")

    if len(bc.chain) <= 1:
        return index()

    # Random tamper
    if tamper_type == "random":
        block = random.choice(bc.chain[1:])

    # Specific block tamper
    elif tamper_type == "specific" and block_number:
        block_index = int(block_number)
        if block_index < len(bc.chain):
            block = bc.chain[block_index]
        else:
            return index()
    else:
        return index()

    # Modify patient heart rate
    if isinstance(block.data, list) and len(block.data) > 0:
        block.data[0]["heart_rate"] += random.randint(100, 500)

    return index()


# =============================
# Repair Chain
# =============================
@app.route("/repair")
def repair_chain():
    bc.repair_chain()
    return index()


# =============================
# Blockchain Viewer
# =============================
@app.route("/chain")
def view_chain():
    invalid_blocks = bc.get_invalid_blocks()

    comparison = {}
    field_changes = {}

    for block in bc.chain:
        comparison[block.index] = {
            "stored": block.hash,
            "recalculated": block.calculate_hash()
        }
        field_changes[block.index] = block.get_field_changes()

    return render_template(
        "chain.html",
        chain=bc.chain,
        invalid_blocks=invalid_blocks,
        comparison=comparison,
        field_changes=field_changes
    )


# =============================
# Graph Page
# =============================
@app.route("/graphs")
def graphs():
    return render_template("graphs.html")


if __name__ == "__main__":
    app.run(debug=True)