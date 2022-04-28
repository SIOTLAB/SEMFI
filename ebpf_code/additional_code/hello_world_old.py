#!/usr/bin/python

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb
import time



prog = """
#define BPF_SK_LOOKUP 36
#include <uapi/linux/ptrace.h>
#include <bcc/proto.h>
#include <uapi/linux/ptrace.h>
#include <linux/dma-mapping.h>
#include </home/ans/Desktop/linux-5.8/include/linux/ieee80211.h>
#include </home/ans/Desktop/linux-5.8/include/uapi/linux/time.h>


int hello(void *ctx) {
    bpf_trace_printk("Hello world\\n");
    return 0;
}
"""

b = BPF(text=prog)
clone = b.get_syscall_fnname("clone")
b.attach_kprobe(event=clone, fn_name="hello")
b.trace_print()

# This prints out a trace line every time the clone system call is called

# If you rename hello() to kprobe__sys_clone() you can delete the b.attach_kprobe() line, because bcc can work
# out what event to attach this to from the function name.
