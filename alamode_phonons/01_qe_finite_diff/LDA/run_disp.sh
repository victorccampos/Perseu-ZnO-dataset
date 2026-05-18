#!/usr/bin/env bash
JOBNAME="Phonon (QE + ALAMODE)"

NP=64
NK=8
PWX=pw.x
for infile in disp*.pw.in; do
    [ -e "$infile" ] || { echo "Nenhum arquivo disp*.pw.in encontrado."; exit 1; }

    outfile="${infile%.in}.out"

    echo "RUN : [$(date "+%a %d %b %Y %H:%M:%S")]: $infile -> $outfile "
    mpirun -np "$NP" "$PWX" -nk "$NK" < "$infile" > "$outfile"
    echo "DONE: [$(date "+%a %d %b %Y %H:%M:%S")]"
    echo 
done

# NOTIFICAÇÃO DE TÉRMINO
SCRIPT_DIR="$HOME/ZnO_database/scripts"
EMAIL_SCRIPT="$SCRIPT_DIR/send_email.py"

cd "$SCRIPT_DIR" || { echo "Erro ao acessar $SCRIPT_DIR"; exit 1; }

echo "Enviando notificação de término..."
python "$EMAIL_SCRIPT" "$JOBNAME finished!"