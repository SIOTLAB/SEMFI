import logging
import os
import sys
import json
index_list = ['1', '2']

f_1 = open("percent_duty_cycle.js", "w")
f_1.write('percentages=\'[')

f_2 = open("rx_num_packets.js", "w")
f_2.write('rx_num_packets=\'[')

f_3 = open("tx_num_packets.js", "w")
f_3.write('tx_num_packets=\'[')

data_1 = {}
data_2 = {}
data_3 = {}
for index in index_list:
    with open("graph_insights" + "_" + index + "_" + index + ".js") as raw_file:
        lines = raw_file.readlines()
    data_1["percent"+ '_' + index + '_' + index] = float(lines[0])
    data_2["rx_packets"+ '_' + index + '_' + index] = int(lines[1])
    data_3["tx_packets"+ '_' + index + '_' + index] = int(lines[2])
    raw_file.close()
    print("done " + index)

json.dump(data_1, f_1)
json.dump(data_2, f_2)   
json.dump(data_3, f_3)  
f_1.write(']\';')
f_2.write(']\';')
f_3.write(']\';')

f_1.close()
f_2.close()
f_3.close()