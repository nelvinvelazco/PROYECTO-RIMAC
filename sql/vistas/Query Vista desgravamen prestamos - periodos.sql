CREATE OR REPLACE VIEW `produccion.Vw_ERRORES_desgravamen_prestamos` AS
WITH registros_unicos AS (
  -- Paso 1: elimino duplicados completos
  SELECT DISTINCT *
  FROM `produccion.ERRORES_desgravamen_Prestamos_Periodos`
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
  FEC__INICIO,
  FECHA_PERIODO,
  MONEDA,
  ORIGEN_ERROR,
  TIPO_MOVIMIENTO,
  TIPO_ERROR,
  DESCRIPCION_ERROR,
  COUNT(*) AS Cant_Errores,           -- número de IDDET únicos en este grupo
  SUM(PRIMABRUTACAN) AS Monto_Prima -- suma de prima única por IDDET
FROM errores
GROUP BY FEC__INICIO, FECHA_PERIODO, MONEDA, ORIGEN_ERROR, TIPO_MOVIMIENTO, TIPO_ERROR, DESCRIPCION_ERROR