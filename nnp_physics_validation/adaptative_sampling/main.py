from qe_interface import write_pwscf_input_frames, run_qe_frames
from adaptative_sampling import write_xsf_output_frames
from pathlib import Path


if __name__ == "__main__":
    md_trajectory = "../thermal_expansion/100K/trajectories/ZnO-222-100K.lammpstrj"
    
    espresso_dir = Path("PWSCF-222-100K/")
    
    write_pwscf_input_frames(lammspstraj=md_trajectory, directory=espresso_dir)
    
    
    run_qe_frames(espresso_dir, np=16, num_files=10, run_every=2)
        
    convert_xsf = input("Convert XSF files? [yes | no]\n")    
    
    if convert_xsf == "yes":
        write_xsf_output_frames(espresso_dir=espresso_dir)

    
