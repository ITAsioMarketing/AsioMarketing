import csv
import easygui
import os

def leer_archivo(path:str):
	with open(path, 'r', newline='', encoding='utf-8') as file:
		reader = csv.reader(file)
		header = next(reader)
		contenido = [n for n in reader if n != []]
	return header, contenido

def obtener_numeros(contenido, columna_numeros=13):
	return list(set([n[columna_numeros] for n in contenido]))

def guardar_archivo_csv(path, encabezados, contenido):
	with open(path, 'w', newline = '', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(encabezados)
		writer.writerows(contenido)
	return True

def guardar_archivo_txt(path, encabezados, contenido):
	with open(path, 'w', encoding='utf-8') as file:
		file.write("\t".join(encabezados)+'\n')
		for row in contenido:
			fila = [str(item) for item in row]
			file.write("\t".join(fila)+'\n')
	return True

path = easygui.fileopenbox()
header, contenido = leer_archivo(path)
columna_numeros = 13

# obtengo lista de numeros
lista_telefonos = obtener_numeros(contenido, columna_numeros)

# obtengo las veces que un numero se repite
repeticion_num = []
for i, telefono in enumerate(lista_telefonos):
	repeticion_num.append(0)
	for row in contenido:
		if row[columna_numeros] == telefono:
			repeticion_num[i] += 1

# Convertir datos a un diccionario
data_tel = dict(zip(lista_telefonos, repeticion_num))


# Guardar datos en csv
header_out = ['Numero de telefono','Repeticion']
conten_out = [[key, data_tel[key]] for key in data_tel]
new_path = easygui.filesavebox(default = "conteo.csv",filetypes=["*.csv", "*.txt"])


_, extension = os.path.splitext(new_path)

extension = extension.lower()

if extension == ".csv":
	guardar_archivo_csv(new_path, header_out, conten_out)
if extension == ".txt":
	guardar_archivo_txt(new_path, header_out, conten_out)

print(f'Se guardaron {len(data_tel)} registros en \'{new_path}\'')