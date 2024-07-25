
def generInp(
        inp_name = "a",
        op_name = "a",
        tfinal = 120.0,
        tout = 0.25,
        nstate = 3,
        nmode = 90,
    ):
    kmax = 10
    input_file = f"{inp_name}.inp"
    for i in range(1, kmax+1):
        m = 2**i
        if nmode<m:
            nlayer = i
            m2 = m//2
            nmode_extra = nmode - m2
            break
    nmode1 = m2 - nmode_extra

    f = open(input_file, 'w')

    f.write('#'*72 + '\n')
    f.write('\n')
    f.write("RUN-SECTION\n")
    f.write(f"name = {inp_name}\n")
    f.write("propagate\n")
    f.write("steps\n")
    f.write("auto\n")
    f.write("gridpop\n")
    #f.write("psi\n")
    f.write("tinit  = 0.00\n")
    f.write(f"tfinal = {tfinal}\n")
    f.write(f"tout   = {tout}\n")
    f.write("end-run-section\n")
    f.write("\n")
    f.write("OPERATOR-SECTION\n")
    f.write(f"opname = {op_name}\n")
    f.write("end-operator-section\n")
    f.write("\n")
    f.write("PRIMITIVE-BASIS-SECTION\n")
    for imode in range(1,nmode+1):
        f.write(f"  {imode}a    HO    30    0.00    1.0    1.00\n")
    f.write(f"    el    el    {nstate}\n")
    f.write("end-pbasis-section\n")
    f.write("\n")
    f.write("mlbasis-section\n")
    f.write(f"0> {nstate} {nstate}\n")
    f.write("  1> [el]\n")
    for imode in range(1, nmode+1):
        if imode<=nmode1:
            n = nlayer
            imode0 = imode - 1
        else:
            n = nlayer + 1
            imode0 = imode + nmode1 - 1
        for i in range(n-1, 0, -1):
            m = 2**i
            if imode0%m==0:
                ilayer = n - i
                i1 = ilayer
                f.write('  '*i1 + f'{ilayer}> 6 6\n')
        i1 = n
        f.write("  "*i1 + f"{n}> [{imode}a]\n")
    f.write("end-mlbasis-section\n")
    f.write("\n")
    f.write("INTEGRATOR-SECTION\n")
    f.write("  VMF\n")
    f.write("  RK8 = 1.0d-7\n")
    #f.write("  RK5 = 1.0d-7\n")
    #f.write("  proj-h\n")
    f.write("end-integrator-section\n")
    f.write("\n")
    f.write("INIT_WF-SECTION\n")
    f.write("build\n")
    f.write("  init_state =    1\n")
    for imode in range(1, nmode+1):
        f.write(f"  {imode}a    HO    0.00    0.00    1.0\n")
    f.write("end-build\n")
    f.write("end-init_wf-section\n")
    f.write("\n")
    f.write("end-input\n")


    f.close()

if __name__=='__main__':
    generInp()
