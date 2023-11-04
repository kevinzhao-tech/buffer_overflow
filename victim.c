#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int chk_password() {
    const char passwd[16] = "password123";
    // buffer for gets
    char input_passwd[32];

    char msg[32] = "Enter your password\n";
    char try_again_msg[32] = "Try again :(\n";
    char success_msg[32] = "Try again :(\n";

    printf("%s", msg);

    gets(input_passwd);

    int success = strcmp(input_passwd, passwd) == 0;
        
    if (!success) {
        printf("%s", try_again_msg);
    } else {
        printf("%s", success_msg);
    }

    return success;
}

int main(int argc, char **argv) {

    int success = 0;
    for (size_t i = 0; i < 3; ++i) {
        if (chk_password()) {
            success = 1;
            break;
        }
    }
    
    if (!success) {
        printf("Failed.. Out of attempts :(\n");
    }

    return 0;
}