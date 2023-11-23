#include <stdio.h>
#include <string.h>

void bar() {
    printf("bar() has been hijacked!\n");
}

void foo(char *input) {
    char buffer[10];

    // Vulnerable to buffer overflow
    strcpy(buffer, input);

    printf("foo() is executing...\n");
}

int main() {
    // This input is crafted to cause a buffer overflow
    // It will need to be adjusted based on the memory layout of the program
    // WARNING: This is an unsafe operation and should only be done in a controlled environment
    //char input[] = "AAAAAAAAAABBBBBBBBBBCCCCCCCCCCDDDDDDDDDD"; // Extend this string to overwrite the return address
    char input[] = "AAAAAAAAAAAAAAAAAA\x69\x51\x55\x55\x55\x55\x00\x00";
    foo(input);

    printf("Back in main function\n");

    return 0;
}

