#!/bin/bash
mkdir -p benchmark_info
cd benchmark_info

echo "=== CPU Info ===" > hardware_summary.txt
lscpu >> hardware_summary.txt

echo -e "\n=== Memory Info ===" >> hardware_summary.txt
free -h >> hardware_summary.txt

echo -e "\n=== Disk Info ===" >> hardware_summary.txt
lsblk >> hardware_summary.txt

echo -e "\n=== System Info ===" >> hardware_summary.txt
uname -a >> hardware_summary.txt
hostnamectl >> hardware_summary.txt

echo -e "\n=== GPU Info ===" >> hardware_summary.txt
lspci | grep -i vga >> hardware_summary.txt

# Se tiver NVIDIA
if command -v nvidia-smi &> /dev/null; then
    echo -e "\n=== NVIDIA GPU ===" >> hardware_summary.txt
    nvidia-smi >> hardware_summary.txt
fi

echo -e "\nResumo salvo em benchmark_info/hardware_summary.txt"
