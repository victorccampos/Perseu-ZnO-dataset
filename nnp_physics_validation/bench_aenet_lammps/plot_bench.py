import matplotlib.pyplot as plt
import re
import os

# --- CONFIGURAÇÃO ---
# Subtitua pelo nome do seu arquivo de texto
NOME_ARQUIVO = "benchmark_result.txt" 
# ---------------------

processors = []
wall_times_minutes = []

# Verifica se o arquivo realmente existe no diretório atual
if not os.path.exists(NOME_ARQUIVO):
    print(f"Erro: O arquivo '{NOME_ARQUIVO}' não foi encontrado no diretório atual.")
    print(f"Diretório atual: {os.getcwd()}")
else:
    # Lendo o arquivo linha por linha
    with open(NOME_ARQUIVO, 'r', encoding='utf-8') as file:
        for line in file:
            # Regex para capturar o número de procs e o tempo (H:M:S)
            match = re.search(r'(\d+)\.procs\.out:Total wall time: (\d+):(\d+):(\d+)', line)
            if match:
                procs = int(match.group(1))
                hours = int(match.group(2))
                minutes = int(match.group(3))
                seconds = int(match.group(4))
                
                # Converte o tempo total para minutos
                total_minutes = (hours * 60) + minutes + (seconds / 60.0)
                
                processors.append(procs)
                wall_times_minutes.append(total_minutes)

    # Verifica se conseguimos extrair dados antes de plotar
    if not processors:
        print("Aviso: Nenhum dado foi extraído. Verifique se o formato das linhas no arquivo está idêntico ao padrão.")
    else:
        # Ordenar os dados de forma crescente pelo número de processadores
        sorted_data = sorted(zip(processors, wall_times_minutes))
        processors, wall_times_minutes = zip(*sorted_data)

        # --- Criação do Gráfico ---
        plt.figure(figsize=(9, 5))
        plt.plot(processors, wall_times_minutes, marker='o', color='#2ca02c', linestyle='-', linewidth=2, markersize=8)

        # Customização do Layout
        plt.title('Benchmark LAMMPS + ænet (ZnO)', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Número de Processadores (MPI)', fontsize=11)
        plt.ylabel('Tempo de Execução (Minutos)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(processors)  # Força exibir todos os pontos de cores testados no eixo X

        # Adiciona rótulos com os tempos exatos acima de cada ponto
        for x, y in zip(processors, wall_times_minutes):
            plt.text(x, y + 0.3, f"{y:.1f} min", ha='center', va='bottom', fontsize=9, fontweight='semibold')

        plt.tight_layout()
        
        # Opcional: Salva o gráfico como imagem antes de exibir
        plt.savefig('scaling_curve.png', dpi=300)
        
        plt.show()
