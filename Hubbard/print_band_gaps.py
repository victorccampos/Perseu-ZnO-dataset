from pathlib import Path
import re

# Diretório onde estão os outputs do QE
output_dir = Path("./hub_outputs")  # altere se necessário

# Arquivo de saída com os resultados
results_file = output_dir / Path("bandgaps.dat")

# Expressão regular para encontrar os níveis de energia
pattern = re.compile(
    r"highest\s+occupied,\s+lowest\s+unoccupied\s+level\s*\(ev\)\s*:\s*([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)"
)

results = []

# Loop por todos os arquivos .out
for file in sorted(output_dir.glob("*.out")):
    text = file.read_text(errors="ignore")
    matches = pattern.findall(text)
    if matches:
        # Se houver múltiplas ocorrências, usa a última (resultado final)
        ho, lu = map(float, matches[-1])
        band_gap = lu - ho
        results.append((file.stem, band_gap))
    else:
        print(f"Aviso: não encontrou níveis em {file.name}")

# Ordena os resultados pelo valor crescente do band gap
results.sort(key=lambda x: x[1])

# Salva os resultados em duas colunas: nome e band_gap
with results_file.open("w") as f:
    for name, gap in results:
        #f.write(f"{name:<30s} {gap:10.4f}\n")
        f.write(f"{name},{gap:.4f}\n")

print(f"✅ {len(results)} resultados salvos em {results_file.resolve()} (ordenados por band gap crescente)")
