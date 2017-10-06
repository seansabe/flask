#!/usr/bin/python
#
# El siguiente programa permite obtener algunos valores de un sistema operativo
# Linux (algunas cosas funcionan en Mac) pero que se accede a la informacion a
# traves de Web Services.
#
# El proposito es que usted haga una especie de "llene los espacios en blanco"
# para que se vaya familiarizando con la forma como se desarrollan los Web
# Services.
#
# La forma como se accede a los web services disponibles en esta aplicacion
# se pueden ver en este video https://asciinema.org/a/E8IRAWHvzd8zOLuI0o1DjYNnN
#

# Librerias que se requieren para correr la aplicacion
from flask import Flask, jsonify, request, make_response
import subprocess, pickle

# Se crea un objeto de tipo Flask llamado 'app'
app = Flask(__name__)


#
# Web service que entrega lista de tipo de sistemas operativos que son soportados por VirtualBox.
# Metodo de acceso
# Comando: VBoxManage list ostypes
# La forma como debe consumirse este servicio desde terminal es: curl http://localhost:5000/vms/ostypes
#
@app.route('/vms/ostypes', methods=['GET'])
def ostypes():
    soPermit = subprocess.check_output(['VBoxManage', 'list', 'ostypes'])
    return soPermit


#
# Web service que entrega la lista de máquinas virtuales que pertenecen al usuario.
# Metodo de acceso
# Comando VBoxManage list vms
# La forma como debe consumirse este servicio desde terminal es: curl http://localhost:5000/vms
#
@app.route('/vms', methods=['GET'])
def vms():
    vmsList = subprocess.check_output(['VBoxManage', 'list', 'vms'])
    return vmsList


#
# Web service que entrega la lista de las máquinas que se encuentran en ejecución.
# Metodo de acceso
# Comando: VBoxManage list runningvms
# La forma como debe consumirse este servicio desde terminal es: curl http://localhost:5000/vms/running
#
@app.route('/vms/running', methods=['GET'])
def vmbRunVm():
    vmsRunList = subprocess.check_output(['VBoxManage', 'list', 'runningvms'])
    return vmsRunList


#
# Web services que recupera informacion de número de CPUs, memoria RAM e interfaces de red de una maquina virtual,
# se debe ingresar el nombre de la mauina virtual.
# Metodo de acceso
# Comando: VBoxManage showvminfo ?????
# La forma como debe consumirse este servicio desde terminal es: curl http://localhost:5000/vms/info/vmname
#
@app.route('/vms/info/<string:param>/<string:param2>', methods=['GET'])
def vbmNCPUS(param, param2):
    vboxManage = subprocess.Popen(['VBoxManage', 'showvminfo', param], stdout=subprocess.PIPE)
    if (param2 == "cpu"):
        grepCPU = subprocess.Popen(['grep', 'Number of CPUs'], stdin=vboxManage.stdout, stdout=subprocess.PIPE)
        valueCPUS = subprocess.check_output(['cut', '-d', ':', '-f', '2'], stdin=grepCPU.stdout)
        return valueCPUS
    elif (param2 == "ram"):
        grepRAM = subprocess.Popen(['grep', 'Memory size'], stdin=vboxManage.stdout, stdout=subprocess.PIPE)
        valueRAM = subprocess.check_output(['cut', '-d', ':', '-f', '2'], stdin=grepRAM.stdout)
        return valueRAM
    elif (param2 == "ired"):
        grepNIC = subprocess.Popen(['grep', 'NIC'], stdin=vboxManage.stdout, stdout=subprocess.PIPE)
        grepV = subprocess.Popen(['grep', '-v', 'disabled'], stdin=grepNIC.stdout, stdout=subprocess.PIPE)
        grepMAC = subprocess.Popen(['grep', 'MAC'], stdin=grepV.stdout, stdout=subprocess.PIPE)
        tr = subprocess.Popen(['tr', '-s', ' '], stdin=grepMAC.stdout, stdout=subprocess.PIPE)
        cut = subprocess.Popen(['cut', '-d', ' ', '-f', '6'], stdin=tr.stdout, stdout=subprocess.PIPE)
        valueIFRED = subprocess.check_output(['cut', '-d', ',', '-f', '1'], stdin=cut.stdout)
        return valueIFRED
    else:
        return make_response(jsonify({'error': 'Possible values swpd, free, buff, cache'}), 404)

#
# Web services que crea una maquina virtual.
# Ejecuta el script de creacion de maquina virtual debe mandar en al url los parametros 4
# nucleos, 580 MB de RAM y la maquina se debe llamar os-web
#./CreateVirtualMachine.sh UbuntuServerXenial Ubuntu 2024 548 1
# La forma como debe consumirse este servicio desde terminal es:
# curl -i -H "Content-Type: application/js on" -X POST -d '{"vmName":"os-web","vmRam":"548","vmCpu":"1"}' http://localhost:5000/vms/
#
@app.route('/vms', methods=['POST'])
def create_task():
    vmName = request.json['vmName']
    vmRam = request.json['vmRam']
    vmCpu = request.json['vmCpu']
    vmsCreate = subprocess.check_output(['./createvm.sh', vmName, vmRam, vmCpu])
    return jsonify({'Create Virtual machin': 'Succesfull'})



#
# Web services que elimina una maquina virtual.
# Ejecuta el script de borrado de maquina virtual ingresando como parametro de entrada el nombre de la maquina virtual
# La forma como debe consumirse este servicio desde terminal es: curl -i -X DELETE http://localhost:5000/vms/vmname
#
@app.route('/vms/<string:param>', methods=['DELETE'])
def delete_task(param):
    if (param != None):
        # VBoxManage controlvm $1 poweroff
        # VBoxManage unregistervm $1 --delete
        deleteCtrlvm = subprocess.check_output(['./deletevm.sh', param])
    else:
        return make_response(jsonify({'error': 'Name virtual machine cant be null. VBoxManage showvminfo param'}), 404)

    return jsonify({'Delete Virtual machin': 'Succesfull'})


#
# Este es el punto donde arranca la ejecucion del programa
#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
