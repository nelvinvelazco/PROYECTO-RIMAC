import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import chardet
import calendar


cod_a_considerar = ("901", "902", "903", "906", "941", "943", "972", "959", "961", "968", "963", "964", "962", "951", "958", "953", "954", "952", "969")

# Obtener la ruta de "Mis Documentos" del usuario
mis_documentos = Path.home() / "Documents"

# Crear el nombre del archivo con fecha y hora actual
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
NomLog = mis_documentos / f"Errores_GeneraciónArchivoCNT_{timestamp}.csv"



## Funciones que validan si es fin de mes, se replica la funcionalidad de ADD_MONTHS de oracle

def is_last_day_of_month(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return date.day == last_day

def add_months_oracle_style(dFechaIni, nCantMeses):
    tentative_date = dFechaIni + relativedelta(months=nCantMeses)
    if is_last_day_of_month(dFechaIni):
        last_day = calendar.monthrange(tentative_date.year, tentative_date.month)[1]
        return tentative_date.replace(day=last_day)
    else:
        return tentative_date



def obtener_directorio():
    directorio_script = Path(__file__).resolve().parent
    current_directory = directorio_script
    nueva_carpeta = directorio_script / 'resultados_sustento'
    nueva_carpeta_2 = directorio_script / 'resultados_sustento'/ 'Archivos_partidos'
    nueva_carpeta.mkdir(exist_ok=True)
    nueva_carpeta_2.mkdir(exist_ok=True)

    print(f"La carpeta '{nueva_carpeta}' ha sido creada o ya existía.")

    return nueva_carpeta, current_directory
def obtener_variables(cod_prod) :
    #print(cod_prod)
    cCodProdPagosV2 =  {
            951:"ok",
            952: "ok",
            953: "ok",
            954: "ok",
            956: "ok",
            958 : "ok",
            959 : "ok",
            961 : "ok",
            962: "ok",
            963 : "ok",
            964 : "ok",
            968 : "ok"
        }
    
    cCodProdEquiv = {
        900 : '910',
        901 : '911',
        902 : '912',
        903 : '913',
        906 : '916',
        918 : '918',
        919 : '919',
        941 : '941',
        951 : '951',
        952 : '952',
        953 : '953',
        954 : '954',
        956 : '956',
        958 : '958',
        959 : '959',
        961 : '961',
        962 : '962',
        963 : '963',
        964 : '964',
        968 : '968',
        972 : '972'
    }
    
    cCodProdPagos = {
        918 : "ok",
        919 : "ok"
    }

    flag_cCodProdPagosV2 = ''
    flag_cCodProdEquiv = ''
    flag_cCodProdPagos = ''

    try:
            flag_cCodProdPagosV2 = cCodProdPagosV2[cod_prod]
             
    except: 
            flag_cCodProdPagosV2 = "INVALIDO"
    try:
            flag_cCodProdEquiv = cCodProdEquiv[cod_prod] 

    except: 
            flag_cCodProdEquiv = "INVALIDO"
    try:
            flag_cCodProdPagos = cCodProdPagos[cod_prod] 
    except: 
            flag_cCodProdPagos = "INVALIDO"
    
    return flag_cCodProdPagosV2, flag_cCodProdEquiv ,flag_cCodProdPagos

# Diccionario con las posiciones de los campos (inicio, fin) usando índices basados en 0
def obtener_posiciones(desc_posicion):
    positions = {'cCodProdExt': (34, 37),    
        'cNumCertExt': (70, 90),   
        'cCodMoneda': (57, 60),    
        'cPeriodo_1': (121, 125),
        'cPeriodo_2': (126,128),
        'cMontoAseg' : (196,211),
        'cTasaSinRec' : (211,221),
        'cPlanCred' : (221,223),
        'cPlanTipDesgra' : (223,225),
        'cPorRecargo' : (225,232),
        'cFecIniPago': (232,240),
        'cFecFinPago' : (240,248),
        'cFormaPago' : (110,111),
        'cPrimaDesg_1' : (290,304),
        'cPrimaDesg_2': (304,305)
                                }
    return positions[desc_posicion][0], positions[desc_posicion][1]



def RPAD(texto, longitud_total,text):
    return texto + text*(longitud_total - len(texto))


def CONVIERTE_CHAR_A_NUMERO(cDig):


      
  if cDig == 'A' :
    return 'P1'
  elif cDig == 'B' :
    return 'P2'
  elif cDig == 'C' :
    return 'P3'
  elif cDig == 'D' :
    return 'P4'
  elif cDig == 'E' :
    return 'P5'
  elif cDig == 'F' :
    return 'P6'
  elif cDig == 'G' :
    return 'P7'
  elif cDig == 'H' :
    return 'P8'
  elif cDig == 'I' :
    return 'P9'
  elif cDig == 'J' :
    return 'N1'
  elif cDig == 'K' :
    return 'N2'
  elif cDig == 'L' :
    return 'N3'
  elif cDig == 'M' :
    return 'N4'
  elif cDig == 'N' :
    return 'N5'
  elif cDig == 'O' :
    return 'N6'
  elif cDig == 'P' :
    return 'N7'
  elif cDig == 'Q' :
    return 'N8'
  elif cDig == 'R' :
    return 'N9'
  elif cDig == '{' :
    return 'N0'
  else:
    return 'P0'




def detectar_codificacion(archivo):
    with open(archivo, 'rb') as f:
        resultado = chardet.detect(f.read(10000))
    print(resultado['encoding'])
    return resultado['encoding']



def process_large_file():
    kc_Cero = '00000000000000{'

    output_path, input_path = obtener_directorio()
    output_path = str(output_path) + "/" + "nombre_archivo.txt"
    input_path = str(input_path) + "/SUST0525.txt"
    enconding = detectar_codificacion(input_path)
    len_file = 0
    max_file = 50000
    conteo = 0
    num = 0
    with open(input_path, 'r', encoding='latin-1') as file, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        for line in file:
            conteo += 1
            #print(num)
            num += 1  
            cLinea2 = ''
            nError = 0
            nNewTramaPago = 0
            nCont = 0
            
            cCodProdExt = line[obtener_posiciones('cCodProdExt')[0]:obtener_posiciones('cCodProdExt')[1]]
            if cCodProdExt not in cod_a_considerar:
                pass
            else:

              cNumCertExt = line[obtener_posiciones('cNumCertExt')[0]:obtener_posiciones('cNumCertExt')[1]]
              cCodMoneda = line[obtener_posiciones('cCodMoneda')[0]:obtener_posiciones('cCodMoneda')[1]]
              cPeriodo = line[obtener_posiciones('cPeriodo_1')[0]:obtener_posiciones('cPeriodo_1')[1]] + line[obtener_posiciones('cPeriodo_2')[0]:obtener_posiciones('cPeriodo_2')[1]] 
              cCodProdPagosV2,cCodProdEquiv, cCodProdPagos= obtener_variables(int(cCodProdExt))
              if cCodProdPagosV2 !='INVALIDO':
                  nNewTramaPago = 1
              # Construir la nueva línea concatenando los valores extraídos y constantess
          #    print('nNewTramaPago')
          #    print(nNewTramaPago)
              if nNewTramaPago == 1 : 
                  cMontoAseg 	= line[obtener_posiciones('cMontoAseg')[0]:obtener_posiciones('cMontoAseg')[1]]
                  cTasaSinRec = line[obtener_posiciones('cTasaSinRec')[0]:obtener_posiciones('cTasaSinRec')[1]]
                  cPlanCred	= line[obtener_posiciones('cPlanCred')[0]:obtener_posiciones('cPlanCred')[1]]
                  cPlanTipDesgra = line[obtener_posiciones('cPlanTipDesgra')[0]:obtener_posiciones('cPlanTipDesgra')[1]]
                  cPorRecargo	= line[obtener_posiciones('cPorRecargo')[0]:obtener_posiciones('cPorRecargo')[1]]
                  #print(cPorRecargo)
                  cFecIniPago	= line[obtener_posiciones('cFecIniPago')[0]:obtener_posiciones('cFecIniPago')[1]]
                  cFecFinPago = line[obtener_posiciones('cFecFinPago')[0]:obtener_posiciones('cFecFinPago')[1]]
              if  (cCodProdEquiv != 'INVALIDO' and cCodProdPagos == 'INVALIDO') or  ( cCodProdEquiv!= 'INVALIDO' and cCodProdPagos == 'INVALIDO' and cCodProdPagosV2 == 'INVALIDO') :
                      cLinea2 = cCodProdExt + cNumCertExt + line[90:110] + '01'
                      cLinea2 = cLinea2 + cCodMoneda +'4'   	    
                      cLinea2 =RPAD(cLinea2,346,' ')
                      cLinea2 = cLinea2 + line[110:111]
                      cFormaPago =line[obtener_posiciones('cFormaPago')[0]:obtener_posiciones('cFormaPago')[1]]
                      #print(cLinea2)
                      cLinea2 = RPAD(cLinea2,376,' ')
                      frec_pago = {'A':12,
                                  'B': 2,
                                  'M': 1,
                                  'S' : 6,
                                  'T': 3}
                      try:
                          nCantMeses = frec_pago[cFormaPago]
                          dFechaIni = datetime.strptime(line[129:131] +'/'+ line[126:128] +'/'+ line[121:125 ],"%d/%m/%Y")
                          dFechaFin = add_months_oracle_style(dFechaIni, nCantMeses)
                          #dFechaFin = dFechaIni + relativedelta( months= nCantMeses)
                          
                          cFecha =dFechaFin.strftime("%d/%m/%Y")

                      except:
                          nCantMeses = 0

#                      dFechaIni = datetime.strptime(line[129:131] +'/'+ line[126:128] +'/'+ line[121:125 ],"%d/%m/%Y")
 #                     dFechaFin = dFechaIni + relativedelta( months= nCantMeses)

  #                    cFecha =dFechaFin.strftime("%d/%m/%Y")
              else:
                    nCantMeses = 0

              if nNewTramaPago == 1 :
                    cLinea2 = cLinea2 + cFecIniPago
              else:
                    cLinea2 = cLinea2 + line[121:125] + line[126:128] + line[129:131]
              if nCantMeses != 0:
                  if nNewTramaPago == 1 :
                      cLinea2 = cLinea2 + cFecFinPago
                      
                  else:
                      cLinea2 = cLinea2 + cFecha[6:10] + cFecha[3:5] + cFecha[0:2]
                      #print(cLinea2)
                      #print(cFecha[6:10] + cFecha[3:5] + cFecha[0:2])
              else:
                  if nNewTramaPago == 1 : 
                      cLinea2 = cLinea2 + cFecFinPago
                  else:
                      cLinea2 = cLinea2 + line[121:125] + line[126:128] + line[129:131]
              ##print(cMontoAseg)
              if nNewTramaPago == 1 :
                      cLinea2 = RPAD(cLinea2,396, '0')
                      cLinea2 = cLinea2 + cMontoAseg
              else:
                  cLinea2 = RPAD(cLinea2,411,'0')

              cLinea2 = cLinea2 + kc_Cero

              if nNewTramaPago == 1 :
                      cLinea2 = RPAD(cLinea2,432,' ')
                      cLinea2 = cLinea2 + cTasaSinRec + cPorRecargo
                      cLinea2 = RPAD(cLinea2,635, ' ')
                      cLinea2 = cLinea2 + cPlanCred + cPlanTipDesgra
              else:
                  cLinea2 = RPAD(cLinea2,639,' ')

              cLinea2 = cLinea2 + line[256:258]
              cPrimaDesg = line[290:304] + CONVIERTE_CHAR_A_NUMERO(line[304:305])[1:2]

              cPrimaDesem = line[275:289] + CONVIERTE_CHAR_A_NUMERO(line[289:290])
    #          print(CONVIERTE_CHAR_A_NUMERO(line[145:146]))
              if CONVIERTE_CHAR_A_NUMERO(line[145:146]) == "P0":
                  cMonto = line[131:146]
                
              else:
                  cMonto = line[131:145] + CONVIERTE_CHAR_A_NUMERO(line[145:146])
                  nError = nError + 1
                  cError = 'El Mto de la Prima No Tiene un Formato Correcto'
              
              if CONVIERTE_CHAR_A_NUMERO(line[160:161]) != "P0":
                  nError = nError + 1
                  cError = 'El Mto de la Comisión No Tiene un Formato Correcto'
              if CONVIERTE_CHAR_A_NUMERO(line[168:169]) != "P0":
                  nError = nError + 1
                  cError = 'El Mto del Porcentaje de Comisión No Tiene un Formato Correcto'
              if nError >= 1:
                  nCont = nCont + 1 

      # Si es la primera vez, crear el archivo y escribir encabezado
              #print(nCont)
              if nCont == 1:
                  pass
              #print(nError)
              if nError >= 1:
                  pass
              
              
              else:
              #     print(line[275:290])
                #    print(len(line[275:290]))
     #               print(line[275:290])
      #              print(line[290:305])
               #     print(cLinea2)
                #    print(line[275:290])
                    if line[275:290] == kc_Cero and line[290:305] == kc_Cero:   
       #               print('aqui')
                      cLinea = cLinea2[0:411] + cMonto
                      cLinea = cLinea + cLinea2[426:]

                      #print(cLinea)
                      outfile.write(cLinea + '\n')
                      ##outfile.write(cLinea2 + '\n')
                    else:
                      ## Genera archivo para el AS400
                      cLinea = cLinea2[0:411] + cPrimaDesg
                      cLinea = cLinea + cLinea2[426:]
                      outfile.write(cLinea + '\n')

                      ##outfile.write(cLinea2 + '\n')

                      ##Genera archivo para el ACSELX
                    #  print(cLinea)
                      
                      cLinea = cCodProdEquiv + cLinea2[3:411] 
                      cLinea = cLinea + cPrimaDesem
                      cLinea = cLinea + cLinea2[426:]
                      ##outfile.write(cLinea2 + '\n')  
                     # print(cLinea)
           
        #              print(cLinea2)                    
                      cLinea2 = cCodProdExt 
              
#    divide_file()          
              
 

def divide_file ():
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

  return split_files

if __name__ == "__main__":
  process_large_file()
  


