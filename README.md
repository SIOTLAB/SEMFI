# SEMFI: Software-based Energy Monitoring Tool for WiFi Devices

## Description:
Many WiFi-based Internet of Things (IoT) devices rely on limited energy resources such as battery. Although monitoring and studying the energy consumption of these devices is essential, the use of external, hardware-based energy measure- ment tools is costly and non-scalable, and also introduces many challenges regarding the connectivity of such tool with devices. In this paper, we propose Software-based Energy Management Tool for WiFi (SEMFI), a novel tool to collect, analyze, and monitor the power cycles of IoT devices without need for any external tools. The basic idea is to modify the WiFi Access Point (AP)’s software to keep track of the power status of stations reported in packets. SEMFI also includes backends and frontend components for data storage, analysis, and visualization. We demonstrate the effectiveness and features of SEMFI via empirical evaluations.

## Installation:
1. Install eBPF from iovisor/bcc. Each kingdel has version 21. 
  - Run this command to install all the dependencies for ebpf
     ```sudo apt install -y bison build-essential cmake flex git libedit-dev \ libllvm7 llvm-7-dev libclang-7-dev python zlib1g-dev libelf-dev libfl-dev  python3- distutils ```
2. Run the following commands to install bcc and eBPF:
    ``` mkdir bcc/build; cd bcc/build
    cmake ..
    make -j8
    cmake -DPYTHON_CMD=python3 .. # build python3 binding
    make -j8
    sudo apt install python3.8-distutils
    sudo make install ```
3. Additional commands:
    ``sudo apt install python3-pip
    pip3 install matplotlib
    sudo apt-get install python3-bpfcc``
4. Additional hostapd installation commands:
    ```sudo apt-get install libssl-dev
    sudo apt install libnl-3-dev
    sudo apt-get install libnl-genl-3-dev```
5. Run the PEM file: `sudo strace -e bpf python3 PEM_final_Ebpf_main.py`
    - Be sure the PEM file has the correct pathways in the include/import statements!
    - Used https://www.linuxcompatible.org/story/linux-kernel-51080-released/ to download linux 5.10.80 onto desktop.

## Organization / Layout:
- `ebpf_logs/`:
    - When running the PEM code, it outputs all the data that is piped into a text file called `ebpf_devices_output.txt` in the directory `ebpf_logs/`
    - The Ebpf_Logs_Processing.py file creates text files for each device in this directory 
- `pre_processing_kern_log_logs/`:
    - `Data_Processing` file creates a `kern_logs` that is stored in the directory `pre_processing_kern_log_logs/`
- `hostapd_logs/`:
    - When running the hostapd command, it pipes its output into a file called `host_logs.txt`
- `analyzing_logs/`:
    - Running the `Analyzing_Delay_Components.py` file creates a `host_logs_filtered.txt`, which is piped into this directory

## How to generate graphs:
*Note: For ease of explanation, the commands assume the repository is stored on Desktop*

1 - Run Hostapd:
```sudo ~/Desktop/new_hostapd/hostapd-2.7/hostapd/hostapd -dd -t ~/Desktop/new_hostapd/hostapd-2.7/hostapd/hostapd.conf | tee ~/Desktop/ebpf_code/hostapd_logs/host_logs_1.txt```

 *The log file host_logs_1.txt will be in /ebpf_code/hostapd_logs/*

2 - Run Ebpf:
```sudo strace -e bpf python3 PEM_final_Ebpf_main.py > ebpf_logs/ebpf_devices_output.txt```

*The command will log all of the information about all devices connected to the AP via hostapd in a file, located in `/ebpf_code/ebpf_logs/`*

*The log file will contain low level details such as when a packet was formed, when it entered, when it went from one module to another module, etc; when the beacon was supposed to be formed vs when it actually was ready and when it was sent out.*

*Use your devices at this time. When finished, proceed with the following steps.*


3 - Run ebpf and data processing:
```sudo python3 Ebpf_Logs_Processing.py ``` ⇒ “done + index” to terminal

*This script takes the ebpf_devices_output log file from the PEM code and splits up the information between all of the devices connected to the AP. It creates log files for each device, called `ebpf_devices1.txt`, with the number corresponding to the device’s AID. These log files are located in `/ebpf_code/ebpf_logs/`*

``` sudo python3 Data_Processing.py ``` ⇒ outputs “done” to terminal

*This script operates on the log files created by the `Ebpf_Logs_Processing` script and creates `kern_logs1.txt`, with the number corresponding to the device’s AID. These log files are located in `/ebpf_code/pre_processing_kern_log_logs/`*

4 - Run analyzing:
```sudo python3 Analyzing_Delay_Components.py``` ⇒ creates an html graph which will be updated on the frontend

*This script operates on the kern_logs generated by the `Data_Processing` script, and also operates on the `host_logs_1` generated by the hostapd command, and it creates host_logs_filtered.txt by grepping for 2021 in `host_logs_1`. This script will result in `host_logs_filtered.txt`, `output.txt`, and `app.log`, which is stored in `/ebpf_code/analyzing_logs/`. This will also generate graphs for a given device.*


## How to run the frontend:
Open the file in the `frontend/static/ directory` titled `home.html`.


