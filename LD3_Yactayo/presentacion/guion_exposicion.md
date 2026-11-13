# Guion de exposición — LD3 IGBT

**Expositor:** Leonardo Sait Yactayo Tolentino · **Fecha:** 21 de octubre de 2026  
**Duración estimada:** 6–8 minutos, más preguntas.

## Diapositiva 1 — Presentación (25 s)

“Buenos días, profesora. Soy Leonardo Yactayo y voy a presentar el Laboratorio Dirigido número 3, sobre la caracterización y simulación comparativa de transistores IGBT en LTspice. Me enfocaré en el apagado, la corriente de cola y dos decisiones de diseño: la inductancia del circuito y la resistencia de compuerta.”

## Diapositiva 2 — Fundamento y metodología (60 s)

“El IGBT combina una compuerta MOS con conducción bipolar. Al encenderse, los portadores inyectados en la región de deriva reducen la caída en conducción. Al apagar, el canal de compuerta se cierra, pero queda carga almacenada en esa región; su extracción y recombinación prolongan la corriente de cola.

Para observar la conmutación utilicé el ensayo de doble pulso: el primer pulso establece corriente en el inductor y el segundo permite analizar el apagado. Los bancos Duncan N y P se evaluaron a 400 voltios, 100 microhenrios y RG de 10 ohmios, a 27 grados y con inductancia de lazo ideal. En Fuji mantuve el bus y la carga, e incorporé 25 nanohenrios de inductancia parásita a 25 grados. Las polaridades de compuerta y del bus se invierten para el caso P.”

## Diapositiva 3 — Resultados Duncan N/P (60–70 s)

“Aquí se muestran las tres señales del banco: VGE, VCE e IC. El N-IGBT nominal opera a 19 amperios y el P-IGBT a 40 amperios. En esas condiciones, los resultados de caída en conducción fueron 1,88 y 2,51 voltios, respectivamente; las energías de apagado integradas fueron 691,5 y 2115,3 microjulios.

Estas condiciones nominales no tienen la misma corriente, así que no las presento como una comparación N/P a corriente igualada. El informe también conserva un control P a 19,48 amperios: la corriente, la caída en conducción y la energía están respaldadas por el log, pero sus métricas dinámicas no se consideran verificadas porque no se conservó el RAW. Tampoco atribuyo la diferencia únicamente a la movilidad: son macromodelos distintos, con parámetros internos distintos.”

## Diapositiva 4 — Retardo, energía y cola (65–75 s)

“El retardo se midió entre el cruce del 90 por ciento de VGE y el 90 por ciento de IC. Los cursores reales de LTspice dan 150,81 nanosegundos para N y 194,37 para P. Para P, el cálculo automatizado del log da 194,57 nanosegundos; por eso distingo la lectura manual de la medición automatizada.

La integración gráfica de LTspice da 691,48 microjulios para el apagado de N. Es energía eléctrica integrada según el método del banco; no equivale directamente al calor interno del chip. En este ensayo Duncan se integra VCE por la corriente del shunt de emisor, que también contiene la componente de compuerta. La curva ayuda a ver la cola: una vez que cae la corriente principal, todavía persiste una corriente menor por los portadores almacenados.”

## Diapositiva 5 — Fuji y diodo co-pack (55–65 s)

“En la familia Fuji incluí una inductancia de lazo de 25 nanohenrios. Con 50 amperios, el pico VCE fue 442,36 voltios, es decir, 42,36 por encima del bus. A 75 amperios llegó a 445,98 voltios, 45,98 por encima. La relación inductiva V igual a L por di/dt explica por qué la pendiente de corriente influye en ese pico.

En este ensayo de lado bajo, las trazas discreta y co-pack casi coinciden. Durante el apagado del interruptor, el diodo integrado queda polarizado en inversa y la rueda libre circula por el diodo superior D1. En una rama de medio puente, el diodo co-pack sí puede conducir la corriente reactiva cuando conmuta el dispositivo opuesto.”

## Diapositiva 6 — Área de chip y RG (65–75 s)

“Primero comparo F01 y F05 a la misma corriente de 50 amperios. El chip de 75 amperios baja VCE en conducción de 1,362 a 1,181 voltios, pero Eoff sube 28,2 por ciento. Es un compromiso entre área, conducción y carga de conmutación; no tomo CGE y Cies como si fueran la misma magnitud.

Luego comparo F02 y F06, ambos a 50 amperios, duplicando RG de 10 a 20 ohmios. El pico sobre el bus baja de 42,36 a 25,94 voltios, una reducción de 38,8 por ciento. A cambio, Eoff aumenta 70,5 por ciento. La compuerta más lenta reduce di/dt y la sobretensión, pero alarga la transición y eleva la energía integrada.”

## Diapositiva 7 — Conclusiones (45–55 s)

“Me quedo con cuatro ideas. Primero, el cierre del canal MOS no elimina de inmediato la corriente: la carga almacenada explica la cola. Segundo, las cifras dependen de la corriente, del modelo y de la topología, así que hay que respetar las condiciones de cada comparación y el estado de verificación. Tercero, la inductancia de lazo y el co-pack muestran que el resultado depende del circuito. Cuarto, el diseño debe equilibrar caída en conducción, sobretensión y energía de apagado; RG permite controlar el pico, pero existe un costo energético medido.”

## Diapositiva 8 — Cierre (10 s)

“Con esto termino mi exposición. Muchas gracias, profesora.”

## Preguntas técnicas posibles

**1. ¿Por qué aparece corriente de cola si la compuerta ya apagó el IGBT?**  
Porque al cerrarse el canal MOS todavía quedan portadores minoritarios almacenados en la región de deriva. Su extracción y recombinación tardan más que el cierre del canal y sostienen la cola de corriente.

**2. ¿Se puede concluir que el P-IGBT es más lento que el N-IGBT?**  
No con una comparación directa de los nominales: se ensayaron a 40 A y 19 A, respectivamente. El control P a 19,48 A respalda valores estáticos y Eoff en el log, pero las métricas dinámicas no están verificadas sin el RAW. Además, las tarjetas Duncan son macromodelos diferentes; el resultado no aísla la movilidad como causa. CGE tampoco debe confundirse con Cies.

**3. ¿Eoff es el calor disipado dentro del chip?**  
No necesariamente. Es la integral eléctrica operacional durante la ventana de apagado y depende de cómo se mide la corriente en cada banco. Sin un modelo térmico y un balance de energía interno, no equivale directamente al calor del silicio.

**4. ¿Por qué el diodo co-pack casi no cambia el resultado en el DPT de lado bajo?**  
Durante el apagado del transistor bajo, VCE sube y el diodo antiparalelo queda polarizado en inversa. En este circuito la corriente inductiva recircula por D1. El co-pack puede ser relevante como rueda libre en una topología de puente cuando conduce la rama opuesta.

**5. ¿Qué implica duplicar RG?**  
En F02/F06, pasar de 10 a 20 ohmios reduce la sobretensión sobre el bus de 42,36 a 25,94 V, pero aumenta Eoff 70,5 por ciento. Es una elección entre limitar di/dt y sobretensión o reducir la energía y el tiempo de conmutación.
