import threading
import time

class BankAccount:
    def __init__(self, id_num, balance):
        self.id = id_num
        self.balance = balance
        self.lock = threading.Semaphore(1)

def transfer(from_acc, to_acc, amount):
    name = threading.current_thread().name
    
    # 1. Sort accounts by ID to fix Deadlock
    if from_acc.id < to_acc.id:
        first, second = from_acc, to_acc
    else:
        first, second = to_acc, from_acc

    # 2. Lock the first account (Smaller ID)
    print(f"[{name}] Locking Account {first.id}...")
    first.lock.acquire()
    print(f"[{name}] Locked Account {first.id}")

    time.sleep(1) 
    
    # 3. Lock the second account (Larger ID)
    print(f"[{name}] Waiting for Account {second.id}...")
    second.lock.acquire()
    print(f"[{name}] Locked Account {second.id}")
    
    # 4. Transfer with Amount
    from_acc.balance -= amount
    to_acc.balance += amount
    print(f"[{name}] Transferring ${amount}... Success")
    
    # 5. Release
    second.lock.release()
    first.lock.release()
    print(f"[{name}] Released locks\n")

if __name__ == "__main__":
    acc1 = BankAccount(1, 1000)
    acc2 = BankAccount(2, 1000)

    t1 = threading.Thread(target=transfer, args=(acc1, acc2, 100), name="Thread-1")
    t2 = threading.Thread(target=transfer, args=(acc2, acc1, 100), name="Thread-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()