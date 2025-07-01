import easygui
import os
from datetime import datetime, timedelta

def restar_horas(fecha:str):
	fecha = datetime.strptime(fecha,"%d/%b/%Y %H:%M:%S")
	fecha = fecha - timedelta(hours = 6)
	return fecha.strftime("%d/%b/%Y %H:%M:%S")

def acomodar_mes(fecha:str):
	global meses
	meses = {'Jan':'Ene','Apr':'Abr','Aug':'Ago'}
	
	for mes in meses:
		if mes in fecha:
			fecha = fecha.replace(mes, meses[mes])
	return fecha



path = easygui.fileopenbox(msg="Selecciona un archivo csv")

if path:
	with open(path,'r', encoding='utf-8') as archivo:
		text = archivo.readlines()

# text = text.split('\n')
# headers = text[0]
# text.pop(0)
headers = text[0].split(",")
text.pop(0)
for i, col in enumerate(headers):
	headers[i] = col.strip()
	print(f'{i}.\t{col}')

for i, col in enumerate(text):
	text[i] = col.strip()
	text[i] = col.split(',')
	text[i].pop(-1)

for row in text:
	print(row, end='\n\n')

csv=[]

# for i, headers in enumerate(text[0].split(",")):
# 	print(f'{i}.\t{headers}')

for i, value in enumerate(text):
	# Separar dia de la semana:
	wday = value.split(', ', 1)
	# Separar fecha
	date = wday[1].split(' ',3)
	# Separar hora
	time = date[3]
	# Convertir dia de la semana
	wday = wday[0]
	# Convertir fecha
	date = '/'.join(date[0:3])
	# Convertir hora
	time = time.replace(" GMT", "")

	# t_hour, t_min, t_sec = time.split(":")
	# t_hour = str(int(t_hour) - 6)
	# print(t_hour, t_min, t_sec)
	# time = ":".join([t_hour, t_min, t_sec])
	
	# Convertir a CSV
	csv.append(" ".join([date, time]))
for i, linea in enumerate(csv):
	csv[i] = restar_horas(linea)
	csv[i] = acomodar_mes(csv[i])

with open(path, 'w', encoding='utf-8') as archivo:
	for linea in csv:
		archivo.write(linea+' \n')

carpeta = os.path.dirname(path)

easygui.msgbox("¡El proceso se completó con éxito!", title="proceso terminado")

os.system(f'explorer "{carpeta}"')