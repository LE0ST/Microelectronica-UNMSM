# Modelos Tecnologicos PTM para LD2 (modelos/)

Este directorio contiene los modelos predictivos BSIM4 (PTM) utilizados a lo largo del Laboratorio Dirigido N. 2, siguiendo estrictamente el requerimiento de la Seccion 4.1 de la guia oficial LabDirigido2.pdf.

---

## 1. Regla de Prevencion de Colisiones (Seccion 4.1 de la Guia)

En SPICE, todas las tarjetas PTM originales declaran sus modelos como genericos:
\\spice
.model  nmos  nmos  level = 54
.model  pmos  pmos  level = 54
\Si se incluyen dos archivos originales en la misma simulacion (por ejemplo, para comparar 45nm HP frente a 45nm LP o 130nm), la ultima definicion sobreescribe silenciosamente a la primera. Por tal motivo, la guia impone como **obligatorio** el renombrado de modelos a archivos \.lib\.

---

## 2. Modelos Generados y Mapeo de Nombres

| Archivo Original (\modelos/originales/\) | Archivo Renombrado (\modelos/\) | Nombre Modelo NMOS | Nombre Modelo PMOS | Nivel BSIM4 |
| :--- | :--- | :--- | :--- | :---: |
| %nm_HP.pm\ | \ptm45hp.lib\ | mos_45hp\ | \pmos_45hp\ | 54 |
| %nm_LP.pm\ | \ptm45lp.lib\ | mos_45lp\ | \pmos_45lp\ | 54 |
| Xnm_bulk.pm\ | \ptm130.lib\ | mos_130\ | \pmos_130\ | 54 |

### Transformacion Aplicada
Equivalente a los comandos sed estipulados en la Seccion 4.1:
\\ash
sed -e 's/^\.model  *nmos  *nmos/.model nmos_45hp nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_45hp pmos/' 45nm_HP.pm > ptm45hp.lib

sed -e 's/^\.model  *nmos  *nmos/.model nmos_45lp nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_45lp pmos/' 45nm_LP.pm > ptm45lp.lib

sed -e 's/^\.model  *nmos  *nmos/.model nmos_130 nmos/' \
    -e 's/^\.model  *pmos  *pmos/.model pmos_130 pmos/' 130nm_bulk.pm > ptm130.lib
\
### Verificacion de Modelos Unicos (grep '^.model')
Ejecutado sobre los archivos generados:
\ptm45hp.lib: .model nmos_45hp nmos  level = 54
ptm45hp.lib: .model pmos_45hp pmos  level = 54
ptm45lp.lib: .model nmos_45lp nmos  level = 54
ptm45lp.lib: .model pmos_45lp pmos  level = 54
ptm130.lib: .model nmos_130 nmos  level = 54
ptm130.lib: .model pmos_130 pmos  level = 54
\Resultado: **6 modelos independientes y distintos**, garantizando cero colisiones.

---

## 3. Verificacion de Parametros Clave (Tabla 4.2 de la Guia vs. Archivos Reales)

| Parametro | Guia: 45nm HP | Archivo: 45nm HP | Guia: 45nm LP | Archivo: 45nm LP | Guia: 130nm | Archivo: 130nm | Concordancia |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| VDD nominal | 1.0 V | (En netlist) | 1.1 V | (En netlist) | 1.3 V | (En netlist) | Si |
| Vth0 NMOS | 0.469 V | 0.46893 V | 0.623 V | 0.62261 V | 0.378 V | 0.3782 V | Si |
| Vth0 PMOS | -0.492 V | -0.49158 V | -0.587 V | -0.58700 V | -0.321 V | -0.3210 V | Si |
| toxe NMOS | 1.25 nm | 1.25e-9 m | 1.80 nm | 1.80e-9 m | 2.25 nm | 2.25e-9 m | Si |
| u0 NMOS (m^2/V*s) | 0.054 | 0.054 | 0.049 | 0.049 | 0.059 | 0.05928 | Si |
| u0 PMOS (m^2/V*s) | 0.020 | 0.020 | 0.021 | 0.021 | 0.0084 | 0.00835 | Si |
| vsat NMOS (m/s) | 1.7e5 | 170000 | 1.3e5 | 130000 | 1.0e5 | 100370 | Si |
| nfactor NMOS | 2.22 | 2.22 | 1.60 | 1.60 | 1.50 | 1.50 | Si |
| Lminima | 45 nm | 45 nm | 45 nm | 45 nm | 130 nm | 130 nm | Si |

### Parametros Adicionales Extraidos para Calculos Analiticos
* **Capacitancias de union drenador/fuente (Actividad 2):**
  * cjd = cjs = 0.0005 F/m^2 = 0.5 fF/um^2 (45nm HP)
  * cjswd = cjsws = 5e-10 F/m = 0.5 fF/um (45nm HP)
  * cjswgd = cjswgs = 5e-10 F/m = 0.5 fF/um (45nm HP)
* **Capacitancia de solapamiento compuerta-drenador (Actividad 5):**
  * cgdo = 1.1e-10 F/m = 0.11 fF/um (45nm HP y LP)
  * cgdo = 2.4e-10 F/m = 0.24 fF/um (130nm bulk)
* **Parametros de fuga subumbral:**
  * voff = -0.13 V (NMOS HP/LP/130nm)
  * eta0 = 0.0055 (45nm HP), 0.0125 (45nm LP), 0.0092 (130nm)
