import textfsm
from netmiko import ConnectHandler

def get_device_neighbor_details(ip, username, password, enable_secret,SyslogServer):
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

    config_commands = [
        f'logging {SyslogServer}'
    ]

    #output = ssh_connection.send_config_set(config_commands)

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
        version_template = textfsm.TextFSM(open("Templates/cisco_ios_show_version.textfsm"))
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
    version_result = int_brief_result
    #Informacion de interfaces
    int_brief_result += ssh_connection.send_command("show ip interface brief", delay_factor=2)#te consigue la informacion de interfaces del dispositivo

    intv6_brief_result += ssh_connection.send_command("show ipv6 interface brief", delay_factor=2)#te consigue la informacion de interfaces del dispositivo

    version_result += ssh_connection.send_command("show version", delay_factor=2)#te consigue la informacion del dispositivo
    #Desconectar SSH
    ssh_connection.disconnect()

    #procesar info para enviar a servidor
    fsm_int_results = int_brief_template.ParseText(int_brief_result)
    fsm_intv6_results = intv6_brief_template.ParseText(intv6_brief_result)
    version_result = version_template.ParseText(version_result)

    for x in fsm_intv6_results:
        if x[1][0] == "unassigned":
            x[1].append("unassigned")

    result =[fsm_int_results,fsm_intv6_results,version_result]

    return result

def ssh_login(device_ip, username, password, secret):
    device = {
        'device_type': 'cisco_ios', 
        'host': device_ip,
        'username': username,
        'password' : password,
        'secret' : secret
    }

    try:
        ssh_session = ConnectHandler(**device)
        print("¡Conexión SSH exitosa!")
        return ssh_session
    except Exception as e:
        print("Error al iniciar sesión SSH:", str(e))
        return None
    
#1
def change_hostname(device_ip, username, password,secret,hostname):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f"hostname {hostname}"
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#2
def change_int_ip(device_ip, username, password,secret,ip,mask,interface):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f'interface {interface}',
                f'ip address {ip} {mask}',
                'no shutdown'
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#3
def change_int_desc(device_ip, username, password,secret,interface,desc):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f'interface {interface}',
                f'description {desc}'
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#4
def change_motd(device_ip, username, password,secret,motd):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f'banner motd ^{motd}^'
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#5
def change_intv6_ip(device_ip, username, password,secret,ipv6,mask,interface):
    ssh = ssh_login(device_ip, username, password,secret,)
    config_commands = [
                f'interface {interface}',
                f'ipv6 address {ipv6}{mask}',
                'no shutdown'
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#6
def ipv6_unicast(device_ip, username, password,secret):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                "ipv6 unicast-routing"
            ]
    
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#7
def ip_route(device_ip, username, password,secret,ip,mask,rute,DA):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f'ip route {ip} {mask} {rute} {DA}'
            ]
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#8
def ipv6_route(device_ip, username, password,secret,ipv6,mask,rute, da):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
                f'ip route {ipv6}{mask} {rute} {da}'
            ]
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#9
def new_user(device_ip, username, password,secretpass,user,priv,secret):
    ssh = ssh_login(device_ip, username, password,secretpass)
    config_commands = [
                f"username {user} privilege {priv} secret {secret}"
            ]
    ssh.send_config_set(config_commands)
    ssh.disconnect()
#10
def loggin_syn(device_ip, username, password,secret,):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        'line vty 0 15',
        'logging synchronous'
        'exit',
        'line console 0',
        'logging synchronous'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#11
def conf_syslog(device_ip, username, password,secret, serverIp):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        f'logging {serverIp}'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#12
def dhcp_v4(device_ip, username, password,secret, dhcpPool,interfaceIp, network, mask, dnsServer, domainName):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        f'ip dhcp pool {dhcpPool}'
        f'default-router {interfaceIp}'
        f'network {network} {mask}'
        f'dns-server {dnsServer}'
        f'domain-name {domainName}'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#13
def ssh_authentication_retry(device_ip, username, password,secret, retries):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        f'ip ssh authentication {retries}'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#14
def ssh_time_out(device_ip, username, password,secret, timeOut):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        f'ip ssh time {timeOut}'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#15
def save_config(device_ip, username, password,secret):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        'copy running-config startup-config'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()
#16
def password_encryption(device_ip, username, password,secret):
    ssh = ssh_login(device_ip, username, password,secret)
    config_commands = [
        'service password-encryption'
    ]
    output = ssh.send_config_set(config_commands)
    ssh.disconnect()

def show_runn(device_ip, username, password,secret):
    ssh = ssh_login(device_ip, username, password,secret)
    output = ssh.send_command("show ip interface brief")
    ssh.disconnect()
    return output