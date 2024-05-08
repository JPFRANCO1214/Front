from Devices import Device
import time
import concurrent.futures
from functions import get_device_neighbor_details, get_device_info
import json

# Inicio del tiempo
inicio = time.time()

if __name__ == "__main__":

    all_devices = []
    used_IPs = []
    unused_IPs = []
    neighbor_device = []
    deviceNum = 0
    counter = 0 
    ind = 0

    json_Pack = []

    ip = "192.168.0.1"#input("Hola ip")
    username = "gmedina"# input("Hola username")
    password ="cisco" #input("Hola password")
    secret = "cisco"#input("Hola secret")

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Lanzamos las tareas
            devicet = executor.submit(get_device_info,ip,username,password,secret)
            neighbor =executor.submit(get_device_neighbor_details,ip,username,password,secret)
            # Obtenemos los resultados

            current_device = devicet.result()#aqui no jala
            neighbor_device,type = neighbor.result()#aqui no jala

            #creo un objeto tipo device

            all_devices.append(Device(ip))      
            all_devices[deviceNum].set_interfaces(current_device[0],current_device[1])

            for x in range(len(neighbor_device)):
                all_devices[deviceNum].interfaces
                if neighbor_device[x][0] == current_device[0][0]:
                    break
                for z in all_devices[deviceNum].interfaces:
                    if z["Interface"] == neighbor_device[x][5] or z["Interface"] == "Vlan1":
                        local_Ip = z["IPv4"]
                        all_devices[deviceNum].set_connections(neighbor_device[x][4],local_Ip, type[x][2], neighbor_device[x][5], neighbor_device[x][2])

            for x in all_devices[deviceNum].interfaces:
                if x["IPv4"] != 'unassigned':
                    used_IPs.append(x["IPv4"])
                  

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

            for x in unused_IPs:
                if x in used_IPs:
                    unused_IPs.remove(x)

            if len(unused_IPs) == 0:
                break

    for device in all_devices:
        interfaces = [{'Interface': i['Interface'], 'IPv4': i['IPv4'], 'IPv6': i['IPv6'], 'Link-local': i['Link-local']} for i in device.interfaces]
        connections = [{'Connected_from_Interface': c['Connected_from_Interface'], 'From_IP': c['From_IP'], 'Device': c['Device'], 'Connected_to_Interface': c['Connected_to_Interface'], 'To_IP': c['To_IP']} for c in device.connections]
        json_Pack.append({
            'deviceType': device.deviceType,
            'ip': device.ip,
            'interfaces': interfaces,
            'connections': connections
        })
        ind += 1
    res = json.dumps(json_Pack)
    print(res)
    # Fin del tiempo
    #fin = time.time()
    # Cálculo del tiempo transcurrido
    #tiempo_transcurrido = fin - inicio
    #print("Tiempo transcurrido:", tiempo_transcurrido, "segundos")