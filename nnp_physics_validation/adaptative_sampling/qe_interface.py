"""
Script to interface Quantum Espresso with ASE for adaptative sampling.

Config general PWSCF parameters, espresso profiles and calculators.
"""

from ase import Atoms, io


from pathlib import Path
import subprocess


PSEUDODIR = "/home/jvc/nnp_physics_validation/pseudopotentials/"
PSEUDOPOTENTIALS = {
    "Zn": "Zn_pseudo-dojo_NC_SR_LDA.upf",
    "O": "O_pseudo-dojo_NC_SR_LDA.upf",
}

INPUT_DATA = {
    "control": {
        "calculation": "scf",
        "prefix": "ZnO_LDA",
        "pseudo_dir": f"{PSEUDODIR}",
        "outdir": "./",
        "disk_io": "none",
        "verbosity": "high",
        "tprnfor": True,
        "tstress": True,
    },
    "system": {"ibrav": 0, "ecutwfc": 80, "ecutrho": 320, "occupations": "fixed"},
    "electrons": {"conv_thr": 1e-8, "mixing_beta": 0.3},
}


def write_pwscf_input_frames(lammpstraj: str, directory=".") -> None:
    Path(directory).mkdir(exist_ok=True)
    frames: list[Atoms] = io.read(
            filename=lammpstraj,
            format="lammps-dump-text",
            index=":",
            specorder=["Zn", "O"],
        )

    assert_error = "All frames must have 32 atoms due to computational resources."
    assert all([len(frame) == 32 for frame in frames]), assert_error

    for i, image in enumerate(frames):
        io.write(
            f"{directory}/frame_pwscf_{i:03d}.in",
            image,
            format="espresso-in",
            input_data=INPUT_DATA,
            pseudopotentials=PSEUDOPOTENTIALS,
            kpts=(3, 3, 2),
            crystal_coordinates=True,
        )

    return None


def run_qe_frames(espresso_dir: str | Path, np: int = 16, num_files=None, run_every=1):
    espresso_dir = Path(espresso_dir)

    if not espresso_dir.exists() or not espresso_dir.is_dir():
        print(f"Erro: O diretório '{espresso_dir}' não foi encontrado.")
        return

    arquivos_entrada = sorted(espresso_dir.glob("*.in"))

    if not arquivos_entrada:
        print(f"Nenhum arquivo '.in' encontrado em {espresso_dir}.")
        return
    
    arquivos_entrada = arquivos_entrada[:num_files:run_every]
    filenames = [f.name for f in arquivos_entrada]
    
    run = input(f"Run the following files?\n{filenames}\nOPTIONS: yes | no\n")
    if run == "yes":
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
    else:
        print("Skipped running files. Moving to next step.\n")


if __name__ == "__main__":
    write_pwscf_input_frames(lammpstraj="trajectory_100K.lammpstrj")
