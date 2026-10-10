import os

# Crear DPT_NIGBT_nom.asc a partir de DPT_NIGBT.asc
with open('LD3_Yactayo/esquemas/DPT_NIGBT.asc', 'r', encoding='latin1') as f:
    content_n = f.read()

content_n_nom = content_n.replace(
    'PWL(0 0 10u 0 10.1u 15 30u 15 30.1u 0 35u 0 35.1u 15 36u 15 36.1u 0 60u 0)',
    'PWL(0 0 10.0u 0 10.1u 15 13.65u 15 13.75u 0 18.75u 0 18.85u 15 19.85u 15 19.95u 0 30.0u 0)'
).replace(
    '.tran 0 60u 0 25n uic',
    '.tran 0 30u 0 5n uic'
).replace(
    ';N-IGBT',
    ';N-IGBT Nominal (19A)'
)

with open('LD3_Yactayo/esquemas/DPT_NIGBT_nom.asc', 'w', encoding='latin1') as f:
    f.write(content_n_nom)

# Crear DPT_PIGBT_nom.asc a partir de DPT_PIGBT.asc
with open('LD3_Yactayo/esquemas/DPT_PIGBT.asc', 'r', encoding='latin1') as f:
    content_p = f.read()

content_p_nom = content_p.replace(
    'PWL(0 0 10u 0 10.1u 15 30u 15 30.1u 0 35u 0 35.1u 15 36u 15 36.1u 0 60u 0)',
    'PWL(0 0 10.0u 0 10.1u 15 18.88u 15 18.98u 0 23.98u 0 24.08u 15 25.08u 15 25.18u 0 35.0u 0)'
).replace(
    '.tran 0 60u 0 25n uic',
    '.tran 0 35u 0 5n uic'
).replace(
    ';PIGBT',
    ';P-IGBT Nominal (40A)'
)

with open('LD3_Yactayo/esquemas/DPT_PIGBT_nom.asc', 'w', encoding='latin1') as f:
    f.write(content_p_nom)

print("Esquemas nominales DPT_NIGBT_nom.asc y DPT_PIGBT_nom.asc creados exitosamente.")
