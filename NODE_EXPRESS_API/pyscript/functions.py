import textfsm
from netmiko import ConnectHandler

def get_device_neighbor_details(ip, username, password, enable_secret):
    try:
        cdp_template = textfsm.TextFSM(open("Templates/show_cdp_neighbor_detail.textfsm"))
        type_template = textfsm.TextFSM(open("Templates/cisco_ios_show_cdp_neighbors.textfsm"))
        ssh_connection = []
        cdp_result = []
        type_result = []
        fsm_cdp_results = []
        fsm_type_results = []
        #Inicia SSH
        ssh_connection = ConnectHandler(
            device_type='cisco_ios',
            ip=ip,
            username=username,
            password=password,
            secret=enable_secret
        )
    except Exception as error:
        return error

    ssh_connection.enable()#Activa modo EXEC privilegiado

    cdp_result= ssh_connection.find_prompt() + "\n"#Te da el modo actual de CLI junto con el nombre del host
    type_result = cdp_result


    #Informacion de vecinos
    cdp_result += ssh_connection.send_command("show cdp neighbor detail", delay_factor=2)#te consigue la informacion CDP
    type_result += ssh_connection.send_command("show cdp neighbor", delay_factor=2)#te consigue la informacion CDP

    #Desconectar SSH
    ssh_connection.disconnect()

    #procesar info para enviar a servidor
    fsm_cdp_results = cdp_template.ParseText(cdp_result)
    fsm_type_results = type_template.ParseText(type_result)

    return fsm_cdp_results,fsm_type_results

def get_device_info(ip, username, password, enable_secret):
    try:
        int_brief_template = textfsm.TextFSM(open("Templates/cisco_ios_show_ip_interface_brief.textfsm"))
        intv6_brief_template = textfsm.TextFSM(open("Templates/cisco_ios_show_ipv6_interface_brief.txtfsm"))
        ssh_connection = []
        int_brief_result = []
        intv6_brief_result = []
        fsm_int_results = []
        fsm_intv6_results = []

        #Inicia SSH
        ssh_connection = ConnectHandler(
            device_type='cisco_ios',
            ip=ip,
            username=username,
            password=password,
            secret=enable_secret
        )

    except Exception as error:
        return error

    ssh_connection.enable()#Activa modo EXEC privilegiado

    int_brief_result = ssh_connection.find_prompt() + "\n"#Te da el modo actual de CLI junto con el nombre del host
    intv6_brief_result = int_brief_result
    #Informacion de interfaces
    int_brief_result += ssh_connection.send_command("show ip interface brief", delay_factor=3)#te consigue la informacion de interfaces del dispositivo

    intv6_brief_result += ssh_connection.send_command("show ipv6 interface brief", delay_factor=3)#te consigue la informacion de interfaces del dispositivo

    #Desconectar SSH
    ssh_connection.disconnect()

    #procesar info para enviar a servidor
    fsm_int_results = int_brief_template.ParseText(int_brief_result)
    fsm_intv6_results = intv6_brief_template.ParseText(intv6_brief_result)

    for x in fsm_intv6_results:
        if x[1][0] == "unassigned":
            x[1].append("unassigned")

    result =[fsm_int_results,fsm_intv6_results]

    return result

def ssh_login(device_ip, username, password):
    device = {
        'device_type': 'cisco_ios', 
        'host': device_ip,
        'username': username,
        'password': password,
    }

    try:
        ssh_session = ConnectHandler(**device)
        print("¡Conexión SSH exitosa!")
        return ssh_session
    except Exception as e:
        print("Error al iniciar sesión SSH:", str(e))
        return None
    
def change_hostname(ssh,hostname):
    config_commands = [
                f"hostname {hostname}"
            ]
    
    ssh.send_config_set(config_commands)

def change_int_ip(ssh,ip,mask,interface):

    config_commands = [
                f'interface {interface}',
                f'ip address {ip} {mask}',
                'no shutdown'
            ]
    
    ssh.send_config_set(config_commands)

def change_int_desc(ssh,interface,desc):

    config_commands = [
                f'interface {interface}',
                f'description {desc}'
            ]
    
    ssh.send_config_set(config_commands)

def change_motd(ssh,motd):

    config_commands = [
                f'banner motd ^{motd}^'
            ]
    
    ssh.send_config_set(config_commands)

def change_intv6_ip(ssh,ipv6,mask,interface):

    config_commands = [
                f'interface {interface}',
                f'ipv6 address {ipv6}{mask}',
                'no shutdown'
            ]
    
    ssh.send_config_set(config_commands)

def ipv6_unicast(ssh):

    config_commands = [
                "ipv6 unicast-routing"
            ]
    
    ssh.send_config_set(config_commands)

def ip_route(ssh,ip,mask,rute):
    config_commands = [
                f'ip route {ip}{mask} {rute}'
            ]
    ssh.send_config_set(config_commands)

def ipv6_route(ssh,ipv6,mask,rute):
    config_commands = [
                f'ip route {ipv6}{mask} {rute}'
            ]
    ssh.send_config_set(config_commands)

def new_user(ssh,user,priv,secret):
    config_commands = [
                f"username {user} privilege {priv} secret {secret}"
            ]
    ssh.send_config_set(config_commands)

def loggin_syn(ssh):
    config_commands = [
        'line vty 0 15',
        'logging synchronous'
        'exit',
        'line console 0',
        'logging synchronous'
    ]
    output = ssh.send_config_set(config_commands)


def show_runn(ssh):
    output = ssh.send_command("show ip interface brief")
    return output