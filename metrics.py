import time

latencies = []

def measure(start):
    latencies.append(time.time() - start)

def report():
    if latencies:
        print("Avg latency:", sum(latencies)/len(latencies))