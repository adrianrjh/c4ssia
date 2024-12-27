import telnetlib

def get_olt_info_telnet(hostname, port, username, password):
    try:
        # Conectar al dispositivo usando Telnet
        tn = telnetlib.Telnet(hostname, port)
        # Leer hasta el prompt de login
        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        # Leer hasta el prompt de password
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        # Ejecutar comandos para obtener información
        commands = ['show ont info by-active-status inactive 1/1/1-16']
        for command in commands:
            tn.write(command.encode('ascii') + b"\n")
            output = tn.read_until(b"#").decode('ascii')  # Leer hasta el prompt
            print(f"Output for {command}:\n{output}")
        # Cerrar la conexión
        tn.write(b"exit\n")
        tn.close()
    except Exception as e:
        print(f"Error: {e}")

# Parámetros de conexión
hostname = '192.168.1.3'  # Dirección IP del OLT
port = 23  # Puerto Telnet
username = 'admin'  # Nombre de usuario
password = 'est4m4ss3gur0'  # Contraseña

# Obtener información del OLT usando Telnet
get_olt_info_telnet(hostname, port, username, password)
