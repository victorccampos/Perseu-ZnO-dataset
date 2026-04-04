from pathlib import Path
import dpdata
import random


def get_IO_pairs(pwi_dir: str, pwo_dir: str) -> list[list[str, str]]:
    """
    Monta os pares file_name onde file_name é uma lista cujo primeiro elemento é
    o nome input file e o segundo é o nome do output file.
    Docs deepdata.LabeledSystem:
        #https://docs.deepmodeling.com/projects/dpdata/en/latest/api/dpdata.html#dpdata.LabeledSystem
    """
    pwi_dir = Path(pwi_dir)
    pwo_dir = Path(pwo_dir)

    # ---
    # Ordenação deles
    in_files = sorted(pwi_dir.glob("*.in"))
    out_files = sorted(pwo_dir.glob("*.out"))

    pairs = [[str(in_f), str(out_f)] for in_f, out_f in zip(in_files, out_files)]
    return pairs


def build_multisystem(
    pairs: list[list[str, str]], data_name: str
) -> dpdata.MultiSystems:
    """Pega cada par de I/O do QE (frames) e transforma em um LabeledSystem.
    Cada LabeledSystem é adicionado a um MultiSystem e é retornado esse objeto
    com todos os frames.
    Args:
        pairs: lista de inputs e outputs. Ex: [[01.in, 01.out], [02.in, 02.out]]
        data_name: nome da pasta. Ex: validation_data, training_data.
    Uso:
        ms_train = build_multisystem(training_pairs, "training_data")
        ms_validation = build_multisystem(validation_pairs, "validation_data")

    """
    ms = dpdata.MultiSystems()
    for p in pairs:
        try:
            s = dpdata.LabeledSystem(p, fmt="qe/pw/scf")
            ms.append(s)
        except Exception as e:
            print(f"{' IO FAILED ':=^100}")
            print(f"IN: {p[0]}")
            print(f"OUT: {p[1]}")
            print(f"\tERROR: {e}")

    print("Sistema\n", ms)
    n_frames = ms.get_nframes()
    print(f"Saving system in {data_name} with {n_frames = }")
    ms.to("deepmd/npy", data_name, set_size=n_frames)


def split_train_validation(all_pairs: list[list[str, str]]) -> list[list[str, str]]:
    random.seed(42)
    split_idx = int(0.80 * len(all_pairs))

    train_pairs = all_pairs[:split_idx]
    val_pairs = all_pairs[split_idx:]
    print(f"TAMANHO CONJUNTO DE TREINO: {len(train_pairs)}")
    print(f"TAMANHO CONJUNTO DE VALIDAÇÃO: {len(val_pairs)}")
    return train_pairs, val_pairs


if __name__ == "__main__":
    # --- Inputs e Outputs
    data_dir = "/home/jvc/ZnO_database/data"

    LDA_000_INPUTS = f"{data_dir}/LDA_000_INPUTS"
    LDA_000_OUTPUTS = f"{data_dir}/LDA_000_OUTPUTS"

    LDA_004_INPUTS = f"{data_dir}/LDA_004_INPUTS"
    LDA_004_OUTPUTS = f"{data_dir}/LDA_004_OUTPUTS"

    LDA_006_INPUTS = f"{data_dir}/LDA_006_INPUTS"
    LDA_006_OUTPUTS = f"{data_dir}/LDA_006_OUTPUTS"

    LDA_012_INPUTS = f"{data_dir}/LDA_012_INPUTS"
    LDA_012_OUTPUTS = f"{data_dir}/LDA_012_OUTPUTS"

    pairs_000 = get_IO_pairs(pwi_dir=LDA_000_INPUTS, pwo_dir=LDA_000_OUTPUTS)
    pairs_004 = get_IO_pairs(pwi_dir=LDA_004_INPUTS, pwo_dir=LDA_004_OUTPUTS)
    pairs_006 = get_IO_pairs(pwi_dir=LDA_006_INPUTS, pwo_dir=LDA_006_OUTPUTS)
    pairs_012 = get_IO_pairs(pwi_dir=LDA_012_INPUTS, pwo_dir=LDA_012_OUTPUTS)

    all_pairs = pairs_000 + pairs_004 + pairs_006 + pairs_012

    # Gerando o dataset de treinamento e validação
    train_pairs, val_pairs = split_train_validation(all_pairs)

    print("=" * 100)
    print(f"CONJUNTO DE TREINAMENTO:\n{train_pairs}\n")
    print(f"CONJUNTO DE VALIDAÇÃO:\n{val_pairs}\n")
    print("=" * 100)
    print()

    print("Creating directorys")
    build_multisystem(train_pairs, "training_data")
    build_multisystem(val_pairs, "validation_data")
    print("=" * 100)
