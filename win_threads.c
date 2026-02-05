#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 6

DWORD WINAPI Worker(LPVOID Param)
{
    int id = *(int*)Param;
    printf("Thread %d started\n", id);

    // keep thread alive long enough to see it in Process Explorer
    for (int i = 0; i < 20; i++) {
        printf("Thread %d working...\n", id);
        Sleep(300);
    }

    printf("Thread %d finished\n", id);
    return 0;
}

int main()
{
    HANDLE hThreads[NUM_THREADS];
    DWORD threadIds[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("Main: creating %d threads...\n", NUM_THREADS);

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        hThreads[i] = CreateThread(
            NULL, 0, Worker, &ids[i], 0, &threadIds[i]
        );

        if (hThreads[i] == NULL) {
            printf("CreateThread failed: %lu\n", GetLastError());
            return 1;
        }
    }

    printf("Main: threads created. Waiting...\n");
    WaitForMultipleObjects(NUM_THREADS, hThreads, TRUE, INFINITE);

    for (int i = 0; i < NUM_THREADS; i++) CloseHandle(hThreads[i]);

    printf("Main: done. Press Enter to exit...\n");
    getchar();
    return 0;
}
