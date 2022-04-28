import logging
import os
import sys



# MAC_match = "a4:8:ea:d9:c7:d8"
# MAC_match_with_zero = "a4:08:ea:d9:c7:d8"
# MAC_match_first_three = "a4:0:8"


# 94:65:2d:f1:e2:22
# MAC_match = "a:8:ea:d9:c7:24"
# MAC_match_with_zero = "a4:08:ea:d9:c7:24"
# MAC_match_first_three = "a4:0:8"      



# OURS
# MAC_match = "ba:88:a3:ed:d9:c3"
# MAC_match_with_zero = "ba:88:a3:ed:d9:c3"
# MAC_match_first_three = "ba:88:a3"           



                    
# MAC_match_first_three_with_zero = "a4:08:ea:d9:c7:d8"

logging.basicConfig(filename='pre_processing_kern_log_logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

# logging.basicConfig(level=logging.DEBUG)

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')


# index_list = ['2021_1','2021_2','2021_3','2021_4','2021_5','2021_6','2021_7','2021_8','2021_9','2021_10',
#              '2023_2','2023_3','2023_4','2023_5','2023_6','2023_7','2023_8','2023_9','2023_10',
#              '2025_2','2025_3','2025_4','2025_5','2025_6','2025_7','2025_8','2025_9','2025_10',
#              '2027_1','2027_2','2027_3','2027_4','2027_5','2027_6','2027_7','2027_8','2027_9',
#              '2029_1','2029_2','2029_3','2029_4','2029_5','2029_6','2029_7','2029_8','2029_9','2029_10']
# index_list = ['2025_11','2025_12','2025_13','2025_14','2025_15']


# DOING MAC_MATCH FOR MAC ADDR WITH 0 IN IT:
# MAC_match_list = ["ba:88:a3:ed:d9:c3", "6a:9:3e:12:d9:f8", "1a:e3:a1:68:1:3f"]
# MAC_match_with_zero_list = ["ba:88:a3:ed:d9:c3", "6a:09:3e:12:d9:f8", "1a:e3:a1:68:01:3f"]
# MAC_match_first_three_list = ["ba:88:a3", "6a:0:9", "1a:e3:a1"]

index_list = ['1', '2', '3']
MAC_match_list = ["ba:88:a3:ed:d9:c3", "90:9c:4a:cc:77:94", "1a:e3:a1:68:1:3f"]
MAC_match_with_zero_list = ["ba:88:a3:ed:d9:c3", "90:9c:4a:cc:77:94", "1a:e3:a1:68:01:3f"]
MAC_match_first_three_list = ["ba:88:a3", "90:9c:4a", "1a:e3:a1"]

# for index in index_list:
for i in range (len(index_list)):
    index = index_list[i]
    MAC_match = MAC_match_list[i]
    MAC_match_with_zero = MAC_match_with_zero_list[i]
    MAC_match_first_three = MAC_match_first_three_list[i]

    f = open("pre_processing_kern_log_logs/kern_logs_ebpf" + index + ".txt", "w")
    # f.write("Now the file has more content!")

    with open('ebpf_logs/ebpf_devices_' + index + '.txt') as raw_file:
        lines = raw_file.readlines()
    for i in range(len(lines)):
        logging.debug(lines[i])
        if len(lines[i]) < 5:
            logging.warning(len(lines[i]), ":", lines[i])
        if "[2021][ath_tx_complete_buf]::7::peerd[1]" in lines[i]:
            for j in range(i, len(lines)):
                if "[2021][ath_tx_complete_buf]::7::peerd[2]" in lines[j]:
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("peerd[2]")[1].split(" ")[1]
                    if MAC_match in lines[i]:
                        lines[i] = lines[i].split(MAC_match)[0] + MAC_match_with_zero + lines[i].split(MAC_match)[1]
                    break
            logging.info(lines[i])
            f.write(lines[i])
        if "[2021][ath_tx_txqaddbuf]::7::peerd[1]" in lines[i]:
            for j in range(i, len(lines)):
                if "[2021][ath_tx_txqaddbuf]::7::peerd[2]" in lines[j]:
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("peerd[2]")[1].split(" ")[1]
                    if MAC_match in lines[i]:
                        lines[i] = lines[i].split(MAC_match)[0] + MAC_match_with_zero + lines[i].split(MAC_match)[1]
                    break
            logging.info(lines[i])
            f.write(lines[i])
        if "[br_handle_frame_finish]Source IP[1]=" in lines[i]:
            for j in range(i, len(lines)):
                if "[br_handle_frame_finish]Source MAC[1]=" in lines[j]:
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("Source MAC[1]=")[1]
                    lines[i] = lines[i].replace(MAC_match_first_three, MAC_match_with_zero)
    # 				print(lines[i])
    # 				print("llll")
                    break
            logging.info(lines[i])
            f.write(lines[i])
        if "[dev_hard_start_xmit]Source IP[1]=" in lines[i]:
            for j in range(i, len(lines)):
                if "[dev_hard_start_xmit]Source MAC[1]=" in lines[j]:
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("Source MAC[1]=")[1]
    # 				print("(1)", lines[i])
                    lines[i] = lines[i].replace(MAC_match_first_three, MAC_match_with_zero)
    # 				print(lines[i])
    # 				print("llll")
                    break
            logging.info(lines[i])
            f.write(lines[i])
        if "[2021][ath10k_process_rx]RECEIVED a [data] packet::2::::7::peerd[1]" in lines[i]:
            for j in range(i, len(lines)):
                if ("2021][ath10k_process_rx]RECEIVED a [data] packet::2::::7::peerd[2]" in lines[j]) and ("2021][ath10k_process_rx]RECEIVED a [data] packet::2::::7::peerd[3]" in lines[j+1]):
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("peerd[2]")[1].split(" ")[1].split("\n")[0] + lines[j+1].split("peerd[3]")[1].split(" ", 1)[1]
                    if MAC_match in lines[i]:
                        lines[i] = lines[i].split(MAC_match)[0] + MAC_match_with_zero + lines[i].split(MAC_match)[1]
                    break
            logging.info(lines[i])
            f.write(lines[i])	
        if "swba" in lines[i]:
            if MAC_match in lines[i]:
                        lines[i] = lines[i].split(MAC_match)[0] + MAC_match_with_zero + lines[i].split(MAC_match)[1]
            logging.info(lines[i])

            f.write(lines[i])
        if "[2021][__sta_info_recalc_tim]::7::peerd[1]" in lines[i]:
            for j in range(i, len(lines)-3):
                if ("[2021][__sta_info_recalc_tim]::7::peerd[2]" in lines[j]) and ("[2021][__sta_info_recalc_tim]::7::peerd[3]" in lines[j+1]):
    # 				print("1....", lines[i].split("\n")[0])
    # 				print("2....", lines[j].split("peerd[2]")[1].split(" ")[1].split("\n")[0])
    # 				print("3....", lines[j+1].split("peerd[3]")[1].split(" ", 1)[1])
                    lines[i] = lines[i].split("\n")[0] + ":" + lines[j].split("peerd[2]")[1].split(" ")[1].split("\n")[0] + " " +lines[j+1].split("peerd[3]")[1].split(" ", 1)[1]
                    break
            if MAC_match in lines[i]:
                        lines[i] = lines[i].split(MAC_match)[0] + MAC_match_with_zero + lines[i].split(MAC_match)[1]
            logging.info(lines[i])
            f.write(lines[i])




    f.close()
    print("done")
