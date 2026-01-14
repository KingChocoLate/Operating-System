import threading
import time

class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Semaphore(1)

def transfer(from_acc, to_acc, amount):
    print(f"{threading.current_thread().name} locking {from_acc.name}")
    from_acc.lock.acquire()
    
    time.sleep(1)
    
    print(f"{threading.current_thread().name} waiting for {to_acc.name}")
    to_acc.lock.acquire()
    
    from_acc.balance -= amount
    to_acc.balance += amount
    print(f"{threading.current_thread().name} transfer complete")
    
    to_acc.lock.release()
    from_acc.lock.release()

if __name__ == "__main__":
    acc1 = BankAccount("Account A", 1000)
    acc2 = BankAccount("Account B", 1000)

    t1 = threading.Thread(target=transfer, args=(acc1, acc2, 100))
    t2 = threading.Thread(target=transfer, args=(acc2, acc1, 100))

    t1.start()
    t2.start()

    t1.join()
    t2.join()