from Devices import Device
import time
import sys
import concurrent.futures
from functions import get_device_neighbor_details, get_device_info
import json
import sqlite3



def insert_data_to_database(data):
    try:
        conn = sqlite3.connect('C:/Users/valen/OneDrive/Documents/REDESS/NAS/NODE_EXPRESS_API/pyscript/network_data.db')  
        c = conn.cursor()

        for device in data:
            c.execute('INSERT INTO devices (deviceType, ip, SystemVersion, Model, Serie) VALUES (?, ?, ?, ?, ?)',
                  (device['deviceType'], device['ip'], device['SystemVersion'], device['Model'], device['Serie']))
            device_id = c.lastrowid

            for interface in device['interfaces']:
                c.execute('''INSERT INTO interfaces (device_id, interface, IPv4, IPv6, link_local) VALUES (?, ?, ?, ?, ?)''',
                          (device_id, interface['Interface'], interface['IPv4'], interface['IPv6'], interface['Link-local']))

            for connection in device['connections']:
                c.execute('''INSERT INTO connections (device_id, connected_from_interface, from_ip, connected_to_device, connected_to_interface, to_ip) VALUES (?, ?, ?, ?, ?, ?)''',
                          (device_id, connection['Connected_from_Interface'], connection['From_IP'], connection['Device'], connection['Connected_to_Interface'], connection['To_IP']))

        conn.commit()
        conn.close()
        print("Success")
    except Exception as e:
        print("Error:", e)

try:
    if __name__ == "__main__":
        hostnamesNei = []
        hostNum = 0
        all_devices = []
        used_IPs = ['148.239.61.210']
        unused_IPs = []
        neighbor_device = []
        deviceNum = 0
        counter = 0 
        ind = 0

        json_Pack = []

        ip = "192.168.1.1" #input("Hola ip")
        username = "gmedina" #input("Hola username")
        password = "cisco" #input("Hola password")
        secret = "cisco" #input("Hola secret")
        SyslogServer = "192.168.1.19"

        while True:
            #print(ip)
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # Lanzamos las tareas
                devicet = executor.submit(get_device_info,ip,username,password,secret)
                neighbor =executor.submit(get_device_neighbor_details,ip,username,password,secret,SyslogServer)
                # Obtenemos los resultados
                current_device = devicet.result()#aqui no jala
                neighbor_device,type = neighbor.result()#aqui no jala
                
                for x in neighbor_device:
                    HostNei = x[1]
                    HostNei = HostNei.rstrip('.uag.mx')
                    hostnamesNei.append(HostNei)

                #creo un objeto tipo device
                all_devices.append(Device(ip))      
                all_devices[deviceNum].set_interfaces(current_device[0],current_device[1],current_device[2][0][4])
                for x in range(len(neighbor_device)):
                    all_devices[deviceNum].interfaces
                    if neighbor_device[x][0] == current_device[0][0]:
                        break
                    for z in all_devices[deviceNum].interfaces:
                        if z["Interface"] == neighbor_device[x][5] or z["Interface"] == "Vlan1":
                            local_Ip = z["IPv4"]
                            all_devices[deviceNum].set_connections(all_devices[deviceNum].hostname,neighbor_device[x][4],local_Ip,hostnamesNei[hostNum], type[x][2], neighbor_device[x][5], neighbor_device[x][2])
                            if len(hostnamesNei)-1 > hostNum:
                                hostNum += 1

                hostnamesNei = []
                hostNum = 0

                all_devices[deviceNum].setInfo(current_device[2][0][14][0],current_device[2][0][0],current_device[2][0][1])

                for x in all_devices[deviceNum].interfaces:
                    if x["IPv4"] != 'unassigned':
                        used_IPs.append(x["IPv4"])
                        if x["IPv4"] in unused_IPs:
                            unused_IPs.remove(x["IPv4"])

                if ip not in used_IPs:
                    used_IPs.append(ip)

                for x in neighbor_device:
                    if x[2] not in used_IPs:
                        if x[2] not in unused_IPs:
                            unused_IPs.append(x[2])

                if ip in unused_IPs: 
                    unused_IPs.remove(ip)

                if len(unused_IPs) >= 1:
                    deviceNum += 1
                    ip = unused_IPs[0]

                #print('Usadas:',used_IPs,'No usadas: ',unused_IPs)

                for x in unused_IPs:
                    if x in used_IPs:
                        unused_IPs.remove(x)

                if len(unused_IPs) == 0:
                    break

        for device in all_devices:
            interfaces = [{'Interface': i['Interface'], 'IPv4': i['IPv4'], 'IPv6': i['IPv6'], 'Link-local': i['Link-local']} for i in device.interfaces]
            connections = [{"MyHost":device.hostname,'Connected_from_Interface': c['Connected_from_Interface'], 'From_IP': c['From_IP'],'HostNei': c['HostNei'], 'Device': c['Device'], 'Connected_to_Interface': c['Connected_to_Interface'], 'To_IP': c['To_IP']} for c in device.connections]
            json_Pack.append({
                'deviceType': device.deviceType,
                'ip': device.ip,
                'SystemVersion': device.SysVersion,
                'Model': device.modelo,
                'Serie': device.numeroSerie,
                'interfaces': interfaces,
                'connections': connections,
                'MyHost' : device.hostname
            })
            ind += 1
            
            #print(device)
        res = json.dumps(json_Pack)
        #insert_data_to_database(json_Pack)

        print(res)
except Exception as error:
        print("Error:",error)