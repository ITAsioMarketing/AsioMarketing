from icecream import ic
from faker import Faker
import random
import datetime
import easygui

fake = Faker('es_MX')

headers = [
	'id_llamada',
	'nombre_cliente',
	'telefono_cliente',
	'nombre_agente',
	'telefono_agente',
	'fecha_hora'
]

agentes = [
	f'{fake.first_name()} {fake.last_name()} {fake.last_name()}' for _ in range(10)
]

telefonos_agentes  = [
	f'{fake.phone_number()}' for _ in range(10)
]

clientes = [
	f'{fake.first_name()} {fake.last_name()} {fake.last_name()}' for _ in range(100)
]

telefonos_clientes  = [
	f'{fake.phone_number()}' for _ in range(100)
]


headers = ",".join(headers)
headers += '\n'

registros = []

print("Creando archivo de Agentes...")
with open("Agentes.txt", 'w', encoding='utf-8') as f:
	print("Escribiendo encabezados...")
	f.write('id_agente,nombre_agente,telefono_agente\n')
	print("¡Encabezados escritos correctamente!")
	print("Escribiendo datos de agentes...")
	for i, agente in enumerate(agentes):
		f.write(f'{i+1},{agente},{telefonos_agentes[agentes.index(agente)]}\n')
	print("¡Datos de agentes escritos correctamente!")
print("¡Archivo de Agentes creaado con exito!")

print()

print("Creando archivos de Clientes...")
with open("Clientes.txt", 'w', encoding='utf-8') as f:
	print("Escribiendo encabezados...")
	f.write('id_cliente,nombre_cliente,telefono_cliente\n')
	print("¡Encabezados escritos correctamente!")
	print("Escribiendo datos de los clientes...")
	for i, cliente in enumerate(clientes):
		f.write(f'{i+1},{cliente},{telefonos_clientes[clientes.index(cliente)]}\n')
	print("¡Datos de los clientes escritos correctamente!")
print("¡Archivo de Clientes creaado con exito!")

print()

print("Creando tabla de registros...")
path = easygui.filesavebox()
# Escritura de archivo csv
print("Escribiendo encabezados...")
with open(path, 'w', encoding='utf-8') as f:
	f.write(headers)
print("¡Encabezados escritos correctamente!")
print("Llenando tabla...")
with open(path, 'a', encoding='utf-8') as f:
	for i in range(1, 1001):
		agente = random.choice(agentes)
		id_agente = agentes.index(agente)
		telefono_agente = telefonos_agentes[id_agente]

		fecha = fake.date_time_between(start_date='-5d', end_date='now')
		fecha = fecha.strftime("%d/%m/%Y %H:%M")

		cliente = random.choice(clientes)
		id_cliente = clientes.index(cliente)
		telefono_cliente = telefonos_clientes[id_cliente]

		datos_registros = ",".join([str(i), cliente, telefono_cliente, agente, telefono_agente, fecha])
		datos_registros += '\n'

		registros.append(datos_registros)

	f.writelines(registros)
print("¡Tabla llena correctamente!")
print(f"¡Tabla de registros creada correctamente! ({path})")