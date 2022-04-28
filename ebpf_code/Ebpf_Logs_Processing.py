import logging
import os
import sys

index_list = ['1', '2', '3']

for index in index_list:

    f = open("ebpf_logs/ebpf_devices_" + index + ".txt", "w")
    # f.write("Now the file has more content!")

    with open('ebpf_logs/ebpf_devices_output.txt') as raw_file:
        lines = raw_file.readlines()
    for i in range(len(lines)):
        starting_device_flag = "STARTING_MATCHING_DEVICE_" + index
        ending_device_flag = "ENDING_MATCHING_DEVICE_" + index
        if starting_device_flag in lines[i]:
            for j in range(i+1, len(lines)):
                if ending_device_flag in lines[j]:
                    break
                f.write(lines[j])
    f.close()
    print("done" + index)