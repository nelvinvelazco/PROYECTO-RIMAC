
SELECT FECHA_DECLARADO, COUNT(*) AS Contador
FROM `produccion.Declarados_CONTICASA`
GROUP BY FECHA_DECLARADO;

--------------------------------------------------------
CREATE OR REPLACE VIEW `produccion.Vw_Declarados_CONTICASA_VS_ERRORES` AS
SELECT dc.*, er.CODPROD, er.NRO_CERT_BANCO, er.INDICADOR, er.DESCRIPCION1, er.DESCRIPCION2, er.DATALLE
FROM `produccion.Declarados_CONTICASA` dc
LEFT JOIN `produccion.Errores_CONTICASA` er ON er.POLIZA_Y_CERTIFICADO = dc.POLIZA_Y_CERTIFICADO 
                                            AND er.MES= dc.FECHA_DECLARADO;



SELECT CODIGO_ERROR, COD_DE_CERTIFICADO, LINEA_TRAMA
FROM `produccion.ERRORES_desgravamen_TKT`
WHERE DESCRIPCION_ERROR = 'ERROR EN ALTA';


SELECT FECHA_DECLARADO,MONEDA, SUM(PRIMA_TOTAL)
FROM `produccion.Declarados_CONTICASA`
GROUP BY FECHA_DECLARADO, MONEDA;


SELECT COD_DE_CERTIFICADO, NRO_LOTE, IDEDET, FEC__INICIO, FEC__FIN, LINEA_TRAMA
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE CODIGO_ERROR = '1155';


SELECT ep.IDEERROR, COD_DE_CERTIFICADO, NRO_LOTE, IDEDET, FEC__INICIO, FEC__FIN
FROM `produccion.ERRORES_desgravamen_prestamos` ep
INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
WHERE te.CODIGO_ERROR = '7460' AND ep.TIPO_MOVIMIENTO_NUM IN ('1','4');

------------------------------------------------------------------------------------

WITH registros_ultimos AS (
  -- Paso 1: elimino duplicados completos
  SELECT *
  FROM `produccion.ERRORES_desgravamen_prestamos`
  WHERE FECHA_PERIODO = '2025-08-20'

),
Unicos_IDEEDET AS (
  -- Paso 2: me quedo con una sola fila por IDEDET y periodo (última por FEC__INICIO)
  SELECT *
  FROM (
    SELECT 
      t.*,
      ROW_NUMBER() OVER (
        PARTITION BY IDEDET
      ) AS rn
    FROM registros_ultimos t
  )
  WHERE rn = 1
)
SELECT ep.CODIGO_ERROR, te.DESC_ERROR_SAS, MONEDA, count(*) AS Nro_Errores, SUM(PRIMABRUTACAN) AS TOTAL_PRIMA
FROM Unicos_IDEEDET ep
INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.CODIGO_ERROR = te.CODIGO_ERROR
WHERE ep.DESCRIPCION_ERROR = 'ERROR EN ALTA'
GROUP BY ep.CODIGO_ERROR, te.DESC_ERROR_SAS ,ep.MONEDA
ORDER BY ep.CODIGO_ERROR;

----------------------- Crear Copia de Tabla de errores TC --------------------------

CREATE OR REPLACE TABLE `produccion.ERRORES_desgravamen_TC_Periodos` AS
SELECT *
FROM `produccion.ERRORES_desgravamen_TC`;

----------------------- Crear Copia de Tabla de errores PRESTAMOS --------------------------

CREATE OR REPLACE TABLE `produccion.ERRORES_desgravamen_TKT_Periodos` AS
SELECT *
FROM `produccion.ERRORES_desgravamen_TKT`;

-------------- Cantidad de errores por Codigo_Error ---------------------
SELECT te.CODIGO_ERROR, te.DESC_ERROR_SAS, count(*) AS Nro_Errores
FROM `produccion.ERRORES_desgravamen_TC` ep
INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
GROUP BY te.CODIGO_ERROR, te.DESC_ERROR_SAS
ORDER BY Nro_Errores DESC;

-------------------- Erroes por tipo de movimiento
SELECT distinct ep.COD_DE_CERTIFICADO, te.CODIGO_ERROR, te.IDEERROR, te.DESCRIPCION_ERROR, te.DESC_ERROR_SAS, ep.LINEA_TRAMA
FROM `produccion.ERRORES_desgravamen_TC` ep
INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
WHERE ep.TIPO_MOVIMIENTO_NUM = '4';

--------------------------------------------------------------------------
SELECT te.CODIGO_ERROR, te.DESC_ERROR_SAS, FEC__INICIO
FROM `produccion.ERRORES_desgravamen_TKT` ep
INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
WHERE ep.DESCRIPCION_ERROR_SAS like '%EDAD%';


--------------- Consulta de errore TC --------------------------------
SELECT COD_DE_CERTIFICADO,e.CODIGO_ERROR, e.DESC_ERROR_SAS, LINEA_TRAMA
FROM `produccion.ERRORES_desgravamen_TC` t
INNER JOIN `produccion.Tabla_Errores_SAS` e ON t.IDEERROR = e.IDEERROR
WHERE t.FEC__INICIO BETWEEN '2025-01-01' AND '2025-12-31';

------- Certificados y linea de trama unicos, extrayendo fecha_inicio_seguro
WITH certificados_unicos AS (
  SELECT DISTINCT COD_DE_CERTIFICADO, LINEA_TRAMA
  FROM `produccion.ERRORES_desgravamen_TC` t
  INNER JOIN `produccion.Tabla_Errores_SAS` e ON t.IDEERROR = e.IDEERROR
  WHERE e.CODIGO_ERROR = '0941' AND t.TIPO_MOVIMIENTO_NUM = '4'
  ORDER BY COD_DE_CERTIFICADO 
)
SELECT COD_DE_CERTIFICADO, PARSE_DATE('%Y%m%d', SUBSTR(LINEA_TRAMA, 377, 8)) AS FECHA_INICIO_SEGURO, LINEA_TRAMA
FROM certificados_unicos;

-----------------
SELECT COD_DE_CERTIFICADO,e.CODIGO_ERROR, e.DESC_ERROR_SAS
FROM `produccion.ERRORES_desgravamen_TC` t
INNER JOIN `produccion.Tabla_Errores_SAS` e ON t.IDEERROR = e.IDEERROR
WHERE DESC_ERROR_SAS LIKE '%TIPO%';

------------------ AGRUPAR POR DESCRIPCION Y IDEERRROR PARA CONCATENAR LOS NROS DE LOTES -----------------------

WITH lotes_unicos AS (
  SELECT DISTINCT ep.IDEERROR, NRO_LOTE
  FROM `produccion.ERRORES_desgravamen_prestamos` ep
  INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
  WHERE te.CODIGO_ERROR IN ('0011','0035','0010','8023','1135','0005','0061') AND ep.TIPO_MOVIMIENTO_NUM IN ('4')
)
SELECT IDEERROR, 'ERROR EN CARGA DE TRAMA' AS CATEGORIA, STRING_AGG(CAST(NRO_LOTE AS STRING), ', ') AS NROS_LOTES
FROM lotes_unicos
GROUP BY IDEERROR;
---------------------------------------------------------------------------

WITH lotes_unicos AS (
  SELECT DISTINCT ep.IDEERROR, ep.DESCRIPCION_ERROR, NRO_LOTE
  FROM `produccion.ERRORES_desgravamen_prestamos` ep
  INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
  WHERE ep.TIPO_MOVIMIENTO_NUM IN ('1')
)
SELECT IDEERROR, DESCRIPCION_ERROR AS CATEGORIA, STRING_AGG(CAST(NRO_LOTE AS STRING), ', ') AS NROS_LOTES
FROM lotes_unicos
GROUP BY IDEERROR, DESCRIPCION_ERROR
ORDER BY CATEGORIA;

------------------------ Traer las tramas unicas con algunas condiciones ----------------------------

WITH idedet_unicos AS (
  SELECT DISTINCT IDEDET
  FROM `produccion.ERRORES_desgravamen_prestamos`
  WHERE TIPO_MOVIMIENTO_NUM IN ('4') AND DESCRIPCION_ERROR = 'ERROR EN ALTA'
),
lotes_tramas AS ( 
  SELECT NRO_LOTE,LOTES_ANTERIORES, LINEA_TRAMA
  FROM `produccion.ERRORES_desgravamen_prestamos` ep
  LEFT JOIN idedet_unicos iu ON ep.IDEDET = iu.IDEDET
  WHERE ep.DESCRIPCION_ERROR <> 'ERROR EN ALTA' AND iu.IDEDET IS NULL
)
SELECT DISTINCT LINEA_TRAMA
FROM lotes_tramas
WHERE 
NRO_LOTE NOT IN (1346835,1346832,1346817,1346810,1346800,
                      1346761,1346749,1346733,1346690,1346534,
                      1346528,1346524,1346523) OR 
NOT REGEXP_CONTAINS(lotes_anteriores,
  r'\b(1346835|1346832|1346817|1346810|1346800|1346761|1346749|1346733|1346690|1346534|1346528|1346524|1346523)\b'
);

----------------------------------------------------------------------------------------------

WITH lotes_seleccionados AS(
  SELECT TIPO_SEGURO, TIPO_MOVIMIENTO_NUM, LINEA_TRAMA
  FROM `produccion.ERRORES_desgravamen_prestamos`
  WHERE 
  NRO_LOTE NOT IN (1346835,1346832,1346817,1346810,1346800,
                      1346761,1346749,1346733,1346690,1346534,
                      1346528,1346524,1346523) AND
  NOT REGEXP_CONTAINS(LOTES_ANTERIORES,
    r'\b(1346835|1346832|1346817|1346810|1346800|1346761|1346749|1346733|1346690|1346534|1346528|1346524|1346523)\b'
  )
)
SELECT DISTINCT TIPO_SEGURO, LINEA_TRAMA
FROM lotes_seleccionados
WHERE TIPO_MOVIMIENTO_NUM = '1'
ORDER BY TIPO_SEGURO ASC;


-------------------------------------------------------------------------------


WITH lotes_seleccionados AS(
  SELECT TIPO_SEGURO, TIPO_MOVIMIENTO_NUM, LINEA_TRAMA
  FROM `produccion.ERRORES_desgravamen_prestamos`
  WHERE 
  NRO_LOTE IN (1346835,1346832,1346817,1346810,1346800,
                      1346761,1346749,1346733,1346690,1346534,
                      1346528,1346524,1346523) OR 
  REGEXP_CONTAINS(LOTES_ANTERIORES,
    r'\b(1346835|1346832|1346817|1346810|1346800|1346761|1346749|1346733|1346690|1346534|1346528|1346524|1346523)\b')
)
SELECT DISTINCT TIPO_SEGURO, LINEA_TRAMA
FROM lotes_seleccionados
WHERE TIPO_MOVIMIENTO_NUM = '4'
ORDER BY TIPO_SEGURO ASC;


SELECT DISTINCT TIPO_SEGURO, LINEA_TRAMA
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE TIPO_MOVIMIENTO_NUM IN ('1', '4');


SELECT DISTINCT tr.TRAMA, dp.IDEDET, dp.NRO_LOTE
FROM `produccion.tramas_buscar` tr
LEFT JOIN `produccion.ERRORES_desgravamen_prestamos` dp ON tr.TRAMA = dp.LINEA_TRAMA
WHERE TIPO_MOVIMIENTO_NUM IN ('4');


----------------------- Transformar fecha y enumerar ------------------------

WITH certificados_fecha AS (
      SELECT *, PARSE_DATE('%d/%m/%Y', fecha_recepcion) AS fecha_recepcion1 
FROM `produccion.sustento_enumerar`
)
 SELECT certificado, fecha_recepcion1, ROW_NUMBER() OVER (PARTITION BY Certificado ORDER BY   fecha_recepcion1) AS nro_reg,
 FROM certificados_fecha;

---------------------- Convenios en error con enumeracion y conteo ----------------

WITH tramas_unicas AS (
  SELECT DISTINCT SUBSTR(LINEA_TRAMA, 4, 20) AS CERTIFICADO, LINEA_TRAMA, FEC__INICIO, FEC__FIN
  FROM `produccion.ERRORES_desgravamen_prestamos`
  WHERE TIPO_SEGURO IN ('958','968','972') AND TIPO_MOVIMIENTO_NUM = '4' AND CODIGO_ERROR <> '1155'
)
SELECT t.CERTIFICADO, ROW_NUMBER() OVER (PARTITION BY t.CERTIFICADO ORDER BY t.FEC__INICIO) AS NRO_REG,
      COUNT(*) OVER (PARTITION BY t.CERTIFICADO) AS CANT_PAGOS, t.FEC__INICIO, t.FEC__FIN, t.LINEA_TRAMA,
FROM tramas_unicas t
ORDER BY t.CERTIFICADO, FEC__INICIO;


SELECT ep.IDEDET, ep.LINEA_TRAMA
  FROM `produccion.ERRORES_desgravamen_prestamos` ep
  INNER JOIN `produccion.Tabla_Errores_SAS` te ON ep.IDEERROR = te.IDEERROR
  WHERE ep.DESCRIPCION_ERROR = 'CAMPOS EN BLANCO'  AND ep.TIPO_MOVIMIENTO_NUM IN ('4','1');

--------------------- IDEDETs antes de 18-10 que no se encuentran despues de esa fecha --------------

WITH Idedet_anterior AS(
SELECT DISTINCT IDEDET
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE FECHA_CARGA < '2025-10-18'
),
Idedet_Ultimo AS(
SELECT DISTINCT IDEDET
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE FECHA_CARGA >= '2025-10-18'
)
SELECT *
FROM Idedet_anterior ia
LEFT JOIN Idedet_Ultimo iu ON ia.IDEDET = iu.IDEDET
WHERE iu.IDEDET IS NULL;

-----------------------------------------------------------------

SELECT DESCRIPCION_ERROR, COUNT (*) AS CANT_REG, SUM(PRIMABRUTACAN) AS TOTAL_PRIMA
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE TIPO_SEGURO NOT IN ('958','968','972') 
      AND CODIGO_ERROR <> '1155' AND FECHA_CARGA >= '2025-10-18'
GROUP BY DESCRIPCION_ERROR
ORDER BY TOTAL_PRIMA DESC;


SELECT DISTINCT NRO_LOTE, IDEDET, SUBSTR(LINEA_TRAMA, 4, 20) AS CERTIFICADO
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE TIPO_SEGURO NOT IN ('958','968','972') 
  AND FECHA_CARGA >= '2025-10-18'
  AND DESCRIPCION_ERROR = 'VALIDACIONES CONSECUENCIA ACSEL E';


SELECT SUBSTR(LINEA_TRAMA, 4, 20) AS CERTIFICADO, NRO_LOTE, IDEDET, FEC__INICIO, FEC__FIN,
      CODIGO_ERROR, IDEERROR, PRIMABRUTACAN, TIPO_MOVIMIENTO_NUM, LINEA_TRAMA
FROM `produccion.certificados_moraima` cm
INNER JOIN `produccion.ERRORES_desgravamen_prestamos` e ON cm.CERTIFICADO = SUBSTR(LINEA_TRAMA, 4, 20)
WHERE FECHA_CARGA >= '2025-10-18'

