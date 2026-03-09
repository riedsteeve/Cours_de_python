#Petit test en réseau

import socket

target = "epsi.fr"

ip = socket.gethostbyname(target)

print(f"L'ip de ce sites est : {ip}")