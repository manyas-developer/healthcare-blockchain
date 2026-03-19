import matplotlib.pyplot as plt

# =========================
# Experiment 1 - Batch size vs Latency
# =========================
batch_sizes = [3, 5, 7]
batch_latency = [0.00098, 0.00119, 0.00124]

plt.figure()
plt.plot(batch_sizes, batch_latency, marker='o')
plt.title("Batch Size vs Latency")
plt.xlabel("Batch Size")
plt.ylabel("Latency (sec)")
plt.grid(True)
plt.savefig("static/batch_graph.png")
plt.close()


# =========================
# Experiment 2 - Streaming Interval vs Latency
# =========================
sleep_values = [2, 1, 0.5]
sleep_latency = [0.00119, 0.00099, 0.00099]

plt.figure()
plt.plot(sleep_values, sleep_latency, marker='o')
plt.title("Streaming Interval vs Latency")
plt.xlabel("Sleep Time (sec)")
plt.ylabel("Latency (sec)")
plt.grid(True)
plt.savefig("static/sleep_graph.png")
plt.close()


# =========================
# Experiment 3 - PBFT Nodes vs Latency
# (Updated realistic values if needed)
# =========================
nodes = [3, 5, 7]
node_latency = [0.4011/20, 0.4227/20, 0.5839/20]  
# Converted from total time per block (optional refinement)

plt.figure()
plt.plot(nodes, node_latency, marker='o')
plt.title("PBFT Nodes vs Latency")
plt.xlabel("Number of Nodes")
plt.ylabel("Latency per Block (sec)")
plt.grid(True)
plt.savefig("static/node_graph.png")
plt.close()


# =========================
# Experiment 4 - PBFT Nodes vs Throughput
# (NEW - Publication Strength)
# =========================
throughput = [49.86, 47.31, 34.25]

plt.figure()
plt.plot(nodes, throughput, marker='o')
plt.title("PBFT Nodes vs Throughput")
plt.xlabel("Number of Nodes")
plt.ylabel("Throughput (blocks/sec)")
plt.grid(True)
plt.savefig("static/throughput_graph.png")
plt.close()


print("All graphs saved successfully!")