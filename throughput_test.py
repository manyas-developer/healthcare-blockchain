# import time
# import statistics
# from blockchain import Blockchain
# from pbft import pbft_consensus, set_nodes


# def run_experiment(node_count, total_blocks=100):
#     """
#     Runs PBFT experiment for given node count
#     Returns:
#         avg_latency
#         std_latency
#         throughput
#     """

#     set_nodes(node_count)
#     bc = Blockchain()

#     latencies = []
#     start_total = time.time()

#     for i in range(total_blocks):
#         data = [{"shipment_id": i, "temperature": 5}]

#         start = time.time()

#         if pbft_consensus(data):
#             bc.add_block(data)

#         end = time.time()

#         latencies.append(end - start)

#     total_time = time.time() - start_total

#     avg_latency = statistics.mean(latencies)
#     std_latency = statistics.stdev(latencies)
#     throughput = total_blocks / total_time

#     return avg_latency, std_latency, throughput


# if __name__ == "__main__":

#     node_sizes = [3, 5, 7, 9, 11]

#     print("PBFT PERFORMANCE RESULTS")
#     print("=" * 50)

#     for n in node_sizes:
#         avg, std, thr = run_experiment(n, total_blocks=100)

#         print(f"Nodes: {n}")
#         print(f"Average Latency: {avg:.6f} sec")
#         print(f"Std Deviation: {std:.6f}")
#         print(f"Throughput: {thr:.2f} blocks/sec")
#         print("-" * 50)

import time
import statistics
import matplotlib.pyplot as plt
from blockchain import Blockchain
from pbft import pbft_consensus, set_nodes


def run_experiment(node_count, total_blocks=100):

    set_nodes(node_count)
    bc = Blockchain()

    latencies = []

    start_total = time.time()

    for i in range(total_blocks):

        data = [{"patient": i, "heart_rate": 70}]

        start = time.time()

        if pbft_consensus(data):
            bc.add_block(data)

        end = time.time()

        latencies.append(end - start)

    total_time = time.time() - start_total

    avg_latency = statistics.mean(latencies)
    throughput = total_blocks / total_time

    return avg_latency, throughput


if __name__ == "__main__":

    node_sizes = [3,5,7,9,11,20,30,40,50,60,70,80,90,100]

    latency_results = []
    throughput_results = []

    print("PBFT SCALABILITY RESULTS")
    print("="*50)

    for n in node_sizes:

        latency, throughput = run_experiment(n)

        latency_results.append(latency)
        throughput_results.append(throughput)

        print(f"Nodes: {n}")
        print(f"Latency: {latency:.6f} sec")
        print(f"Throughput: {throughput:.2f} blocks/sec")
        print("-"*40)


    # -------- LATENCY GRAPH --------
    plt.figure()

    plt.plot(node_sizes, latency_results, marker='o')

    plt.title("PBFT Latency vs Node Count")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Latency (seconds)")
    plt.grid(True)

    plt.show()


    # -------- THROUGHPUT GRAPH --------
    plt.figure()

    plt.plot(node_sizes, throughput_results, marker='o')

    plt.title("PBFT Throughput vs Node Count")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Throughput (blocks/sec)")
    plt.grid(True)

    plt.show()