import time
import random

# =========================================
# Dynamic Node Configuration
# =========================================

nodes = ["Apollo", "Fortis", "Manipal", "AIIMS", "Narayana"]

last_failed = []
last_malicious = []


# -----------------------------------------
# Set dynamic node count (for experiments)
# -----------------------------------------
def set_nodes(count):
    global nodes
    nodes = [f"Node_{i}" for i in range(count)]


def get_nodes():
    return nodes


def get_node_status():
    return last_failed, last_malicious


# =========================================
# PBFT Consensus Simulation
# =========================================

def pbft_consensus(batch):
    """
    Simulates PBFT consensus with:
    - Network delay
    - Byzantine faulty nodes
    - Malicious behavior
    - 2f + 1 approval requirement
    """

    global last_failed, last_malicious

    n = len(nodes)

    # PBFT fault tolerance condition
    f = (n - 1) // 3

    if n < 3 * f + 1:
        return False

    # Reset previous status
    last_failed = []
    last_malicious = []

    # -------------------------------------
    # Random Byzantine Fault Simulation
    # -------------------------------------

    # Simulate up to f faulty nodes
    faulty_count = random.randint(0, f)

    if faulty_count > 0:
        last_failed = random.sample(nodes, faulty_count)

    # Simulate malicious nodes separately
    malicious_count = random.randint(0, f)

    if malicious_count > 0:
        remaining_nodes = [n for n in nodes if n not in last_failed]
        if remaining_nodes:
            last_malicious = random.sample(
                remaining_nodes,
                min(malicious_count, len(remaining_nodes))
            )

    # -------------------------------------
    # Simulated Network Delay
    # -------------------------------------

    approvals = 0

    for node in nodes:
        # realistic distributed delay
        time.sleep(random.uniform(0.005, 0.02))

        # Failed nodes do not respond
        if node in last_failed:
            continue

        # Malicious nodes reject valid batch
        if node in last_malicious:
            continue

        approvals += 1

    # PBFT requires 2f + 1 approvals
    required_votes = 2 * f + 1

    return approvals >= required_votes