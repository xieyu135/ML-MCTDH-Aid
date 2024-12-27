
import sympy as sp
from scipy.integrate import quad

pop_thre = 0.99999

def calcPop(n_pbasis, q_mean):
    x = sp.symbols('x')
    def psi(n = 3):
        hermite_poly = sp.hermite(n, x)
        N_n = sp.sqrt(1/(2**n * sp.factorial(n))) * sp.pi **(-1/4)
        psi_n = N_n * sp.exp(- x**2 / 2) * hermite_poly
        return psi_n
    phi = sp.pi **(-1/4) * sp.exp(- (x-q_mean)**2 / 2)
    ssum = 0
    for i in range(n_pbasis):
        psi_n = psi(i)
        expr = phi*psi_n
        integral, error = quad(lambda x: expr.subs(sp.symbols('x'), x), -100, 100)
        t = integral**2
        ssum+= t
        print(i, t)
    print('sum:', ssum)
    return ssum
def checkPop(n_pbasis, q_mean, pop_thre):
    x = sp.symbols('x')
    def psi(n = 3):
        hermite_poly = sp.hermite(n, x)
        N_n = sp.sqrt(1/(2**n * sp.factorial(n))) * sp.pi **(-1/4)
        psi_n = N_n * sp.exp(- x**2 / 2) * hermite_poly
        return psi_n
    phi = sp.pi **(-1/4) * sp.exp(- (x-q_mean)**2 / 2)
    ssum = 0
    for i in range(n_pbasis):
        psi_n = psi(i)
        expr = phi*psi_n
        integral, error = quad(lambda x: expr.subs(sp.symbols('x'), x), -100, 100)
        t = integral**2
        print(i, t)
        ssum+= t
        if ssum>pop_thre:
            return True
        
    print('sum:', ssum)
    return ssum>pop_thre

def npbasisCvg(new_input_file, pop_thre):
    print('Begin to get mode_npbasis_dict')
    input_f = open("input", "r")
    mode_npbasis_dict = {}
    flag = 0
    while True:
        line = input_f.readline()
        if not line or 'end-pbasis-section' in line:
            break
        line = line.rstrip()
        if flag==1:
            alist = line.split()
            # print(alist)
            # exit()
            if alist[0]!='el':
                mode_npbasis_dict[alist[0]] = int(alist[2])
        if 'PRIMITIVE-BASIS-SECTION' in line:
            flag = 1
    input_f.close()
    # print(mode_npbasis_dict)
    n_mode = len(mode_npbasis_dict)


    print('Begin to get mode_qmean_max_dict')
    output_f = open("output", "r")
    mode_qmean_max_dict = {}
    for k in mode_npbasis_dict:
        mode_qmean_max_dict[k] = 0.
    flag = 0
    count = 0
    while True:
        line = output_f.readline()
        if not line:
            break
        line = line.rstrip()
        if flag==1:
            alist = line.split()
            mode = alist[0]
            # q_mean_abs = abs(float(alist[3]))
            q_mean = float(alist[3])
            dq_mean = float(alist[5])
            q_mean_abs = (q_mean**2 + dq_mean**2)**0.5
            if q_mean_abs>mode_qmean_max_dict[mode]:
                mode_qmean_max_dict[mode] = q_mean_abs
            count+= 1
        if count>=n_mode:
            flag = 0
            count = 0
        if 'population' in line:
            flag = 1
    output_f.close()
    # print(mode_qmean_max_dict)

    print('Begin to cvg n_pbasis.')
    for mode in mode_qmean_max_dict:
        q_mean = mode_qmean_max_dict[mode]
        n_pbasis = mode_npbasis_dict[mode]
        print(f'mode: {mode}')
        # pop = calcPop(n_pbasis, q_mean)
        # print(f'{mode}: {pop}')
        if not checkPop(n_pbasis, q_mean, pop_thre):
            for i in range(30):
                n_pbasis_1 = n_pbasis + i
                pop_1 = calcPop(n_pbasis_1, q_mean)
                if pop_1>=pop_thre:
                    mode_npbasis_dict[mode] = n_pbasis_1
                    break
            else:
                print(f'60 pbasis is not enough for mode {mode}.')
                exit()
    
    print('Begin to read new_input_file')
    new_input_f = open(new_input_file, "r")
    flag = 0
    head = []
    tail = []
    while True:
        line = new_input_f.readline()
        if not line:
            break
        line = line.rstrip()
        if flag==0:
            head.append(line)
        elif flag==1:
            alist = line.split()
            if alist[0]!='el':
                pass
            else:
                flag = 2
                tail.append(line)
        elif flag==2:
            tail.append(line)
        if 'PRIMITIVE-BASIS-SECTION' in line:
            flag = 1
    new_input_f.close()
    
    print('Begin to write new_input_file')
    # new_input_file = 'test.inp'
    new_input_f = open(new_input_file, "w")
    for line in head:
        new_input_f.write(line+'\n')
    for mode, n_pbasis in mode_npbasis_dict.items():
        line = f'  {mode}    HO    {n_pbasis}    0.00    1.0    1.00'
        new_input_f.write(line+'\n')
    for line in tail:
        new_input_f.write(line+'\n')
    new_input_f.close()
if __name__=='__main__':
    npbasisCvg('penta_c60_562cut0.5_ml_tree2_a66-1.inp', pop_thre)

