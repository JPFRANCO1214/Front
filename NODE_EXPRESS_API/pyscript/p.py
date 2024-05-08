from netmiko import ConnectHandler
import textfsm
from functions import get_device_neighbor_details, get_device_info
device = {
        'device_type': 'cisco_ios', 
        'host': '192.168.0.18',
        'username': 'gmedina',
        'password': 'cisco',
    }

try:
    ssh_session = ConnectHandler(**device)
    cdp_result= ssh_session.find_prompt() + "\n"#Te da el modo actual de CLI junto con el nombre del host

    cdp_result += ssh_session.send_command("show cdp neighbor detail", delay_factor=2)#te consigue la informacion CD
    #procesar info para enviar a servidor
    print(cdp_result)
    ssh_session.disconnect()
except Exception as e:
    print("Error al iniciar sesión SSH:", str(e))