from icecream import ic
import datetime
import csv
import easygui

# Obtiene los encabezados (probablement eno muy util en este ejemplo)
path = easygui.fileopenbox()
with open(path, 'r', newline='', encoding='utf-8') as f:
	lector_csv = csv.reader(f)
	encabezados = next(lector_csv)

	contenido = list(lector_csv)
# print(encabezados)

# Obtiene y filtra los numeros de los clientes
lista_numeros_clientes = []
for linea in contenido:
	lista_numeros_clientes.append(linea[2])

lista_numeros_clientes_filtrada = list(set(lista_numeros_clientes))


# cuenta cuantas veces se repite un numero
conteo = {}

for numero in lista_numeros_clientes_filtrada:
	cant = lista_numeros_clientes.count(numero)
	conteo[numero] = [cant,[]]

# Agrega cuales registros tienen el telefono del cliente
for linea in contenido:
	id_llamada = linea[0]
	numero_cliente = linea[2]

	conteo[numero_cliente][1].append(id_llamada)

# for n in conteo:
# 	print(f'{conteo[n]}\t{n}')


with open("registros_llamadas.txt", 'w', encoding='utf-8') as f:
	for i, numero in enumerate(conteo, 1):
		f.write(f'{i} - {numero} ({conteo[numero][0]}):\n')
		for registro in conteo[numero][1]:
			f.write(f'\t{registro}\n')
		f.write('\n')

maxim = 0
for n in conteo:
	if conteo[n][0] > maxim:
		maxim = conteo[n][0]

minim = len(contenido)
for n in conteo:
	if conteo[n][0] < minim:
		minim = conteo[n][0]

print(maxim)
print(minim)