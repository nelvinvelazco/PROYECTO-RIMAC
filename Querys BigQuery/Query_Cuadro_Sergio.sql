CREATE OR REPLACE TABLE `develop.temp_resultados` AS
WITH base AS (
  SELECT 
    Certificado,
    Fecha_Afiliacion,
    Tipo_de_seguro,
    Fecha_Inicio_Seguro,
    Fecha_Fin_Seguro,
    Moneda,
    prima,
    fecha_recepcion,
    CONCAT(Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro) AS llave
  FROM `develop.TABLA_PRESTAMOS_BBVA`
  WHERE Tipo_de_seguro IN ('972', '968', '958') 
    AND Tipo_Registro = '01' 
    AND Tipo_Movimiento IN ('1','4')
),

-- 1. Marcar si la fecha es válida (no comienza con "00")
marcados AS (
  SELECT 
    b.*,
    CASE WHEN STARTS_WITH(Fecha_Afiliacion, '00') THEN 0 ELSE 1 END AS es_valida
  FROM base b
),

-- 2. Priorizar válidos, pero si todos son "00…" quedarnos con 1
priorizados AS (
  SELECT m.*,
         ROW_NUMBER() OVER (
           PARTITION BY llave
           ORDER BY es_valida DESC, Fecha_Afiliacion ASC
         ) AS rn_global
  FROM marcados m
),

-- 3. Resolver duplicados válidos
resueltos AS (
  SELECT *
  FROM (
    SELECT p.*,
           ROW_NUMBER() OVER (
             PARTITION BY llave, Tipo_de_seguro, Fecha_Inicio_Seguro
             ORDER BY Fecha_Afiliacion ASC
           ) AS rn
    FROM priorizados p
    WHERE rn_global = 1 OR es_valida = 1
  )
  WHERE rn = 1
)

SELECT 
  Certificado,
  PARSE_DATE('%Y%m%d', Fecha_Afiliacion) AS Fecha_Afiliacion,
  Tipo_de_seguro,
  Fecha_Inicio_Seguro,
  Fecha_Fin_Seguro,
  prima,
  llave,
  Moneda,
  fecha_recepcion
FROM resueltos
ORDER BY llave;


-------------------------------------------------------------------


WITH resumen AS (
  SELECT 
    Tipo_de_seguro,
    FORMAT_DATE('%b-%y', DATE_TRUNC(SAFE_CAST(fecha_recepcion AS DATE), MONTH)) AS PERIODO,
    COUNT(*) AS CANTIDAD,
    SUM(CASE WHEN Moneda = 'PEN' THEN prima ELSE 0 END) AS PEN,
    SUM(CASE WHEN Moneda = 'USD' THEN prima ELSE 0 END) AS USD
  FROM `develop.temp_resultados`
  GROUP BY Tipo_de_seguro,PERIODO
)
SELECT *
FROM resumen
ORDER BY PARSE_DATE('%b-%y', PERIODO), Tipo_de_seguro;
