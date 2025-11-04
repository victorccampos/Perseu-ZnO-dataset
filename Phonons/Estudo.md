# 1. Padrões de Deslocamentos com alm

No cabeçalho do `alm.in`, algumas seções importantes:
> MODE = suggest  
> &interaction NORDER = 1

_NORDER = 1_ significa aproximação harmônica, i.e, $U \propto x^2$.

```bash
$ alm alm_si.in > alm_si.log1 
```

No final do arquio `alm_si.log1` temos a info:

```
 Number of disp. patterns for  HARMONIC : 1

 Suggested displacement patterns are printed in the following files: 
  HARMONIC : si222.pattern_HARMONIC


 Job finished at Sat Nov  1 11:16:56 2025
```

O que significa que temos apenas UM padrão de deslocamento para IFCs *harmônica*.
Esse "modo" ficou salvo no arquivo `${PREFIX}.pattern_HARMONIC`.


    Check number of displacements of the output:  
    
    $ grep "Number of disp." alm_si.log1


# 2. Cálculo das Forças Atômicas nas cofigurações geradas no passo 1.

Nesse passo decide-se um $\Delta u$ (~ 0.01 Angstroms para regime harmônico) e a partir
desse $\Delta u$ cria-se os inputs para os cálculos autoconsistentes do DFT (PWscf).

O __ALAMODE__ tem uma interface direta com o __Quantum ESPRESSO__.

```bash
$ python displace.py --QE=si222.pw.in --mag=0.01 -pf si222.pattern_HARMONIC
```

O `displace.py` gerar os arquivos de input necessários.

Nesse passo aqui, é necessário fornecer um arquivo de Input para o --QE={pwi.in}!!!.
No tutorial, ele está no diretório de referência: 

DIR: `https://github.com/ttadano/alamode/blob/develop/example/Si/reference/si222.pw.in`

Além disso, deve-se baixar o pseudopotencial do Si do Exemplo:  

```bash
$ wget https://pseudopotentials.quantum-espresso.org/upf_files/Si.pz-n-kjpaw_psl.0.1.UPF
```

Se tudo ocorreu bem, o Terminal parecerá com isso:

```bash
(alamode) jvc@perseu:~/alamode/example/Si$ python ../../tools/displace.py --QE=si222.pw.in --mag=0.01 -pf si222.pattern_HARMONIC
*****************************************************************
    displace.py --  Generator of displaced configurations        
                      Version. 1.2.1                             
*****************************************************************

 Output format                  : Quantum-ESPRESSO pw.in format
 Structure before displacements : si222.pw.in
 Output file names              : disp{counter}.pw.in
 Magnitude of displacements     : 0.01 Angstrom
 Number of atoms                : 64

 Displacement mode              : Finite displacement

 1 displacement pattern are generated from
 the given *.pattern_* files

 Number of displacements        : 1
-----------------------------------------------------------------

All input files are created.
```

É instrutivo ver as diferenças entre o `pwi.in` fornecido em --QE= e os arquivos
disp{counter}.in gerados com:

$ diff `pwi.in` `disp{counter}.in`


Agora, rodamos uma conta scf com os arquivos `disp{}.in` gerados com o programa `displace.py`.

Assim que as contas são concluídas, os `disp{}.out` são processados com auxílio da tool `extract.py`:


```bash
$python ../../tools/extract.py --QE=si222.pw.in *.pw.out > DFSET_harmonic
```
E cria-se o arquivo `DFSET_harmonic`, _"displacement-force data sets"_ cujo formato é:

> Estrutura 1:
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtable displaystyle="true" columnalign="right center left right center left" columnspacing="0em 0.278em 0em 0.278em 0em" rowspacing="3pt">
    <mtr>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>2</mn>
        <mo stretchy="false">)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd></mtd>
      <mtd>
        <mi></mi>
        <mrow data-mjx-texclass="ORD">
          <mo>&#x22EE;</mo>
        </mrow>
      </mtd>
      <mtd></mtd>
      <mtd></mtd>
      <mtd>
        <mi></mi>
        <mrow data-mjx-texclass="ORD">
          <mo>&#x22EE;</mo>
        </mrow>
      </mtd>
      <mtd></mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mrow data-mjx-texclass="ORD">
          <mi data-mjx-auto-op="false">NAT</mi>
        </mrow>
        <mo stretchy="false">)</mo>
      </mtd>
    </mtr>
  </mtable>
</math>
> Estrutura 2:
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mtable displaystyle="true" columnalign="right center left right center left" columnspacing="0em 0.278em 0em 0.278em 0em" rowspacing="3pt">
    <mtr>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>u</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>x</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>y</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
      <mtd>
        <msub>
          <mi>f</mi>
          <mrow data-mjx-texclass="ORD">
            <mi>z</mi>
          </mrow>
        </msub>
        <mo stretchy="false">(</mo>
        <mn>1</mn>
        <mo stretchy="false">)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd></mtd>
      <mtd>
        <mi></mi>
        <mrow data-mjx-texclass="ORD">
          <mo>&#x22EE;</mo>
        </mrow>
      </mtd>
      <mtd></mtd>
      <mtd></mtd>
      <mtd>
        <mi></mi>
        <mrow data-mjx-texclass="ORD">
          <mo>&#x22EE;</mo>
        </mrow>
      </mtd>
      <mtd></mtd>
    </mtr>
  </mtable>
</math>

- NAT : número de átomos na Supercélula
- Unidades de deslocamento e força em Bohr e Ry/bohr, respectivamente.

Esse arquivo criado servirá para __estimar as constantes de força interatômicas__ (IFCs).

# 3. Ajuste das constantes de forças via alm.in + DFSET

É feito uma otimização, _least-square fitting_ adicionando a seção ao `alm.in`:

    &optimize
        DFSET = DFSET_harmonic

e agora, ao invés de sugerir os padrões de deslocamento _MODE = suggest_, agora alteramos para:

    &general
    MODE = optimize 


São criados dois novos arquivos:

    Force constants in a human-readable format : si222.fcs
    Input data for the phonon code ANPHON      : si222.xml


Executamos com:

    $ alm alm_opt.in > alm_opt.log2

No `alm_opt.log2` podemos trackear o erro com :

    $ grep "Fitting error" alm_opt.log2

Dos arquivos criados, o que será utilizado em seguida é o `si222.xml`!

O Quantum ESPRESSO gerou um _outro_ arquivo xml, com prefix diferente (`si`)!! Não confundir os dois `si.xml` (QE) $\ne$ `si222.xml` (ALAMODE).

# 4. Dispersão de Fônons e DOS.

Precisamos preparar agora um _input_ para o cálculo de __dispersão de fônons__. Agora, usamos o programa `anphon`.


Na seção `&general`, adicionamos dois campos:

- MASS   (massa do Silício)
- FCSXML (o _xml_ gerado no passo anterior)

Definimos em `&cell` agora, os vetores da `célula primitiva`!.

Diremos que se trata de um cálculo de dispersão de fônons ao colocar:

    &general
    ...
    MODE = phonons
    ...
    /

    &kpoint
    1 # KPMODE = 1 : line mode
    # Pontos de Alta Simetria (reciprocal path).
    /
O KPMODE pode ser 1, modo de linha que o caminho na BZ é escrito por extenso:

    G 0.0 0.0 0.0 X 0.5 0.5 0.0 51
    X 0.5 0.5 1.0 G 0.0 0.0 0.0 51
    G 0.0 0.0 0.0 L 0.5 0.5 0.5 51

ou com KPMODE=2, que é um mesh uniform.

    20 20 20

Executamos a conta para a __dispersão de fônons__ com:

     anphon si_phononband.in > si_phononband.log

As bandas serão armazenadas no arquivo `$(PREFIX).bands = si222.bands`.

Pode usar o tool `plotband.py` para ver as bandas.
