import os
import pandas as pd
import re
import numpy as np

names_col = [
    "Tipo de seguro",      
    "Certificado ", 
    "Numero Interno Del Canal",    
    "Tipo de Registro",   
    "Moneda",   
    "Tipo de Movimiento",   
    "Apellido Paterno",   
    "Apellido Materno",   
    "Nombres",   
    "Sexo",   
    "Estado Civil",   
    "Fecha de Nacimiento",   
    "Tipo de Documento de Identidad",   
    "Numero de Documento de Identidad",
    "Dirección Domiciliaria",   
    "Referencia",   
    "Referencia2",   
    "Urbanización",   
    "Mz/Lte/Nro",   
    "Apto/Int",   
    "Distrito",    
    "Departamento",   
    "Código Postal",   
    "País",   
    "Periodo de pago",   
    "Prefijo Calle,Av,Jr",   
    "Prefijo 2",   
    "Provincia",   
    "Distrito_2",
    "Prefijo Teléfono",   
    "Numero Teléfono",   
    "Fecha de Afiliación",
    "Fecha de inicio del seguro",   
    "Fecha fin del seguro ",   
    "Plazo del seguro",   
    "Monto Asegurado ",   
    "Prima",   
    "Período de Gracia",   
    "Código de Beneficiario",   
    "Clase de Prima",   
    "Tipo de Titular",   
    "Mayor a 65 Años",
    "Tasa sin Recargo",
    "porcentaje de recargo",
    "Filler",
    "Tiempo de Periodo de Gracia",
    "Tipos de Endoso",
    "Tipos de Extorno",
    "Tipo de cambio",
    "Póliza",
    "Sumatoria de Capital en Cúmulo",
    "Correo electrónico",
    "Plan de crédito",
    "Planes Tipo Desgravamen",
    "Planes de Seguro (o Modalidad)"        
    ]
colspecs_col = [
    (0, 3),      
   (3, 23), 
    (23, 43), 
    (43,45),    
    (45, 48),   
    (48, 49),   
     (49, 79),   
    (79, 109),   
    (109, 139),   
    (139, 140),   
    (140, 141),   
    (141, 149),   
    (149, 150),   
    (150, 160),
    (160, 210),   
    (210, 235),   
    (235, 260),   
    (260, 290),   
    (290, 298),   
    (298, 306),   
    (306, 336),    
    (336, 338),   
    (338, 343),   
    (343, 346),   
    (346, 347),   
    (347, 350),   
    (350, 353),   
    (353, 355),   
    (355, 358),   
    (358, 361),   
    (361, 368),
    (368, 376),   
    (376, 384),   
    (384, 392),   
    (392, 396),   
    (396, 411),   
    (411, 426),   
    (426, 427),   
    (427, 429),   
    (429, 430),
    ###--
    (430,431),   
    (431, 432),   
    (432, 442),   
    (442, 449),   
    (449, 522),
    (522, 524),   
    (524, 527),   
    (527, 530),
    (530,540),
    (540,550),
    (550,565),
    (565,635),
    (635,637),
    (637,639),
    (639,641)   
    ]
dtypes = {
    "Tipo de seguro": str,      
    "Certificado ": str, 
    "Numero Interno Del Canal": str,    
    "Tipo de Registro": float,   
    "Moneda": str,   
    "Tipo de Movimiento": str,   
    "Apellido Paterno": str,   
    "Apellido Materno": str,   
    "Nombres": str,   
    "Sexo": str,   
    "Estado Civil": str,   
    "Fecha de Nacimiento": str,   
    "Tipo de Documento de Identidad": str,   
    "Numero de Documento de Identidad": str,
    "Dirección Domiciliaria": str,   
    "Referencia": str,   
    "Referencia2": str,   
    "Urbanización": str,   
    "Mz/Lte/Nro": str,   
    "Apto/Int": str,   
    "Distrito": str,    
    "Departamento": str,   
    "Código Postal": str,   
    "País": str,   
    "Periodo de pago": str,   
    "Prefijo Calle,Av,Jr": str,   
    "Prefijo 2": str,   
    "Provincia": str,   
    "Distrito_2": str,   
    "Prefijo Teléfono":str,
    "Numero Teléfono": float,   
    "Fecha de Afiliación": str,
    "Fecha de inicio del seguro": str,   
    "Fecha fin del seguro ": str,   
    "Plazo del seguro": str,   
    "Monto Asegurado ": str,   
    "Prima": str,   
    "Período de Gracia": str,   
    "Código de Beneficiario": str,   
    "Clase de Prima": str,   
    "Tipo de Titular": str,   
    "Mayor a 65 Años":str,
    "Tasa sin Recargo": str,
    "porcentaje de recargo" : str,
    "Filler" : str,
    "Tiempo de Periodo de Gracia" : str,
    "Tipos de Endoso" : str,
    "Tipos de Extorno": str,
    "Tipo de cambio": str,
    "Póliza":str,
    "Sumatoria de Capital en Cúmulo":str,
    "Correo electrónico":str,
    "Plan de crédito":str,
    "Planes Tipo Desgravamen":str,
    "Planes de Seguro (o Modalidad)":str      
}
dir_global_sas = 'd:/users/ehonores/OneDrive - Rimac Seguros y Reaseguros/General - Squad Vida BS&Alianzas/Nuevo Orden/Usuarios/Eduardo Honores/Automatización/Convertidor de tramas/Pruebas_piloto/SAS/PRESTAMOS + MIG/'
valores_a_reemplazar =  {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0, '{': 0,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9
}

def directorio (var_dir):
    if var_dir == 'SAS':
        dir_global_sas = 'd:/users/ehonores/OneDrive - Rimac Seguros y Reaseguros/General - Squad Vida BS&Alianzas/Nuevo Orden/Usuarios/Eduardo Honores/Automatización/Convertidor de tramas/Pruebas_piloto/SAS/PRESTAMOS + MIG/'
        return dir_global_sas
    elif var_dir == 'M':
        dir_global_sas = 'd:/users/ehonores/OneDrive - Rimac Seguros y Reaseguros/General - Squad Vida BS&Alianzas/Nuevo Orden/Usuarios/Eduardo Honores/Automatización/Convertidor de tramas/Pruebas_piloto/SUSTENTOS/SUSTENTO_MENSUAL/'
        return dir_global_sas
    else:
        dir_global_sas = 'd:/users/ehonores/OneDrive - Rimac Seguros y Reaseguros/General - Squad Vida BS&Alianzas/Nuevo Orden/Usuarios/Eduardo Honores/Automatización/Convertidor de tramas/Pruebas_piloto/SAS/TC + TKT/'
        return dir_global_sas

def dir_padre(dir_global):
    contenido = os.listdir(dir_global_sas)
    cont_padre = []
    for fichero in contenido:
        if os.path.isdir(os.path.join(dir_global, fichero)):
            cont_padre.append(fichero)
        else:
            print('no es un directorio')
    return cont_padre


def dir_hijos(var):
    dir_global = directorio(var)
    dir_hijo = []
    carpetas = dir_padre(dir_global)
    if len(carpetas) == 0 :
       ruta = dir_global
    else:
        for i in carpetas:
            print()
            contenido = os.listdir(dir_global +i+'/')
            
            for fichero in contenido:
                if os.path.isdir(os.path.join(dir_global +i+'/', fichero)):
                    dir_hijo.append(dir_global +i+'/' +fichero + '/')
        #print(dir_hijo)
    return dir_hijo

def dir_general(var):
    rutas = []
    return dir_hijos(var)
           # print(rutas)
def dir_detalle(ruta):
    dir_sobrino = []
    contenido = os.listdir(ruta)
    
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta, fichero)):
            dir_sobrino.append(ruta +fichero )
    print(len(dir_sobrino))
    return dir_sobrino


def reemplazar_valores(x):
    letra = x[-1]
    valor = valores_a_reemplazar.get(letra, 0)
   # print(x[:-1] + str(valor))
    return x[:-1] + str(valor)


def consolidar_sas(count,txt,df_summ):
    print(txt)
    flag_periodo = txt[203:209]
    print('flag periodo')
    print(flag_periodo)
    flag_nom_file = txt[210:].rstrip('.csv')
    
        #print(txt)

    df =pd.read_csv(
        txt)
  #  df.to_csv('test_original.csv')
    print('dfdf')
    print(df)
    df_1 = df[['NUMCERTIFICADOEXT','VIGENCIA_INICIO','VIGENCIA_FIN','ESTADO','PRIMA']]

    df_1['PER_DEC'] = flag_periodo
    df_1['NAM_FILE'] = flag_nom_file
    df_1['VIGENCIA_INICIO'] = pd.to_datetime(df_1['VIGENCIA_INICIO'], format='%d/%m/%Y')
    df_1['VIGENCIA_INICIO'] = df_1['VIGENCIA_INICIO'].dt.strftime('%Y%m%d')
    df_1['VIGENCIA_FIN'] = pd.to_datetime(df_1['VIGENCIA_FIN'], format='%d/%m/%Y')
    df_1['VIGENCIA_FIN'] = df_1['VIGENCIA_FIN'].dt.strftime('%Y%m%d')
    df_1['NUMCERTIFICADOEXT'] = "00"+df_1['NUMCERTIFICADOEXT'].astype(str)
    df_1['LLAVE'] = df_1['NUMCERTIFICADOEXT'].astype(str) + '/' + df_1['VIGENCIA_INICIO'].astype(str)
    
    cond_1 =  (df_1['ESTADO'] == "ANU")  & (df_1['ESTADO'] == "ERR") & (df_1['ESTADO'] == "CAR")
    cond_2 = (df_1['ESTADO'] == "PRO") 
    df_1.loc[cond_1, 'ESTADO_COD'] = 0
    df_1.loc[cond_2, 'ESTADO_COD'] = 1

    # Ordena el DataFrame por la columna 'origen' en orden ascendente

    df_resumido = df_1[['PER_DEC','LLAVE','NUMCERTIFICADOEXT','VIGENCIA_INICIO','VIGENCIA_FIN','ESTADO','NAM_FILE','PRIMA','ESTADO_COD']]

    if count == 0:
        
        return df_resumido
        df.to_excel('cusco_txts_duplicados.xlsx',index=False)
        #print(df1)
    else:
       # print(df2)
        df3 =pd.concat([df_resumido,df_summ])
        df3.reset_index(drop=True,inplace=True)
        #print(df3)
        return df3



def consolidar_sustento_mensual(count,txt,df_summ):
    print('txt')
    print(txt)
    flag_ind =txt[163:].rstrip('.txt')
    print('flag_ind')
    print(flag_ind)
    flag_periodo = txt[160:160]

    try:
        #print(txt)

        df =pd.read_fwf(
            txt, index_col=False,colspecs=colspecs_col,names=names_col,dtype=dtypes)
        print("Rellenando valores NaN en columnas específicas:")
        new_values = {'Prima': '0', 'Monto Asegurado ': '0'}
        df['Prima'] = df['Prima'].apply(reemplazar_valores)
        df['Prima'] = df['Prima'].astype(str).str.lstrip('0') 
        df['Prima'] = pd.to_numeric(df['Prima'],errors="coerce") / 100  # Dividir por 100 después de convertir
        df['Monto Asegurado '] = df['Monto Asegurado '].apply(reemplazar_valores)
        df['Monto Asegurado '] = pd.to_numeric(df['Monto Asegurado '],errors="coerce") / 100
        df['Certificado '] = df['Certificado '].str.lstrip('0')
        df['Periodo'] = df['Fecha de inicio del seguro'].str.slice(0, 6)
        df['Periodo'] = flag_periodo
        df['flag_ind'] = flag_ind

      #  df_tasa = df[['Periodo','Tasa sin Recargo','Moneda']]
      #  df_tasa.drop_duplicates().reset_index(inplace=True)
    except:

        df =pd.read_fwf(
            txt, index_col=False,colspecs=colspecs_col,names=names_col, encoding= 'latin-1',dtype=dtypes)
        print("Rellenando valores NaN en columnas específicas:")
        df['Monto Asegurado '].fillna('0', inplace=True)
        df['Prima'] = df['Prima'].apply(reemplazar_valores)
        df['Prima'] = df['Prima'].astype(str).str.lstrip('0')
        df['Prima'] = pd.to_numeric(df['Prima'],errors="coerce") / 100  # Dividir por 100 después de convertir
        df['Monto Asegurado '] = df['Monto Asegurado '].apply(reemplazar_valores)
        df['Monto Asegurado '] = pd.to_numeric(df['Monto Asegurado '],errors="coerce") / 100
        df['Certificado '] = df['Certificado '].str.lstrip('0')
        df['Periodo'] = df['Fecha de inicio del seguro'].str.slice(0, 6)
        df['Periodo'] = flag_periodo
        df['flag_ind'] = flag_ind
    df['Certificado '] = "00"+df["Certificado "]
    df['LLAVE'] = df["Certificado "] + "/" + df['Fecha de inicio del seguro']
    
  #  df.to_csv('test_original.csv')
    df_resumido = df[['Periodo','LLAVE','Certificado ','Fecha de inicio del seguro','Fecha fin del seguro ','Tipo de seguro','Prima','Moneda']]
    #print(df_resumido)
    if count == 0:
        
        return df_resumido
        df.to_excel('cusco_txts_duplicados.xlsx',index=False)
        #print(df1)
    else:
       # print(df2)
        df3 =pd.concat([df_resumido,df_summ])
        df3.reset_index(drop=True,inplace=True)
        #print(df3)
        return df3


def consolidar_diario(count,txt,df_summ):
    print('txt')
    print(txt)
    flag_ind =txt[163:].rstrip('.txt')
    print('flag_ind')
    print(flag_ind)
    flag_periodo = txt[190:196]
    print('flagperiodo')
    print(flag_periodo)
    
    try:
        #print(txt)

        df =pd.read_fwf(
            txt, index_col=False,colspecs=colspecs_col,names=names_col,dtype=dtypes)
        print("Rellenando valores NaN en columnas específicas:")
        new_values = {'Prima': '0', 'Monto Asegurado ': '0'}
        print(df.fillna(value=new_values))
        df['Prima'] = df['Prima'].apply(reemplazar_valores)
        df['Prima'] = df['Prima'].astype(str).str.lstrip('0') 
        df['Prima'] = pd.to_numeric(df['Prima'],errors="coerce") / 100  # Dividir por 100 después de convertir
        df['Monto Asegurado '] = df['Monto Asegurado '].apply(reemplazar_valores)
        df['Monto Asegurado '] = pd.to_numeric(df['Monto Asegurado '],errors="coerce") / 100
        df['Certificado '] = df['Certificado '].str.lstrip('0')
        df['Periodo'] = df['Fecha de inicio del seguro'].str.slice(0, 6)
        df['Periodo'] = flag_periodo
        df['flag_ind'] = flag_ind

      #  df_tasa = df[['Periodo','Tasa sin Recargo','Moneda']]
      #  df_tasa.drop_duplicates().reset_index(inplace=True)
    except:

        df =pd.read_fwf(
            txt, index_col=False,colspecs=colspecs_col,names=names_col, encoding= 'latin-1',dtype=dtypes)
        df['Prima'].fillna('0', inplace=True)
        df['Monto Asegurado '].fillna('0', inplace=True)
        df['Prima'] = df['Prima'].apply(reemplazar_valores)
        df['Prima'] = df['Prima'].astype(str).str.lstrip('0')
        df['Prima'] = pd.to_numeric(df['Prima'],errors="coerce") / 100  # Dividir por 100 después de convertir
        df['Monto Asegurado '] = df['Monto Asegurado '].apply(reemplazar_valores)
        df['Monto Asegurado '] = pd.to_numeric(df['Monto Asegurado '],errors="coerce") / 100
        df['Certificado '] = df['Certificado '].str.lstrip('0')
        df['Periodo'] = df['Fecha de inicio del seguro'].str.slice(0, 6)
        df['Periodo'] = flag_periodo
        df['flag_ind'] = flag_ind
    
    df['Certificado '] = "00"+df["Certificado "]
    df['LLAVE'] = df["Certificado "] + "/" + df['Fecha de inicio del seguro']
    filtro = df['Tipo de Movimiento'].isin(['4'])
    filtrado_1 = df[filtro]

    #TC = 918
    #TKT = 919
    filtro_2 = filtrado_1['Tipo de seguro'].isin(['918','919','966'])
    filtrado_2 = filtrado_1[filtro_2]
    filtrado_2 = filtrado_2.reset_index(drop=True)
    df_resumido = filtrado_2[['Periodo','LLAVE','Certificado ','Fecha de inicio del seguro','Fecha fin del seguro ','Tipo de seguro','Prima','Moneda']]

    if count == 0:
        
        return df_resumido
        df.to_excel('cusco_txts_duplicados.xlsx',index=False)
        #print(df1)
    else:
       # print(df2)
        df3 =pd.concat([df_resumido,df_summ])
        df3.reset_index(drop=True,inplace=True)
        #print(df3)
        return df3
def main_2 (var):
    txt =dir_general(var)
    print(txt)
    a = ''
    b = ''
    count = 0
    año = '0'
    mes = '0'
    print(len(txt))
    for i in txt:
        for x in dir_detalle(i):
            
            if count < 0 or count >= 1000*len(txt):
                count += 1
                print(count)
                pass
            else:
                print(count)
                if var == 'SAS' :
                    if count == 0:
                        b = consolidar_sas(count,x,a)
                    else:
                        b = consolidar_sas(count,x,b)
                    #print(len(b['certificado/fecha_ini_seguro/fecha_fin_seguro']))
                    print(count)
                    count += 1
                elif var == 'M' :
                    if count == 0:
                        b = consolidar_sustento_mensual(count,x,a)
                    else:
                        b = consolidar_sustento_mensual(count,x,b)
                    #print(len(b['certificado/fecha_ini_seguro/fecha_fin_seguro']))
                    print(count)
                    count += 1
                else:
                    if count == 0:
                        b = consolidar_diario(count,x,a)
                    else:
                        b = consolidar_diario(count,x,b)
                    #print(len(b['certificado/fecha_ini_seguro/fecha_fin_seguro']))
                    print(count)
                    count += 1
    
    if var == 'SAS':
        b_sorted = b.sort_values(by='ESTADO_COD').reset_index()
        # Elimina duplicados considerando solo las columnas deseadas, por ejemplo 'col1' y 'col2'
        # Conservando la primera aparición (que será la de menor fecha por el orden previo)
        b_clean = b_sorted.drop_duplicates(subset=['LLAVE'], keep='first').reset_index()
        b_clean.to_csv('consolidado_sas.csv',index=False)
    elif var == 'M':
 #       df_sin_duplicados = b.drop_duplicates().reset_index()
        
        print(b)
        b['es_duplicado'] = b.duplicated()
        b.to_csv('consolidado_sus_mensual.csv',index=False)
    else:
        b.to_csv('consolidado_sus_diario',index=False)
    

def cruce_final():
    df_sas = pd.read_csv('consolidado_sas.csv')
    df_tramas = pd.read_csv('consolidado_sus_mensual.csv')
    print(df_tramas)

    resultado = pd.merge(df_tramas, df_sas[['LLAVE', 'ESTADO']], how='outer', indicator=True).reset_index()

    duplicados = resultado[resultado['es_duplicado']==True]
    duplicados.to_csv('duplicados.csv',index=False)
    
    # Filtrar las filas que no tienen coincidencia
    
    
    df_no_match = resultado[resultado['_merge'] != 'both']
    
    df_no_match.to_csv('no_match.csv',index=False)
    #resultado.to_csv('resultado_final.csv',index=False)
    #resultado['LLAVE_GROUP'] =resultado['Tipo de seguro'].astype(str) + '/'+ resultado['Fecha de inicio del seguro'].astype(str) + '/' + resultado['ESTADO'] + '/'+ resultado['Moneda']
    #print(resultado)
    #resultado_grouped = resultado.groupby(['LLAVE_GROUP']).agg({    
    #    'Prima': 'sum',
    #    'Certificado ' : 'count'
    #}).reset_index()
    #resultado_grouped.to_csv('resultado_final_agrupado.csv' , index=False)
    #print(resultado)
if __name__ == "__main__":
    main_2('M')
    cruce_final()
    #test = pd.read_csv('Cusco_temp.csv')
    #result = audit(test)
    #result.to_csv('cusco_res.csv')

