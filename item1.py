#Script que imprime el nombre de los integrantes del grupo
integrante = [
    "Juan Calderon"
    "Sede Plaza Oeste"
]

print("Integrante y Sede --> ")
for integran in integrante:
    print(integran)

vlan = int(input("Introduce el número de VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} pertenece al rango normal.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} pertenece al rango extendido.")
else:
    print(f"La VLAN {vlan} no está en un rango válido."