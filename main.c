#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argv, char** argc) {
	char sh[] = "/bin/sh";
	setuid(0);
	// system(sh);
	execve("/bin/sh", 0, 0);
	return 0;
}
