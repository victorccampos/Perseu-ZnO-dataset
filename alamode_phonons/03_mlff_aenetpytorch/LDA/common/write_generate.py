from pathlib import Path


template = """OUTPUT  ZnO_LDA.train

TYPES
2
Zn    -5683.175154809524  ! eV
O     -439.95272806294315 ! eV

SETUPS
Zn  '/home/victorcampos/aenet-PyTorch/DatasetLDA/models/common/Zn.fingerprint.stp'
O  '/home/victorcampos/aenet-PyTorch/DatasetLDA/models/common/O.fingerprint.stp'

FORCES
{force_percent}

FILES
"""


def write_generate(template_string, force_percent, xsf_dirs):
    filename = f"GENERATE_{force_percent}.in"


    all_files: list[str] = [str(file) for d in xsf_dirs for file in sorted(d.glob("*.xsf"))]
    
    content = template_string.format(force_percent=force_percent)
    num_files = len(all_files)
    
    print(f"Writing generate with {num_files} files.")
    
    with open(filename, "w") as fp:
        
        fp.write(content)

        # Número de arquivos
        fp.write(f"{num_files}\n")
        
        # Caminhos absolutos
        for file in all_files:
            fp.write(file + "\n")

    return
        


if __name__ == "__main__":
    data = Path("/home/victorcampos/aenet-PyTorch/DatasetLDA/data")
    traininig = data / "dataset" / "train"  
    subsets_names = [
        "LDA_118_XSF",
        "LDA_214_XSF",
        "LDA_333_XSF",
        "LDA_normal_modes_3x3x3",
    ]

    subsets: list[Path] = [data / f"subsets/{s}" for s in subsets_names]
    xsf_data: list[Path] = [traininig, *subsets]

    
    

    
    write_generate(
        template_string=template,
        force_percent="15",
        xsf_dirs=xsf_data
    )


