import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class bank implements Runnable {
    int balance = 0;
    Lock lock = new ReentrantLock();

    private int deposit () {
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return balance += 100;
    }

    private int withdraw () {
        return balance -= 100;
    }

    private int get_value () {
        return balance;
    }

    @Override
    public void run () {
        //lock.lock();
        deposit();
        System.out.println("Value for Thread after deposit " + Thread.currentThread().getName() + " " + get_value());

        withdraw();
        System.out.println("Value for Thread after withdraw " + Thread.currentThread().getName() + " " + get_value());
    }
}
