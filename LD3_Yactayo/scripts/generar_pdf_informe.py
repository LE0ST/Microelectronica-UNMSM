# -*- coding: utf-8 -*-
"""
generar_pdf_informe.py
Generador integral del informe de laboratorio en LaTeX y compilación a PDF para LD3.
Autor: Leonardo Sait Yactayo Tolentino (23190214)
UNMSM - FIEE | Microelectrónica y Sistemas Nanoelectrónicos (2026-II)
Docente: MsC. Luz Adanaqué Infante
"""

import os
import subprocess

tex_content = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noshorthands,es-tabla,es-nodecimaldot]{babel}
\usepackage{lmodern}

\usepackage[a4paper,top=1.8cm,bottom=1.8cm,left=1.8cm,right=1.8cm,
            headheight=18pt,footskip=0.75cm]{geometry}

\usepackage{amsmath,amssymb}
\usepackage{bm}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage[most]{tcolorbox}
\usepackage{hyperref}
\usepackage[section]{placeins}
\usepackage{needspace}
\usepackage{pdflscape}
\usepackage{subcaption}

% Optimización de colocación de flotantes para evitar páginas vacías
\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.88}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.68}
\setcounter{totalnumber}{6}
\setcounter{topnumber}{4}
\setcounter{bottomnumber}{4}
\setlength{\floatsep}{6pt plus 2pt minus 2pt}
\setlength{\textfloatsep}{10pt plus 2pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}

\definecolor{navy}{HTML}{1E2761}
\definecolor{coral}{HTML}{C0392B}
\definecolor{grisclaro}{HTML}{F8F9FA}
\definecolor{bordegris}{HTML}{BDC3C7}

\hypersetup{
  colorlinks=true,
  linkcolor=navy,
  urlcolor=coral,
  citecolor=navy,
  pdftitle={Informe de Laboratorio Dirigido Nro. 3 - Transistores IGBT},
  pdfauthor={Leonardo Sait Yactayo Tolentino - UNMSM FIEE}
}

% Encabezados y pies de página simplificados y académicos
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\color{navy}\textbf{UNMSM -- FIEE} \textbar\ Microelectrónica y Sistemas Nanoelectrónicos}
\fancyhead[R]{\footnotesize\color{navy}Laboratorio Dirigido N.\textsuperscript{o} 3: Transistores IGBT}
\fancyfoot[C]{\footnotesize\color{navy}\thepage}
\renewcommand{\headrulewidth}{0.6pt}
\renewcommand{\footrulewidth}{0.0pt}

% Estilo limpio para páginas apaisadas (sin choque de líneas verticales)
\fancypagestyle{landscapestyle}{
  \fancyhf{}
  \fancyfoot[C]{\footnotesize\color{navy}\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

\titleformat{\section}{\large\bfseries\color{navy}}{\thesection.}{0.5em}{}[\vspace{-2pt}\rule{\textwidth}{0.6pt}\vspace{-4pt}]
\titleformat{\subsection}{\normalsize\bfseries\color{navy}}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\small\bfseries\color{navy}}{\thesubsubsection.}{0.5em}{}
\titlespacing*{\section}{0pt}{9pt plus 2pt minus 2pt}{4pt plus 1pt minus 1pt}
\titlespacing*{\subsection}{0pt}{6pt plus 2pt minus 1pt}{3pt plus 1pt minus 1pt}
\titlespacing*{\subsubsection}{0pt}{4pt plus 1pt minus 1pt}{2pt plus 1pt minus 1pt}

\newtcolorbox{cuadronota}[1][]{
  colback=grisclaro,
  colframe=navy,
  fonttitle=\bfseries\footnotesize\color{white},
  coltitle=white,
  colbacktitle=navy,
  enhanced,
  attach boxed title to top left={yshift=-2mm,xshift=4mm},
  title={#1},
  arc=1.5mm,
  boxrule=0.8pt,
  top=2.5mm,
  bottom=2mm,
  left=3mm,
  right=3mm
}

\begin{document}

% ------------------- ENCABEZADO INSTITUCIONAL / PORTADA -------------------
\begin{center}
  {\large\scshape\bfseries Universidad Nacional Mayor de San Marcos}\\[1pt]
  {\small (Universidad del Perú, Decana de América)}\\[1pt]
  {\normalsize\bfseries Facultad de Ingeniería Electrónica y Eléctrica}\\[2pt]
  {\footnotesize Escuela Profesional de Ingeniería Electrónica}\\[5pt]
  \hrule height 1.2pt \vspace{4pt}
  {\Large\bfseries\color{navy} INFORME DE LABORATORIO DIRIGIDO N.\textsuperscript{o} 3}\\[3pt]
  {\large\bfseries\color{coral} Caracterización y Simulación Comparativa de Transistores IGBT en LTspice}\\[4pt]
  \hrule height 0.8pt \vspace{6pt}
  
  \begin{tabular}{@{}p{2.3cm} p{5.6cm} p{4.9cm} p{4.5cm}@{}}
    \textbf{Asignatura:} & \multicolumn{3}{l}{Microelectrónica y Sistemas Nanoelectrónicos (Semestre 2026-II)} \\
    \textbf{Docente:} & MsC. Luz Adanaqué Infante & \textbf{Emisión de la guía:} & 7 de octubre de 2026 \\
    \textbf{Estudiante:} & Leonardo Sait Yactayo Tolentino & \textbf{Código:} & 23190214 \\
    \textbf{Modalidad:} & Individual & \textbf{Exposición:} & 21 de octubre de 2026 \\
    \textbf{Herramienta:} & LTspice 26.0 (Entorno SPICE) & \textbf{Metodología:} & Doble Pulso (DPT) \\
  \end{tabular}
\end{center}

\vspace{-4pt}

% ------------------- RESUMEN -------------------
\section{Resumen y Datos Generales}
El presente informe documenta el desarrollo experimental y analítico del \textbf{Laboratorio Dirigido N.\textsuperscript{o} 3}, dedicado al estudio del comportamiento transitorio y físico de transistores bipolares de compuerta aislada (IGBT) mediante el método de ensayo de doble pulso (\textit{Double Pulse Test}, DPT) en el simulador LTspice 26.0, conforme a las directivas de la guía oficial de laboratorio de la profesora MsC. Luz Adanaqué Infante (emitida el 7 de octubre de 2026, con exposición programada para el 21 de octubre de 2026).

La experiencia se desarrolló en dos fases complementarias:
\begin{enumerate}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Parte I (Comparación entre canales N y P):} Se implementaron los circuitos DPT para el N-IGBT (\texttt{XIRGBC20S}, $600\text{ V}, 19\text{ A}$) y el P-IGBT (\texttt{XPIGBT}, $600\text{ V}, 40\text{ A}$) utilizando los macromodelos conductuales de Duncan Electronics. Se midieron en simulación las formas de onda $V_{GE}, V_{CE}, I_C$, el tiempo de retardo de apagado ($t_{d(\text{off})}$) mediante cursores en LTspice, el tiempo de caída ($t_f$), la corriente de cola (\textit{tail current}) y la energía de apagado ($E_{\text{off}}$) por integración directa de potencia, contrastando las observaciones con la hoja de datos del fabricante (IRGBC20S).
  \item \textbf{Parte II (Módulos comerciales Fuji Electric Serie X):} Se caracterizó una serie de cuatro modelos \textit{Trench Field-Stop} de 7.\textsuperscript{a} generación a $650\text{ V}$ en configuraciones discretas y co-empaquetadas (\textit{Co-Pack}): \texttt{FGW50XS65} y \texttt{FGW50XS65C} ($50\text{ A}$), y \texttt{FGW75XS65} y \texttt{FGW75XS65C} ($75\text{ A}$). Se evaluó la sobretensión inductiva ($V_{CE,\text{peak}}$) ante una inductancia de lazo $L_\sigma = 25\text{ nH}$, el rol circuital del diodo co-pack en topología de lado bajo, el compromiso entre pérdidas estáticas y dinámicas al variar el tamaño del chip, y la sensibilidad al duplicar la resistencia de compuerta ($R_G = 10\ \Omega \to 20\ \Omega$).
\end{enumerate}
Se integran las capturas directas de pantalla obtenidas en la interfaz de LTspice (esquemas, formas de onda, cursores e integrales), preservando la evidencia auténtica de simulación.

% ------------------- INTRODUCCIÓN Y MARCO TEÓRICO -------------------
\section{Introducción y Fundamento Teórico}

\subsection{Estructura Interna del Transistor IGBT}
El transistor IGBT combina la alta impedancia de entrada y facilidad de control por tensión de un MOSFET con la baja caída de tensión en saturación y alta densidad de corriente de un transistor bipolar de unión (BJT). Físicamente, un N-IGBT vertical consta de cuatro capas alternadas ($P^+ - N^- - P - N^+$): el substrato inferior $P^+$ actúa como inyector de colector; la región intermedia $N^-$, ancha y de bajo dopado, es la región de deriva que soporta la tensión de bloqueo; el cuerpo $P$ aloja el canal de inversión inducido por la compuerta aislada; y la difusión $N^+$ conforma el emisor.

\subsection{Modulación de Conductividad}
En un MOSFET de alta tensión, la resistencia de la región de deriva ($R_{DS(\text{on})}$) crece intensamente con la tensión de ruptura. En el IGBT, cuando la compuerta supera la tensión de umbral ($V_{GE} > V_{th}$), el canal MOS conduce electrones hacia la base $N^-$. Esto polariza en directa la unión $P^+ / N^-$ inferior, inyectando una densidad masiva de huecos (minoritarios) en la región de deriva. Para preservar la neutralidad de carga, se acumulan electrones en igual proporción. Esta inundación de portadores eleva la densidad libre ($p \approx n \gg N_D^-$) varios órdenes de magnitud sobre el dopado térmico, provocando el colapso de la resistencia óhmica de la región de deriva. Este fenómeno, denominado \textbf{modulación de conductividad}, permite caídas de tensión de saturación de apenas $1.3\text{ V} - 2.0\text{ V}$ incluso a corrientes de decenas de amperios.

\subsection{Asimetría de Conducción: Canal N frente a Canal P}
En el silicio, la movilidad de los electrones ($\mu_n \approx 1400\text{ cm}^2/\text{V}\cdot\text{s}$) es aproximadamente el triple de la movilidad de los huecos ($\mu_p \approx 450\text{ cm}^2/\text{V}\cdot\text{s}$). 
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{N-IGBT:} El canal MOSFET de control es de electrones (alta movilidad) y excita la base de un BJT PNP de salida.
  \item \textbf{P-IGBT:} El canal de control es de huecos (baja movilidad) y excita un BJT NPN con región de deriva $P^-$.
\end{itemize}
En el silicio, la menor movilidad de los huecos impone una mayor resistencia específica para una misma área, lo cual influye en el dimensionamiento del canal y de la región de deriva. No obstante, debe evitarse asociar automáticamente la movilidad con la velocidad de recombinación, la cual depende del tiempo de vida medio y de la densidad de centros de recombinación. En la simulación circuital SPICE, las diferencias transitorias observadas entre modelos responden fundamentalmente a la formulación paramétrica de cada subcircuito (capacitancias internas, tiempos de tránsito y topología equivalente), más que a un efecto microscópico aislado de transporte.

\subsection{Mecanismo de Apagado y Corriente de Cola (\textit{Tail Current})}
Durante el corte con carga inductiva en el ensayo DPT, la eliminación de portadores de carga transcurre en dos fases físicas diferenciadas:
\begin{enumerate}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Extinción del canal MOS y extracción activa por campo eléctrico (\textit{sweep-out}):} Al descender $V_{GE}$ por debajo de la tensión de umbral $V_{th}$, el canal de inversión se cierra rápidamente ($\sim 20-40\text{ ns}$), interrumpiendo la corriente de electrones. Al elevarse bruscamente la tensión $V_{CE}$ ($dv/dt$ elevado), la región de carga espacial en la unión $P\text{-cuerpo} / N^-\text{-deriva}$ se expande velozmente hacia la base $N^-$, barriendo activamente los portadores móviles libres en la zona desértica.
  \item \textbf{Recombinación espontánea en la base neutra remanente:} Una vez que $V_{CE}$ alcanza la tensión total de bus ($V_{bus} = 400\text{ V}$) y $dv/dt \approx 0$, la expansión de la zona de carga espacial se detiene. El exceso de portadores minoritarios (huecos) atrapados en la región de deriva neutra remanente no dispone de campo eléctrico ni de terminal exterior para su extracción rápida; por consiguiente, deben desaparecer por recombinación espontánea electrón-hueco, gobernada por el tiempo de vida medio en alto nivel $\tau_{HL}$:
  \begin{equation}
    i_C(t) \approx I_{\text{tail},0} \cdot \exp\left(-\frac{t}{\tau_{HL}}\right)
  \end{equation}
  Como esta corriente residual fluye cuando $V_{CE}$ ya alcanzó la tensión total de bus ($400\text{ V}$), el producto $V_{CE} \cdot I_C$ origina pérdidas de energía significativas ($E_{\text{off}}$).
\end{enumerate}

\subsection{Técnica Double Pulse Test (DPT) e Inductancias Parásitas}
El ensayo de doble pulso (norma IEC 60747-9) permite evaluar la conmutación a corrientes elevadas sin inducir calentamiento térmico acumulado:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Primer pulso ($t_{p1}$):} Carga el inductor $L$ hasta la corriente de prueba deseada: $I_{L} \approx \frac{V_{bus}}{L} t_{p1}$.
  \item \textbf{Intervalo muerto ($t_{\text{fw}}$):} El IGBT se apaga brevemente y la corriente conmuta hacia el diodo de marcha libre superior.
  \item \textbf{Segundo pulso ($t_{p2}$):} Reenciende el transistor para evaluar el transitorio y ejecuta el segundo apagado a la corriente nominal objetivo.
\end{itemize}
En presencia de inductancia parásita de lazo ($L_\sigma$), la tasa de caída de corriente ($di_C/dt$) induce una sobretensión en bornes del transistor: $V_{CE,\text{peak}} = V_{bus} + L_\sigma \cdot |di_C/dt|$.

% ------------------- METODOLOGÍA EXPERIMENTAL -------------------
\section{Metodología de Simulación y Entorno Experimental}

\subsection{Esquemas del Banco de Ensayo DPT en LTspice}
Siguiendo las indicaciones de la guía docente (Figura~2 y Sección~5.1 de la guía), se implementaron en LTspice los esquemas circuitales para ambos tipos de transistores. En la Figura~\ref{fig:esquemas_ltspice} se presentan los diagramas priorizando la visibilidad de los lazos de potencia, diodos de libre circulación y nodos de medida:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Banco N-IGBT (Lado bajo / Low-Side):} Emisor conectado a tierra mediante una resistencia shunt $R_2 = 1\text{ m}\Omega$ (para medir corriente); inductor de carga $L_1 = 100\ \mu\text{H}$ ($R_{ser} = 1\text{ m}\Omega$) en serie con la fuente DC de $V_{bus} = 400\text{ V}$; diodo de marcha libre ultrarrápido $D_1$ (\texttt{DMOD}, con $TT = 35\text{ ns}, RS = 0.01\ \Omega$) en antiparalelo con $L_1$; y fuente de pulsos PWL ($0\text{ V} \to 15\text{ V}$) con $R_G = 10\ \Omega$.
  \item \textbf{Banco P-IGBT (Lado alto / High-Side):} Emisor conectado a la referencia a través de $R_2 = 1\text{ m}\Omega$; colector conectado al inductor $L_1$ hacia la barra de $-400\text{ V}$; diodo $D_1$ con ánodo a $V_{bus}$ y cátodo a colector; y excitación de compuerta con pulsos negativos ($0\text{ V} \to -15\text{ V}$) respecto al emisor.
\end{itemize}

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.485\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/evidencias_ltspice/E00_circuito_nigbt_crop.png}
    \caption*{(a) Banco DPT para N-IGBT (\texttt{DPT\_NIGBT\_nom.asc}).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.485\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/evidencias_ltspice/E00_circuito_pigbt_crop.png}
    \caption*{(b) Banco DPT para P-IGBT (\texttt{DPT\_PIGBT\_nom.asc}).}
  \end{minipage}
  \caption{Esquemas circuitales interactivos implementados en LTspice para los bancos de prueba de doble pulso (DPT) de N-IGBT y P-IGBT, conforme a la guía oficial, priorizando la legibilidad de la topología circuital.}
  \label{fig:esquemas_ltspice}
\end{figure}

\subsection{Medición de Corrientes Terminales y Procedimiento Operacional}
En los macromodelos Duncan (Parte I), la corriente se midió sobre la resistencia shunt de emisor de $1\text{ m}\Omega$ ($I(R2)$), la cual en transitorios rápidos incluye una pequeña corriente de compuerta ($I_E = I_C + I_G$). En la Serie Fuji (Parte II), se insertaron fuentes de tensión continua ideales de $0\text{ V}$ como amperímetros para medir $I_C$ directamente en el terminal de colector sin perturbaciones.

Las variables principales se definen operacionalmente de la siguiente manera:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{$V_{CE(\text{on})}$:} Tensión colector-emisor medida en conducción estacionaria ($50\text{ ns}$ antes del segundo apagado).
  \item \textbf{$t_{d(\text{off})}$:} Intervalo temporal entre el $90\%$ del comando de compuerta y el $90\%$ de la corriente previa de colector. Para el N-IGBT, corresponde al \textbf{flanco descendente} de $V_{GE}$ al cruzar $13.5\text{ V}$ ($90\%$ de $+15\text{ V}$); para el P-IGBT, corresponde al \textbf{flanco ascendente hacia $0\text{ V}$} al cruzar $-13.5\text{ V}$ (cuando $|V_{GE}|$ desciende al $90\%$).
  \item \textbf{$t_f$:} Tiempo transcurrido entre el $90\%$ y el $10\%$ de la corriente de colector ($I_C$).
  \item \textbf{$E_{\text{off}}$:} Energía eléctrica integrada durante el apagado mediante el producto de magnitudes terminales en la ventana de conmutación. En Duncan se integró $V_{CE}(t) \cdot I_E(t)$ sobre el shunt $R_2$ (lo que incluye la corriente capacitiva de compuerta $I_G$); en Fuji se integró la potencia neta de puerto $V_{CE}(t) \cdot I(V_{\text{sens\_C}})$. Se precisa que estas integrales cuantifican la energía eléctrica transferida en los terminales según la metodología de cada banco, distinguiendo la corriente del shunt de la corriente neta de colector, sin equipararse directamente al calor interno del silicio debido a la energía almacenada en parásitos y el balance energético global.
  \item \textbf{Corriente de cola ($I_{C,\text{tail}}$):} En modelos Duncan se detectó por el punto de quiebre donde la pendiente instantánea decrece al $5\%$ de la máxima pendiente de corte ($\left|\frac{di}{dt}\right| \le 0.05 \cdot \left|\frac{di}{dt}\right|_{\max}$); en Fuji se adoptó la convención operacional unívoca del $5\%$ de la corriente previa ($I_{C,\text{tail}} = 0.05 \cdot I_{C,\text{pre}}$).
\end{itemize}

% ------------------- RESULTADOS PARTE I -------------------
\section{Resultados Experimentales — Parte I: Modelos Duncan (Canal N vs Canal P)}

\subsection{EXP-01: Ensayo DPT en N-IGBT (\texttt{XIRGBC20S}, 19 A nominal)}
Se ejecutó la simulación del N-IGBT bajo $V_{bus} = 400\text{ V}, R_G = 10\ \Omega$ y $L = 100\ \mu\text{H}$. Con un primer pulso de duración $t_{p1} = 3.65\ \mu\text{s}$, el inductor acumuló la corriente nominal requerida, alcanzándose en el segundo pulso un valor estacionario de $I_{C,\text{on}} = 19.00\text{ A}$ con una caída directa de $V_{CE(\text{on})} = 1.88\text{ V}$. En la Figura~\ref{fig:dpt_nigbt_global} se aprecia la captura directa de la simulación en LTspice, donde las tres señales solicitadas ($V_{GE}, V_{CE}, I_C$) se visualizan ordenadas en paneles sincronizados.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.88\textwidth]{../figuras/evidencias_ltspice/E01_dpt_nigbt_global.png}
  \caption{Formas de onda globales obtenidas en LTspice para el N-IGBT (\texttt{XIRGBC20S}) a $19\text{ A}$ nominal: (a) doble pulso $V_{GE}$ ($0\to 15\text{ V}$), (b) tensión colector-emisor $V_{CE}$ ($0\to 400\text{ V}$) y (c) corriente medida en el shunt de emisor $I(R2)$, utilizada para estimar la corriente de colector $I_C$ ($0\to 19\text{ A}$).}
  \label{fig:dpt_nigbt_global}
\end{figure}

\subsection{EXP-02: Ensayo DPT en P-IGBT (\texttt{XPIGBT}, 40 A nominal)}
Para el P-IGBT, se configuró la fuente de compuerta con pulsos negativos de $0\text{ V} \to -15\text{ V}$ y la barra colectora a $-400\text{ V}$. Con $t_{p1} = 8.88\ \mu\text{s}$, se alcanzaron $|I_{C,\text{on}}| = 40.01\text{ A}$ nominales con una caída directa de $|V_{CE(\text{on})}| = 2.51\text{ V}$. Adicionalmente, se configuró un ensayo con un pulso inicial de $3.55\ \mu\text{s}$ a $-15\text{ V}$ ($3.65\ \mu\text{s}$ de base hasta el corte; $3.75\ \mu\text{s}$ base a base) para evaluar al P-IGBT a una corriente similar de $19.48\text{ A}$ (frente a los $19.00\text{ A}$ del N-IGBT). En este ensayo (\texttt{dpt\_pigbt\_19a.cir}), el archivo de log acredita directamente $I_{C,\text{pre}} = 19.48\text{ A}$, $|V_{CE(\text{on})}| = 1.72\text{ V}$ y $E_{\text{off}} = 1011.8\ \mu\text{J}$; las directivas \texttt{.meas} fijas del log arrojaron $t_{d(\text{off})} = 218.23\text{ ns}$ y $t_f = 268.09\text{ ns}$. Al no haberse conservado el archivo RAW en el repositorio, los valores bajo criterio dinámico se clasifican como no verificados documentalmente. La Figura~\ref{fig:dpt_pigbt_global} exhibe las formas de onda completas en LTspice.

\paragraph{Ensayos Exploratorios a Corriente Elevada ($\approx 80\text{ A}$):}
De forma complementaria, en la Tabla~\ref{tab:duncan} se incluyen los registros 02 y 04 correspondientes a ensayos exploratorios con pulsos de excitación prolongados donde la corriente inductiva alcanzó niveles de $82.31\text{ A}$ en el N-IGBT y $83.22\text{ A}$ en el P-IGBT. Cabe precisar que estas condiciones exceden las especificaciones nominales continuas del fabricante ($I_C = 19\text{ A}$ y $40\text{ A}$ a $25^\circ\text{C}$). En particular, para el IRGBC20S la hoja de datos fija una corriente pulsada máxima admisible de $I_{CM} = 76\text{ A}$, por lo que alcanzar $82.31\text{ A}$ sobrepasa dicho régimen límite de catálogo. Estos casos se presentan exclusivamente con fines de sensibilidad y cotejo numérico en el entorno SPICE, sin que ello constituya una verificación del límite completo del Área de Operación Segura (SOA) —lo cual requeriría el análisis de sus curvas y tiempos de pulso específicos— ni represente una condición de funcionamiento admisible en el silicio real.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.88\textwidth]{../figuras/evidencias_ltspice/E02_dpt_pigbt_global.png}
  \caption{Formas de onda globales obtenidas en LTspice para el P-IGBT (\texttt{XPIGBT}) a $40\text{ A}$ nominal: (a) compuerta $V_{GE}$ ($0\to -15\text{ V}$), (b) tensión $V_{CE}$ y (c) corriente del shunt de emisor $|I(R2)| = -I(R2)$, utilizada para estimar la corriente de colector $|I_C|$ ($0\to 40\text{ A}$).}
  \label{fig:dpt_pigbt_global}
\end{figure}

\subsection{EXP-03: Caracterización de la Corriente de Cola (\textit{Tail Current})}
Al ampliar el flanco del segundo apagado, se evidencia claramente la inflexión entre el corte rápido del canal MOS y la recombinación asintótica de portadores minoritarios:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item En el N-IGBT ($19\text{ A}$): el quiebre de derivada se produce en $t = 20.258\ \mu\text{s}$, iniciando la cola con $I_{C,\text{tail}} = 0.94\text{ A}$ ($4.93\%$ de la corriente previa).
  \item En el P-IGBT ($40\text{ A}$): el inicio ocurre en $t = 25.655\ \mu\text{s}$ con $|I_{C,\text{tail}}| = 1.81\text{ A}$ ($4.53\%$).
\end{itemize}
En la Figura~\ref{fig:tail_zoom} se detalla la derivada numérica y la prolongación de la corriente residual.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.78\textwidth]{../figuras/fig3_detalle_corriente_cola.png}
  \caption{EXP-03: Acercamiento al segundo flanco de apagado y detección de la corriente de cola mediante quiebre de derivada para N-IGBT ($19\text{ A}$) y P-IGBT ($40\text{ A}$).}
  \label{fig:tail_zoom}
\end{figure}

\subsection{EXP-04: Medición del Retardo $t_{d(\text{off})}$ con Cursores y Cotejo con Datasheet}
Siguiendo la indicación expresa de la guía docente (\textit{«Utilizando los cursores de LTspice, obtenga el valor del tiempo de retardo de apagado ($t_{d(\text{off})}$) midiendo el intervalo entre el 90\% de $V_{GE}$ y el 90\% de $I_C$»}), se colocaron los cursores interactivos sobre las trazas de compuerta y corriente en un mismo panel con doble eje Y en LTspice:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Medición en N-IGBT (\texttt{XIRGBC20S}, Figura~\ref{fig:cursores_medicion}(a)):}
    \begin{itemize}[noitemsep]
      \item Cursor 1 en $V_{GE}$ (flanco descendente): $13.502988\text{ V}$ en $t_1 = 19.861622\ \mu\text{s}$.
      \item Cursor 2 en $I_C$: $17.113018\text{ A}$ en $t_2 = 20.012432\ \mu\text{s}$.
      \item Retardo manual medido en la caja flotante de LTspice: $\bm{t_{d(\text{off})} = 150.81081\text{ ns}}$.
      \item Retardo calculado por la directiva \texttt{.meas}: $\bm{150.827513\text{ ns}}$ (concordancia del $99.99\%$).
    \end{itemize}
  \item \textbf{Medición en P-IGBT (\texttt{XPIGBT}, Figura~\ref{fig:cursores_medicion}(b)):}
    \begin{itemize}[noitemsep]
      \item Cursor 1 en $V_{GE}$ (flanco ascendente hacia $0\text{ V}$): $-13.486733\text{ V}$ en $t_1 = 25.093283\ \mu\text{s}$.
      \item Cursor 2 en $|I_C|$: $36.039449\text{ A}$ en $t_2 = 25.287649\ \mu\text{s}$.
      \item Retardo manual medido en la caja flotante de LTspice: $\bm{t_{d(\text{off})} = 194.3662\text{ ns}}$.
      \item Retardo calculado por la directiva \texttt{.meas}: $\bm{194.573629\text{ ns}}$ (concordancia del $99.89\%$).
    \end{itemize}
\end{itemize}
La leve discrepancia de fracciones de nanosegundo entre la medición manual y el comando \texttt{.meas} se explica de forma natural por la resolución finita del cursor posicionado sobre la cuadrícula gráfica frente a la interpolación numérica continua interna que efectúa el solucionador SPICE.

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.485\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/evidencias_ltspice/E03_cursores_tdoff_nigbt.png}\\[4pt]
    \includegraphics[width=0.82\textwidth]{../figuras/evidencias_ltspice/E03_cursor_zoom.png}
    \caption*{(a) N-IGBT: oscilograma global y ampliación fiel del cuadro de cursores ($t_{d(\text{off})} = 150.81\text{ ns}$).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.485\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/evidencias_ltspice/E04_cursores_tdoff_pigbt.png}\\[4pt]
    \includegraphics[width=0.82\textwidth]{../figuras/evidencias_ltspice/E04_cursor_zoom.png}
    \caption*{(b) P-IGBT: oscilograma global y ampliación fiel del cuadro de cursores ($t_{d(\text{off})} = 194.37\text{ ns}$).}
  \end{minipage}
  \caption{Medición interactiva de retardos $t_{d(\text{off})}$ en LTspice mediante cursores en umbrales de $90\%$. Se incluye el oscilograma completo junto con la ampliación directa y fidedigna de las cajas flotantes con las lecturas diferenciales.}
  \label{fig:cursores_medicion}
\end{figure}

\paragraph{Cotejo Crítico con la Hoja de Datos Oficial (Datasheet):}
La hoja de datos del IRGBC20S (International Rectifier, Farnell 68617) especifica para sus condiciones normalizadas ($V_{CC} = 480\text{ V}$, $I_C = 10\text{ A}$, $R_G = 50\ \Omega$, $V_{GE} = 15\text{ V}$, $T_j = 25^\circ\text{C}$) un retardo de apagado típico de $\bm{820\text{ ns}}$ (máximo $\bm{1200\text{ ns}}$) y un tiempo de caída típico de $\bm{910\text{ ns}}$ (máximo $\bm{1600\text{ ns}}$). La diferencia frente al valor simulado de $150.83\text{ ns}$ responde a la combinación de factores de ensayo y simplificaciones del macromodelo:
\begin{enumerate}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Condiciones de polarización y excitación:} El ensayo de catálogo se realiza a una corriente menor ($I_C = 10\text{ A}$ frente a los $19.00\text{ A}$ nominales ensayados en LTspice) pero con una resistencia de compuerta sensiblemente mayor ($R_G = 50\ \Omega$ frente a $10\ \Omega$) y mayor tensión de bus ($480\text{ V}$ frente a $400\text{ V}$). La mayor resistencia $R_G$ ralentiza fuertemente la descarga de la carga de compuerta ($Q_G$) en el dispositivo físico, ensanchando tanto $t_{d(\text{off})}$ como $t_f$.
  \item \textbf{Naturaleza y parametrización del macromodelo:} El modelo conductual de Duncan Electronics (\texttt{nigbt.lib}) es una representación analógica simplificada basada en un subcircuito MOSFET-BJT con tiempo de tránsito bipolar parametrizado en $TF = 16.8\text{ ns}$ e inductancia interna de emisor $LE = 7.5\text{ nH}$. Al tratarse de un modelo conductual aproximado, no incorpora la totalidad de efectos físicos de inyección en régimen de alta potencia ni recombinación bidimensional presentes en el silicio real de primera generación, resultando en una respuesta transitoria inherentemente más ágil que la medida en laboratorio.
\end{enumerate}

\subsection{EXP-05: Energía de Apagado $E_{\text{off}}$ e Integración Gráfica en LTspice}
Para calcular la energía eléctrica integrada durante el apagado ($E_{\text{off}}$) se graficó la potencia instantánea $(V(VC)-V(VE)) \cdot I(R2)$ y se realizó la integración directa en LTspice manteniendo presionada la tecla \textbf{Ctrl} y haciendo clic sobre la etiqueta de la traza en el intervalo de apagado $[19.85\ \mu\text{s}, 25.00\ \mu\text{s}]$. Como se aprecia en la captura auténtica de la Figura~\ref{fig:energia_ltspice}, el cuadro de diálogo oficial de LTspice arroja una integral de $\bm{691.48\ \mu\text{J}}$ ($0.6915\text{ mJ}$) y una potencia promedio de $134.27\text{ W}$, en total acuerdo con los $\bm{691.478\ \mu\text{J}}$ calculados por la directiva \texttt{.meas}. Esta integral cuantifica la energía eléctrica integrada en el corte según la metodología del banco sobre el shunt de emisor, sin equipararse directamente al calor interno del silicio debido a la energía almacenada en parásitos y el balance energético.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.74\textwidth]{../figuras/evidencias_ltspice/E05_energia_eoff_integral.png}\\[4pt]
  \includegraphics[width=0.34\textwidth]{../figuras/evidencias_ltspice/E05_energia_zoom.png}
  \caption{Cálculo de energía $E_{\text{off}}$ mediante integración gráfica interactiva en LTspice (Ctrl + Clic en la traza de potencia instantánea en el intervalo de apagado): oscilograma global de potencia y ampliación directa del cuadro de diálogo donde se confirma la lectura nítida de la integral de $691.48\ \mu\text{J}$ y potencia media de $134.27\text{ W}$.}
  \label{fig:energia_ltspice}
\end{figure}

Para el P-IGBT a $40\text{ A}$, la energía integrada resultó en $E_{\text{off}} = 2115.3\ \mu\text{J}$. En la Figura~\ref{fig:energia_comparativa} se ilustra la curva comparativa de acumulación energética y potencia entre ambos dispositivos.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.74\textwidth]{../figuras/fig5_potencia_energia_apagado.png}
  \caption{Comparación de potencia instantánea $p(t)$ e integración acumulada de energía de apagado $E_{\text{off}}(t)$ para N-IGBT y P-IGBT.}
  \label{fig:energia_comparativa}
\end{figure}

% ------------------- RESULTADOS PARTE II -------------------
\section{Resultados Experimentales — Parte II: Fuji Electric Serie X}

Esta fase comprendió 6 configuraciones únicas (F01 a F06) evaluadas a $T = 25.0^\circ\text{C}$ con inductancia parásita de lazo $L_\sigma = 25\text{ nH}$ ($R_{ser} = 10\text{ m}\Omega$), sin amortiguamiento paralelo artificial.

\subsection{EXP-06 y EXP-07: Sobretensión y Diodo Co-Pack en 50 A y 75 A}
Se comparó el modelo discreto frente al modelo co-pack con diodo antiparalelo integrado (\texttt{FGW50XS65} vs \texttt{FGW50XS65C} en 50 A; \texttt{FGW75XS65} vs \texttt{FGW75XS65C} en 75 A):
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item En 50 A: la sobretensión inductiva alcanzó $V_{CE,\text{peak}} = 442.36\text{ V}$ ($+42.36\text{ V}$ sobre el bus de 400 V), con $t_{d(\text{off})} = 231.10\text{ ns}$ y $E_{\text{off}} = 1066.98\ \mu\text{J}$ en el discreto frente a $231.09\text{ ns}$ y $1066.98\ \mu\text{J}$ en el co-pack (Figura~\ref{fig:copack_ambos}(a)).
  \item En 75 A: el pico alcanzó $V_{CE,\text{peak}} = 445.98\text{ V}$ ($+45.98\text{ V}$), con $t_{d(\text{off})} = 293.18\text{ ns}$ y $E_{\text{off}} = 2052.75\ \mu\text{J}$ en el discreto frente a $293.16\text{ ns}$ y $2052.74\ \mu\text{J}$ en el co-pack (Figura~\ref{fig:copack_ambos}(b)).
\end{itemize}
\textbf{Explicación Física y Relevancia en Topologías de Puente:} En la topología DPT de lado bajo empleada en este laboratorio, el diodo co-pack tiene su ánodo conectado al emisor ($0\text{ V}$) y su cátodo al colector ($VC$). Durante el corte inductivo del transistor, $V_{CE}$ se eleva a más de $400\text{ V}$, imponiendo una fuerte polarización inversa sobre el diodo co-pack ($V_{AK} \approx -442\text{ V}$). Por consiguiente, este diodo no conduce corriente directa de potencia y la circulación de rueda libre la efectúa exclusivamente el diodo superior del banco ($D_1$). Las curvas de conmutación son virtualmente idénticas en el conmutador de lado bajo, presentando únicamente diferencias numéricas despreciables ($\le 0.02\text{ ns}$ en retardo y $\le 0.01\ \mu\text{J}$ en pérdidas), las cuales caen dentro del margen de resolución numérica del solver.

La verdadera importancia técnica del diodo co-pack se manifiesta en \textbf{topologías de medio puente y puente completo} (inversores de tracción y accionamientos de motores). En dichas ramas, cuando conmuta el transistor opuesto, el diodo co-pack entra en conducción directa para sostener la continuidad de la corriente reactiva de carga, introduciendo dos efectos determinantes:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Pérdidas de conducción:} Durante el intervalo de retorno de corriente, la disipación estacionaria del diodo es gobernada por su caída directa ($P_{\text{cond}} \approx V_F \cdot I_D$).
  \item \textbf{Dinámica de recuperación inversa ($Q_{rr}$):} Al reconmutar el transistor complementario, el diodo debe evacuar su carga minoritaria almacenada, originando un pico transitorio de corriente inversa ($I_{rrm}$) durante un lapso $t_{rr}$. Esta corriente se superpone al encendido del interruptor activo, incrementando sensiblemente sus pérdidas de energía de encendido ($E_{\text{on}}$) y excitando oscilaciones de alta frecuencia.
\end{itemize}

\paragraph{Verificación Analítica de la Sobretensión Inductiva ($L_\sigma \cdot |di/dt|_{\max}$):}
Para comprobar la consistencia física de la sobretensión simulada frente a la ley de Faraday ($V_{L\sigma} = L_\sigma \cdot |di/dt|_{\max}$), se contrastó el sobreimpulso $\Delta V = V_{CE,\text{peak}} - V_{bus}$ con la predicción analítica bajo $L_\sigma = 25\text{ nH}$:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Módulo de 50 A (F01/F02, $R_G = 10\ \Omega$):} Con $|di/dt|_{\max} = 1669.5\text{ A}/\mu\text{s}$, el voltaje inducido es $V_{L\sigma} = 25\text{ nH} \times 1669.5\text{ A}/\mu\text{s} = 41.74\text{ V}$, reproduciendo el \textbf{98.5\%} de la sobretensión simulada ($\Delta V = +42.36\text{ V}$).
  \item \textbf{Módulo de 75 A (F03/F04, $R_G = 10\ \Omega$):} Con $|di/dt|_{\max} = 1818.0\text{ A}/\mu\text{s}$, el valor teórico es $V_{L\sigma} = 25\text{ nH} \times 1818.0\text{ A}/\mu\text{s} = 45.45\text{ V}$, correspondiente al \textbf{98.8\%} de la sobretensión simulada ($\Delta V = +45.98\text{ V}$).
  \item \textbf{Sensibilidad con $R_G = 20\ \Omega$ (F06):} Con $|di/dt|_{\max} = 1019.4\text{ A}/\mu\text{s}$, se obtiene $V_{L\sigma} = 25\text{ nH} \times 1019.4\text{ A}/\mu\text{s} = 25.49\text{ V}$, reproduciendo el \textbf{98.3\%} de $\Delta V = +25.94\text{ V}$.
\end{itemize}
Esta concordancia analítica superior al 98\% respalda con claridad la contribución dominante de la inductancia parásita concentrada de lazo en el sobreimpulso observado; no obstante, debe matizarse que no constituye por sí sola una demostración del balance completo de la sobretensión ni identifica de manera inequívoca cada componente residual (tales como caídas resistivas parásitas, efectos capacitivos no lineales de juntura o dinámicas distribuidas del montaje).

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.40\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/fig6_sobretension_copack_50a.png}
    \caption*{(a) Módulo de 50 A (\texttt{FGW50XS65} vs \texttt{C}).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.40\textwidth}
    \centering
    \includegraphics[width=\textwidth]{../figuras/fig7_sobretension_copack_75a.png}
    \caption*{(b) Módulo de 75 A (\texttt{FGW75XS65} vs \texttt{C}).}
  \end{minipage}
  \caption{EXP-06 y EXP-07: Sobretensión inductiva en modelos discretos y co-pack de Fuji Electric a $L_\sigma = 25\text{ nH}$. Las curvas de tensión y corriente resultan virtualmente idénticas en el interruptor de lado bajo.}
  \label{fig:copack_ambos}
\end{figure}

\FloatBarrier
\subsection{EXP-08: Escalamiento del Tamaño de Chip (50 A frente a 75 A)}
Se analizaron los modelos \texttt{FGW50XS65} y \texttt{FGW75XS65}:
\begin{enumerate}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Comparación a corriente igualada ($50\text{ A}$, F01 vs F05):} Al operar el chip de 75 A a los mismos 50 A que el chip menor, la tensión de saturación $V_{CE(\text{on})}$ disminuye de $1.362\text{ V}$ a $1.181\text{ V}$ ($-181\text{ mV}$, una reducción de $-13.3\%$ en pérdidas de conducción), gracias a la menor densidad de corriente ($J = I/A$). Sin embargo, las mayores capacitancias parásitas de compuerta (parámetro de subcircuito $C_{GE} = 9.50\text{ nF}$ vs $6.77\text{ nF}$) incrementan el retardo $t_{d(\text{off})}$ en $+40.5\%$ ($231.1\text{ ns} \to 324.8\text{ ns}$) y las pérdidas $E_{\text{off}}$ en $+28.2\%$ ($1067\ \mu\text{J} \to 1368\ \mu\text{J}$).
  \item \textbf{A corriente nominal de cada modelo ($50\text{ A}$ vs $75\text{ A}$, F01 vs F03):} La caída en conducción resulta similar ($1.362\text{ V}$ vs $1.356\text{ V}$), pero la energía de apagado casi se duplica ($2052.75\ \mu\text{J}$ vs $1066.98\ \mu\text{J}$, $+92.4\%$) al interrumpir $50\%$ más corriente en presencia de mayor carga minoritaria almacenada (Figura~\ref{fig:area}).
\end{enumerate}

\vspace{0.15cm}
\noindent\begin{minipage}{\textwidth}
  \centering
  \includegraphics[width=0.48\textwidth]{../figuras/fig8_comparativa_area_50vs75.png}
  \captionof{figure}{EXP-08: Efecto del área de silicio en conmutación: formas de onda de tensión y corriente comparando operación a corriente igualada ($50\text{ A}$) y nominal ($50\text{ A}$ vs $75\text{ A}$).}
  \label{fig:area}
\end{minipage}

\FloatBarrier
\subsection{EXP-09: Sensibilidad a la Resistencia de Compuerta ($R_G = 10\ \Omega \to 20\ \Omega$)}
En el modelo \texttt{FGW50XS65C} a $50\text{ A}$ (F02 vs F06):
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item Duplicar $R_G$ a $20\ \Omega$ disminuye la magnitud de la corriente instantánea de descarga de la compuerta ($i_G(t) = \frac{v_{\text{drv}}(t) - v_G(t)}{R_G}$, con $v_{\text{drv}} = 0\text{ V}$ en el corte), ralentizando la descarga de la capacitancia Miller ($C_{res}$) y prolongando la meseta de tensión.
  \item Como consecuencia, la tasa máxima de corte $|di/dt|_{\text{max}}$ se reduce de $1669.6\text{ A}/\mu\text{s}$ a $1019.4\text{ A}/\mu\text{s}$ ($-38.9\%$).
  \item La sobretensión inducida por la inductancia parásita de lazo ($L_\sigma = 25\text{ nH}$) desciende de $+42.36\text{ V}$ a $+25.94\text{ V}$ ($-38.8\%$), reduciendo el pico absoluto a $425.94\text{ V}$ y alejando al transistor de su límite de ruptura dieléctrica.
  \item Sin embargo, el tiempo de caída de corriente se ensancha ($t_f$ pasa de $31.4\text{ ns}$ a $57.3\text{ ns}$, $+82.5\%$), incrementando las pérdidas de energía de apagado en $+70.5\%$ ($1066.98\ \mu\text{J} \to 1818.73\ \mu\text{J}$) (Figura~\ref{fig:rg}).
\end{itemize}

\vspace{0.15cm}
\noindent\begin{minipage}{\textwidth}
  \centering
  \includegraphics[width=0.48\textwidth]{../figuras/fig9_sensibilidad_rg_conmutacion.png}
  \captionof{figure}{EXP-09: Efecto de duplicar $R_G$ ($10\ \Omega \to 20\ \Omega$): evolución de tensión de compuerta, mitigación de sobretensión en colector y penalización en energía de apagado.}
  \label{fig:rg}
\end{minipage}

En síntesis, los resultados de simulación con la familia Trench Field-Stop de Fuji Electric muestran que el diseño de etapas de potencia con IGBTs involucra un triple compromiso físico: (1) el área de silicio, donde chips de mayor calibre reducen la caída de conducción a costa de mayores pérdidas de corte y retardo; (2) la topología circuital, donde el diodo co-pack no interviene en lado bajo pero resulta imprescindible en ramas de puente; y (3) la resistencia de compuerta $R_G$, que permite atenuar sobretensiones destructivas $L_\sigma \cdot di/dt$ a costa de una severa penalización energética. En la siguiente sección se condensan cuantitativamente todas las magnitudes evaluadas.

\FloatBarrier
% ------------------- TABLAS CONSOLIDADAS (LANDSCAPE 2 PÁGINAS) -------------------
\begin{landscape}
\pagestyle{landscapestyle}

\section{Tablas Consolidadas de Resultados Experimentales}

\begin{cuadronota}[Diferencias Metodológicas entre Familias de Modelos]
  Para interpretar correctamente los datos numéricos, es indispensable distinguir las condiciones particulares de cada banco de ensayo:
  \begin{itemize}[leftmargin=*, noitemsep, topsep=1pt]
    \item \textbf{Macromodelos Duncan (Tabla~\ref{tab:duncan}):} Evaluados a $T = 27^\circ\text{C}$ con inductancia de lazo ideal ($L_\sigma = 0\text{ nH}$). La corriente terminal se midió mediante resistencia shunt de emisor de $1\text{ m}\Omega$ ($I_E = I_C + I_G$), integrando $V_{CE} \cdot I_E$ durante el corte. Se prescinde de la columna de pendiente máxima $|di/dt|_{\max}$ al no ser requerida por la guía docente (los valores medios $I_{\text{pre}}/t_f$ no representan derivadas instantáneas de corte). El inicio de la corriente de cola se delimitó en el quiebre de derivada de corte: $\left|\frac{di}{dt}\right| \le 0.05 \cdot \left|\frac{di}{dt}\right|_{\max}$ ($5\%$ del valor pico local de caída).
    \item \textbf{Módulos Fuji Serie X (Tablas~\ref{tab:fuji_estatica} y \ref{tab:fuji_dinamica}):} Evaluados a $T = 25.0^\circ\text{C}$ con inductancia parásita física de lazo $L_\sigma = 25\text{ nH}$ ($R_{ser} = 10\text{ m}\Omega$). La corriente de colector $I_C$ se midió directamente en el terminal con sensor ideal de $0\text{ V}$, y el inicio de cola se delimitó bajo la convención operacional unívoca del $5\%$ ($I_{C,\text{tail}} = 0.05 \cdot I_{C,\text{pre}}$). Los retardos $t_{d(\text{off})}$ de la tabla corresponden al post-procesamiento en Python con umbral dinámico del $90\%$ de $V_{GE,\text{pre}}$ real (evaluada $40\text{ ns}$ antes del corte), arrojando $+56.5\%$ al duplicar $R_G$ ($+60.4\%$ bajo directivas \texttt{.meas} con umbral fijo de $13.5\text{ V}$).
  \end{itemize}
\end{cuadronota}

\vspace{0.25cm}

\begin{table}[htbp]
\centering
\small
\setlength{\tabcolsep}{5.5pt}
\caption{Resultados experimentales en macromodelos Duncan Electronics ($T = 27^\circ\text{C}$, $L_\sigma = 0\text{ nH}$, $R_G = 10\ \Omega$, $V_{bus} = 400\text{ V}$).}
\label{tab:duncan}
\begin{tabular}{@{}c l l c c c c c c c c c@{}}
\toprule
\textbf{Reg.} & \textbf{Configuración} & \textbf{Modelo} & \textbf{Enc.} & $I_{\text{target}}$ [A] & $I_{C,\text{pre}}$ [A] & $V_{CE(\text{on})}$ [V] & $t_{d(\text{off})}$ [ns] & $t_f$ [ns] & $E_{\text{off}}$ [µJ] & $I_{C,\text{tail}}$ [A] & \textbf{\%}$E_{\text{tail}}$ \\
\midrule
\textbf{01} & N-IGBT Nominal & \texttt{XIRGBC20S} & TO-220 & 19.0 & 19.00 & 1.88 & 150.83 & 185.24 & 691.5 & 0.94 & 4.73\% \\
\textbf{02} & N-IGBT Sobrecarga & \texttt{XIRGBC20S} & TO-220 & 80.0 & 82.31 & 6.57 & 103.32 & 196.03 & 3402.5 & 2.31 & 2.25\% \\
\textbf{03} & P-IGBT Nominal & \texttt{XPIGBT} & TO-220 & 40.0 & 40.02 & 2.51 & 194.57 & 268.42 & 2115.3 & 1.81 & 4.33\% \\
\textbf{04} & P-IGBT Sobrecarga & \texttt{XPIGBT} & TO-220 & 80.0 & 83.22 & 4.25 & 172.32 & 275.03 & 4698.9 & 2.86 & 2.99\% \\
\textbf{05} & P-IGBT Control 19A & \texttt{XPIGBT} & TO-220 & 19.0 & 19.48 & 1.72 & N/V* & N/V* & 1011.8 & N/V* & N/V* \\
\bottomrule
\end{tabular}
\end{table}

\vspace{0.12cm}
\noindent{\footnotesize\textit{*Nota sobre Reg.~05 (P-IGBT Control 19A):} Las magnitudes $I_{C,\text{pre}} = 19.48\text{ A}$, $V_{CE(\text{on})} = 1.72\text{ V}$ y $E_{\text{off}} = 1011.8\ \mu\text{J}$ están acreditadas en el log (\texttt{dpt\_pigbt\_19a.log}). Los valores bajo criterio dinámico figuran como No Verificados (N/V) al no conservarse el archivo RAW; las lecturas de \texttt{.meas} en el log con umbrales fijos fueron $t_{d(\text{off})} = 218.23\text{ ns}$ y $t_f = 268.09\text{ ns}$.}\\[3pt]
\noindent{\footnotesize\textit{Nota documental:} En la página horizontal siguiente se desglosan los resultados de los 6 ensayos en la familia comercial Fuji Electric Serie X, organizados en dos tablas temáticas para garantizar la legibilidad completa de todos los parámetros.}

\newpage

\subsection{Resultados Experimentales de la Suite Fuji Electric Serie X (EXP-06 a EXP-09)}

\begin{table}[htbp]
\centering
\small
\setlength{\tabcolsep}{6.0pt}
\caption{Módulos Fuji Electric Serie X: condiciones de polarización estática y sobretensión inductiva ($T = 25.0^\circ\text{C}$, $L_\sigma = 25\text{ nH}$, $V_{bus} = 400\text{ V}$).}
\label{tab:fuji_estatica}
\begin{tabular}{@{}c c l l c c c c c c c@{}}
\toprule
\textbf{Reg.} & \textbf{Id} & \textbf{Configuración} & \textbf{Modelo} & \textbf{Enc.} & $I_{\text{target}}$ [A] & $I_{C,\text{pre}}$ [A] & $R_G$ [$\Omega$] & $V_{CE(\text{on})}$ [V] & $V_{CE,\text{peak}}$ [V] & \textbf{Sobretensión} [$\Delta V$] \\
\midrule
\textbf{06} & F01 & 50A Discreto & \texttt{FGW50XS65}  & TO-247 & 50.0 & 50.013 & 10 & 1.362 & 442.36 & $+42.36\text{ V}$ ($+10.6\%$) \\
\textbf{07} & F02 & 50A Co-Pack  & \texttt{FGW50XS65C} & TO-247 & 50.0 & 50.012 & 10 & 1.362 & 442.36 & $+42.36\text{ V}$ ($+10.6\%$) \\
\textbf{08} & F03 & 75A Discreto Nom. & \texttt{FGW75XS65}  & TO-247 & 75.0 & 75.230 & 10 & 1.356 & 445.98 & $+45.98\text{ V}$ ($+11.5\%$) \\
\textbf{09} & F04 & 75A Co-Pack Nom.  & \texttt{FGW75XS65C} & TO-247 & 75.0 & 75.233 & 10 & 1.356 & 445.98 & $+45.98\text{ V}$ ($+11.5\%$) \\
\textbf{10} & F05 & 75A Discreto @ 50A & \texttt{FGW75XS65}  & TO-247 & 50.0 & 50.362 & 10 & 1.181 & 436.37 & $+36.37\text{ V}$ ($+9.1\%$) \\
\textbf{11} & F06 & 50A Co-Pack @ $20\,\Omega$ & \texttt{FGW50XS65C} & TO-247 & 50.0 & 50.123 & 20 & 1.392 & 425.94 & $+25.94\text{ V}$ ($+6.5\%$) \\
\bottomrule
\end{tabular}
\end{table}

\vspace{0.35cm}

\begin{table}[htbp]
\centering
\small
\setlength{\tabcolsep}{5.2pt}
\caption{Módulos Fuji Electric Serie X: dinámica transitoria de conmutación, pérdidas energéticas y corriente de cola ($T = 25.0^\circ\text{C}$).}
\label{tab:fuji_dinamica}
\begin{tabular}{@{}c c l l c c c c c c c@{}}
\toprule
\textbf{Reg.} & \textbf{Id} & \textbf{Configuración} & \textbf{Modelo} & $t_{d(\text{off})}$ [ns] & $t_f$ [ns] & $|di/dt|_{\max}$ [A/µs] & $E_{\text{off}}$ [µJ] & $I_{C,\text{tail}}$ (5\%) [A] & $E_{\text{tail}}$ [µJ] & \textbf{\%}$E_{\text{tail}}$ \\
\midrule
\textbf{06} & F01 & 50A Discreto & \texttt{FGW50XS65}  & 231.10 & 31.38 & 1669.5 & 1066.98 & 2.50 & 4.68 & 0.44\% \\
\textbf{07} & F02 & 50A Co-Pack  & \texttt{FGW50XS65C} & 231.09 & 31.38 & 1669.6 & 1066.98 & 2.50 & 4.68 & 0.44\% \\
\textbf{08} & F03 & 75A Discreto Nom. & \texttt{FGW75XS65}  & 293.18 & 40.48 & 1818.0 & 2052.75 & 3.76 & 7.56 & 0.37\% \\
\textbf{09} & F04 & 75A Co-Pack Nom.  & \texttt{FGW75XS65C} & 293.16 & 40.48 & 1818.4 & 2052.74 & 3.76 & 7.57 & 0.37\% \\
\textbf{10} & F05 & 75A Discreto @ 50A & \texttt{FGW75XS65}  & 324.75 & 34.18 & 1429.8 & 1367.85 & 2.52 & 4.39 & 0.32\% \\
\textbf{11} & F06 & 50A Co-Pack @ $20\,\Omega$ & \texttt{FGW50XS65C} & 361.60 & 57.27 & 1019.4 & 1818.73 & 2.51 & 8.74 & 0.48\% \\
\bottomrule
\end{tabular}
\end{table}

\end{landscape}
\pagestyle{fancy}
\FloatBarrier

% ------------------- CONCLUSIONES TÉCNICAS (>= 1 PÁGINA) -------------------
\section{Conclusiones Técnicas Fundamentadas en Física de Semiconductores}

\subsection{Asimetría Fundamental entre Canales N y P}
Al comparar en simulación el N-IGBT (\texttt{XIRGBC20S}) con el P-IGBT (\texttt{XPIGBT}), los resultados de los archivos de log acreditan que el dispositivo de canal P presentó mayores pérdidas de conmutación: en el ensayo de control a corriente similar ($19.48\text{ A}$ frente a $19.00\text{ A}$), la energía eléctrica integrada durante el apagado ($E_{\text{off}}$) alcanzó $1011.8\ \mu\text{J}$ frente a $691.5\ \mu\text{J}$ ($+46.3\%$). En las condiciones nominales verificadas con cursores, el retardo $t_{d(\text{off})}$ fue de $194.57\text{ ns}$ en P-IGBT ($40\text{ A}$) frente a $150.83\text{ ns}$ en N-IGBT ($19\text{ A}$); en el ensayo de control a $19.48\text{ A}$, las directivas \texttt{.meas} fijas del log registraron $t_{d(\text{off})} = 218.23\text{ ns}$ y $t_f = 268.09\text{ ns}$, clasificándose los valores bajo criterio dinámico como no verificados al no conservarse el archivo RAW.

En la teoría de semiconductores, la movilidad de los electrones en silicio ($\mu_n \approx 1400\text{ cm}^2/\text{V}\cdot\text{s}$) supera a la de los huecos ($\mu_p \approx 450\text{ cm}^2/\text{V}\cdot\text{s}$), fundamentando una mayor resistencia específica para dispositivos de canal P. No obstante, debe enfatizarse que los resultados de simulación SPICE no permiten aislar la movilidad microscópica como causa directa cuantificada. La comparación involucra dos macromodelos conductuales independientes (\texttt{nigbt.lib} frente a \texttt{pigbt.lib}) que difieren en su parametrización interna: capacitancias parásitas de compuerta y juntura, resistencias de subcircuito y tiempos de tránsito del BJT equivalente ($TF = 16.8\text{ ns}$ en el BJT PNP del N-IGBT frente a los parámetros del BJT NPN del P-IGBT). Por consiguiente, la mayor lentitud y disipación observadas en simulación reflejan la respuesta particular de los macromodelos y sus componentes equivalentes, constituyendo la movilidad únicamente el marco teórico general. Tras el corte del canal MOS, la corriente remanente en ambos dispositivos decae gobernada tanto por el barrido de portadores bajo el crecimiento de tensión ($dv/dt$) como por la recombinación en la base de deriva neutra.

\subsection{Función Física y Comportamiento Circuital del Diodo Co-Empaquetado (Co-Pack)}
Los resultados de los ensayos EXP-06 y EXP-07 confirmaron que, dentro del banco de prueba de doble pulso en lado bajo, las formas de onda de tensión, corriente, sobretensión máxima ($442.36\text{ V}$ en 50 A; $445.98\text{ V}$ en 75 A) y energía de apagado ($1066.98\ \mu\text{J}$ en 50 A; $2052.74\ \mu\text{J}$ en 75 A) son virtualmente coincidentes entre los modelos discretos y co-pack.

La explicación es estrictamente circuital: en el conmutador de lado bajo, el diodo co-pack está conectado en antiparalelo entre emisor y colector. Durante el apagado, la tensión de colector sube a más de $400\text{ V}$, imponiendo una polarización inversa permanente en este diodo ($V_{AK} < 0$), por lo que no conduce corriente directa. La libre circulación de la corriente inductiva la asume el diodo superior del banco ($D_1$). Las diferencias numéricas entre ambos modelos son mínimas ($\le 0.02\text{ ns}$ en retardo y $\le 0.01\ \mu\text{J}$ en energía), no siendo relevantes para la resolución práctica ni las métricas evaluadas en este ensayo. Esto evidencia que el diodo co-pack no ejerce una función protectora sobre el propio interruptor durante su corte, sino que está pensado para operar en \textbf{topologías de medio puente o puente completo} (inversores de tracción y convertidores en cuatro cuadrantes), donde asume la corriente de carga reactiva al conmutar el interruptor complementario. En dicho entorno, el diodo introduce pérdidas de conducción proporcionales a su caída directa ($P_{\text{cond}} \approx V_F \cdot I_D$) y, fundamentalmente, su dinámica de recuperación inversa ($Q_{rr}, I_{rrm}, t_{rr}$) incrementa de manera sustancial la energía de encendido ($E_{\text{on}}$) del transistor opuesto de la rama.

\subsection{Compromiso de Conducción frente a Conmutación al Variar el Tamaño del Chip}
El análisis comparativo entre los modelos \texttt{FGW50XS65} y \texttt{FGW75XS65} puso en evidencia el clásico compromiso de diseño:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{A corriente igualada ($50\text{ A}$, F01 vs F05):} El chip de 75 A redujo la caída directa $V_{CE(\text{on})}$ de $1.362\text{ V}$ a $1.181\text{ V}$ ($-181\text{ mV}$, una mejora de $-13.3\%$), gracias a una menor densidad de corriente $J = I/A$.
  \item \textbf{Penalización en conmutación:} El retardo $t_{d(\text{off})}$ aumentó en $+40.5\%$ ($231.1\text{ ns} \to 324.8\text{ ns}$) y las pérdidas $E_{\text{off}}$ crecieron en $+28.2\%$ ($1067\ \mu\text{J} \to 1368\ \mu\text{J}$), debido a que el chip de mayor área posee mayores capacitancias parásitas (parámetro de subcircuito $C_{GE}$ de $9.50\text{ nF}$ vs $6.77\text{ nF}$) y almacena mayor cantidad de carga.
\end{itemize}
En convertidores de potencia, seleccionar un chip sobredimensionado en corriente reduce las pérdidas estáticas de conducción, pero incrementa las pérdidas por evento de conmutación, por lo que el beneficio neto dependerá del punto de operación y la frecuencia de trabajo del circuito.

\subsection{Compromiso en la Selección de la Resistencia de Compuerta ($R_G$)}
Los resultados de simulación del ensayo EXP-09 muestran que duplicar $R_G$ de $10\ \Omega$ a $20\ \Omega$ tiene un efecto directo sobre el compromiso entre sobretensión inductiva y disipación energética:
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item La menor velocidad de descarga de compuerta redujo la tasa de corte $|di/dt|_{\text{max}}$ en un $-38.9\%$ ($1669.6\text{ A}/\mu\text{s} \to 1019.4\text{ A}/\mu\text{s}$), mitigando la sobretensión inductiva sobre el bus de $+42.36\text{ V}$ a $+25.94\text{ V}$ (una reducción de $-38.8\%$).
  \item A cambio, el tiempo de conmutación se prolongó ($t_f$ creció $+82.5\%$) y las pérdidas de energía de apagado aumentaron en $+70.5\%$ ($1066.98\ \mu\text{J} \to 1818.73\ \mu\text{J}$).
\end{itemize}
El dimensionamiento de $R_G$ no debe orientarse únicamente a minimizar las pérdidas de conmutación, ya que valores excesivamente bajos elevan la tasa $|di/dt|$ y pueden generar picos de sobretensión destructivos o interferencias electromagnéticas severas.

\FloatBarrier
% ------------------- CUESTIONARIO OFICIAL -------------------
\section{Cuestionario Oficial de la Guía Docente}

\subsection{Pregunta 4.1: Visualización transitoria de señales en canales N y P}
\textbf{Enunciado:} \textit{«Ejecute la simulación. Grafique de forma clara $V_{GE}, V_{CE}$ y la corriente de colector $I_C$ para ambos casos.»}\\
\textbf{Respuesta:} Se graficaron de forma ordenada las tres señales para ambos dispositivos: en la Figura~\ref{fig:dpt_nigbt_global} se presenta el N-IGBT a corriente nominal ($19\text{ A}$), y en la Figura~\ref{fig:dpt_pigbt_global} se presenta el P-IGBT a corriente nominal ($40\text{ A}$) bajo excitación de compuerta negativa ($0\text{ V} \to -15\text{ V}$).

\subsection{Pregunta 4.2: Inicio de la fase de corriente de cola y justificación física}
\textbf{Enunciado:} \textit{«Determine el valor de la corriente de colector ($I_C$) en el punto exacto donde inicia la fase asintótica denominada tail current. Explique, basándose en la física del dispositivo, por qué esta corriente no cae instantáneamente a cero.»}\\
\textbf{Respuesta Cuantitativa:} Para el N-IGBT a $19\text{ A}$, el quiebre de derivada sitúa el inicio de cola en $t = 20.258\ \mu\text{s}$ con $I_{C,\text{tail}} = 0.94\text{ A}$ ($4.93\%$). En los modelos de Fuji Serie X a $50\text{ A}$, la convención operacional adoptada sitúa el umbral en $2.50\text{ A}$ ($5\%$). Se precisa que este porcentaje es una convención operacional de ingeniería para una delimitación reproducible, y no una frontera microscópica estricta.\\
\textbf{Justificación Física:} La corriente no cae a cero de forma instantánea debido a la dinámica en dos etapas de los portadores minoritarios: al extinguirse el canal MOS, la expansión de la zona de carga espacial barre los portadores de la región desértica activa (*sweep-out*), pero tras alcanzar el bus de tensión ($dv/dt \approx 0$), los portadores remanentes en la base neutra quedan sin campo de arrastre y deben desaparecer mediante recombinación espontánea electrón-hueco, gobernada por el tiempo de vida media $\tau_{HL}$.

\subsection{Pregunta 4.3: Tiempo de retardo $t_{d(\text{off})}$ y comparación con hoja de datos}
\textbf{Enunciado:} \textit{«Utilizando los cursores de LTspice, obtenga el valor del tiempo de retardo de apagado ($t_{d(\text{off})}$) midiendo el intervalo entre el 90\% de $V_{GE}$ y el 90\% de $I_C$. Compare este dato con el valor proporcionado en la hoja de datos (datasheet) del fabricante y justifique cualquier discrepancia encontrada.»}\\
\textbf{Respuesta Cuantitativa:} En la simulación interactiva con cursores de LTspice (Figura~\ref{fig:cursores_medicion}(a)), el retardo medido para el N-IGBT (\texttt{XIRGBC20S}) fue de $\bm{150.81\text{ ns}}$ (y $\bm{150.83\text{ ns}}$ mediante directiva \texttt{.meas}). La hoja de datos oficial del fabricante (IRGBC20S, Farnell 68617) especifica bajo $V_{CC} = 480\text{ V}$, $I_C = 10\text{ A}$ y $R_G = 50\ \Omega$ un retardo típico de $\bm{820\text{ ns}}$ (máximo $\bm{1200\text{ ns}}$) y un tiempo de caída típico de $\bm{910\text{ ns}}$ (máximo $\bm{1600\text{ ns}}$).\\
\textbf{Justificación de la Discrepancia:} La divergencia responde conjuntamente a factores de ensayo y a simplificaciones del modelo: (1) el ensayo del fabricante emplea una resistencia de compuerta cinco veces mayor ($R_G = 50\ \Omega$ frente a $10\ \Omega$), menor corriente ($10\text{ A}$ frente a $19\text{ A}$) y mayor tensión ($480\text{ V}$ frente a $400\text{ V}$), lo que ralentiza sensiblemente la evacuación de carga de compuerta en el silicio real; y (2) el macromodelo de Duncan Electronics parametriza un tiempo de tránsito bipolar rápido ($TF = 16.8\text{ ns}$) e inductancia interna de emisor $LE = 7.5\text{ nH}$ dentro de una estructura conductual simplificada que no modela la totalidad de retardos por recombinación bidimensional de un dispositivo físico real.

\subsection{Pregunta 4.4: Cálculo de $E_{\text{off}}$ y fracción atribuible a la corriente de cola}
\textbf{Enunciado:} \textit{«Calcule la energía de apagado ($E_{\text{off}}$) mediante la integral del producto $V_{CE} \cdot I_C$ durante el periodo de conmutación. ¿Qué porcentaje de esta energía total es atribuible exclusivamente al periodo de la corriente de cola?»}\\
\textbf{Respuesta Cuantitativa:}
\begin{itemize}[leftmargin=*, noitemsep, topsep=2pt]
  \item En LTspice, la integración gráfica directa (Ctrl + Clic en traza de potencia, Figura~\ref{fig:energia_ltspice}) confirmó $E_{\text{off}} = \bm{691.48\ \mu\text{J}}$ y potencia promedio de $134.27\text{ W}$, idéntico a la directiva \texttt{.meas}.
  \item N-IGBT (\texttt{XIRGBC20S}, $19\text{ A}$): $E_{\text{off}} = 691.5\ \mu\text{J}$; energía en cola $E_{\text{tail}} = 32.7\ \mu\text{J}$ ($4.73\%$).
  \item P-IGBT (\texttt{XPIGBT}, $40\text{ A}$): $E_{\text{off}} = 2115.3\ \mu\text{J}$; energía en cola $E_{\text{tail}} = 91.6\ \mu\text{J}$ ($4.33\%$).
  \item Fuji Trench-FS (\texttt{FGW50XS65}, $50\text{ A}$): $E_{\text{off}} = 1066.98\ \mu\text{J}$; bajo la convención del $5\%$, $E_{\text{tail}} = 4.68\ \mu\text{J}$ ($0.44\%$).
\end{itemize}

\subsection{Pregunta 4.5: Sobretensión inductiva y efecto del diodo integrado}
\textbf{Enunciado:} \textit{«Observe el comportamiento del voltaje colector-emisor ($V_{CE}$) durante el apagado e identifique el valor del pico de sobretensión causado por las inductancias parásitas. ¿Cómo varía este pico de voltaje al comparar los modelos con y sin diodo de marcha libre integrado?»}\\
\textbf{Respuesta Cuantitativa:} Con $L_\sigma = 25\text{ nH}$, el pico inductivo alcanzó $442.36\text{ V}$ a 50 A ($+42.36\text{ V}$ sobre el bus) y $445.98\text{ V}$ a 75 A ($+45.98\text{ V}$). El cálculo analítico $V_{L\sigma} = L_\sigma \cdot |di/dt|_{\max}$ predice $41.74\text{ V}$ (50 A) y $45.45\text{ V}$ (75 A), reproduciendo más del 98\% del sobreimpulso simulado, lo cual respalda la contribución dominante de la inductancia parásita de lazo sin constituir por sí sola una demostración exhaustiva de la totalidad del balance de tensiones. Al comparar los modelos discretos y co-pack (\texttt{FGW50XS65} vs \texttt{FGW50XS65C}), el pico de sobretensión resultó virtualmente indistinguible ($442.36\text{ V}$ con diferencias menores a $0.01\text{ V}$).\\
\textbf{Justificación Física:} En el circuito DPT de lado bajo, el diodo co-pack está polarizado en inversa ($V_C > 0 \implies V_{AK} < 0$) y no conduce corriente directa; la libre circulación la realiza el diodo superior $D_1$. En topologías de puente, este diodo asume el retorno reactivo, disipando pérdidas de conducción ($P_{\text{cond}} \approx V_F \cdot I_D$) e incrementando las pérdidas de encendido ($E_{\text{on}}$) de la rama por recuperación inversa ($Q_{rr}$).

\subsection{Pregunta 4.6: Efecto de duplicar la resistencia de compuerta ($R_G$)}
\textbf{Enunciado:} \textit{«Analice la relación entre la resistencia de compuerta ($R_G$) utilizada y el tiempo de retardo medido. Según sus resultados, ¿qué impacto tendría duplicar el valor de $R_G$ sobre las pérdidas por conmutación y la velocidad de respuesta del dispositivo?»}\\
\textbf{Respuesta Cuantitativa:} Al duplicar $R_G$ de $10\ \Omega$ a $20\ \Omega$ en el \texttt{FGW50XS65C}:
\begin{enumerate}[leftmargin=*, noitemsep, topsep=2pt]
  \item \textbf{Velocidad de respuesta:} En post-procesamiento con umbral dinámico de $V_{GE}$, el retardo $t_{d(\text{off})}$ aumenta de $231.09\text{ ns}$ a $361.60\text{ ns}$ (+56.5\%) ($+60.4\%$ bajo \texttt{.meas} con umbral fijo de $13.5\text{ V}$), mientras que el tiempo de caída $t_f$ se ensancha de $31.38\text{ ns}$ a $57.27\text{ ns}$ (+82.5\%).
  \item \textbf{Sobretensión:} La menor tasa de corte ($|di/dt|_{\text{max}}$ cae $-38.9\%$) reduce la sobretensión de $+42.36\text{ V}$ a $+25.94\text{ V}$ ($-38.8\%$).
  \item \textbf{Pérdidas de conmutación:} Las pérdidas $E_{\text{off}}$ se incrementan en $+70.5\%$ ($1066.98\ \mu\text{J} \to 1818.73\ \mu\text{J}$).
\end{enumerate}

% ------------------- REFERENCIAS -------------------
\vspace{-2pt}
\section{Referencias Bibliográficas}
{\small
\begin{enumerate}[leftmargin=*, itemsep=0.5pt, topsep=1pt, parsep=0pt]
  \item \textbf{Adanaqué Infante, L.} (2026). \textit{Laboratorio Dirigido Nro. 03: IGBTs}. Guía de laboratorio de Microelectrónica y Sistemas Nanoelectrónicos, FIEE, Universidad Nacional Mayor de San Marcos (UNMSM).
  \item \textbf{International Rectifier.} (1998). \textit{IRGBC20S: Standard Speed IGBT ($V_{CES} = 600\text{ V}, I_C = 19\text{ A}$)}. Hoja de datos Farnell Document 68617.
  \item \textbf{Fuji Electric Co., Ltd.} (2020). \textit{FGW50XS65 / FGW50XS65C: 650V / 50A Trench Field-Stop IGBT (Serie X de 7.\textsuperscript{a} generación)}. Hoja de datos y librería de macromodelos SPICE.
  \item \textbf{Fuji Electric Co., Ltd.} (2020). \textit{FGW75XS65 / FGW75XS65C: 650V / 75A Trench Field-Stop IGBT (Serie X de 7.\textsuperscript{a} generación)}. Hoja de datos y librería de macromodelos SPICE.
  \item \textbf{Duncan, S.} (1995). \textit{SPICE Macromodels for Insulated Gate Bipolar Transistors (NIGBT \& PIGBT)}. Duncan's Amp Pages.
  \item \textbf{Baliga, B. J.} (2015). \textit{The IGBT Device: Physics, Design and Applications of the Insulated Gate Bipolar Transistor}. William Andrew Publishing / Elsevier, Oxford, UK.
  \item \textbf{International Electrotechnical Commission.} (2019). \textit{IEC 60747-9: Semiconductor devices - Discrete devices - Part 9: Insulated-gate bipolar transistors (IGBTs)}. Standard Measurement Methods.
\end{enumerate}
}

\end{document}
'''

tex_file = os.path.abspath('LD3_Yactayo/informe/informe_ld3_yactayo.tex')
with open(tex_file, 'w', encoding='utf-8') as f:
    f.write(tex_content)
print(f'Archivo TeX escrito exitosamente: {tex_file}')

informe_dir = os.path.dirname(tex_file)
print(f'Compilando en: {informe_dir}')

# Pasada 1
res1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'informe_ld3_yactayo.tex'], cwd=informe_dir, capture_output=True, text=True)
print(f'Pasada 1 Returncode: {res1.returncode}')

# Pasada 2
res2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'informe_ld3_yactayo.tex'], cwd=informe_dir, capture_output=True, text=True)
print(f'Pasada 2 Returncode: {res2.returncode}')

pdf_path = os.path.join(informe_dir, 'informe_ld3_yactayo.pdf')
if os.path.exists(pdf_path):
    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f'PDF generado exitosamente: {pdf_path} ({size_mb:.2f} MB)')
else:
    print('Error: PDF no encontrado. Salida de compilación:')
    print(res2.stdout[-1000:])
