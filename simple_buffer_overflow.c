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
    char input[] = "AAAAAAAAAAAAAAAAAA\x69\x51\x55\x55\x55\x55\x00\x00"; //address obtained through gdb debugging p &bar

    foo(input);

    printf("Back in main function\n");

    return 0;
}

