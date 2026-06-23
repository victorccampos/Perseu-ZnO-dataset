import subprocess
from pathlib import Path


def executar_jobs_qe(
    espresso_dir: str | Path, np: int, num_files: None | int = None, run_every: int = 1
):
    """
    Args:
        espresso_dir (str | Path): Diretório contendo os arquivos de entrada do Quantum ESPRESSO.
        np (int): Número de processos a serem utilizados na execução paralela.

    """
    espresso_dir = Path(espresso_dir)

    if not espresso_dir.exists() or not espresso_dir.is_dir():
        print(f"Erro: O diretório '{espresso_dir}' não foi encontrado.")
        return

    # Itera sobre todos os arquivos com a extensão definida no diretório
    arquivos_entrada = sorted(espresso_dir.glob("*.in"))

    if not arquivos_entrada:
        print(f"Nenhum arquivo '.in' encontrado em {espresso_dir}.")
        return
    arquivos_entrada = arquivos_entrada[:num_files:run_every]
    for pwi in arquivos_entrada:
        pwo = pwi.with_suffix(".out")

        print(f"[{pwi.name}] Iniciando execução...")
        comando = ["mpirun", "-np", str(np), "pw.x"]

        with open(pwi, "r") as f_in, open(pwo, "w") as f_out:
            try:
                subprocess.run(comando, stdin=f_in, stdout=f_out, check=True)
                print(
                    f"[{pwi.name}] Finalizado com sucesso. Saída salva em: {pwo.name}"
                )

            except subprocess.CalledProcessError as e:
                print(
                    f"[{pwi.name}] Erro durante a execução. Código de saída: {e.returncode}"
                )

            except FileNotFoundError:
                print(
                    "Erro: Comando 'mpirun' ou 'pw.x' não encontrado. Verifique suas variáveis de ambiente."
                )
                break
