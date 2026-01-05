import threading
import time
import random
from collections import deque
from threading import Semaphore

# Configuration
BUFFER_SIZE = 100
buffer = deque(maxlen=BUFFER_SIZE)

# Semaphores
mutex = Semaphore(1)         # Protects buffer access
empty_slots = Semaphore(100) # Tracks individual particle spaces
pairs_ready = Semaphore(0)   # Tracks available pairs for consumer

def producer(name):
    while True:
        # 1. Produce pair
        time.sleep(random.uniform(0.5, 1.0))
        p1, p2 = f"{name}-A", f"{name}-B"

        # 2. Wait for two spaces
        empty_slots.acquire()
        empty_slots.acquire()

        # 3. Critical Section
        with mutex:
            buffer.append(p1)
            buffer.append(p2)
            print(f"[{name}] placed pair ({p1}, {p2}) | Buffer size: {len(buffer)}")

        # 4. Signal that a full pair is ready
        pairs_ready.release()

def consumer():
    while True:
        # 1. Wait for a full pair to be ready
        pairs_ready.acquire()

        # 2. Critical Section
        with mutex:
            p1 = buffer.popleft()
            p2 = buffer.popleft()
            print(f"[Consumer] fetched ({p1}, {p2}) | Buffer size: {len(buffer)}")

        # 3. Signal that two slots are now empty
        empty_slots.release()
        empty_slots.release()

        # 4. Process/Ship
        print(f"-> Shipped pair: {p1} & {p2}\n")
        time.sleep(random.uniform(0.8, 1.5))

if __name__ == "__main__":
    print("=== Problem 1: Particle Pair Synchronization ===\n")
    # Start 3 Producers and 1 Consumer
    for i in range(1, 4):
        threading.Thread(target=producer, args=(f"Prod{i}",), daemon=True).start()

    threading.Thread(target=consumer, daemon=True).start()

    # Keep main thread alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Simulation...")