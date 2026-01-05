import threading
import time

# Semaphores
a = threading.Semaphore(1)  # Starts at 1 so "H" can print first
b = threading.Semaphore(0)  # Controls "L"s
c = threading.Semaphore(0)  # Controls "O"

def process1():
    a.acquire()  # Wait for 'a'
    print("H", end='', flush=True)
    print("E", end='', flush=True)
    # Signal 'b' twice because we need two "L"s from Process 2
    b.release()
    b.release()

def process2():
    # This runs twice because Process 1 signals 'b' twice
    for _ in range(2):
        b.acquire()  # Wait for 'b'
        print("L", end='', flush=True)
        c.release()  # Signal 'c' that one "L" is done

def process3():
    # Wait for 'c' twice (ensures both "L"s are finished)
    c.acquire()
    c.acquire()
    print("O", end='', flush=True)
    print("\n[Done]")

if __name__ == "__main__":
    print("=== Problem 2: HELLO Printer ===")
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()