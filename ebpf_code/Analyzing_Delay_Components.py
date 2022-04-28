#!/usr/bin/python
import json
# -*- coding: utf-8 -*-
import os
import time
import threading
import math
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt, mpld3
import numpy as np
import statistics
import bisect
from decimal import Decimal
import sys
import os
import pandas as pd


device_names = ["iPhone 13 Pro", "iPad Pro", "Apple Watch", "MacBook Pro"]
# MAC_match = "c4:4b:d1:80:5:e8"
# MAC_match_with_zero = "c4:4b:d1:80:05:e8"
# MAC_match_first_three = "c4:4b:d1"  


# Sreya's iPhone (index 1): ba:88:a3:ed:d9:c3
# MAC_match = "ba:88:a3:ed:d9:c3"
# MAC_match_with_zero = "ba:88:a3:ed:d9:c3"
# MAC_match_first_three = "ba:88:a3" 
# set_plt_limits = 1
# index = '1'
# index_int = 1
# identifier = 'VODL'

# Sreya's iPad (index 2): 1a:e3:a1:68:01:3f
MAC_match = "1a:e3:a1:68:01:3f"
MAC_match_with_zero = "1a:e3:a1:68:01:3f"
MAC_match_first_three = "1a:e3:a1" 
set_plt_limits = 1
index = '2'
index_int = 2
identifier = 'VODL'

# Sreya's watch (index 3): 6a:09:3e:12:d9:f8



# Sreya's Mac (index 4): 90:9c:4a:cc:77:94




# Mode 0 => cumulative energy measurements from start to the end. Provides only one value of energy measurements.
# Mode 1 => energy measurements every interval, from start to end. Provides (end-start)/INTERVAL values of measurement. NOTE: provides cumulatibe measurements, i.e., adds the current values of sleep/wake time to the previous ones
# Mode 2 => energy measurements every interval, from start to end. Provides (end-start)/INTERVAL values of measurement. NOTE: provides Indepent measurements, i.e., gets the current values of sleep/wake time during that time slot
# print(sys.argv[0]) ... host_logs_process.py
# print(sys.argv[1]) ... INDEX

# set_plt_limits = 1
# index = '1'
# identifier = 'VODL'

# if len(sys.argv) < 2:
#   print("file extension indexer needed .... USAGE: python host_logs_process.py <INDEX>")
#   sys.exit("Values do not match")

#not needed for ANS!
# def find(name, path):
#     print("Searching for " + "hostapd_logs/host_logs_" + sys.argv[1] + ".txt" +  " @ " + path)
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return os.path.join(root, name)
#         else:
#             return 0

def cdf_plot(data):
  N = len(data)
  # sort the data in ascending order
  x = np.sort(data)
  # get the cdf values of y
  y = np.arange(N) / float(N)
  # plotting
  plt.xlabel('x-axis')
  plt.ylabel('y-axis')
    
  plt.title('CDF using sorting the data')
    
  plt.plot(x, y, marker='o')
  plt.show()


#res_1 = find("host_logs_" + sys.argv[1] + ".txt", "/home/ans/Desktop/ebpf_code/")

# if res_1 != 0:
#   print("file with this index found, please try another index ..." + "host_logs_" + sys.argv[1] + ".txt")
#   sys.exit("Exiting")


MODE = 2
INTERVAL = .002
lines_processed = 0
class DEVICES:
    instances = []
    instances_MAC = []
    def __init__(mysillyobject, MACADDR, ASSOC=0, DISASSOC=0, LI=0, N=0, AID=0):
        mysillyobject.device_name = device_names[index_int-1]
        mysillyobject.MACADDR = MACADDR
        mysillyobject.ASSOC = ASSOC
        mysillyobject.DISASSOC = DISASSOC
        mysillyobject.LI = LI
        mysillyobject.AID = AID
        mysillyobject.N = N
        mysillyobject.time_STA_wake = 0
        mysillyobject.time_STA_sleep = 0
        mysillyobject.time_accounted_for = ASSOC
        mysillyobject.time_accounting_complete = 0
        mysillyobject.n_beacons = 0
        mysillyobject.average_awake_time = 0.0
        mysillyobject.total_sleep_time = 0
        mysillyobject.total_awake_time = 0
        mysillyobject.beacon_wakeup = 0
        mysillyobject.beacon_wakeup_ts = []
        mysillyobject.beacon_wakeup_ts_notifier = []
        mysillyobject.list_percentwakeperinterval = []
        mysillyobject.tx_timestamp = []
        mysillyobject.tx_notifier_waste = []
        mysillyobject.tx_num_packets = 0
        mysillyobject.rx_data_timestamp = []
        mysillyobject.rx_data_notifier = []
        mysillyobject.rx_PS_timestamp = []
        mysillyobject.rx_PS_notifier = []
        mysillyobject.rx_num_packets = 0
        mysillyobject.wake_after_PS = []
        mysillyobject.PSPOLL_after_beacon = []
        mysillyobject.NULLwakeup_after_beacon = []
        mysillyobject.NULLwakeup_after_beacon_timestamp = []
        mysillyobject.NULLwakeup_after_beacon_timestamp_chanU = []
        mysillyobject.DATA_after_beacon = []
        mysillyobject.DATA_after_beacon_timestamp = []
        mysillyobject.DATA_after_beacon_timestamp_chanU = []
        mysillyobject.DATA_after_NULL = []
        mysillyobject.DATA_after_NULL_timestamp = []
        mysillyobject.DATA_after_NULL_timestamp_chanU = []
        mysillyobject.beacon_tims_ts = []
        mysillyobject.beacon_tims_notifier = []
        mysillyobject.packet_arrival_ts = []
        mysillyobject.packet_arrival_notifier = []
        
        mysillyobject.perf_br_handle_frame_finish_ts = []
        mysillyobject.perf_dev_hard_start_xmit_ts = []
        mysillyobject.perf_swba_ts = []
        mysillyobject.perf_rx_ts = []
        mysillyobject.perf_process_buffer_ts = []
        mysillyobject.perf_tx_complete_buf_ts = []
        
        mysillyobject.perf_ath10k_br_dev_val = []
        mysillyobject.perf_ath10k_dev_swba_val = []
        mysillyobject.perf_ath10k_swba_rx_val = []
        mysillyobject.perf_ath10k_rx_tx_val = []
        mysillyobject.perf_ath10k_txcomp_val = []
        
        mysillyobject.perf_ath10k_br_dev_ts = []
        mysillyobject.perf_ath10k_dev_swba_ts = []
        mysillyobject.perf_ath10k_swba_rx_ts = []
        mysillyobject.perf_ath10k_rx_tx_ts = []
        mysillyobject.perf_ath10k_txcomp_ts = []
        
        mysillyobject.perf_ath10k_br_dev_ts_chanU = []
        mysillyobject.perf_ath10k_dev_swba_ts_chanU = []
        mysillyobject.perf_ath10k_swba_rx_ts_chanU = []
        mysillyobject.perf_ath10k_rx_tx_ts_chanU = []
        mysillyobject.perf_ath10k_txcomp_ts_chanU = []
        
        mysillyobject.curr_ps_state = 1 #0 is OFF and 1 is ON
        mysillyobject.__class__.instances.append(mysillyobject)
        mysillyobject.__class__.instances_MAC.append(MACADDR)

    def print_obj_details(obj_abc):
        print ('Hello my MACADDR is:',obj_abc.MACADDR)
        print ('Hello my ASSOC is:', obj_abc.ASSOC)
        print ('Hello my DISASSOC is:',obj_abc.DISASSOC)
        print ('Hello my LI is:', obj_abc.LI)

    @classmethod
    def printInstances(cls):
        for instance in cls.instances:
            print ("MAC: ", instance.MACADDR)
            print ("\tASSOC: ",instance.ASSOC)
            print ("\tDISASSOC: ",instance.DISASSOC)
            print ("\tLI: ",instance.LI)
            print ("\tcurr_ps_state: ",instance.curr_ps_state)
            print ("\ttime_STA_wake: ",instance.time_STA_wake)
            print ("\ttime_STA_sleep: ",instance.time_STA_sleep)
            print ("\ttime_accounted_for: ",instance.time_accounted_for)
            print ("\ttime_accounting_complete: ",instance.time_accounting_complete)
            print ("\tNumber of Beacons: ",instance.n_beacons)
            print ("\tWakeups due to LI: ",instance.beacon_wakeup)
            print ("\tAID: ",instance.AID)
            print ("\tN: ",instance.N)
            print("\n\n\n")
            # print()


def countX(lst, x): 
    count = 0
    for ele in lst: 
        if (ele == x): 
            count = count + 1
    return count 

os.system('cat hostapd_logs/host_logs_1.txt | grep \"\\[2021\\]\" > /home/ans2/Desktop/ebpf_code/analyzing_logs/host_logs_filtered.txt')



# os.system('cat /home/siot_king_b/Desktop/2021_MAP/PEM/PSM2021_ac/hostapd_logs/host_logs_' + sys.argv[1] + '.txt | grep \"\\[2021\\]\" > /home/siot_king_b/Desktop/2021_MAP/PEM/PSM2021_ac/hostapd_logs/host_logs_filtered_' + sys.argv[1] + '.txt')




# Using readlines() 
file1 = open('analyzing_logs/host_logs_filtered.txt', 'r') 
Lines = file1.readlines() 

count = 0
# Strips the newline character 
for i in range(0, len(Lines)):
    line = Lines[i]
    # print("Line{}: {}".format(count, line.strip())) 
    substring = "ADD"
    if substring in line:
        # print ((line.split(' ')[3]).split('\n')[0])
        # checking if the next line has LI
        substring = "LI"
        if substring in Lines[i+1] and "AID" in Lines[i+3]:
          DEVICES((line.split(' ')[3]).split('\n')[0], ASSOC =  (float)(line.split(':')[0]), N=countX(DEVICES.instances_MAC, (line.split(' ')[3]).split('\n')[0]), LI =(float)(Lines[i+1].split('=')[1]), AID =(int)(Lines[i+3].split('=')[1]))
        else:
          DEVICES((line.split(' ')[3]).split('\n')[0], ASSOC =  (float)(line.split(':')[0]), N=countX(DEVICES.instances_MAC, (line.split(' ')[3]).split('\n')[0]))
        # print(DEVICES.instances_MAC)
        # print("ASSOC time: ", (float)(line.split(':')[0]))
        # print(countX(DEVICES.instances_MAC, (line.split(' ')[3]).split('\n')[0]))          
    substring = "DEL_STATION"
    if substring in line:
      substring = "Success"
      if substring in line:
        # print("found ", substring)
        # print("found ", (float)(line.split(':')[0]))
        # print(line.split(' ')[4])
        for i in DEVICES.instances:
          # print(i.MACADDR)
          if(line.split(' ')[4] == i.MACADDR):
            j = i
            # print("found!!")
        # print("----->", j.MACADDR, j.N)
        # print((float)(line.split(':')[0]))
        j.DISASSOC = (float)(line.split(':')[0])

DEVICES.printInstances()

print(DEVICES.instances_MAC)

for i in DEVICES.instances:
  print(i.MACADDR)




file1 = open('pre_processing_kern_log_logs/kern_logs_ebpf'+ index + '.txt', 'r') 
# file1 = open('/home/siot_king_b/Desktop/2021/PSM2021_ac/kern_logs/kern_logs.txt', 'r') 
Lines = file1.readlines() 

count = 0



with open('pre_processing_kern_log_logs/kern_logs_ebpf' + index + '.txt', "r") as file:
# with open('/home/siot_king_b/Desktop/2021/PSM2021_ac/kern_logs/kern_logs.txt', "r") as file:
    first_line = file.readline()
    for last_line in file:
        pass
exp_start_time = (float)(first_line.split(' ')[0])
exp_end_time = (float)(last_line.split(' ')[0])


def periodic_energy_measurment (start_time, end_time):
  global lines_processed
  # print(lines_processed, len(Lines))
  for h in range(lines_processed, len(Lines)):
      line = Lines[h]
      # print("----------1")
      # print(line, "a", start_time,"b", end_time, "c")
      # print("----------2")
      if((float)(line.split(' ')[0]) > end_time):
        # print("break")
        break
      if ((float)(line.split(' ')[0]) > start_time) and ((float)(line.split(' ')[0]) < end_time):
#         print(line)
        substring = "ath10k_process_rx"
        if substring in line:
          # print("ath10k_process_rx")
          last_line_time = (float)(line.split(' ')[0])
          # logging the UPlink packets from the devices
          if "3::ftype 8 ::4::stype 80" in line: #data packets
            for i in DEVICES.instances:
              substring = i.MACADDR.strip()
              if substring in line and i.time_accounting_complete == 0 :
                i.rx_data_timestamp.append((float)(line.split(' ')[0]))
                i.rx_data_notifier.append(100.8)
                i.rx_num_packets = i.rx_num_packets + 1
                # DATA_after_beacon
#                 if (len(i.rx_data_timestamp)>1 and len(i.beacon_wakeup_ts)>1 and len(i.rx_PS_timestamp)>1):
#                     i.DATA_after_beacon.append(i.rx_data_timestamp[-1] - (i.beacon_wakeup_ts[-1]))
#                     i.DATA_after_beacon_timestamp.append(i.rx_data_timestamp[-1])
#                     i.DATA_after_NULL.append(i.rx_data_timestamp[-1] - float(i.rx_PS_timestamp[-1]))
#                     i.DATA_after_NULL_timestamp.append(i.rx_PS_timestamp[-1])
#                     print("1:", i.rx_data_timestamp[-1], " ... ", i.beacon_wakeup_ts[-1])
          if ("3::ftype 8 ::4::stype 40" in line) or ("3::ftype 4 ::4::stype a0" in line): #PSM packets
            # print("PSM packets")
            for i in DEVICES.instances:
              substring = i.MACADDR.strip()
              # print("devices mac :", substring)
              # print("line ", line)
              # print("i.time_accounting_complete ", i.time_accounting_complete)
              if substring in line and i.time_accounting_complete == 0 :
                # print("found substring")
                i.rx_PS_timestamp.append((Decimal)(line.split(' ')[0]))
                i.rx_PS_notifier.append(100.6)
                if ("3::ftype 4 ::4::stype a0" in line):
                  if (len(i.rx_PS_timestamp)>1 and len(i.beacon_wakeup_ts)>1):
                    i.PSPOLL_after_beacon.append(i.rx_PS_timestamp[-1] - (Decimal)(i.beacon_wakeup_ts[-1]))
#                 if ("3::ftype 8 ::4::stype 40" in line):
#                   print(line)  
#                   if (len(i.rx_PS_timestamp)>1 and len(i.beacon_wakeup_ts)>1):
#                     i.NULLwakeup_after_beacon.append(i.rx_PS_timestamp[-1] - (Decimal)(i.beacon_wakeup_ts[-1]))
#                     i.NULLwakeup_after_beacon_timestamp.append(i.rx_PS_timestamp[-1])
          # 
          last_line_time = (float)(line.split(' ')[0])
          # 
          for i in DEVICES.instances:
            substring = i.MACADDR.strip()
            if i.time_accounting_complete == 0:
              if i.DISASSOC != 0 and (((float)(line.split(' ')[0])) - i.DISASSOC > 0):
                i.time_accounting_complete = 1
                # print("Done accounting _for : ", i.MACADDR, "... ", i.N, i.time_accounting_complete)
            if substring in line and i.time_accounting_complete == 0 :
              # print("The line: ", line, " concerns with :", i.MACADDR)
              line_time = (float)(line.split(' ')[0])
              # print(line_time)
              if ":PM 0" in line:#station waking up
                if i.curr_ps_state == 1:
                  # print(i.MACADDR, "[", i.N, "]" " is waking up ", "was awake for : ")
                  i.time_STA_wake = i.time_STA_wake+ (line_time - i.time_accounted_for)
                  i.time_accounted_for = line_time
                  i.curr_ps_state = 1
                elif i.curr_ps_state == 0:
                  # print(i.MACADDR, "[", i.N, "]" " is waking up ", "was asleep")
                  i.perf_rx_ts.append(line_time)
                  i.time_STA_sleep = i.time_STA_sleep + (line_time - i.time_accounted_for)
                  i.time_accounted_for = line_time
                  i.curr_ps_state = 1
                  if (len(i.beacon_wakeup_ts)>1):
                    i.NULLwakeup_after_beacon.append(line_time - (float)(i.beacon_wakeup_ts[-1]))
                    i.NULLwakeup_after_beacon_timestamp.append(line_time)
              elif  ":PM 1000" in line:#station going to sleep
                if i.curr_ps_state == 1:
                  # print(i.MACADDR, "[", i.N, "]" " is going to sleep ", "was awake")
                  i.time_STA_wake = i.time_STA_wake + (line_time - i.time_accounted_for)
                  i.time_accounted_for = line_time
                  i.curr_ps_state = 0
                elif i.curr_ps_state == 0:
                  # print(i.MACADDR, "[", i.N, "]" " is going to sleep ", "was asleep")
                  i.time_STA_sleep = i.time_STA_sleep + (line_time - i.time_accounted_for)
                  i.time_accounted_for = line_time
                  i.curr_ps_state = 0
              else:
                print("Not right")
        elif "br_handle_frame_finish" in line:
          for i in DEVICES.instances:
            substring = i.MACADDR
            if substring in line and i.time_accounting_complete == 0 :
                i.perf_br_handle_frame_finish_ts.append((float)(line.split(' ')[0]))
        elif "dev_hard_start_xmit" in line:
          for i in DEVICES.instances:
            substring = i.MACADDR
            if substring in line and i.time_accounting_complete == 0 :
                i.perf_dev_hard_start_xmit_ts.append((float)(line.split(' ')[0]))
        elif "ath_tx_txqaddbuf" in line:
          for i in DEVICES.instances:
            substring = i.MACADDR
            if substring in line and i.time_accounting_complete == 0 :
                i.perf_process_buffer_ts.append((float)(line.split(' ')[0]))
        elif "ath_tx_complete_buf" in line:
          # print("ath_tx_complete_buf")
#           print(line)
          for i in DEVICES.instances:
            substring = i.MACADDR
            if substring in line and i.time_accounting_complete == 0 :
              i.perf_tx_complete_buf_ts.append((float)(line.split(' ')[0]))
              # print((line.split(' ')[0]))
              # print((Decimal)(line.split(' ')[0]))
              # print("%.4f" % (float)(line.split(' ')[0]))
              i.tx_timestamp.append((Decimal)(line.split(' ')[0]))
              i.tx_notifier_waste.append(100.4)
              i.tx_num_packets = i.tx_num_packets + 1
              if (len(i.tx_timestamp)>1 and len(i.beacon_wakeup_ts)>1 and len(i.rx_PS_timestamp)>1):
                # print(i.tx_timestamp[-1])
                # print(i.rx_PS_timestamp[-1])
                i.DATA_after_beacon.append(float(i.tx_timestamp[-1]) - float(i.beacon_wakeup_ts[-1]))
                i.DATA_after_beacon_timestamp.append(i.tx_timestamp[-1])
                i.DATA_after_NULL.append(float(i.tx_timestamp[-1]) - float(i.rx_PS_timestamp[-1]))
                i.DATA_after_NULL_timestamp.append(i.rx_PS_timestamp[-1])
                # i.wake_after_PS.append(i.tx_timestamp[-1] - i.rx_PS_timestamp[-1])
                # print("i.wake:",i.wake_after_PS[-1])
              if (len(i.perf_br_handle_frame_finish_ts)>1 
                  and len(i.perf_dev_hard_start_xmit_ts)>1 
                  and len(i.perf_swba_ts)>1
                  and len(i.perf_rx_ts)>1 
                  and len(i.perf_process_buffer_ts)>1
                  and len(i.perf_tx_complete_buf_ts)>1):
#                 print("TODO")
                print("RIGHT")
                print((len(i.perf_br_handle_frame_finish_ts),len(i.perf_dev_hard_start_xmit_ts),
              len(i.perf_swba_ts),
              len(i.perf_rx_ts), 
              len(i.perf_process_buffer_ts),
              len(i.perf_tx_complete_buf_ts)))
                i.perf_ath10k_br_dev_val.append(i.perf_dev_hard_start_xmit_ts[-1] - i.perf_br_handle_frame_finish_ts[-1])
                i.perf_ath10k_dev_swba_val.append(i.perf_swba_ts[-1] - i.perf_dev_hard_start_xmit_ts[-1])
                i.perf_ath10k_swba_rx_val.append(i.perf_rx_ts[-1] - i.perf_swba_ts[-1])
                i.perf_ath10k_rx_tx_val.append(i.perf_process_buffer_ts[-1] - i.perf_rx_ts[-1])
                i.perf_ath10k_txcomp_val.append(i.perf_tx_complete_buf_ts[-1] - i.perf_process_buffer_ts[-1])
                
                i.perf_ath10k_br_dev_ts.append(i.perf_br_handle_frame_finish_ts[-1])
                i.perf_ath10k_dev_swba_ts.append(i.perf_dev_hard_start_xmit_ts[-1])
                i.perf_ath10k_swba_rx_ts.append(i.perf_swba_ts[-1])
                i.perf_ath10k_rx_tx_ts.append(i.perf_rx_ts[-1])
                i.perf_ath10k_txcomp_ts.append(i.perf_process_buffer_ts[-1])
              else:
                print((len(i.perf_br_handle_frame_finish_ts),len(i.perf_dev_hard_start_xmit_ts),
              len(i.perf_swba_ts),
              len(i.perf_rx_ts), 
              len(i.perf_process_buffer_ts),
              len(i.perf_tx_complete_buf_ts)))
              # bisect.bisect(a, x)
        elif "ath10k_wmi_event_host_swba" in line:
#           print(line)
          temp_tim = line.split("bitmap: ")[1]
          # print(temp_tim)
#           print(((":" + temp_tim.rstrip().strip() + ":")))
          temp_tim_hex = str(bin(int(temp_tim.rstrip().strip(),16))[2:])
          # print("temp_tim_hex", temp_tim_hex)
          for i in DEVICES.instances:
            i.beacon_wakeup_ts.append((float)(line.split(' ')[0]))
            i.beacon_wakeup_ts_notifier.append(100)
            # print((i.AID))
            if isinstance(i.AID, int) == True and len(temp_tim_hex) > i.AID and i.time_accounting_complete == 0 :
              # print("1...",i.MACADDR, i.AID)
              if (temp_tim_hex[-(i.AID+1)] == '1') or (temp_tim.rstrip().strip() == '40'):
                # print("2...", temp_tim_hex, -(i.AID+1),i.MACADDR, i.AID)
            # if "bitmap: 2" in line:
                i.beacon_tims_ts.append((float)(line.split(' ')[0]))
                i.beacon_tims_notifier.append(100.2)
                i.perf_swba_ts.append((float)(line.split(' ')[0]))
#               else:
#                 print("+++++++++++++")
# #                 print("temp_tim.rstrip().strip()", temp_tim.rstrip().strip())
#                 print("temp_tim_hex", temp_tim_hex)
#                 print("(i.AID+1)", (i.AID+1))
#                 print("temp_tim_hex[-(i.AID+1)]", temp_tim_hex[-(i.AID+1)])
        elif "__sta_info_recalc_tim" in line:
          # print("__sta_info_recalc_tim")
          for i in DEVICES.instances:
            substring = i.MACADDR
            if substring in line and i.time_accounting_complete == 0 :
              i.packet_arrival_ts.append((float)(line.split(' ')[0]))
              i.packet_arrival_notifier.append(99.8)
        lines_processed = lines_processed +1
  for I in DEVICES.instances:
    if end_time > I.time_accounted_for and I.time_accounting_complete == 0:
      if I.curr_ps_state == 0:
        I.time_STA_sleep = I.time_STA_sleep + (end_time - I.time_accounted_for)
      elif I.curr_ps_state == 1:
        I.time_STA_wake = I.time_STA_wake + (end_time - I.time_accounted_for)
      I.time_accounted_for = end_time
  # bEACONS:
  for I in DEVICES.instances:
    I.n_beacons = (int)((end_time - start_time)/.1024)
    if (I.LI>0):
      I.beacon_wakeup = (int)(I.n_beacons/I.LI) 
    if((I.time_STA_wake + I.time_STA_sleep)>0):
      I.list_percentwakeperinterval.append((int)(I.time_STA_wake/(I.time_STA_wake + I.time_STA_sleep)*100))
      I.average_awake_time += ((I.time_STA_wake/(I.time_STA_wake + I.time_STA_sleep))*100)
      I.total_sleep_time = I.total_sleep_time + I.time_STA_sleep
      I.total_awake_time = I.total_awake_time + I.time_STA_wake
      
      # print((int)(I.time_STA_wake/(I.time_STA_wake + I.time_STA_sleep)))
      # print("============================================================================================================")
      # print(I.rx_PS_timestamp)
      # print(I.tx_timestamp)
      # print("length of wake_after_PS:")
      # print(len(I.wake_after_PS))
      # print("length of rx_PS_timestamp:")
      # print(len(I.rx_PS_timestamp))
      # print("length of tx_timestamp:")
      # print(len(I.tx_timestamp))
      
      
      # NORMALIZED. IT WORKS. DONT DELETE BELOW
      # if (len(I.rx_PS_timestamp) > 0):
      #   val_to_sub = I.rx_PS_timestamp[0]
      #   normalized_rx_PS_timestamp = [val - val_to_sub for val in I.rx_PS_timestamp]
      #   print("============================================================================================================")
      #   print(normalized_rx_PS_timestamp)
      # NORMALIZED. IT WORKS. DONT DELETE ABOVE
      
      # | 0.05/ 0.01 + 0.05 | 0.09 / 0.09 + 0.06 | |

      # | 0 | 1 | 2 | 
      # 0.01 0.05 0.06 0.09 | 1.02  1.10  1.23  1.24 | 2.09
      #   A   S     A   S     A     S       A     S
      #check which unit to use and check for sleep/awake time within a second and if it goes over add that to new
      #second. Make sure to modulus each awake/sleep time by 1000 for seconds or more for minutes. 

      # | 0.01 + 0.91 | 0.13  0.76 + 0.02 | |  ==> sleep LIST

      # | 0.04 + 0.03 | 0.08 + 0.01 | |  ==> awake per second List awake[0] / awake[0] + asleep[0]

      # sleep[0] = 0.92
      # awake[0] = 0.07
      # duty cycle for second 0:  ( 0.07 / 0.07 + 0.92 ) * 100


      # sleep[1] = 0.91
      # awake[1] = 0.09
      # duty cycle for second 0:  ( 0.09 / 0.09 + 0.91 ) * 100



      # VARIABLE: last_awake_timestamp: 0.06
      # VARIABLE: last_sleep_timestamp: 0.09


    else:
      I.list_percentwakeperinterval.append(0)




start_time_list = []
timestamp = []

if MODE == 0:
  print("***********", exp_start_time, "--t-->", exp_end_time, "***********")
  periodic_energy_measurment(exp_start_time, exp_end_time)
if MODE == 1:
  for t in range(0, int(exp_end_time) - int(exp_start_time)):
    print("***********", exp_start_time+t, "--t-->", exp_start_time + t+1, "***********")
    periodic_energy_measurment(exp_start_time+t, exp_start_time + t+1)
# for t in range(0, int(exp_end_time) - int(exp_start_time), INTERVAL):
if MODE == 2:
  for t in np.arange(0, int(exp_end_time) - int(exp_start_time), INTERVAL):
    # print("***********", exp_start_time+t, "--t-->", exp_start_time + t + INTERVAL, "***********")
    # print(((exp_start_time + t+INTERVAL) - (exp_start_time+t)))
    if ((exp_start_time + t+INTERVAL) - (exp_start_time+t)) < 1:
      # print("calling periodic_energy_measurment")
      periodic_energy_measurment(exp_start_time+t, exp_start_time + t+INTERVAL)
      # print("lines_processed--",lines_processed)
      #  print("t:", t)
      start_time_list.append(exp_start_time+t)
      timestamp.append(t)

    for I in DEVICES.instances:
      I.time_STA_wake = 0
      I.time_STA_sleep = 0
        #   print("start_time_list", len(start_time_list))
        #   print("beacon_time", I.beacon_wakeup_ts)
        #   print("y",len(I.list_percentwakeperinterval))




for I in DEVICES.instances:
  lst = I.tx_timestamp
  lst = [float(i) for i in lst]
  I.tx_timestamp = lst

  lst = I.beacon_wakeup_ts
  lst = [float(i) for i in lst]
  I.beacon_wakeup_ts = lst
  
  lst = I.rx_data_timestamp
  lst = [float(i) for i in lst]
  I.rx_data_timestamp = lst
  
  lst = I.rx_PS_timestamp
  lst = [float(i) for i in lst]
  I.rx_PS_timestamp = lst
  
  lst = I.beacon_tims_ts
  lst = [float(i) for i in lst]
  I.beacon_tims_ts = lst
  
  lst = I.packet_arrival_ts
  lst = [float(i) for i in lst]
  I.packet_arrival_ts = lst

s = 40

count = 0

for I in DEVICES.instances:
    data = {}
    count += 1
  # if I.MACADDR == "a4:08:ea:b9:45:ba":
    fig = plt.figure()
    print(len(I.tx_timestamp))
    # print("======================================================  X axis ======================================================")
    # print(start_time_list-np.min(I.beacon_wakeup_ts))
    # print("======================================================  Y axis ======================================================")
    # print(I.list_percentwakeperinterval)
    # print("======================================================  percent_Wakeperinterval ======================================================")
    # print(np.mean(I.list_percentwakeperinterval))
    # print("======================================================  average_awake_time ======================================================")
    # print(I.average_awake_time)
    # print("======================================================  differently calculated average ======================================================")
    # print((I.total_awake_time / (I.total_sleep_time + I.total_awake_time)) * 100) 
    
    
    if (I.total_sleep_time + I.total_awake_time > 0):
      with open('graph_insights' + '_' + index + '_' + str(count) + '.js', 'w') as f:
        # f.write('percentages=\'[')
        value = round((I.total_awake_time / (I.total_sleep_time + I.total_awake_time)) * 100,2)
        f.write(str(value))
        f.write("\n")
        f.write(str(I.rx_num_packets))
        f.write("\n")
        f.write(str(I.tx_num_packets))
        # data["percent"+ '_' + index + '_' + str(count)] = value
        # json.dump(data, f)
        # f.write(']\';')
        # f.write(str(round((I.total_awake_time / (I.total_sleep_time + I.total_awake_time)) * 100,2)))
    print("total time ", I.total_sleep_time + I.total_awake_time)
    # plt.plot(start_time_list, I.list_percentwakeperinterval, figure = fig)
    # plt.plot(timestamp, I.list_percentwakeperinterval, figure = fig)
    # print("Timestamp: ", len(timestamp))
    # print("percent_wake_per_interval:", len(I.list_percentwakeperinterval))
    # [0,100,0,| 100,100,100,0]
    prev_time = -1
    percent = 0.0
    average_duty_cycle = []
    list_seconds = []
    # list_seconds.append(0)
    prev_second = 0
    awake_duration_per_second = 0.0
    sleep_duration_per_second = 0.0
    last_time_accounted_for = 0.0
    # print(I.list_percentwakeperinterval)
    
    for i in range(len(timestamp)):
      t = timestamp[i]
      state = I.list_percentwakeperinterval[i]
    # for t, state in timestamp, I.list_percentwakeperinterval:
      if (t < prev_second + 1): # modulo magic: same second
        if (state == 0): 
          sleep_duration_per_second  += (t - last_time_accounted_for)
          last_time_accounted_for = t
        elif (state == 100): 
          awake_duration_per_second  += (t - last_time_accounted_for)
          last_time_accounted_for = t
      else: # next second
        # process the prev seconds' readings
          duty_cycle = (awake_duration_per_second / (sleep_duration_per_second + awake_duration_per_second)) * 100
          average_duty_cycle.append(duty_cycle)
          prev_second += 1
          list_seconds.append(prev_second)
        # increment whatever variables correspond to the seconds
    # plt.plot(list_seconds, average_duty_cycle, figure = fig)

    plt.xticks(np.arange(0,list_seconds[-1],step=10))

    plt.scatter(list_seconds, average_duty_cycle, s = 2, figure = fig)
    plt.plot(list_seconds, average_duty_cycle)
    

    # plt.plot(start_time_list-np.min(I.beacon_wakeup_ts), I.list_percentwakeperinterval, figure = fig)
    # plt.scatter(I.tx_timestamp-np.min(I.beacon_wakeup_ts), I.tx_notifier_waste, marker='v',s=s)
    # plt.scatter(I.beacon_wakeup_ts-np.min(I.beacon_wakeup_ts), I.beacon_wakeup_ts_notifier, marker='x',s=s)
    # plt.scatter(I.rx_data_timestamp-np.min(I.beacon_wakeup_ts), I.rx_data_notifier, marker='^',s=s)
    # plt.scatter(I.rx_PS_timestamp-np.min(I.beacon_wakeup_ts), I.rx_PS_notifier, marker='>',s=s)
    # plt.scatter(I.beacon_tims_ts-np.min(I.beacon_wakeup_ts), I.beacon_tims_notifier, marker='*',s=s)
    # plt.scatter(I.packet_arrival_ts-np.min(I.beacon_wakeup_ts), I.packet_arrival_notifier, marker='d',s=s)
    plt.ylim([0,110])
    plt.xlabel("Seconds")
    plt.ylabel('Duty Cycle %')
    plt.title("Duty Cycle % per Second for \n" + I.device_name, figure = fig)

    # plt.title(I.MACADDR)sys.argv[1]
    if I.MACADDR == MAC_match_with_zero:
      plt.savefig("_Power_Pattern\n" + I.MACADDR, bbox_inches='tight')
    # plt.plot(np.array(I.beacon_wakeup_ts)-np.min(Xa), Ya, 'o')
    ax = plt.gca()
    # ax.get_xaxis().get_major_formatter().set_useOffset(False)
    # plt.yticks([], figure = fig)
    # plt.show()
    # mpld3.show()
    fig.set_size_inches(4, 3)
    file_name = "./figure_" + index + "_" + str(count)  + ".html"
    mpld3.save_html(fig, file_name)
    f.close()


    


for i in DEVICES.instances:
  print(i.MACADDR)
  print(i.AID)
  print()
# print("start_time_list", len(start_time_list))

print("Length of mac instances", len(DEVICES.instances_MAC))
