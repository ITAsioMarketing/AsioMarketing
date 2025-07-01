import csv
import os
import easygui
from collections import defaultdict
from datetime import datetime, timedelta

# Funciones
# ====================================
def leer_archivo_csv(path):
	with open(path, 'r', newline='', encoding='utf-8') as file:
		reader = csv.reader(file)
		headers = next(reader)
		content = [n for n in reader if n != []]
	return headers, content

def acomodar_fecha(fecha):	
	dtime = datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S GMT") - timedelta(hours = 6)
	dtime = dtime.strftime("%d/%m/%Y %H:%M:%S")
	return dtime

def escribir_archivo_csv(path, headers, content):
	with open(path, 'w', newline = '', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(headers)
		writer.writerows(content)

def generar_reporte_simple(content):
	llamadas_realizadas = defaultdict(int)			# Total llamadas realizadas
	llamadas_contestadas = defaultdict(int)		# Total llamadas contestadas
	suma_duracion = defaultdict(int)			# Suma de tiempo de llamadas
	llamadas_efectivas = defaultdict(int)		# total de llamadas de más de 7 min (420 seg)

	fecha = 2
	formato_fecha = "%d/%m/%Y %H:%M:%S"
	for row in content:
		fecha_str = row[2]
		try:
			fecha = datetime.strptime(fecha_str, formato_fecha)
		except ValueError:
			continue

		if row[5] != 'outgoing':
			continue

		fecha_rango = fecha.replace(minute = 0, second = 0, microsecond = 0)
		dia = fecha.strftime("%d/%m/%Y")
		hora_inicio = fecha_rango.strftime("%H:%M:%S")
		hora_fin = (fecha_rango + timedelta(hours=1)).strftime("%H:%M:%S")

		clave = (dia, hora_inicio, hora_fin)
		llamadas_realizadas[clave] += 1

		if row[6] == "answered":
			llamadas_contestadas[clave] += 1
			suma_duracion[clave] += int(row[29])
			if int(row[29]) >= 420:
				llamadas_efectivas[clave] += 1
		
	datos_subir = []
	for clave in llamadas_realizadas:
		try:
			datos_subir.append(
				list(clave) + 
				[llamadas_realizadas[clave]] +
				[llamadas_contestadas[clave]] +
				[llamadas_efectivas[clave]]+
				[formato_tiempo(suma_duracion[clave] / llamadas_contestadas[clave])] +
				[f'{round(llamadas_contestadas[clave]/llamadas_realizadas[clave], 2) *100}%'] +
				[f'{round(llamadas_efectivas[clave]/llamadas_contestadas[clave], 2) *100}%'] 
			)
		except ZeroDivisionError:
			datos_subir.append(
				list(clave) +
				[llamadas_realizadas[clave]] +
				[llamadas_contestadas[clave]] +
				[llamadas_efectivas[clave]]+
				[formato_tiempo(0)] +
				[f'{round(llamadas_contestadas[clave]/llamadas_realizadas[clave], 2) *100}%'] +
				[f'{round(llamadas_efectivas[clave]/llamadas_contestadas[clave], 2) *100}%'] 
			)

	headers = ['Fecha', 'Hora Inicio', 'Hora Fin', 'Total llamadas realizadas', 'Total llamadas contestadas', 'Total llamadas efectivas', 'Duración promedio (MM:SS)', 'Porcentaje llamadas contestadas', 'Porcentaje llamadas efectivas']
	new_path = easygui.filesavebox(default='Reporte simple.csv')

	escribir_archivo_csv(new_path, headers, datos_subir)

def formato_tiempo(tiempo):
	minutos = tiempo //60
	segundos = tiempo % 60
	return f'{int(minutos)} min {int(segundos)} seg'

def generar_reporte_por_agente(content):
	nombres_agentes = list(set([n[24] for n in content])) 		# Nombre de los agentes (filtrados y sin duplicados)
	tiempo_prom_llamada = [0 for _ in nombres_agentes]			# Tiempo total de llamada por agente
	llamadas_contestadas = [0 for _ in nombres_agentes]			# Total llamadas contestadas por agente
	llamadas_realizadas = [0 for _ in nombres_agentes]			# Total llamadas realizadas por agente
	llamadas_efectivas = [0 for _ in nombres_agentes]			# Total llamadas efectivas (mayores a 7 min ())

	for i, row in enumerate(content):
		for j, nombre in enumerate(nombres_agentes):
			if row[5] == "outgoing" and row[24] == nombre:
				llamadas_realizadas[j] += 1
				if row[6] == "answered":
					llamadas_contestadas[j] += 1
					tiempo_prom_llamada[j] += int(row[29])
					if int(row[29]) >= 420:
						llamadas_efectivas[j] += 1

	datos_subir = []

	for i, nombre in enumerate(nombres_agentes):
		if llamadas_realizadas[i] == 0:
			continue
		if llamadas_contestadas[i] == 0:
			datos_subir.append(
				[nombre,
				 llamadas_realizadas[i],
				 llamadas_contestadas[i],
				 '',
				 llamadas_efectivas[i],
				 formato_tiempo(tiempo_prom_llamada[i]),
				 f'{round(llamadas_contestadas[i]/llamadas_realizadas[i], 2) *100}%',
				 f'{round(llamadas_efectivas[i]/llamadas_contestadas[i], 2)*100}%'
				]
			)
		else:
			datos_subir.append(
				[nombre,
				 llamadas_realizadas[i],
				 llamadas_contestadas[i],
				 '',
				 llamadas_efectivas[i],
				 formato_tiempo(tiempo_prom_llamada[i]/llamadas_contestadas[i]),
				 f'{llamadas_contestadas[i]/llamadas_realizadas[i]*100}%',
				 f'{llamadas_efectivas[i]/llamadas_contestadas[i]*100}%'
				]
			)

	headers_estadistica = ['Agente', 'llamadas realizadas', 'llamadas contestadas', 'Llamadas repetidas', 'Llamadas efectivas', 'tiempo promedio en llamadas', 'Porcentaje llamadas contestadas', 'Porcentaje llamadas efectivas']
	escribir_archivo_csv(easygui.filesavebox(default = "estadisticas por agente.csv"), headers_estadistica, datos_subir)

# ====================================



# Inicio del programa
# ====================================

path = easygui.fileopenbox()
headers, content = leer_archivo_csv(path)



# Acomodar fecha	
# Necesita			<- path, headers, content
# Devueve			-> headers, content
# ====================================

for i, row in enumerate(content):
	content[i][2] = acomodar_fecha(row[2])

escribir_archivo_csv(path, headers, content)
headers, content = leer_archivo_csv(path)

# ====================================



# Reporte Simple
# Necesita			<- content
# Devueve			-> 
# ====================================

generar_reporte_simple(content)

# ====================================


# Estadisticas
# Necesita			<- content
# Devueve			-> 
# ====================================

generar_reporte_por_agente(content)


# ====================================


# Fin del programa
# ====================================