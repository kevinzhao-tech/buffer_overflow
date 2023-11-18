#include <stdio.h>
#include <stdlib.h>
// gcc srop.c -o srop -no-pie -fno-stack-protector
void syscall_(){
       __asm__("syscall; ret;");
}

void set_rax(){
       __asm__("movl $0xf, %eax; ret;");
}

int main(){
       // ONLY SROP!
       char *const str = "/bin/sh";
       char buff[100];
       printf("Buff @%p, can you SROP?\n", buff);
       read(0, buff, 5000);
       return 0;
}