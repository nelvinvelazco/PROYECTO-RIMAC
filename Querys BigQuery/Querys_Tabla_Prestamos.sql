---------------------------- CONVIVENCIA DE PLANES ------------------------
WITH prestamos_prev_tipo_seguro AS (
SELECT DISTINCT Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, 
      Tipo_Movimiento ,Tipo_de_seguro,
      LAG(Tipo_de_seguro) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_Tipo_de_seguro,
      trama_original
FROM `develop.TABLA_PRESTAMOS_BBVA`
)
SELECT *
FROM prestamos_prev_tipo_seguro
WHERE Tipo_de_seguro != prev_Tipo_de_seguro;

------------------------ CRUCE CONVIVENCIA DE PLANES CON TABLA DE ERRORES --------------------------------------------------

WITH prestamos_prev_tipo_seguro AS (
SELECT DISTINCT Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, 
      Tipo_Movimiento ,Tipo_de_seguro,
      LAG(Tipo_de_seguro) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_Tipo_de_seguro,
      --trama_original
FROM `develop.TABLA_PRESTAMOS_BBVA`
),
certificados_unicos AS (
  SELECT distinct Certificado
  FROM prestamos_prev_tipo_seguro
  WHERE Tipo_de_seguro != prev_Tipo_de_seguro
)
SELECT SUBSTR(LINEA_TRAMA, 4, 20) AS CERTIFICADO, LINEA_TRAMA
FROM certificados_unicos ce
LEFT JOIN `produccion.ERRORES_desgravamen_prestamos` dp ON ce.certificado = dp.COD_DE_CERTIFICADO
WHERE  FECHA_CARGA >= '2025-10-18';
---------------------------------------------------------

SELECT Certificado, Fecha_Inicio_Seguro, 
       Tasa_sin_Recargo, Prima, fecha_recepcion
FROM `develop.TABLA_PRESTAMOS_BBVA`
WHERE Tipo_Movimiento = '4' AND fecha_recepcion BETWEEN '2023-03-01' AND '2023-08-31'
ORDER BY Certificado, Fecha_Inicio_Seguro;
--------------------------------------------------------

WITH prestamos_prev_Prima AS (
SELECT Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, 
      Tipo_Movimiento ,Prima, LAG(Prima) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_Prima
FROM `develop.TABLA_PRESTAMOS_BBVA`
)
SELECT *
FROM prestamos_prev_Prima
WHERE Prima != prev_Prima
ORDER BY Certificado, Fecha_Inicio_Seguro;


SELECT trama, Certificado, Fecha_Inicio_Seguro
FROM `produccion.tramas_buscar_sustento` tr
LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` ts ON tr.TRAMA = ts.trama_original
WHERE Certificado is not null;

SELECT DISTINCT trama, COD_DE_CERTIFICADO, FEC__INICIO
FROM `produccion.tramas_buscar_sustento` tr
LEFT JOIN `produccion.ERRORES_desgravamen_prestamos` ts ON tr.TRAMA = ts.LINEA_TRAMA
WHERE COD_DE_CERTIFICADO is not null;


------------------ cruce con tabla sustento -------------------------------------
WITH certificado_fecha AS(
  SELECT CONCAT(SUBSTR(TRAMA, 4, 20), SUBSTR(TRAMA, 377, 6)) AS CERTIFICADO_FECHA
  FROM `produccion.tramas_buscar_sustento`
),
tramas_sustento AS(
  SELECT trama_original, fecha_recepcion, 
        CONCAT(Nro_Certificado, CONCAT(SUBSTR(Fecha_de_Liquidacion, 1, 4),SUBSTR(Fecha_de_Liquidacion, 6, 2))) AS CERTIFICADO_FECHA
  FROM `develop.TABLA_SUSTENTO_BBVA`
)
SELECT c.CERTIFICADO_FECHA, ts.trama_original, ts.fecha_recepcion
FROM certificado_fecha c
INNER JOIN tramas_sustento ts ON c.CERTIFICADO_FECHA = ts.CERTIFICADO_FECHA;


---------------------- Tramas omitiendo fecha afiliacion que comienza con 000 si se repite
WITH certificados_filtro AS( 
SELECT Certificado, Fecha_Afiliacion, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, trama_original
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY Certificado, Fecha_Inicio_Seguro ORDER BY 
                            CASE WHEN STARTS_WITH(Fecha_Afiliacion, '000') THEN 1 ELSE 0 END) AS rn
  FROM `develop.TABLA_PRESTAMOS_BBVA`
  WHERE Tipo_de_seguro = '959'
    AND Tipo_Movimiento = '4'
    AND Tipo_Registro = '01'
)
WHERE rn = 1
ORDER BY Certificado, Fecha_Inicio_Seguro
)
SELECT Certificado, ROW_NUMBER() OVER (PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS nro_reg, 
      Fecha_Afiliacion, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, trama_original 
FROM certificados_filtro
ORDER BY certificado, nro_reg;
------------------------------------------ 

WITH certificados AS (
  SELECT CERTIFICADO, FORMAT_DATE('%Y%m%d', PARSE_DATE('%d/%m/%Y', FECHA_INICIO)) AS FECHA_INICIO_SEG
  FROM `develop.temp_certificados_crist`
)
SELECT c.CERTIFICADO, tp.Fecha_Inicio_Seguro, tp.Fecha_Fin_Seguro, Tipo_Movimiento, trama_original, 
FROM certificados c
LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` tp ON c.CERTIFICADO = tp.Certificado
WHERE c.FECHA_INICIO_SEG = tp.Fecha_Inicio_Seguro AND Tipo_Movimiento = '4'
