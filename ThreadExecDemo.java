import java.util.concurrent.*;
import java.util.*;

public class ThreadExecDemo {

    static void doWork(String taskName) {
        String t = Thread.currentThread().getName();
        System.out.println(taskName + " running on " + t);
        try { Thread.sleep(800); } catch (InterruptedException ignored) {}
    }

    // Fork/Join task
    static class SumTask extends RecursiveTask<Long> {
        private final long[] arr;
        private final int start, end;
        private static final int THRESHOLD = 20000;

        SumTask(long[] arr, int start, int end) {
            this.arr = arr; this.start = start; this.end = end;
        }

        @Override
        protected Long compute() {
            if (end - start <= THRESHOLD) {
                long sum = 0;
                for (int i = start; i < end; i++) sum += arr[i];
                return sum;
            }
            int mid = (start + end) / 2;
            SumTask left = new SumTask(arr, start, mid);
            SumTask right = new SumTask(arr, mid, end);
            left.fork();
            long r = right.compute();
            long l = left.join();
            return l + r;
        }
    }

    public static void main(String[] args) throws Exception {

        // 1) SingleThreadExecutor
        ExecutorService single = Executors.newSingleThreadExecutor();
        for (int i = 1; i <= 6; i++) {
            int id = i;
            single.submit(() -> doWork("SingleTask-" + id));
        }
        single.shutdown();
        single.awaitTermination(10, TimeUnit.SECONDS);

        System.out.println("-----");

        // 2) CachedThreadPool
        ExecutorService cached = Executors.newCachedThreadPool();
        for (int i = 1; i <= 10; i++) {
            int id = i;
            cached.submit(() -> doWork("CachedTask-" + id));
        }
        cached.shutdown();
        cached.awaitTermination(10, TimeUnit.SECONDS);

        System.out.println("-----");

        // 3) Fork/Join Parallelism
        long[] data = new long[2_000_000];
        Arrays.fill(data, 1);

        ForkJoinPool pool = new ForkJoinPool(); // uses multiple worker threads
        long result = pool.invoke(new SumTask(data, 0, data.length));
        System.out.println("ForkJoin sum = " + result);

        // Keep app alive for visualization (important!)
        System.out.println("Keep running 20s for visualization...");
        Thread.sleep(20000);
    }
}
