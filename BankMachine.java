public class BankMachine {
    public static void main(String[] args) throws InterruptedException {
        bank bank_instance = new bank();
            Thread t1 = new Thread(bank_instance, "Thread1");
            Thread t2 = new Thread(bank_instance, "Thread2");
            Thread t3 = new Thread(bank_instance, "Thread3");

            t1.start();
            t2.start();
            t3.start();

            t1.join();
            t2.join();
            t3.join();
    }
}