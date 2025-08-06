import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import os
from datetime import datetime
from collections import defaultdict
import time



def listar_archivos_input (): 
    archivos_sustento = []
    archivos_diario = []
    ruta = obtener_directorio()
    print('rutarutaruta')
    print(ruta)
    ruta_final_sustento = ruta /'FILTRO'/'INPUT'/ 'SUSTENTO'
    ruta_final_diario = ruta /'FILTRO'/'INPUT'/ 'DIARIO' 
    archivos_sus = os.listdir(ruta_final_sustento)
    print(archivos_sus)
    archivos_dia = os.listdir(ruta_final_diario)
    print(archivos_dia)
    for archivo in archivos_sus:
        archivos_sustento.append(archivo)
    for archivo in archivos_dia:
        archivos_diario.append(archivo)
    print(archivos_sustento)
    return archivos_sustento[0] , archivos_diario


def listar_archivos_input_partic (): 
    archivos_sustento = []
    archivos_diario = []
    ruta = obtener_directorio()
    print('rutarutaruta')
    print(ruta)
    ruta_final_sustento = ruta /'PARTIR'/'INPUT'/ 'SUSTENTO'
    ruta_final_diario = ruta /'PARTIR'/'INPUT'/ 'DIARIA' 
    archivos_sus = os.listdir(ruta_final_sustento)
    print(archivos_sus)
    archivos_dia = os.listdir(ruta_final_diario)
    print(archivos_dia)
    for archivo in archivos_sus:
        archivos_sustento.append(archivo)
    for archivo in archivos_dia:
        archivos_diario.append(archivo)
    print(archivos_sustento)
    return archivos_sustento[0] , archivos_diario[0]



def consolidar_pagos_diarios(archivos_diarios,directorio_actual):


    ruta_input_diario = directorio_actual 
    
    # Lista de nombres de archivos a consolidar
    archivos = archivos_diarios

    # Nombre del archivo de salida
    archivo_salida = 'consolidado_diario.txt'

    # Abrir el archivo de salida en modo escritura
    with open(ruta_input_diario/archivo_salida, 'w') as salida:
        # Iterar sobre cada archivo
        for nombre in archivos:
                print(nombre)
                with open(ruta_input_diario/'FILTRO'/'INPUT'/'DIARIO'/nombre, 'r') as f:
                    contenido = f.read()
                    salida.write(contenido + '\n')  # Agregar contenido y una nueva línea
            
    print(f"Los archivos han sido consolidados en {archivo_salida}.")



def filtrar_pagos():
    
    fecha_formateada = datetime.today().strftime('%Y%m')
    periodo_actual = fecha_formateada + '01'

    nombre_prestamos = '20100130204_0157001_'+ periodo_actual + '_001.txt'
    nombre_mig = '20100130204_0169001_'+ periodo_actual + '_001.txt'
    nombre_mype = '20100130204_0157006_' + periodo_actual + '_001.txt'
    nombre_tc = '20100130204_0158001_'+ periodo_actual + '_001.txt' #tc
    nombre_tkt = '20100130204_0155001_'+ periodo_actual + '_001.txt' #tkt

    print(periodo_actual)
    archivo_input_sustento,archivos_diarios = listar_archivos_input()
    prestamos = ("901", "902", "903", "906", "943", "972", "959", "961", "968", "963", "964", "962", "951", "958", "953", "954", "952", "969")
    migracion = '941'
    trama_diaria_cods = ['918','919','966']
    TC = '918'
    TKT = '919'
    MYPE = '966'
    directorio_actual = obtener_directorio()
    consolidar_pagos_diarios(archivos_diarios,directorio_actual)

    ruta_input_sustento = directorio_actual 
    print(ruta_input_sustento)
    ruta_output = directorio_actual

    ruta_archivo = ruta_input_sustento /'FILTRO'/ 'INPUT' / 'SUSTENTO' / archivo_input_sustento
    # Detectar codificación

    # Leer con la codificación detectada

    with open(ruta_archivo, "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    productos_prestamos = []

    # Iteramos sobre cada línea
    for linea in lineas:
        codigo = linea[34:37]  # Posiciones 5 a 9 (índices 4 a 8)
        if "941" == codigo or codigo in prestamos:
            productos_prestamos.append(linea)
   #     elif  codigo in prestamos:
    #        productos_prestamos.append(linea)
        else:
            pass
    # Guardamos los resultados en archivos separados
#    with open(ruta_output /"migracion.txt", "w", encoding="utf-8") as archivo_901:
 #       archivo_901.writelines(productos_migracion)

    with open(ruta_output /'FILTRO'/'OUTPUT'/'PAGOS_PRESTAMOS'/ "pagos_prestamos.txt", "w", encoding="utf-8") as archivo_902_903:
        archivo_902_903.writelines(productos_prestamos)

    print('aquiiii')


###TRAMA DIARIA
    
    with open('consolidado_diario.txt', "r", encoding='latin-1') as archivo:
        lineas = archivo.readlines()

    productos_tc_tkt_mype = []
    altas_tkt = []
    altas_tc = []
    altas_mype = []
    altas_mig = []
    altas_prestamos = []
    print('aqui')
    # Iteramos sobre cada línea
    for linea in lineas:
        codigo = linea[0:3]
        tip_movimiento = linea[48:49]
        tip_registro = linea[43:45]        
          # Posiciones 5 a 9 (índices 4 a 8)
        if  codigo in trama_diaria_cods and tip_movimiento == '4' :
            productos_tc_tkt_mype.append(linea)
       # elif  codigo == TKT and tip_movimiento == '4'  :
       #     productos_tkt.append(linea)
       # elif  codigo == MYPE and tip_movimiento == '4' :
       #     productos_mype.append(linea)
        elif  codigo == TKT and tip_movimiento == '1'   :
            altas_tkt.append(linea)
        elif  codigo == MYPE and tip_movimiento == '1' :
            altas_mype.append(linea)
        elif  codigo == TC and tip_movimiento == '1'  and tip_registro == '01' :
            altas_tc.append(linea)
        elif  codigo in prestamos and tip_movimiento == '1'  and tip_registro == '01':
            altas_prestamos.append(linea)
        elif codigo == migracion and tip_movimiento == '1':
            altas_mig.append(linea)
        else:
            pass
    # Guardamos los resultados en archivos separados
    
    with open(ruta_output /'FILTRO'/'OUTPUT'/'PAGOS_TRAMA_DIARIA'/"pagos_diaria.txt", "w", encoding="utf-8") as archivo_tc:
        archivo_tc.writelines(productos_tc_tkt_mype)
    with open(ruta_output /'PARTIR'/'INPUT'/'DIARIA'/"pagos_diaria.txt", "w", encoding="utf-8") as archivo_tc:
        archivo_tc.writelines(productos_tc_tkt_mype)
    with open(ruta_output /'FILTRO'/'OUTPUT'/'ALTAS'/ nombre_tc, "w", encoding="utf-8") as file_tc:
        file_tc.writelines(altas_tc)
    with open(ruta_output /'FILTRO'/'OUTPUT'/'ALTAS'/ nombre_tkt, "w", encoding="latin-1") as file_tkt:
        file_tkt.writelines(altas_tkt)
    with open(ruta_output /'FILTRO'/'OUTPUT'/'ALTAS'/ nombre_mype, "w", encoding="utf-8") as file_mype:
        file_mype.writelines(altas_mype)
    with open(ruta_output /'FILTRO'/'OUTPUT'/'ALTAS'/ nombre_prestamos, "w", encoding="utf-8") as file_prestamos:
        file_prestamos.writelines(altas_prestamos)
    with open(ruta_output /'FILTRO'/'OUTPUT'/'ALTAS'/ nombre_mig, "w", encoding="utf-8") as file_mig:
        file_mig.writelines(altas_mig)


def divide_func():



  lines_per_file = 50000
  input_path , output_path,= obtener_directorio()
  new_directory = str(input_path) +'/Archivos_partidos/'
  #input_path = str(input_path) + "/prueba.txt" 
  input_path = str(output_path) + "/resultados_sustento/" + "nombre_archivo.txt"
  max_rows = 2
  with open(input_path, 'r', encoding='utf-8') as file:
      total_lines = sum(1 for _ in file)

  if total_lines <= lines_per_file:
      return [input_path]  # No es necesario dividir

  num_files = math.ceil(total_lines / lines_per_file)
  split_files = []

  with open(input_path, 'r', encoding='utf-8') as file:
      for i in range(num_files):
          part_filename = f"{new_directory}file_part_{i+1}.txt"
          with open(part_filename, 'w', encoding='utf-8') as part_file:
              for _ in range(lines_per_file):
                  line = file.readline()
                  if not line:
                      break
                  part_file.write(line)
          split_files.append(part_filename)



def construir_nombre_archivo(codigo,fecha_actual ,parte):
    # Simulación de estructura: <código fijo>_<código fijo>_<fecha>_<parte>
    # Puedes ajustar los valores fijos según tu lógica real
    parte_str = f"{parte:003d}"  # relleno con ceros a la izquierda
    return f'{codigo}_{fecha_actual}_{parte_str}.txt'


def bucle_divide():
    
    fecha_formateada = datetime.today().strftime('%Y%m')
    periodo_actual = fecha_formateada + '01'

    nombre_prestamos = '20100130204_0157001_'+ periodo_actual + '_00'
    nombre_mig = '20100130204_0169001_'+ periodo_actual + '_00'
    nombre_mype = '20100130204_0157001_' + periodo_actual + '_00'
    nombre_tc = '20100130204_0158001_'+ periodo_actual + '_00' #tc
    nombre_tkt = '20100130204_0155001_'+ periodo_actual + '_00' #tkt


    prestamos = {"901", "902", "903", "906", "943", "972", "959", "961", "968", "963", "964", "962", "951", "958", "953", "954", "952", "969"}
    migracion = '941'
    trama_diaria_cods = ['918','919','966']
    TC = '918'
    TKT = '919'
    MYPE = '966'
    archivo_input_sustento,archivos_diarios = listar_archivos_input_partic()
    
    directorio_actual = obtener_directorio()
    ruta_archivo_sustento = directorio_actual /'PARTIR'/ 'INPUT' / 'SUSTENTO' / archivo_input_sustento
    ruta_archivo_diario = directorio_actual /'PARTIR'/ 'INPUT' / 'DIARIA' / archivos_diarios
    ruta_output_sustento =  directorio_actual /'PARTIR'/ 'OUTPUT' / 'SUSTENTO' 
    ruta_output_diario = directorio_actual /'PARTIR'/ 'OUTPUT' / 'DIARIA'
##sustento
    productos = defaultdict(list)
    with open(ruta_archivo_sustento, "r", encoding="utf-8") as f:
        for linea in f:
            codigo = linea[0:3]
            if codigo in prestamos :
                productos["20100130204_0157001"].append(linea)
            elif codigo == migracion: 
                productos['20100130204_0169001_'].append(linea)

    # Obtener fecha actual en formato yyyymmdd
    # Escribir archivos por código de producto, dividiendo en bloques de 50,000 líneas
    for codigo, lineas in productos.items():
        for i in range(0, len(lineas), 50000):
            bloque = lineas[i:i+50000]
            parte = i //50000 + 4 
            print(parte)
            nombre_archivo = construir_nombre_archivo(codigo,periodo_actual,parte)
           # nombre_archivo = f"{codigo}{periodo_actual}_00{i//50000 + 4}.txt"
            ruta_archivo = os.path.join(ruta_output_sustento, nombre_archivo)
            with open(ruta_archivo, "w", encoding="utf-8") as f_out:
                f_out.writelines(bloque)

#DIARIO
    productos = defaultdict(list)
    with open(ruta_archivo_diario, "r", encoding="utf-8") as f:
        for linea in f:
            codigo = linea[0:3]
            if codigo ==  TKT :
                productos["20100130204_0155001_"].append(linea)
            elif codigo == TC: 
                productos['20100130204_0158001_'].append(linea)
            elif codigo == MYPE:
                productos['20100130204_0157004_'].append(linea)

    # Obtener fecha actual en formato yyyymmdd
    # Escribir archivos por código de producto, dividiendo en bloques de 50,000 líneas
    for codigo, lineas in productos.items():
        for i in range(0, len(lineas), 50000):
            bloque = lineas[i:i+50000]
            parte = i //50000 + 4 
            print(parte)
            nombre_archivo = construir_nombre_archivo(codigo,periodo_actual,parte)
           # nombre_archivo = f"{codigo}{periodo_actual}_00{i//50000 + 4}.txt"
            ruta_archivo = os.path.join(ruta_output_diario, nombre_archivo)
            with open(ruta_archivo, "w", encoding="utf-8") as f_out:
                f_out.writelines(bloque)

def obtener_directorio():
    directorio_script = Path(__file__).resolve().parent
    current_directory = directorio_script
    nueva_carpeta = directorio_script /'FILTRO'/ 'INPUT' 
    nueva_carpeta_2 = directorio_script /'FILTRO'/ 'OUTPUT'
    nueva_carpeta.mkdir(exist_ok=True)
    nueva_carpeta_2.mkdir(exist_ok=True)
    return directorio_script

if __name__ == "__main__":
    filtrar_pagos()
 #   time.sleep(5)
#    bucle_divide()

 