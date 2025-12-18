import numpy as np
from itertools import product


from pathlib import Path
import subprocess
from datetime import date, datetime

from pprint import pprint


def run_qe_jobs(
    input_files: list[Path],
    output_dir: Path,
    num_processes: int,
    npools: int,
    ndiag: int,
    executable_path: Path | None = None
) -> None:
    """
    Executa múltiplos jobs do Quantum ESPRESSO (pw.x) em sequência.

    Args:
        input_files (List[Path]): Lista de caminhos para arquivos .in.
        output_dir (Path): Diretório onde os .out serão salvos.
        num_processes (int): Número de processos MPI.
        npools (int): Número de pools de FFT.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    exe = str(executable_path.expanduser()) if executable_path else "pw.x"

    for input_path in input_files:
        output_path = output_dir / input_path.with_suffix('.out').name
        command_line = [
            "mpirun", "-np", str(num_processes),
            exe, "-npools", str(npools), "-nd", str(ndiag),
            "-in", str(input_path)
        ]

        try:
            with output_path.open(mode='w') as f_out:
                subprocess.run(command_line, check=True, stdout=f_out, stderr=subprocess.STDOUT)

            print(f"Job completed: {input_path.name} "
                  f"-- {date.today()} {datetime.now().strftime('%H:%M:%S')}")

        except subprocess.CalledProcessError as e:
            print(f"Failed: {input_path.name} -> {e}")
        except subprocess.TimeoutExpired:
            print(f"Timeout: {input_path.name}")
        except Exception as e:
            print(f"Unexpected error: {input_path.name} -> {e}")

def sort_by_supercell(irreducible_sc_shapes, pw_inputs: list[Path]):
    supercells_to_run: list[Path] = []    
    for arr in irreducible_sc_shapes:
        nx, ny, nz = arr
        cellsize= str(nx) + str(ny) + str(nz) # Ex: '111'
        group: list[Path] = [pw_input for pw_input in pw_inputs if cellsize in pw_input.name]    
        supercells_to_run.extend(group)
    return supercells_to_run

def get_irreducible_sc_shapes() -> list[np.ndarray]:
    values = [1, 2, 3]

    # Combinações (nx, ny, nz)
    combinations = [
        np.array([nx, ny, nz])
        for nx, ny, nz in product(values, values, values)
        if nx >= ny  # condição de simetria reduzida
    ]

    # Ordena pelo produto nx * ny * nz
    combinations.sort(key=lambda x: np.prod(x))
    return combinations

if __name__ == '__main__':
    INPUT_DIR = Path('crystalline_structures.in')
    OUTPUT_DIR = INPUT_DIR.with_suffix('.out')
    # MPIRUN 
    PW_BINARY = Path('~/pw_intel.x')
    NP = 32
    NPOOLS = 8
    NDIAG = 4
    
    input_files = sorted([ f for f in INPUT_DIR.iterdir() if f.is_file() \
        and f.name.endswith(".in") ])
 
    supercells_shapes: list[np.ndarray] = get_irreducible_sc_shapes()

    supercells_to_run: list[Path] = sort_by_supercell(
        irreducible_sc_shapes=supercells_shapes,pw_inputs=input_files
    )
 
      
    run_qe_jobs(supercells_to_run, OUTPUT_DIR,
     num_processes=NP, npools=NPOOLS, ndiag=NDIAG, executable_path=PW_BINARY
    )
    

"""
[1 1 1] → multiplicidade: 1 -> num.atomos 4
[1 1 2] → multiplicidade: 2 -> num.atomos 8
[2 1 1] → multiplicidade: 2 -> num.atomos 8
[1 1 3] → multiplicidade: 3 -> num.atomos 12
[3 1 1] → multiplicidade: 3 -> num.atomos 12
[2 1 2] → multiplicidade: 4 -> num.atomos 16
[2 2 1] → multiplicidade: 4 -> num.atomos 16
[2 1 3] → multiplicidade: 6 -> num.atomos 24
[3 1 2] → multiplicidade: 6 -> num.atomos 24
[3 2 1] → multiplicidade: 6 -> num.atomos 24
[2 2 2] → multiplicidade: 8 -> num.atomos 32
[3 1 3] → multiplicidade: 9 -> num.atomos 36
[3 3 1] → multiplicidade: 9 -> num.atomos 36
[2 2 3] → multiplicidade: 12 -> num.atomos 48
[3 2 2] → multiplicidade: 12 -> num.atomos 48
[3 2 3] → multiplicidade: 18 -> num.atomos 72 -> Aqui começa a demorar com 32 procs
[3 3 2] → multiplicidade: 18 -> num.atomos 72
[3 3 3] → multiplicidade: 27 -> num.atomos 108
"""