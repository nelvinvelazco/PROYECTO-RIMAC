--- CERTIFICADOS DE PRESTAMOS-------
WITH certificados_prestamos AS (
  SELECT DISTINCT Nro_Certificado
  FROM `develop.TABLA_SUSTENTO_BBVA`
  WHERE Codigo_Subproducto IN ("901", "902", "903", "906", "941", "943", "972", "959", "961", "968", "963", "964", 
                                "962",   "951", "958", "953", "954", "952", "966")
  AND fecha_recepcion = '2025-08-15'
)
SELECT tp.Tipo_de_seguro, cu.Nro_Certificado, tp.Tipo_Documento_Identidad, tp.Numero_Documento_Identidad, tp.trama_original
FROM certificados_prestamos cu
LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` tp ON cu.Nro_Certificado = tp.Certificado
WHERE tp.Tipo_Movimiento = '1' AND tp.Tipo_Registro = '01';


--- CERTIFICADOS DE TC-------
WITH certificados_prestamos AS (
  SELECT DISTINCT Nro_Certificado
  FROM `develop.TABLA_SUSTENTO_BBVA`
  WHERE Codigo_Subproducto IN ("918") AND fecha_recepcion = '2025-08-15'
)
SELECT tc.Tipo_de_seguro, cu.Nro_Certificado, tc.Tipo_Documento_Identidad, tc.Numero_Documento_Identidad, tc.trama_original
FROM certificados_prestamos cu
LEFT JOIN `develop.TABLA_DTC_BBVA` tc ON cu.Nro_Certificado = tc.Certificado
WHERE tc.Tipo_Movimiento = '1' AND tc.Tipo_Registro = '01';


--- CERTIFICADOS DE TKT-------
WITH certificados_TKT AS (
  SELECT DISTINCT Nro_Certificado
  FROM `develop.TABLA_SUSTENTO_BBVA`
  WHERE Codigo_Subproducto IN ("919") AND fecha_recepcion = '2025-08-15'
)
SELECT tc.Tipo_de_seguro, cu.Nro_Certificado, tc.Tipo_Documento_Identidad, tc.Numero_Documento_Identidad, tc.trama_original
FROM certificados_TKT cu
LEFT JOIN `develop.TABLA_TKT_BBVA` tc ON cu.Nro_Certificado = tc.Certificado
WHERE tc.Tipo_Movimiento = '1' AND tc.Tipo_Registro = '01';

----- UNICOS ------
SELECT DISTINCT *
FROM `develop.SUCAVE_TKT_0825`