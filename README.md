# ML-MCTDH-Aid

The purpose of the development of the ML-MCTDH-Aid suit is to set up a freely available, open-source code to support the efficient and effective simulation of the quantum dynamics using the ML-MCTDH method provided in the Heidelberg package. Particularly, this project largely extends the practical usage of the ML-MCTDH method in the treatment of the nonadiabatic dynamics of the high-dimensional linear-vibronic-coupling models. The package is composed of several highly modular components. To maximize the functional independence of each part, the entire code is well-divided into four parts, namely, a model Hamiltonian construction tool, a tree structure generation tool, a tree optimization program tool, and the basis number modification tool. During execution, each part of the code shares the same simple input files, making the whole suit easy to use.

Examples are given in the 'examples' directory.

The brief introduction are given below.
1. The generation of .inp and .op files
    After preparing the files: config.json  kappa.dat  omega_eV.dat  vmat.dat, run 'python /path/to/gener_inp_op.py' to generate .inp and .op files.
    Examples are given in examples/gener_inp_op. You can follow it to prepare input files.

2. Convergence
    After a ML-MCTDH calculation, you can run 'python /path/to/cvg_gener_inp.py' to generate a new .inp file.
    An example is given in examples/convergence/anthracene_C60/a. Go into it, and run the script you can get a .inp file named a-1.inp.

3. Tree optimization
    After a ML-MCTDH calculation, you can run 'python /path/to/tree_opt.py' to generate a new .inp file with optimized tree structure.
    An example is given in examples/tree_opt/site_exciton/a. Go into it and run the script you can get a .inp file named a_opt-1.inp.
