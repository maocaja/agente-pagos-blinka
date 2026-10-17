# Estado del arte: agente de IA para revisar facturas de proveedores (pagar, frenar, escalar)

Fecha de consulta de todas las fuentes: 2026-10-16.

Leyenda de estado: LEIDO = pagina o documento abierto y leido en vivo con WebFetch/descarga directa. RESUMEN = solo el resultado del buscador (extracto o resumen de una pagina oficial/vendor), sin abrir la pagina completa. NO VERIFICADO = no se pudo leer en una fuente.

## Resumen ejecutivo

1. Los productos de AP con IA (Ramp, Bill, Tipalti, Stampli, Brex, Mercury) automatizan captura, codificacion, aprobacion y duplicados; sus controles de bancos del proveedor son alertas y rutas de aprobacion, no pruebas firmadas.
2. Ninguno documenta (en lo que se pudo leer) una orden de pago firmada ni una prueba verificable de que se cumplieron las reglas; es el hueco que el proyecto puede ocupar.
3. El FBI IC3 (informe 2025) registro 24.768 quejas y US$3.046.598.558 en perdidas por BEC; los controles que recomienda son llamada a numero conocido, demora y doble visto bueno.
4. La inyeccion de instrucciones en facturas esta descrita como escenario en un articulo academico (A2AS) y la defensa propuesta es codificar politica y exigir confirmacion humana para cuentas bancarias; no se hallo un caso real documentado en fuente primaria.
5. Las seis autoridades de facturacion electronica publican esquemas XML/JSON y consultas de validez; la lectura por un tercero extranjero es viable en Colombia (QR/CUFE) y Peru (consulta de validez), y queda sin verificar en los demas.
6. W-8BEN/W-8BEN-E/W-9: el IRS indica que pagos a un extranjero por servicios prestados fuera de EE. UU. no son ingreso de fuente EE. UU. (sin retencion de 30%), pero hay que documentar el estatus del beneficiario.
7. Blinka ofrece cuentas USD, tarjeta, pagos por SPEI/Pix/Bre-B/etc., USDC y back office de facturas y proveedores; su sitio y documentacion publica no mencionan API ni agentes.
8. AP2 (v0.2) define mandatos firmados con restricciones de monto (amount_range, budget) y lista de beneficiarios (allowed_payees) y recibos firmados; TAP de Visa no define limites ni listas; x402 y Agent Pay se cubren parcialmente.

---

## 1. Productos actuales de cuentas por pagar con IA o agentes

| Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|
| Ramp lanzo "Agents for AP" en Bill Pay: codifican facturas (85% de campos contables correctos al primer intento segun Ramp), dan informacion a aprobadores, buscan opciones de pago con tarjeta en portales de proveedores | https://www.pymnts.com/news/artificial-intelligence/2025/ramp-adds-ai-agents-invoice-coding-approval-payment-processing/ | 2026-10-16 | LEIDO (cifra es dato de la empresa) |
| Ramp: los agentes "flag suspicious invoices and vendor changes before a bill is created"; clientes de acceso temprano tuvieron mas de US$1 millon en facturas fraudulentas marcadas en 90 dias | misma URL PYMNTS | 2026-10-16 | LEIDO (cifra de la empresa, no auditada) |
| Ramp: alertas amarillas/rojas por "new or changed bank account details"; el sistema registra quien descarto la alerta y siguio con borrador, aprobacion o pago; la pagina no dice que bloquee el pago y recomienda verificar por otro canal y usar varios niveles de aprobacion | https://support.ramp.com/bill-pay-fraud | 2026-10-16 | LEIDO |
| Ramp: deteccion de duplicados por proveedor, numero de factura y monto; enrutamiento por reglas condicionales | https://ramp.com/blog/ap-automation-software y https://ramp.com/accounts-payable-lp | 2026-10-16 | RESUMEN (marketing) |
| Stampli (Billy): duplicados en tres puntos (ingreso, codificacion, exportacion); coincidencia de numero, proveedor y anio marca duplicado, otras combinaciones marcan "posible duplicado" para revision humana; Billy trabaja bajo supervision humana | https://stampli.com/blog/news/prevent-duplicate-invoice-payments/ | 2026-10-16 | RESUMEN |
| Stampli: verificacion de cambio de datos bancarios | no encontrada | 2026-10-16 | NO VERIFICADO |
| BILL lanzo "BILL AI" en el ano fiscal 2026 con agentes para W-9, soporte, transacciones sin intervencion, conciliacion y codificacion compleja | https://www.sec.gov/Archives/edgar/data/0001786352/000162828026058238/bill-20260630.htm (10-K FY2026) | 2026-10-16 | RESUMEN (no se abrio el 10-K completo) |
| BILL: verificacion de cambio de cuenta bancaria del proveedor y limites de los agentes | no encontrada | 2026-10-16 | NO VERIFICADO |
| Tipalti: agentes de IA que marcan duplicados y anomalias; cadenas de aprobacion, auditoria, cotejo 2 y 3 vias; verificacion de cuenta bancaria del beneficiario no descrita | https://tipalti.com/en-uk/accounts-payable-software/finance-ai/ | 2026-10-16 | RESUMEN (marketing) |
| Brex Payables (2023-2024): extraccion con IA, cotejo con orden de compra, marca facturas sospechosas, aprobaciones multinivel, proveedor ingresa sus datos por enlace seguro; sin evidencia de agentes ni de control de cambio bancario | https://www.brex.com/product-announcements/a-smarter-bill-pay | 2026-10-16 | RESUMEN (no hay datos 2026) |
| Mercury: bill pay con extraccion de datos por IA y bandeja por estado de aprobacion; ACH, wire o cheque | https://mercury.com/bill-pay | 2026-10-16 | RESUMEN |
| Mercury MCP oficial de solo lectura; un MCP comunitario puede escribir pero respeta la politica de aprobacion de la cuenta | listados de terceros (mcp.so, toolradar) | 2026-10-16 | NO VERIFICADO (no se leyo documentacion de Mercury) |
| Airbase | no se investigo en profundidad | 2026-10-16 | NO VERIFICADO |
| Verificacion firmada de ordenes de pago o prueba de cumplimiento de reglas en alguno de estos productos | no encontrada en ninguna fuente leida (solo registros de auditoria de acciones humanas, p. ej. Ramp) | 2026-10-16 | NO VERIFICADO (ausencia de evidencia, no prueba de ausencia) |

Donde no llegan (inferido de lo leido): alertas que la persona puede descartar (Ramp), decisiones de pago no vinculadas criptograficamente a reglas vigentes, nada sobre leer la factura electronica fiscal del pais del proveedor como fuente de verdad, y nada especifico para pagos a contratistas en LatAm con retencion/documentacion fiscal de EE. UU. Estas son inferencias, no afirmaciones de las fuentes.

## 2. Fraude de facturas y cambio de datos bancarios

| Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|
| 2025: 24.768 quejas BEC (21.442 en 2024; 21.489 en 2023) | https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf (pag. 8 y 26) | 2026-10-16 | LEIDO (PDF descargado) |
| 2025: perdidas BEC US$3.046.598.558 (2024: US$2.770.151.146; 2023: US$2.946.830.270), segundo tipo de crimen por perdida tras inversion (US$8.648.617.756) | misma URL | 2026-10-16 | LEIDO |
| Perdidas totales reportadas al IC3 en 2025: US$20,877 mil millones; 1.008.597 quejas | misma URL | 2026-10-16 | LEIDO |
| IC3 2025: empresas reportaron mas de US$30 millones en perdidas por BEC con IA | misma URL | 2026-10-16 | LEIDO |
| Definicion IC3 de BEC: estafa dirigida a negocios que trabajan con proveedores y/o realizan transferencias; usa cuentas de correo y otros medios comprometidos | misma URL | 2026-10-16 | LEIDO |
| Control: verificar un cambio de instrucciones de pago llamando para confirmar verbalmente, con numero de una lista de contactos conocida y no del correo | https://ic3.gov/media/2018/180221.aspx (PSA I-022118) | 2026-10-16 | LEIDO (descarga directa) |
| Control: demorar la transaccion hasta completar verificaciones adicionales | misma PSA 2018 | 2026-10-16 | LEIDO |
| Control: "Verify all payment changes and transactions in person or via a known telephone number" | https://www.ic3.gov/PSA/2020/PSA200406 | 2026-10-16 | LEIDO |
| Control: segunda aprobacion (sign-off) por personal de la empresa para cambios de ubicacion de pago de proveedor | https://www.ic3.gov/PSA/2015/PSA150122.pdf | 2026-10-16 | RESUMEN |
| "Periodo de enfriamiento" como control con ese nombre | no hallado en IC3; la PSA 2018 solo dice demorar hasta verificar | 2026-10-16 | NO VERIFICADO como recomendacion formal con plazo |
| Escenario de inyeccion: instruccion oculta en una factura que hace que un asistente financiero reemplace la cuenta bancaria del proveedor por la del atacante; defensas: agente de solo lectura, delimitar contenido no confiable, politica que exija confirmacion humana para cuentas bancarias | https://arxiv.org/pdf/2510.13825 (A2AS, seccion 6.1, Figura 9) | 2026-10-16 | LEIDO (PDF descargado). Es un escenario propuesto, no un incidente real |
| CrackedPDFs: benchmark de 29.322 PDFs (9.774 con inyeccion) y detector hibrido con F1 0,960; no menciona facturas | https://arxiv.org/abs/2607.19396 (v1 3 jul 2026, v2 2 ago 2026) | 2026-10-16 | LEIDO (solo el resumen) |
| AP2 asume que prevenir la inyeccion de instrucciones es inviable y trata a todo LLM/agente como atacante potencial | https://raw.githubusercontent.com/google-agentic-commerce/AP2/main/docs/ap2/security_and_privacy_considerations.md | 2026-10-16 | LEIDO |
| Casos reales de inyeccion en facturas contra asistentes de IA en produccion, con fuente primaria | no hallado (el buscador devolvio blogs y un caso de Atlassian Rovo que no se abrio) | 2026-10-16 | NO VERIFICADO |

## 3. Facturacion electronica: Mexico, Brasil, Colombia, Chile, Peru, Argentina

Solo se aceptan autoridades o documentacion tecnica oficial. Varias paginas oficiales respondieron con error o no se pudieron abrir; se anota en cada caso.

| Pais | Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|---|
| Mexico | CFDI es XML conforme al Anexo 20; la version 4.0 es la unica valida desde el 1 abril 2023; el complemento Timbre Fiscal Digital es obligatorio | http://omawww.sat.gob.mx/tramitesyservicios/Paginas/anexo_20.htm y guia Anexo 20 | 2026-10-16 | RESUMEN |
| Mexico | La validacion con efecto fiscal la hace un PAC autorizado al timbrar con el sello del SAT | http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/PregFrecCFDIVer4_0.pdf | 2026-10-16 | RESUMEN (el PDF no se pudo abrir: error de conexion) |
| Mexico | Un tercero extranjero puede consultar un CFDI en la herramienta publica del SAT | no leida | 2026-10-16 | NO VERIFICADO |
| Brasil | NF-e: XML validado contra esquemas XSD publicados en el Portal Nacional; paquetes de liberacion vigentes (p. ej. NT 2026.007 v1.00 publicada 31/08/26) | https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=BMPFMBoln3w%3D | 2026-10-16 | RESUMEN |
| Brasil | Autorizacion por SEFAZ y consulta por chave de acesso; consulta publica sin certificado | pagina de consulta no se pudo abrir (demasiadas redirecciones) | 2026-10-16 | NO VERIFICADO |
| Brasil | NFS-e Padrao Nacional: municipio o emisor genera la DPS y la envia al ADN (Ambiente de Dados Nacional); el ADN la acepta o rechaza; API con JSON y eventos en XML firmado | https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/documentacao-atual/manual-municipios-apis-adn-sistema-nacional-nfs-e-v1-2-out21025.pdf | 2026-10-16 | RESUMEN (PDF oficial no abierto; detalles via manuales municipales) |
| Colombia | La factura electronica usa UBL 2.1 obligatorio; el CUFE va en cbc:UUID; validacion previa por la DIAN antes de entregarla al comprador, en fracciones de segundo; documentos Application Response llevan el mismo CUFE | https://www.dian.gov.co/impuestos/factura-electronica/Documents/Anexo-Tecnico-Resolucion-000012-09022021.pdf (v1.8) y https://micrositios.dian.gov.co/sistema-de-facturacion-electronica/validacion-previa/ | 2026-10-16 | LEIDO (micrositio); RESUMEN (anexo). El anexo vigente en 2026 puede ser posterior a v1.8: NO VERIFICADO |
| Colombia | El QR apunta a https://catalogovpfe.dian.gov.co/document/searchqr?documentkey=CUFE, es decir, un tercero con el CUFE puede consultar | anexo tecnico DIAN | 2026-10-16 | RESUMEN |
| Chile | DTE: XML firmado con XMLDSIG y timbre electronico (TED); esquema EnvioDTE_v10.xsd; formato vigente version 2.5 (feb. 2026); la Resolucion 121/2026 describe validaciones de estructura, firma, TED y folio y estados Aceptado / Aceptado con reparos / Rechazado | https://www.sii.cl/servicios_online/3532-formato_xml-3811.html, https://www.sii.cl/factura_electronica/factura_mercado/formato_dte_202602.pdf, https://www.sii.cl/normativa_legislacion/resoluciones/2026/reso121.pdf | 2026-10-16 | RESUMEN |
| Chile | Consulta de autenticidad por un tercero | no hallada | 2026-10-16 | NO VERIFICADO |
| Peru | CPE en UBL 2.1; SUNAT o un OSE (Operador de Servicios Electronicos) validan; "Consulta de Validez del CPE" publica con RUC emisor, tipo, serie-numero, fecha y total; existe servicio BETA para pruebas de estructura | https://e-consulta.sunat.gob.pe/ol-ti-itconsvalicpe/ConsValiCpe.htm, https://cpe.sunat.gob.pe/noticias/servicio-beta-para-realizar-pruebas-ubl-21 | 2026-10-16 | RESUMEN |
| Peru | Hallazgo contradictorio en una pagina de SUNAT sobre si "Aceptada" tiene validez tributaria; se asume que es error de la pagina porque otras paginas SUNAT dicen lo contrario | busqueda SUNAT | 2026-10-16 | RESUMEN, conflicto sin resolver con la fuente original |
| Argentina | ARCA (ex AFIP): web services SOAP WSFEv1; FECAESolicitar asigna CAE y vencimiento; FECompConsultar consulta comprobantes emitidos | https://www.afip.gob.ar/ws/documentacion/ws-factura-electronica.asp, https://www.arca.gob.ar/fe/documentos/manual-desarrollador-ARCA-COMPG-v4-0.pdf | 2026-10-16 | RESUMEN |
| Argentina | Constatacion de comprobantes por un tercero extranjero | no hallada | 2026-10-16 | NO VERIFICADO |

Conclusion de lectura por un tercero extranjero: el formato es publico en los seis paises (XSD/UBL/API documentados), pero la validacion con efecto fiscal la hace la autoridad o un intermediario autorizado (PAC, OSE, DIAN, SEFAZ/ADN, SII, ARCA). Un agente de EE. UU. puede leer el XML y contrastarlo con la consulta publica solo donde esa consulta se confirmo (Colombia con CUFE, Peru con consulta de validez). En los otros no se confirmo si requiere clave fiscal local.

## 4. Pagos transfronterizos a contratistas en LatAm y requisitos fiscales de EE. UU.

| Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|
| Costo promedio global de enviar remesas: 6,36% en el tercer trimestre de 2025 (Issue 54), 6,49% en el primer trimestre de 2025; meta ODS/G20 de 3% a 2030. Son remesas de personas, no pagos B2B | https://remittanceprices.worldbank.org/ (pagina oficial bloqueada con 403 al abrirla; cifras de resultado del buscador sobre el informe) | 2026-10-16 | RESUMEN |
| FSB (9 oct 2025): es improbable lograr mejoras satisfactorias globales segun el calendario 2027; velocidad mayorista mejoro; el costo promedio de remesas casi no se movio; el porcentaje de servicios que liquidan en un dia habil bajo 1,7 puntos a 67,3%; meta mayorista: 75% acreditado en una hora | https://www.fsb.org/2025/10/g20-roadmap-for-cross-border-payments-consolidated-progress-report-for-2025/ | 2026-10-16 | LEIDO (la cifra 67,3% y la meta de una hora vienen del resumen del buscador de la misma pagina) |
| Estudio Mastercard con PCMI y K2 (jul 2025; 70 transacciones, 36 entrevistas): en Brasil 80% de los pagos internacionales de pymes tarda mas de 4 dias, 1 de cada 5 mas de 10; comision promedio de hasta 23,3% al enviar US$250 | https://www.businesswire.com/news/home/20250716203046/en/ ; cobertura https://www.larepublica.co/finanzas/estudio-revelo-que-pagos-transfronterizos-de-pymes-mueve-us-23-000-millones-al-ano-4435073 | 2026-10-16 | RESUMEN. No es independiente (lo encargo Mastercard); no se hallo informe equivalente del BID, CEPAL o BIS sobre B2B en LatAm: NO VERIFICADO |
| Encuesta Flywire: 70% de empresas dejaron de comprar a un proveedor internacional por la experiencia de pago | https://flywire.foleon.com/report/b2b-payments-survey-2024/executive-summary | 2026-10-16 | RESUMEN; fuente de un proveedor de pagos, no independiente |
| IRS: la mayor parte del ingreso de fuente EE. UU. recibido por un extranjero esta sujeto a 30%; se retiene sobre el monto bruto | https://www.irs.gov/publications/p515 (Pub. 515, edicion 2026) | 2026-10-16 | LEIDO (primeras 100.000 de 582.389 caracteres) |
| IRS Pub. 515: compensacion a un extranjero no residente por servicios prestados fuera de EE. UU. "is not considered wages and is not subject to withholding" (aplica a salarios); el texto sobre servicios personales independientes en EE. UU. trata ese ingreso como fuente EE. UU. | https://www.irs.gov/pub/irs-pdf/p515.pdf (lineas "Services performed outside the United States" y "Source of income") | 2026-10-16 | LEIDO parcial. La regla general para contratistas independientes pagados por trabajo hecho fuera de EE. UU. (ingreso de fuente extranjera, sin retencion) se infiere de la regla de fuente; requiere confirmar con asesor fiscal: NO VERIFICADO textualmente para contratistas |
| W-8BEN es el certificado de estatus extranjero para individuos; W-8BEN-E para entidades; sirven para que el agente de retencion trate al beneficiario como extranjero | https://www.irs.gov/individuals/international-taxpayers/forms-for-foreign-beneficial-owners | 2026-10-16 | LEIDO |
| Las instrucciones de W-8BEN indican usar Form 8233 (no W-8BEN) para reclamar exencion por servicios personales de un extranjero no residente | https://www.irs.gov/instructions/iw8ben | 2026-10-16 | RESUMEN |
| W-9 se usa para beneficiarios estadounidenses; sin TIN correcto se aplica retencion de respaldo de 24% en pagos reportables; quien entrega un W-8 valido queda exento de retencion de respaldo y del Form 1099 | https://www.irs.gov/publications/p515 | 2026-10-16 | LEIDO |
| Reporte Form 1042-S (extranjeros) y migracion de FIRE a IRIS (IRIS desde 1 ene 2026; 1042-S 2026 vence 15 mar 2027) | https://www.irs.gov/pub/irs-pdf/p515.pdf (seccion What's New) | 2026-10-16 | LEIDO |

## 5. Blinka

| Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|
| Cuentas USD (ACH y wire), tarjeta Visa Infinite global emitida por Third National, tesoreria de alto rendimiento con fondos de BNY Dreyfus y Morgan Stanley, depositos elegibles asegurados por FDIC via Portage Bank | https://www.blinka.co | 2026-10-16 | LEIDO |
| Pagos: bancarios, locales y onchain; USD por SWIFT a mas de 200 paises y rutas USD locales en Peru, Panama, China y Hong Kong | https://www.blinka.co | 2026-10-16 | LEIDO |
| Rutas locales: SEPA, Colombia (Bre-B), Brasil (Pix, TED), Mexico (SPEI), Argentina, Chile, Peru, Bolivia, Costa Rica, Sudafrica; deposito en Colombia por PSE | https://www.blinka.co | 2026-10-16 | LEIDO |
| Monedas: USD, EUR, COP, BRL, MXN, ARS, CLP, PEN, BOB, CRC, ZAR, mas USDC (Base, Ethereum, Polygon, Celo, Solana) | https://www.blinka.co | 2026-10-16 | LEIDO |
| Back office: facturacion, gestion de proveedores, automatizaciones contables; integraciones con QuickBooks y Stripe | https://www.blinka.co | 2026-10-16 | LEIDO |
| El sitio no menciona API publica, documentacion para desarrolladores ni funciones de agentes | https://www.blinka.co ; https://docs.blinka.co y https://docs.blinka.co/llms.txt (solo 10 paginas legales) | 2026-10-16 | LEIDO. Los Terminos de servicio mencionan "the Blinka platform, APIs, and services" sin referencia publica |
| Prensa: fundada por Juan Pablo y Sebastian Linares, parte de Y Combinator, mas de US$10 millones procesados en dos meses | https://www.larepublica.co/finanzas/colombianos-crearon-una-fintech-en-ee-uu-que-ya-proceso-mas-de-us-10-millones-4500136 | 2026-10-16 | RESUMEN (no es sitio de Blinka; dato de prensa) |

## 6. Protocolos de pagos con agentes

AP2 se leyo en su especificacion primaria v0.2 (repositorio oficial): specification.md completa, security_and_privacy_considerations.md completa, payment_mandate.md (restricciones y ejemplos) y agent_authorization.md (modelo, verificacion). No se leyeron en detalle checkout_mandate.md, flows.md ni implementation_considerations.md (descargados; solo busqueda por palabras clave).

| Afirmacion | Fuente (URL) | Fecha | Estado |
|---|---|---|---|
| AP2 v0.2 asegura pagos hechos por agentes con mandatos firmados (SD-JWT): Checkout Mandate (que se compra) y Payment Mandate (el pago), mas recibos firmados de checkout y de pago | https://raw.githubusercontent.com/google-agentic-commerce/AP2/main/docs/ap2/specification.md | 2026-10-16 | LEIDO |
| Modo "Human Not Present": el usuario firma mandatos abiertos con restricciones; el agente firma los cerrados con su clave (cnf); el verificador comprueba que lo cerrado cumple las restricciones; restriccion desconocida = falla | specification.md y agent_authorization.md (raw GitHub) | 2026-10-16 | LEIDO |
| Restricciones de pago definidas: payment.amount_range (rango de monto), payment.budget (tope total acumulado), payment.agent_recurrence (max_occurrences), payment.allowed_payees (beneficiarios permitidos; el payee debe estar en el arreglo allowed), allowed_payment_instruments, allowed_pisps, reference | https://raw.githubusercontent.com/google-agentic-commerce/AP2/main/docs/ap2/payment_mandate.md | 2026-10-16 | LEIDO |
| Los verificadores (proveedor de credenciales, red, procesador) DEBEN verificar restricciones y devolver recibo firmado; la validacion debe ser en codigo determinista | specification.md | 2026-10-16 | LEIDO |
| Evidencia en disputa: mandatos y recibos juntos dan una imagen "non-repudiable" de la transaccion; retencion y recuperacion quedan fuera del alcance | specification.md | 2026-10-16 | LEIDO |
| AP2 esta pensado para comercio (comerciante, carrito, Shopping Agent); no define factura de proveedor, ni lista de beneficiarios con historial, ni verificacion de cambio bancario | specification.md (roles) | 2026-10-16 | LEIDO (conclusion es inferencia sobre el alcance) |
| Visa Trusted Agent Protocol: firmas de mensaje HTTP (RFC 9421), clave del agente en un almacen confiable, tags agent-browser-auth / agent-payer-auth; NO define limites de gasto por monto ni listas de comercios/beneficiarios | https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications y https://github.com/visa/trusted-agent-protocol | 2026-10-16 | LEIDO (via WebFetch con extracto del contenido) |
| Mastercard Agent Pay: tokens agenticos; en las notas de version de MDES (production 5 ago 2026) hay controles de gasto por token: limites diario, semanal, mensual, por transaccion, absoluto, uso unico, y listas permitir/bloquear por MCC, MID, TCC, tipo de transaccion y geografia, para emisores con Agent Pay | https://developer.mastercard.com/mdes-customer-service/documentation/release-history/release-notes-july2026/ | 2026-10-16 | LEIDO |
| Mastercard Agent Pay: pagina de caso de uso "valida la intencion del titular" y usa tokenizacion | https://developer.mastercard.com/mastercard-checkout-solutions/documentation/use-cases/agent-pay/ | 2026-10-16 | RESUMEN (la pagina dio 404 al abrirla) |
| "Verifiable Intent" de Mastercard y Google (vinculo identidad, instrucciones y resultado) | guia de desarrolladores de Mastercard, via buscador | 2026-10-16 | NO VERIFICADO (no se abrio la fuente) |
| x402: estandar abierto de pago por HTTP (respuesta 402 con instrucciones, el comprador devuelve el payload, el servidor o un facilitador verifica y liquida); la pagina no menciona limites de gasto ni listas de beneficiarios | https://docs.x402.org/introduction | 2026-10-16 | LEIDO (solo la pagina de introduccion) |

Nota sobre alcance: los cuatro protocolos son de comercio entre agente y comercio o de pagos por API; ninguno cubre el caso "factura de proveedor con cuenta bancaria cambiante". AP2 es el unico leido que define monto, presupuesto, beneficiarios permitidos y recibos firmados, y sirve como modelo de datos.

---

## Que cambia para nuestro proyecto

1. Posicionamiento: no competir con la extraccion o codificacion de Ramp, Bill o Tipalti. El hueco es una decision firmada y auditable: cada pagar/frenar/escalar emite un registro firmado con la regla evaluada y su version, algo que no se encontro documentado en ningun producto leido.
2. Modelo de datos: tomar de AP2 los conceptos de restriccion abierta (rango de monto, presupuesto, beneficiarios permitidos, recurrencia), verificacion en codigo determinista y recibo firmado, adaptados a factura de proveedor. No depender de AP2 como protocolo de transporte (es de comercio) y declararlo asi.
3. Regla dura para cambios bancarios: toda factura con cuenta nueva o distinta a la registrada va a escalar, nunca a pagar; la decision la toma codigo determinista, no el modelo. Esto sigue la recomendacion IC3 (llamada a numero conocido, demora, segundo visto bueno) y la defensa del articulo A2AS (confirmacion humana para cuentas bancarias). La cifra para el pitch es US$3.046.598.558 y 24.768 quejas BEC en 2025 (IC3).
4. Entradas y fiscalidad: leer la factura electronica oficial (CFDI, DTE, UBL de Colombia y Peru, NF-e) como fuente estructurada, y contrastar con la consulta publica donde se confirmo (Colombia por CUFE, Peru por consulta de validez). Tratar el contenido libre de la factura como no confiable (instruccion oculta). Incluir en las reglas la lista de documentos del beneficiario (W-8BEN, W-8BEN-E o W-9) y pasar a persona los casos con dudas de retencion en lugar de decidirlos.
5. Integracion con Blinka: su sitio publico no muestra API ni agentes, asi que el prototipo debe simular la orden de pago (formato propio, con rutas y monedas reales de Blinka: SPEI, Pix, Bre-B, USDC) y plantear la integracion como propuesta, sin afirmar que existe una API. Preguntar a Blinka en el hackathon si hay una API privada.

## Lo que no se pudo verificar

- Verificacion de cambio de cuenta bancaria en Stampli, BILL, Tipalti y Brex; productos de Airbase (no investigado); alcance real del MCP oficial de Mercury.
- Que algun producto de AP ofrezca ordenes de pago firmadas o prueba de cumplimiento de reglas (no se hallo; es ausencia de evidencia).
- Casos reales documentados de inyeccion de instrucciones en facturas con fuente primaria (solo el escenario de A2AS y un benchmark general de PDFs).
- "Periodo de enfriamiento" como control IC3 con plazo definido; la segunda aprobacion de la PSA 2015 solo se leyo en resumen.
- Mexico: herramienta publica de consulta de CFDI para terceros; Brasil: consulta publica de NF-e; Chile: consulta de autenticidad del DTE; Argentina: constatacion de comprobantes; vigencia del anexo tecnico DIAN posterior a v1.8; PDFs oficiales de gov.br/nfse y del SAT (no se abrieron).
- Conflicto no resuelto en una pagina de SUNAT sobre validez tributaria de "Aceptada".
- Costo B2B transfronterizo en LatAm con fuente independiente (BIS, CEPAL, BID): no se hallo; las cifras de Mastercard y Flywire son de proveedores de pagos. Cifras del Banco Mundial (6,36%) leidas via buscador porque la pagina dio 403.
- Regla textual del IRS sobre contratistas independientes pagados por trabajo fuera de EE. UU. (se leyo solo la parte de Pub. 515 sobre salarios y fuente; el resto de la publicacion no se leyo completo).
- Mastercard "Verifiable Intent" y la pagina de Agent Pay (404); documentacion publica de API o agentes de Blinka (no existe en lo leido).
- AP2: no se leyeron en detalle checkout_mandate.md, flows.md e implementation_considerations.md.
