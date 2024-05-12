class Device:
    def __init__(self,ip):
        self.deviceType = ""
        self.hostname = ""
        self.ip = ip
        self.interfaces = []
        self.connections = []
        self.SysVersion = None
        self.modelo = None
        self.numeroSerie = None
        self.internet = False

    def set_internet(self):
        self.internet = True

    def set_interfaces(self,intv4,intv6,hostname):
        self.hostname = hostname
        index = 3
        counter = 0
        for x,y in zip(intv4,intv6):
            self.interfaces += [
                {"Interface":x[0],"IPv4":x[1],"IPv6":y[1][1],"Link-local":y[1][0]}
            ]
            counter += 1
         # Actualiza el tipo de dispositivo basado en el número de conexiones
        if counter > 8:
            self.deviceType = "Switch"
        else:
            self.deviceType = "Router"

    def set_connections(self,MyHost,To_interface,From_IP,HostNei,typeD,From_interface,IP_Connected):
        for x in self.connections:
            if x["To_IP"] == IP_Connected:
                return False
        if typeD == "S I":
            typeD = "Switch"
        else:
            typeD = "Router"
        self.connections += [
            {"MyHost":MyHost,"Connected_from_Interface":From_interface,"From_IP":From_IP,"HostNei": HostNei,"Device": typeD,"Connected_to_Interface":To_interface,"To_IP":IP_Connected}
            ]
        
    def to_dict(self):
        # Convertir las listas de interfaces y conexiones en listas de diccionarios
        interfaces_dict = [{"Interface": i["Interface"], "IPv4": i["IPv4"], "IPv6": i["IPv6"], "Link-local": i["Link-local"]} for i in self.interfaces]
        connections_dict = [{"Connected_from_Interface": c["Connected_from_Interface"], "From_IP": c["From_IP"], "Device": c["Device"], "Connected_to_Interface": c["Connected_to_Interface"], "To_IP": c["To_IP"]} for c in self.connections]

        # Crear un diccionario con los datos de Device
        device_dict = {
            "deviceType": self.deviceType,
            "ip": self.ip,
            "interfaces": interfaces_dict,
            "connections": connections_dict
        }

        return device_dict
        
    def setInfo(self,version,model,serial):
        self.SysVersion = version
        self.modelo = model
        self.numeroSerie = serial

    def __str__(self):
        device_str = f"Device Type: {self.deviceType}\n"
        device_str += f"Hostname: {self.hostname}\n"
        device_str += f"IP Address: {self.ip}\n"
        device_str += f"System version: {self.SysVersion}\n"
        device_str += f"Model: {self.modelo}\n"
        device_str += f"Serial: {self.numeroSerie}\n"

        if self.interfaces:
            device_str += "Interfaces:\n"
            for interface in self.interfaces:
                device_str += (
                    f"- Interface: {interface['Interface']}, "
                    f"IPv4: {interface['IPv4']}, "
                    f"IPv6: {interface['IPv6']}, "
                    f"Local-link: {interface['Link-local']}\n"
                )

        if self.connections:
            device_str += "Connections:\n"
            for conn in self.connections:
                device_str += f"-From host: {conn['MyHost']} From Interface: {conn['Connected_from_Interface']}, From IP: {conn['From_IP']},To host: {conn['HostNei']} ,Device: {conn['Device']} , To Interface: {conn['Connected_to_Interface']}, To IP: {conn['To_IP']}\n"
        else:
            device_str += "No connections."

        return device_str