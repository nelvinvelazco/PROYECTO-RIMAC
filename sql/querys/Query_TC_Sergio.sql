SELECT Certificado, COUNT(*) CANTIDAD
FROM `develop.TABLA_DTC_BBVA`
WHERE Tipo_Movimiento IN ('1','4')
GROUP BY Certificado
ORDER BY CANTIDAD DESC;

-----------------------------------------

SELECT Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, Tipo_Movimiento, Tipo_Bin, Multi_Bin
FROM `develop.TABLA_DTC_BBVA`
WHERE Tipo_Movimiento IN ('1','4') AND Certificado = '00110178124000266153';

------------------------------------------

CREATE OR REPLACE TABLE develop.temp_cambios_bin_tc AS
WITH base AS (
  SELECT DISTINCT 
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin
  FROM `develop.TABLA_DTC_BBVA`
  WHERE Tipo_Movimiento IN ('1','4')
),
comparado AS (
  SELECT
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin,
    LAG(Tipo_Bin) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_tipo_bin,
    LAG(Multi_Bin) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_multi_bin
  FROM base
)
SELECT
  Certificado,
  Fecha_Inicio_Seguro,
  Fecha_Fin_Seguro,
  Tipo_Movimiento,
  Tipo_Bin,
  Multi_Bin
FROM comparado
WHERE Tipo_Bin != prev_tipo_bin OR Multi_Bin != prev_multi_bin
ORDER BY Certificado, Fecha_Inicio_Seguro;

-----------------------------------------

SELECT Certificado, PARSE_DATE('%Y%m%d', Fecha_Inicio_Seguro) AS Fecha_Inicio_Seguro, 
  PARSE_DATE('%Y%m%d', Fecha_Fin_Seguro) AS Fecha_Fin_Seguro, Tipo_Movimiento, Tipo_Bin, Multi_Bin
FROM `develop.temp_cambios_bin_tc`
WHERE Multi_Bin = 'EB';


--------------------- cuando cambia tip_bin -------------------------
WITH base AS (
  SELECT DISTINCT 
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin
  FROM `develop.TABLA_DTC_BBVA`
  WHERE Tipo_Movimiento IN ('1','4')
),
comparado AS (
  SELECT
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin,
    LAG(Tipo_Bin) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_tipo_bin
  FROM base
)
SELECT
  Certificado,
  Fecha_Inicio_Seguro,
  Fecha_Fin_Seguro,
  Tipo_Movimiento,
  prev_tipo_bin,
  Tipo_Bin,
  Multi_Bin
FROM comparado
WHERE Tipo_Bin != prev_tipo_bin
ORDER BY Certificado, Fecha_Inicio_Seguro;

------------ cuando cambia multi_Bin-------------------------

WITH base AS (
  SELECT DISTINCT
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin
  FROM `develop.TABLA_DTC_BBVA`
  WHERE Tipo_Movimiento IN ('1','4')
),
comparado AS (
  SELECT
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin,
    LAG(Multi_Bin) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_multi_bin
  FROM base
)
SELECT
  Certificado,
  Fecha_Inicio_Seguro,
  Fecha_Fin_Seguro,
  Tipo_Movimiento,
  Tipo_Bin,
  prev_multi_bin,
  Multi_Bin
FROM comparado
WHERE Multi_Bin != prev_multi_bin
ORDER BY Certificado, Fecha_Inicio_Seguro
LIMIT 900000 OFFSET 1600000;

----------------------- multi_bin = 'EB'---------------------------------
WITH base AS (
  SELECT 
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin
  FROM `develop.TABLA_DTC_BBVA`
  WHERE Tipo_Movimiento IN ('1','4')
),
comparado AS (
  SELECT
    Certificado,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Tipo_Movimiento,
    Tipo_Bin,
    Multi_Bin,
    LAG(Multi_Bin) OVER(PARTITION BY Certificado ORDER BY Fecha_Inicio_Seguro) AS prev_multi_bin
  FROM base
)
SELECT
  Certificado,
  Fecha_Inicio_Seguro,
  Fecha_Fin_Seguro,
  Tipo_Movimiento,
  Tipo_Bin,
  prev_multi_bin,
  Multi_Bin
FROM comparado
WHERE Multi_Bin != prev_multi_bin
  AND Multi_Bin = 'EB'
ORDER BY Certificado, Fecha_Inicio_Seguro;

-----------------------------------------------------

SELECT Certificado, Fecha_Inicio_Seguro_DTC, 
       Tipo_Bin, Multi_Bin, Tasa_sin_Recargo, Prima_DTC
FROM `develop.TABLA_DTC_BBVA`
WHERE Tipo_Movimiento = '4' AND Tasa_sin_Recargo != '00000000'
ORDER BY Certificado, Fecha_Inicio_Seguro_DTC;


SELECT Certificado, Fecha_Inicio_Seguro_DTC, 
       Tipo_Bin, Multi_Bin, Tasa_sin_Recargo, fecha_recepcion, trama_original, Prima_DTC
FROM `develop.TABLA_DTC_BBVA`
WHERE Tipo_Movimiento = '4' AND Certificado = '00110002304000049561'
ORDER BY Certificado, Fecha_Inicio_Seguro_DTC