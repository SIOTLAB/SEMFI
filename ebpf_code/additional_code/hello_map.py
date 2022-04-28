#!/usr/bin/python
from bcc import BPF
from time import sleep

# This outputs a count of how many times the clone and execve syscalls have been made
# showing the use of an eBPF map (called syscall). 

program = """
 BPF_HASH(syscall);
 int kprobe__sys_clone(void *ctx) {
     u64 counter = 0;
     u64 key = 56;
     u64 *p; 
     p = syscall.lookup(&key);
     // The verifier will reject access to a pointer if you don't check that it's non-null first
     // Try commenting out the if test (and its closing brace) if you want to see the verifier do its thing
     if (p != 0) {
         counter = *p;
     }
     counter++;
     syscall.update(&key, &counter);
     return 0;
 }
int kprobe__sys_execve(void *ctx) {
     u64 counter = 0;
     u64 key = 59;
     u64 *p; 
     p = syscall.lookup(&key);
     if (p != 0) {
         counter = *p;
     }
     counter++;
     syscall.update(&key, &counter);
     return 0;
 }
"""

b = BPF(text=program)
while True:
    sleep(2)
    line = ""
    for k, v in b["syscall"].items():
        line += "syscall {0}: {1}\t".format(k.value, v.value)
    print(line)
