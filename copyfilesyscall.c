#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    int src, dest;
    char buffer[1024];
    ssize_t bytesRead;

    // Open result.txt for reading
    src = open("result.txt", O_RDONLY);
    if (src < 0) {
        perror("Error opening result.txt");
        return 1;
    }

    // Open (or create) copyresult.txt for writing
    dest = open("copyresult.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest < 0) {
        perror("Error opening copyresult.txt");
        close(src);
        return 1;
    }

    // Copy loop
    while ((bytesRead = read(src, buffer, sizeof(buffer))) > 0) {
        write(dest, buffer, bytesRead);
    }

    // Close both files
    close(src);
    close(dest);

    write(1, "Copy finished.\n", 15);
    return 0;
}
