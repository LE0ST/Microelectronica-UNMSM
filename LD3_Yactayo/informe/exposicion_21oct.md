# GUION TÉCNICO Y DIAPOSITIVAS DE SUSTENTACIÓN ORAL (21/10/2026)
## LABORATORIO DIRIGIDO N.° 3: CARACTERIZACIÓN Y SIMULACIÓN DE TRANSISTORES IGBT

* **Expositor / Autor:** Leonardo Sait Yactayo Tolentino (`23190214`)  
* **Modalidad:** Individual  
* **Asignatura:** Microelectrónica y Sistemas Nanoelectrónicos — Semestre 2026-II  
* **Docente:** MsC. Luz Adanaqué Infante  
* **Institución:** Facultad de Ingeniería Electrónica y Eléctrica (FIEE) — UNMSM  
* **Fecha de Exposición:** **21 de octubre de 2026**  
* **Duración Prevista:** 12 a 15 minutos de presentación + ronda de preguntas  
* **Requisito Oficial Asociado:** Acápite 1 y Requisito `[REQ-EXP]` de la guía oficial.

---

## 1. Esquema Temporal de la Exposición

| Bloque | Tema | Tiempo Sugerido | Apoyo Visual |
|:---:|:---|:---:|:---:|
| **Bloque 1** | Portada, Objetivos y Arquitectura del Banco DPT | $2\text{ min}$ | Diapositivas 1 y 2 |
| **Bloque 2** | Parte I: Comparativa Canal N vs Canal P (Macromodelos Duncan) | $3.5\text{ min}$ | Diapositivas 3 y 4 (Fig. 1 a 5) |
| **Bloque 3** | Parte II: Módulos Fuji Serie X y Diodo Co-Pack | $3\text{ min}$ | Diapositivas 5 y 6 (Fig. 6 y 7) |
| **Bloque 4** | Escalamiento de Área (50 A vs 75 A) y Sensibilidad $R_G$ | $3.5\text{ min}$ | Diapositivas 7 y 8 (Fig. 8 y 9) |
| **Bloque 5** | Síntesis de Conclusiones Físicas y Lecciones de Simulación | $2\text{ min}$ | Diapositiva 9 |

---

## 2. Guion Detallado Diapositiva por Diapositiva

### Diapositiva 1 — Portada y Metadatos
* **Título:** Caracterización y Simulación Comparativa de Transistores IGBT en LTspice.
* **Expositor:** Leonardo Sait Yactayo Tolentino (Código `23190214`).
* **Mensaje de Apertura:** «Buenos días, profesora Luz Adanaqué y compañeros. En esta experiencia de laboratorio dirigida individual, nos enfocamos en el comportamiento físico y dinámico de transistores IGBT bajo la técnica de ensayo de doble pulso (DPT), comparando dispositivos de canal N frente a canal P, y caracterizando módulos de potencia comerciales de séptima generación de Fuji Electric Serie X.»

### Diapositiva 2 — Metodología de Ensayo Double Pulse Test (DPT) e Instrumentación
* **Concepto:** Técnica estándar de la industria (IEC 60747-9) para evaluar pérdidas dinámicas en inductancia pura ($100\ \mu\text{H}$) sin calentamiento térmico acumulativo.
* **Aspectos Críticos de Instrumentación en SPICE:**
  * Uso de sensores ideales de $0\text{ V}$ (`Vsens_C`, `Vsens_G`, `Vsens_E`) para aislar la corriente terminal de colector de la corriente de compuerta ($I_G$).
  * Calibración rigurosa de pulsos para lograr exactamente la corriente nominal pre-apagado ($\pm 1\%$).
  * Inclusión de inductancia parásita de lazo de conmutación ($L_\sigma = 25\text{ nH}$) para medir la sobretensión real $V_{CE,\text{peak}}$.
  * Método Gear con paso máximo de $1.0\text{ ns}$ para evitar oscilaciones espurias de fuentes `LIMIT`.

### Diapositiva 3 — Parte I: Canal N vs Canal P (Hallazgos EXP-01 a EXP-05)
* **Gráficas Clave:** Figuras 1, 2 y 3 (Formas de onda y corriente de cola).
* **Argumentación Física:**
  * A corriente nominal ($19\text{ A}$ en N vs $40\text{ A}$ en P), el N-IGBT conmuta mucho más rápido ($t_{d(\text{off})} = 150.8\text{ ns}$, $t_f = 185.2\text{ ns}$) que el P-IGBT ($t_{d(\text{off})} = 194.6\text{ ns}$, $t_f = 268.4\text{ ns}$).
  * **Ensayo de Control a $19\text{ A}$ Idénticos:** A la misma corriente, el P-IGBT es un $40.7\%$ más lento en $t_d$, $43.8\%$ más lento en $t_f$ y disipa $46.3\%$ más energía ($1011.8\ \mu\text{J}$ vs $691.5\ \mu\text{J}$).
  * **Causa Física:** Asimetría de movilidad de portadores ($\mu_n \approx 1400$ vs $\mu_p \approx 450\text{ cm}^2/\text{V}\cdot\text{s}$). El P-IGBT tiene canal MOS de huecos y requiere mayor área y capacitancia, acumulando más carga en su base de deriva.

### Diapositiva 4 — Corriente de Cola y Discrepancias frente a Hojas de Datos
* **Gráficas Clave:** Figuras 4 y 5 (Medición de cursores e integración de energía).
* **Física de la Corriente de Cola:** Explicar las dos fases del apagado: corte rápido del canal MOS seguido de la recombinación asintótica lenta de portadores minoritarios en la base flotante del BJT de salida ($i_{\text{tail}} \propto e^{-t/\tau}$).
* **Cotejo con Datasheet IRGBC20S:** Explicar con honestidad por qué en SPICE se obtuvo $150.8\text{ ns}$ frente a los $820\text{ ns}$ del catálogo Farnell 68617:
  * El catálogo oficial utiliza $R_G = 50\ \Omega$ y $V_{bus} = 480\text{ V}$.
  * El circuito de laboratorio usa $R_G = 10\ \Omega$ (descarga $5\times$ más rápida).
  * El macromodelo Duncan parametriza $TF = 16.8\text{ ns}$, modelando un dispositivo más veloz que el silicio estándar físico.

### Diapositiva 5 — Parte II: Módulos Fuji Serie X y Diodo Co-Pack (EXP-06 y EXP-07)
* **Gráficas Clave:** Figuras 6 y 7 (Comparativas Discreto vs Co-Pack en 50 A y 75 A).
* **Hallazgo Contraintuitivo y su Justificación Física:**
  * Las formas de onda con y sin diodo integrado son cuantitativamente idénticas en el interruptor bajo prueba ($V_{CE,\text{peak}} = 442.36\text{ V}$ en ambos casos a 50 A; $445.98\text{ V}$ a 75 A).
  * **¿Por qué?** En el banco DPT de lado bajo, el diodo co-pack está conectado en antiparalelo con ánodo a tierra y cátodo al colector. Durante todo el apagado, $V_{AK} = -V_{CE} < 0$, por lo que **está en polarización inversa permanente**. La libre circulación la realiza el diodo superior $D_1$.
  * **Aporte Técnico:** Aclarar que en convertidores de medio puente (inversores), el diodo co-pack superior sí conduce cuando conmuta el switch inferior, cumpliendo allí su rol de protección bidireccional.

### Diapositiva 6 — Escalamiento de Área de Silicio (50 A vs 75 A, EXP-08)
* **Gráfica Clave:** Figura 8 (Dinámica de tensión y corriente en 50 A chip vs 75 A chip).
* **El Compromiso Estático vs Dinámico:**
  * **Comparación a corriente igualada ($50\text{ A}$, F01 vs F05):** El chip de 75 A reduce la caída de conducción $V_{CE(\text{on})}$ de $1.362\text{ V}$ a **$1.181\text{ V}$ ($-13.3\%$ en pérdidas de conducción)** gracias a su mayor transconductancia MOS ($KP = 9.0$ vs $4.5\text{ A/V}^2$) y menor resistencia óhmica.
  * **Costo Dinámico:** Sus mayores capacitancias ($C_{ies} = 9.5\text{ nF}$ vs $6.77\text{ nF}$, $C_{res} = 6.7\text{ nF}$ vs $4.0\text{ nF}$) incrementan $t_{d(\text{off})}$ en **$+40.5\%$** y la energía de apagado $E_{\text{off}}$ en **$+28.2\%$ ($1067\ \mu\text{J} \to 1368\ \mu\text{J}$)**.

### Diapositiva 7 — Sensibilidad a la Resistencia de Compuerta (EXP-09)
* **Gráfica Clave:** Figura 9 (Sensibilidad $R_G = 10\ \Omega$ vs $20\ \Omega$).
* **El Trade-off Clásico de Conmutación:**
  * Al duplicar $R_G$ a $20\ \Omega$, la tasa de caída $|di/dt|_{\text{max}}$ se amortigua de $1670\text{ A}/\mu\text{s}$ a **$1019\text{ A}/\mu\text{s}$ ($-38.9\%$)**.
  * **Beneficio:** La sobretensión inducida por la inductancia de lazo ($L_\sigma \cdot di/dt$) se reduce de $+42.36\text{ V}$ a **$+25.94\text{ V}$ ($-38.8\%$ de sobretensión)**, reduciendo el pico absoluto de $442.36\text{ V}$ a $425.94\text{ V}$.
  * **Penalización:** La energía disipada de apagado se dispara de $1066.98\ \mu\text{J}$ a **$1818.73\ \mu\text{J}$ (+70.5%)**.

### Diapositiva 8 — Síntesis de Conclusiones y Respuestas a la Guía
* Síntesis de los 4 ejes: Portadores (N vs P), Diodo Co-Pack, Escalamiento de Área y Sintonización de $R_G$.
* Cumplimiento del 100% de la guía oficial en modalidad individual.

---

## 3. Banco de Preguntas Anticipadas de la Docente y Respuestas Físicas

* **P1: ¿Por qué midió la corriente con sensores de 0 V en lugar de usar directamente la corriente del shunt de emisor?**
  * *R:* «Porque en el emisor la corriente $I_E(t) = I_C(t) + I_G(t)$ incluye la corriente capacitiva de compuerta. Durante el flanco de apagado rápido, la descarga de $C_{iss}$ inyecta picos negativos de corriente de compuerta de más de $1\text{ A}$, lo que falseaba la corriente de colector en el shunt y subestimaba la energía de apagado $E_{\text{off}}$ en casi un $3\%$. El sensor de 0 V en colector aísla estrictamente el puerto colector-emisor.»
* **P2: ¿Por qué el diodo co-pack no redujo el sobreimpulso en su simulación?**
  * *R:* «Porque en el banco DPT de un solo interruptor de lado bajo, el diodo co-pack está conectado en antiparalelo con ánodo al emisor y cátodo al colector. Al conmutar el switch, el colector sube a 442 V, polarizando al diodo en inversa. El diodo no conduce corriente directa; la fijación inductiva la realiza el diodo superior $D_1$. El diodo co-pack opera en convertidores de puente completo cuando conmuta el interruptor opuesto.»
* **P3: ¿Qué ventaja tiene usar un IGBT de 75 A si se opera únicamente a 50 A?**
  * *R:* «Reduce las pérdidas estáticas de conducción en un $13.3\%$ ($V_{CE(\text{on})}$ baja de $1.36\text{ V}$ a $1.18\text{ V}$), lo cual es muy ventajoso en aplicaciones de baja frecuencia de conmutación ($\le 5\text{ kHz}$) donde predominan las pérdidas de conducción sobre las de conmutación. En alta frecuencia, la penalización del $28\%$ en $E_{\text{off}}$ degradaría el rendimiento térmico global.»
