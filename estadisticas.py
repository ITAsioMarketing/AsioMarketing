import csv
import os
import easygui

def leer_archivo(path):
	with open(path, 'r', newline="", encoding='utf-8') as file:
		reader = csv.reader(file)
		header = next(reader)
		contenido = [n for n in reader if n != []]
	return header, contenido

def formato_tiempo(tiempo):
	minutos = tiempo //60
	segundos = tiempo % 60
	return f'{int(minutos)} min {int(segundos)} seg'

def quitar_llamadas_repetidas_por_agente(contenido):
	temp_agentes = []
	# Nombres de los agentes
	for i, row in enumerate(contenido):
		temp_agentes.append(row[24])
	temp_agentes = list(set(temp_agentes))

	# temp_llamadas = {n:[] for n in temp_agentes}
	temp_llamadas = []
	# for n in temp_agentes:
	# 	temp_llamadas[n] = []
	for i, row in enumerate(contenido):
		for name in temp_agentes:
			if row[24] == name:
				# temp_llamadas[name].append(set([row[7],row[29]]))
				temp_llamadas.append(i)
	for fila in temp_llamadas[::-1]:
		contenido.pop(fila)

	return temp_llamadas


def escribir_archivo(path, encabezados, contenido):
	with open(path, 'w', newline="", encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(encabezados)
		writer.writerows(contenido)

def escribir_archivo_txt(path, nombres, datos_subir):
	with open(path, 'w',encoding='utf-8') as file:
		for nombres in nombres:
			for linea in datos_subir:
				file.write("".join(linea))

path = easygui.fileopenbox()

header, contenido = leer_archivo(path)

nombres_agentes = list(set([n[24] for n in contenido])) #! nombres filtrados de los agentes
nombres_completa = [n[24] for n in contenido] # nombres sin quitar duplicados

conteo_agentes = []
for i, row in enumerate(contenido):
	for nombre in nombres_agentes:
		if row[5] == "outgoing":
			conteo_agentes.append(nombres_completa.count(nombre))

tiempos_agente = [0 for _ in nombres_agentes]
conteo_llamadas = [0 for _ in nombres_agentes]

for row in contenido:
	for i, nombre in enumerate(nombres_agentes):
		
		if row[24] == nombre:
			if row[5] == 'outgoing' and row[6] == "answered":
				tiempos_agente[i] += int(row[29]) #! Tiempo total de las llamadas de los agentes
				conteo_llamadas[i] += 1

datos_subir = []

for i, tiempo in enumerate(tiempos_agente):
	datos_subir.append([nombres_agentes[i],conteo_agentes[i],conteo_llamadas[i],formato_tiempo(tiempo/conteo_llamadas[i]) if conteo_llamadas[i] != 0 else formato_tiempo(tiempo)])

new_path = easygui.filesavebox()

escribir_archivo(new_path, ['Agente', 'llamadas realizadas', 'llamadas contestadas', 'tiempo promedio en llamadas'], datos_subir)


easygui.msgbox("Se ha completado la operación")

temp = quitar_llamadas_repetidas_por_agente(contenido)


escribir_archivo_txt(easygui.fileopenbox(), )