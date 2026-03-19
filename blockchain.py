import hashlib
import time
import copy
import json


# =========================================
# BLOCK CLASS
# =========================================

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.original_data = copy.deepcopy(data)  # For tamper comparison
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    # -------------------------------------
    # Deterministic Hashing (Research-Grade)
    # -------------------------------------
    def calculate_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }

        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    # -------------------------------------
    # Detect Field-Level Changes
    # -------------------------------------
    def get_field_changes(self):
        changes = []

        if isinstance(self.data, list) and isinstance(self.original_data, list):
            for i in range(min(len(self.data), len(self.original_data))):
                for key in self.original_data[i]:
                    if self.original_data[i][key] != self.data[i].get(key):
                        changes.append({
                            "field": key,
                            "old": self.original_data[i][key],
                            "new": self.data[i].get(key)
                        })

        return changes

    # -------------------------------------
    # Compare Stored vs Recalculated Hash
    # -------------------------------------
    def get_hash_comparison(self):
        recalculated = self.calculate_hash()
        return {
            "stored_hash": self.hash,
            "recalculated_hash": recalculated,
            "match": self.hash == recalculated
        }


# =========================================
# BLOCKCHAIN CLASS
# =========================================

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    # -------------------------------------
    # Full Integrity Validation
    # -------------------------------------
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1️⃣ Check previous hash linkage
            if current.previous_hash != previous.hash:
                return False

            # 2️⃣ Check data integrity
            if current.hash != current.calculate_hash():
                return False

        return True

    # -------------------------------------
    # Get List of Corrupted Blocks
    # -------------------------------------
    def get_invalid_blocks(self):
        invalid = []

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                invalid.append(current.index)

            if current.hash != current.calculate_hash():
                invalid.append(current.index)

        return list(set(invalid))

    # -------------------------------------
    # Repair Chain (For Demo Only)
    # -------------------------------------
    def repair_chain(self):
        """
        Repairs hash chain by recalculating
        previous_hash and hash values sequentially.
        Used only for educational demo.
        """

        for i in range(1, len(self.chain)):
            previous = self.chain[i - 1]
            current = self.chain[i]

            current.previous_hash = previous.hash
            current.hash = current.calculate_hash()