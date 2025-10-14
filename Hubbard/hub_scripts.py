from pathlib import Path
import numpy as np
import re

# Caminho do arquivo de template
template_path = Path("ZnO_Hub.in")

# Leitura do conteúdo original
template = template_path.read_text()

# Criação dos arrays de U para Zn e O
Zn_U_values = np.arange(4.0, 12.5, 0.5)  # 4 até 12 inclusive
O_U_values  = np.arange(4.0, 12.5, 0.5)

# Diretório de saída
output_dir = Path("hub_inputs")
output_dir.mkdir(exist_ok=True)

# Loop duplo para gerar todas as combinações
for Zn_U in Zn_U_values:
    for O_U in O_U_values:
        # Substitui os valores originais de U no template
        new_input = template
        new_input = re.sub(r"U\s+Zn-3d\s+[\d.]+", f"U Zn-3d {Zn_U:.2f}", new_input)
        new_input = re.sub(r"U\s+O-2p\s+[\d.]+",  f"U O-2p {O_U:.2f}",  new_input)

        # Nome do arquivo de saída
        out_name = f"ZnO_Hub_{Zn_U:.2f}_{O_U:.2f}.in"
        (output_dir / out_name).write_text(new_input)

print(f"Arquivos gerados em: {output_dir.resolve()}")
