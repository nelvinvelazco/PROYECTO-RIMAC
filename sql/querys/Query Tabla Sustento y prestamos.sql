SELECT  
  Moneda, 
  count(*) AS Cantidad_registros, 
  sum(Prima) AS Total_Prima, 
FROM `develop.PRESTAMOS_2025_BBVA` 
WHERE fecha_recepcion between '2025-08-4' and '2025-09-01'
GROUP BY Moneda;


SELECT  
  Moneda, 
  count(*) AS Cantidad_registros, 
  sum(Prima) AS Total_Prima, 
FROM `develop.TABLA_SUSTENTO_BBVA` 
WHERE fecha_recepcion ='2025-08-15' and Codigo_Subproducto in ("901", "902", "903", "906", "941", "943", "972", "959", "961", "968", "963", "964", "962", "951", "958", "953", "954", "952", "969","966")
GROUP BY Moneda;
----------------------------------------------------------------------------------------

WITH certificados_unicos AS(
  SELECT  DISTINCT Nro_Certificado
  FROM `develop.TABLA_SUSTENTO_BBVA` 
  WHERE fecha_recepcion ='2025-07-15' and Codigo_Subproducto in ("901", "902", "903", "906", "941", "943", "972",
            "959", "961", "968", "963", "964", "962", "951", "958", "953", "954", "952", "969","966")
)
SELECT cu.Nro_Certificado, tp.trama_original
FROM certificados_unicos cu
LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` tp ON cu.Nro_Certificado = tp.Certificado
WHERE Tipo_Movimiento = '1' AND Tipo_Registro = '01';


SELECT Certificado, count(*) AS contador 
FROM `develop.TABLA_PRESTAMOS_BBVA` 
WHERE Tipo_Movimiento = '1' AND Tipo_Registro = '01'
GROUP BY Certificado
HAVING contador > 1;

-----------------------------------------------------------------------------

SELECT Certificado, trama_original, fecha_recepcion
FROM `develop.TABLA_PRESTAMOS_BBVA` 
WHERE fecha_recepcion BETWEEN '2024-07-01' AND '2025-08-01' AND Tipo_Movimiento = '6';

------- Cruce para ver los certificados en alta --------
SELECT Fecha_Afiliacion, Fecha_Inicio_Seguro, cu.Certificado
FROM `produccion.Temp_certificados` cu
INNER JOIN `develop.TABLA_PRESTAMOS_BBVA` tp ON cu.certificado = tp.Certificado
WHERE Tipo_Movimiento = '1' AND Tipo_Registro = '01';


------- Cruce para ver los certificados martha --------
SELECT cu.Certificado, Fecha_Inicio_Seguro, Fecha_Fin_Seguro, fecha_recepcion, Tipo_Movimiento
FROM `develop.temp_cert_marta` cu
LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` tp ON cu.certificado = tp.Certificado
WHERE Tipo_Movimiento IN ('4');

----------- CONSULTA A TKT ----------------------------
SELECT cu.Certificado, fecha_recepcion, trama_original
FROM `develop.certificados_tkt_16-10` cu
LEFT JOIN `develop.TABLA_TKT_BBVA` tkt ON cu.certificado = tkt.Certificado
WHERE Tipo_Movimiento IN ('4');

SELECT distinct cu.Certificado, fecha_recepcion, trama_original, nombre_archivo_trama
FROM `develop.temp_certificados_tkt-21-11` cu
LEFT JOIN `develop.TABLA_TKT_BBVA` tkt ON cu.certificado = tkt.Certificado
WHERE Tipo_Movimiento IN ('1');

---------------------------------------------------
SELECT Certificado, count(*) AS contador
FROM `develop.temp_pagos_cert1`
GROUP BY CERTIFICADO
ORDER BY CONTADOR DESC;

SELECT *
FROM `develop.temp_pagos_cert1`
WHERE Certificado = '00110760644000068053'
ORDER BY fecha_recepcion DESC;

SELECT *
FROM (
  SELECT 
    cu.Certificado,
    tp.Fecha_Inicio_Seguro,
    SAFE.PARSE_DATE('%Y%m%d', tp.Fecha_Inicio_Seguro) AS Fecha_Inicio,
    tp.Fecha_Fin_Seguro,
    SAFE.PARSE_DATE('%Y%m%d', tp.Fecha_Fin_Seguro)   AS Fecha_Fin,
    tp.fecha_recepcion,
    tp.Tipo_Movimiento,
    ROW_NUMBER() OVER (
      PARTITION BY cu.Certificado
      ORDER BY tp.fecha_recepcion DESC
    ) AS rn
  FROM `develop.temp_cert_marta2` cu
  LEFT JOIN `develop.TABLA_PRESTAMOS_BBVA` tp 
         ON cu.Certificado = tp.Certificado
  WHERE tp.Tipo_Movimiento IN ('4')
)
WHERE rn = 1;

-----------------------