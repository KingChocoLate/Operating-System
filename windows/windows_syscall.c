#include <windows.h>
#include <string.h>

int main() {
    const char *msg = "Hello from Windows WriteFile!\r\n";
    DWORD written;
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);

    WriteFile(hOut, msg, (DWORD)strlen(msg), &written, NULL);

    Sleep(15000); // keep running 15 seconds for ProcMon
    return 0;
}
