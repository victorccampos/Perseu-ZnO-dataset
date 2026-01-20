INPUT_DATA_LDA = {
    "control": {
        "calculation": "scf",
        "prefix": "ZnO_LDA",
        "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_LDA/",
        "outdir": "./",
        "disk_io": "none",
        "verbosity": "high",
        "tprnfor": True
    },
    "system": {
        "ibrav": 0,
        "ecutwfc": 80,
        "ecutrho": 320,
        "occupations": "fixed"
    },
    "electrons": {
        "conv_thr": 1.0e-8,
        "mixing_beta": 0.3
    }
}


INPUT_DATA_PBE = {
    "control": {
        "calculation": "scf",
        "prefix": "ZnO_LDA",
        "pseudo_dir": "/home/jvc/ZnO_database/pseudos/ppdojo_PBE/",
        "outdir": "./",
        "disk_io": "none",
        "verbosity": "high",
        "tprnfor": True
    },
    "system": {
        "ibrav": 0,
        "ecutwfc": 80,
        "ecutrho": 320,
        "occupations": "fixed"
    },
    "electrons": {
        "conv_thr": 1.0e-8,
        "mixing_beta": 0.3
    }
}
