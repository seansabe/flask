#!/bin/bash


VM='Ubuntu-Machine-One'
VBoxManage createhd --filename $VM.vdi --size 32768
VBoxManage createvm --name $VM --ostype "Ubuntu_64" --register
VBoxManage storagectl $VM --name "SATA Controller" --add sata --controller IntelAHCI
VBoxManage storageattach $VM --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM.vdi
VBoxManage storageattach $VM --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium /Users/seansabe/Desktop/taller/ubuntu.iso
VBoxManage modifyvm $VM --ioapic on
VBoxManage modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage modifyvm $VM --memory 1024 --vram 128
VBoxManage modifyvm $VM --nic1 bridged --bridgeadapter1 e1000g0


VM2='Ubuntu-Machine-Two'
VBoxManage createhd --filename $VM2.vdi --size 32768
VBoxManage createvm --name $VM2 --ostype "Ubuntu_64" --register
VBoxManage storagectl $VM2 --name "SATA Controller" --add sata --controller IntelAHCI
VBoxManage storageattach $VM2 --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM2.vdi
VBoxManage storageattach $VM2 --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium /Users/seansabe/Desktop/taller/ubuntu.iso
VBoxManage modifyvm $VM2 --ioapic on
VBoxManage modifyvm $VM2 --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage modifyvm $VM2 --memory 1024 --vram 128
VBoxManage modifyvm $VM2 --nic1 bridged --bridgeadapter1 e1000g0


VM4='Ubuntu-Machine-Three'
VBoxManage createhd --filename $VM4.vdi --size 32768
VBoxManage createvm --name $VM4 --ostype "Ubuntu_64" --register
VBoxManage storagectl $VM4 --name "SATA Controller" --add sata --controller IntelAHCI
VBoxManage storageattach $VM4 --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM4.vdi
VBoxManage storageattach $VM4 --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium /Users/seansabe/Desktop/taller/ubuntu.iso
VBoxManage modifyvm $VM4 --ioapic on
VBoxManage modifyvm $VM4 --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage modifyvm $VM4 --memory 1024 --vram 128
VBoxManage modifyvm $VM4 --nic1 bridged --bridgeadapter1 e1000g0
