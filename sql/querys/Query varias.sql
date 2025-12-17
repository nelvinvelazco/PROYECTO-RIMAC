select fecha_recepcion
FROM `develop.TABLA_TC_BBVA`
WHERE fecha_recepcion between '2025-05-01' AND '2025-07-30';

SELECT  EXTRACT(YEAR FROM fecha_recepcion) as Anio, EXTRACT(MONTH FROM fecha_recepcion) AS Mes, COUNT(*) as Cantidad, 
FROM `develop.TABLA_TC_BBVA`
GROUP BY Anio, Mes
ORDER BY Anio, Mes;

SELECT  EXTRACT(YEAR FROM fecha_recepcion) as Anio, EXTRACT(MONTH FROM fecha_recepcion) AS Mes, COUNT(*) as Cantidad, 
FROM `develop.TABLA_PRESTAMOS_BBVA`
GROUP BY Anio, Mes
ORDER BY Anio, Mes;


SELECT EXTRACT(YEAR FROM fec__inicio) as Anio, EXTRACT(MONTH FROM fec__inicio) AS Mes, 
        count(*) AS Cant_errores, sum(primabrutacan) AS Monto_Prima
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE FECHA_PERIODO BETWEEN '2025-05-01' AND '2025-05-30'
GROUP BY Anio, Mes
ORDER BY Anio, Mes;


SELECT EXTRACT(YEAR FROM fec__inicio) as Anio, EXTRACT(MONTH FROM fec__inicio) AS Mes, 
        count(*) AS Cant_errores, 
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE primabrutacan is NULL
GROUP BY Anio, Mes;


SELECT CODIGO_ERROR, COD_DE_CERTIFICADO, PRIMABRUTACAN, FEC__INICIO
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE FEC__INICIO is null;

SELECT CODIGO_ERROR
FROM `produccion.ERRORES_desgravamen_prestamos`
WHERE FECHA_PERIODO = '2025-09-05';

--DELETE FROM `produccion.ERRORES_desgravamen_prestamos`
--WHERE FECHA_PERIODO = '2025-09-05';

--DELETE FROM `produccion.CONTROL_tramas_diarias`
--WHERE ARCHIVO_TXT = 'RED020125_0301.TXT';


SELECT  
  Moneda, 
  count(*) AS Cantidad_registros, 
  sum(PRIMABRUTACAN) AS Total_Prima, 
FROM `produccion.ERRORES_desgravamen_TC` 
GROUP BY Moneda;

WITH moneda_errada AS (
SELECT MONEDA, PRIMABRUTACAN
FROM `produccion.ERRORES_desgravamen_TC`
WHERE MONEDA NOT IN ('SOL','USD') OR MONEDA IS NULL
)
SELECT  
  Moneda, 
  count(*) AS Cantidad_registros, 
  sum(PRIMABRUTACAN) AS Total_Prima, 
FROM moneda_errada
GROUP BY Moneda;

--UPDATE `produccion.ERRORES_desgravamen_TC` 
--SET MONEDA = 'SIN DATO'
--WHERE MONEDA NOT IN ('SOL','USD') OR MONEDA IS NULL;


------- Crear una tabla particionada a partir de otra ----------
CREATE OR REPLACE TABLE `produccion.TRAMAS_diarias_BBVA_2020`
PARTITION BY DATE(FECHA_DECLARADA)
CLUSTER BY TIPO_DE_SEGURO, FECHA_DE_AFILIACION, TIPO_DE_MOVIMIENTO
AS
SELECT *
FROM `produccion.tramas_diarias_BBVA2020`;