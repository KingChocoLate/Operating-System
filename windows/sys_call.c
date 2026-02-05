#include <windows.h>
#include <stdio.h>

int main(void)
{
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Build: C:\Windows\System32\mspaint.exe without hardcoding WindowsApps
    char sysdir[MAX_PATH];
    char app[MAX_PATH];

    GetSystemDirectoryA(sysdir, MAX_PATH);
    snprintf(app, MAX_PATH, "%s\\mspaint.exe", sysdir);

    BOOL ok = FALSE;

    if (GetFileAttributesA(app) != INVALID_FILE_ATTRIBUTES) {
        // Best: run the EXE directly
        ok = CreateProcessA(app, NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    } else {
        // Fallback: let Windows find it in PATH
        char cmd[] = "mspaint";
        ok = CreateProcessA(NULL, cmd, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    }

    if (!ok) {
        printf("CreateProcess failed. Error=%lu\n", GetLastError());
        return 1;
    }

    printf("Parent PID=%lu | Child PID=%lu\n", GetCurrentProcessId(), pi.dwProcessId);

    Sleep(150000); // keep parent alive so you can screenshot

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 0;
}
