----------------------- VISTA TC ---------------------------------------------
CREATE OR REPLACE VIEW `produccion.Vw_ERRORES_desgravamen_TC` AS
WITH registros_unicos AS (
  -- Paso 1: elimino duplicados completos
  SELECT DISTINCT *
  FROM `produccion.ERRORES_desgravamen_TC_Periodos`
),
errores AS (
  -- Paso 2: me quedo con una sola fila por IDEDET y periodo (última por FEC__INICIO)
  SELECT *
  FROM (
    SELECT 
      t.*,
      ROW_NUMBER() OVER (
        PARTITION BY FECHA_PERIODO, IDEDET
      ) AS rn
    FROM registros_unicos t
  )
  WHERE rn = 1
)
SELECT 
  EXTRACT(YEAR FROM FEC__INICIO) AS ANIO,
  EXTRACT(MONTH FROM FEC__INICIO) AS MES,
  FECHA_PERIODO,
  MONEDA,
  ORIGEN_ERROR,
  TIPO_MOVIMIENTO,
  TIPO_ERROR,
  DESC_ERROR_SAS,
  COUNT(*) AS Cant_Errores,           -- número de IDDET únicos en este grupo
  SUM(PRIMABRUTACAN) AS Monto_Prima -- suma de prima única por IDDET
FROM errores etc
INNER JOIN `produccion.Tabla_Errores_SAS` e ON etc.IDEERROR = e.IDEERROR
GROUP BY ANIO, MES, FECHA_PERIODO, MONEDA, ORIGEN_ERROR, TIPO_MOVIMIENTO, TIPO_ERROR, e.DESC_ERROR_SAS