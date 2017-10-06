#!/bin/bash

#
# Comando en bash para crear maquinas virtuales
# en VirtualBox.
#
# La ejecucion del script recibe como entrada 8 parametros:

#
# $1 = Nombre de Maquina Virtual
## $2 = Cantidad en MB del Disco Duro
## $3 = Cantidad en MB de Memoria RAM
## $4 = Numero de CPUs
#
# usuario@linux~$ ./CreateVirtualMachine.sh UbuntuServerXenial Ubuntu 548 1

# Configura las variables con las entradas del usuario
VM=$1
RAMSIZE=$2
CPUS=$3


# Crear una maquina virtual
VBoxManage createvm --name $VM --register

# Crear disco duro para maquina virtual
VBoxManage createhd --filename $VM.vdi --size 2024 --format VDI

# Crear controlador para dispositivos de almacenamiento
VBoxManage storagectl $VM --name "IDE Controller" --add ide

# Vincula un disco duro virtual al controlador
VBoxManage storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium $VM.vdi

# Especifica el tipo de sistema operativo que tiene la maquina virtual
VBoxManage modifyvm $VM --ostype Ubuntu

# Asigna una cantidad de memoria RAM a la maquina virtual
VBoxManage modifyvm $VM --memory $RAMSIZE

# Asigna un numero de nucleos para CPUs de la maquina virtual
VBoxManage modifyvm $VM --cpus $CPUS

# Establece el porcentaje de procesamiento asignado a la CPU
VBoxManage modifyvm $VM --cpuexecutioncap 100

# Configura la tarjeta de red de la maquina virtual
VBoxManage modifyvm $VM --nic1 bridged
