

---Reporte de errores parametrizar 
with a as (
select 
     det.idelote AS "NRO LOTE",
      app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_lotesant_list(lot.idelote,
                                                       det.codprodext,
                                                       det.ideescenario,
                                                       (select d.numcertificadoext from app_iaa_interfaz.int_lotedetide d where d.idedet = det.idedet) ,
                                                       (select d.fecinipag from app_iaa_interfaz.int_lotedetide d where d.idedet = det.idedet) 
                                                               ) AS "LOTES ANTERIORES",
     lot.feccarga AS "FECHA CARGA",
     det.ideprod AS "CODIGO PRODUCTO",
     (select pro.dscproducto from app_iaa_producto.pro_producto pro where pro.ideprod = det.ideprod) AS "PRODUCTO",
     det.ideplan AS "CODIGO PLAN",
     (select pla.dscplan from app_iaa_producto.pro_plan pla where pla.ideplan = det.ideplan) AS "NOMBRE DE PLAN",
     (select d.numcertificadoext from app_iaa_interfaz.int_lotedetide d where d.idedet = det.idedet) AS "COD DE CERTIFICADO",

     (select max (i2.fecinivig)  from app_iaa_interfaz.int_lotedetide i2
     join app_iaa_interfaz.int_lotedet d2 on i2.idedet = d2.idedet
     where 1=1
     and i2.numcertificadoext = (
                              select d.numcertificadoext from app_iaa_interfaz.int_lotedetide d where d.idedet = det.idedet)
     and app_iaa_interfaz.pq_iaa_intescenario.fn_escenario_es_alta(d2.ideescenario) = 1
     and d2.stsestado not in ( 'ANU', 'ERR') and d2.ideprod = det.ideprod
     ) AS "fecini_alta_CERTIFICADO",
     (select max (i2.fecfinvig)  from app_iaa_interfaz.int_lotedetide i2
     join app_iaa_interfaz.int_lotedet d2 on i2.idedet = d2.idedet
     where 1=1
     and i2.numcertificadoext = (
                              select d.numcertificadoext from app_iaa_interfaz.int_lotedetide d where d.idedet = det.idedet)
     and app_iaa_interfaz.pq_iaa_intescenario.fn_escenario_es_alta(d2.ideescenario) = 1
     and d2.stsestado not in ( 'ANU', 'ERR') and d2.ideprod = det.ideprod
     ) AS "fecfin_alta_CERTIFICADO",
     
     det.idedet AS "IDEDET",
     nvl((select par.abreviatura
            from app_iaa_interfaz.int_escenario esc,
                 app_iaa_interfaz.int_tipoescenario tip,
                 app_iaa_comunes.cfg_parametro par
           where esc.ideescenario = det.ideescenario
             and tip.idetipoescenario = esc.idetipoescenario
             and par.codigoc = tip.idpclaseescenario
             and par.idetippar = 'INT_CLASEESCENARIO'
             and esc.stsescenario = 'S'
             and tip.stsestado = 'ACT'
             and par.indactivo = 'S'
         ),'Sin Movimiento') AS "TIPO MOVIMIENTO",
     --det.idedetori,
     
     /*trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0000511')) fecinivig_cer,
     trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0000411')) fecfinvig_cer,
     trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'PAG0000800')) fecinivig_pag,
     trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'PAG0000900')) fecfinvig_pag,*/
     app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datofecha(nvl( trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0000511'))
                                                              ,trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'PAG0000800')))) "FEC. INICIO",
     app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datofecha(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0000411'))
                                                              ,trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'PAG0000900')))) "FEC. FIN",
     trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0000810')) AS "MONEDA",
     
     --nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0001000')),'0') suma_asegurada,
     --app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0001000')),'0'),100) "SUMA ASEGURADA",
     CASE 
        WHEN regexp_like(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0001000')),'0'), '^\d+(\.\d+)?$')
        THEN to_number(to_char(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(REGEXP_SUBSTR(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0001000')),'0'), '[^.]*'),100),
        '99999999999999999999999.9999999'), '99999999999999999999999.9999999')
        ELSE NULL
        END AS "SUMA ASEGURADA",
     
     --nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000900')),'0') tasa,--tasa sin recargo
     --app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero( nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000900')),'0'),10000000) "TASA",
     CASE 
        WHEN regexp_like(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000900')),'0'), '^\d+(\.\d+)?$')
        THEN to_number(to_char(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(REGEXP_SUBSTR(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000900')),'0'), '[^.]*'),10000000),
        '99999999999999999999999.9999999'), '99999999999999999999999.9999999')
        ELSE NULL
        END AS "TASA",
     
     --nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000400')),'0') ajuste,--para calcular tasa con recargo
     app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datocalculado(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000900')),'0'),10000000),
         app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(case when regexp_like(trim(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000400')),'0'))
                                                                   , '^-?[[:digit:]]*$') then nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'OBJ0000400')),'0') else '0' end,10000)) "TASA RECARGO",

     --app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001011')),'0'),100) primabrutacan,
     CASE 
        WHEN regexp_like(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001011')),'0'), '^\d+(\.\d+)?$')
        THEN to_number(to_char(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(REGEXP_SUBSTR(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001011')),'0'), '[^.]*'),100),
            '99999999999999999999999.9999999'), '99999999999999999999999.9999999')
        ELSE NULL
        END AS "PRIMABRUTACAN",
     
     --app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001111')),'0'),100) primanetacan,
    CASE 
        WHEN regexp_like(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001111')),'0'), '^\d+(\.\d+)?$')
        THEN to_number(to_char(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_datonumero(REGEXP_SUBSTR(nvl(trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'ACU0001111')),'0'), '[^.]*'),100),
            '99999999999999999999999.9999999'), '99999999999999999999999.9999999')
        ELSE NULL
        END AS "PRIMANETACAN",
    
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0002102')) nomcompleto,
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0000202')) apepaterno,
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0000102')) apematerno,
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0001302')) fecnacimiento,
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0003502')) tipdocumento,
      trim(app_iaa_interfaz.pq_iaa_intmonitor.fn_obt_trama(det.idedet, 'TER0002202')) numdocumento,
     lot.nomarchivo AS "NOMBRE DE ARCHIVO"
     ,(select cadtramaori1 from app_iaa_interfaz.int_lotedet d2 where d2.idedet= det.idedetori) AS "LINEA TRAMA"
     
    from app_iaa_interfaz.int_lote lot,
     app_iaa_interfaz.int_lotedet det
    where lot.ideentidad in ( &entidad )
    and lot.idelote in (&idelote)
    --and lot.feccarga >= to_date(&fechaini,'dd/mm/yyyy')--&fechaini--'01/01/2023'
    --and lot.feccarga <= to_date(&fechafin,'dd/mm/yyyy')--&fechafin--'01/05/2023'
    --and lot.feccarga <= to_date('31/12/2024','dd/mm/yyyy')
    and det.idelote = lot.idelote
    --and lot.idelote in (&idelote)--39849, 70461, 70742, 70882, 72944, 72982, 73662, 73913, 75303, 75916, 75919, 76637, 76769, 79527
    
    and det.idptipotrama = 'D'
    and det.stsestado = 'ERR'
), b as (
    select val.idelote,
       val.idedet,
       (CASE 
       WHEN val.idpresponsable ='EXT' THEN 'Error canal'
       WHEN val.idpresponsable ='INT' THEN 'Error Rimac'                          
       ELSE '' END) AS "ORIGEN ERROR",
       val.ideerror as "CODIGO ERROR",
       val.cadresultado as "DESCRIPCION ERROR"
  from app_iaa_interfaz.int_lotedet_val val                          
 where val.stsestado = '1' and ideerror <> '908'--error generico
     and val.idelote in (&idelote)
   and exists (select 1
                 from app_iaa_interfaz.int_lote lot
                 where lot.ideentidad in ( &entidad)
                  --and lot.feccarga >= to_date(&fechaini,'dd/mm/yyyy')--&fechaini '01/01/2023'
                  --and lot.feccarga <= to_date(&fechafin,'dd/mm/yyyy')--&fechafin '01/05/2023'
                  --and lot.feccarga <= to_date('31/12/2024','dd/mm/yyyy')
                  and val.idelote = lot.idelote
                  and lot.idelote in (&idelote)
                  
                  )
          )
  select a.*, b.* from a left join b on a.idedet = b.idedet ;
