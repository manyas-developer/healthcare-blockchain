import time
from blockchain import Blockchain


def centralized_test(total_blocks=100):
    """
    Simulates centralized block creation
    (No consensus overhead)
    """

    bc = Blockchain()

    start = time.time()

    for i in range(total_blocks):
        data = [{"shipment_id": i}]
        bc.add_block(data)

    total_time = time.time() - start
    throughput = total_blocks / total_time

    print("CENTRALIZED SYSTEM RESULTS")
    print("=" * 50)
    print(f"Total Blocks: {total_blocks}")
    print(f"Total Time: {total_time:.6f} sec")
    print(f"Throughput: {throughput:.2f} blocks/sec")


if __name__ == "__main__":
    centralized_test(100)