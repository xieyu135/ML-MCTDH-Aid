#!/usr/bin/python
import read_para 
import gener_ham 

def short_op(op_name='test', para={}, ham_sec=[], unit='eV'):
    op_content = op_head(op_name)
    op_content.append( '\n' )
    op_content.append( 'PARAMETER-SECTION' )
    
    # keys = sorted(para.keys())
    keys = para.keys()
    for key in keys:
        if para[key] != 0 :
            #print para[key]
            n = 25 - len(key)
            s_val = '%.8f' % (para[key])
            n2 = 25 - len(s_val)
            line = key + ' '*n + '=' + ' '*n2 + s_val + ' , ' + unit 
            #line = key + ' '*n + '=' + ' '*n2 + s_val + ' , ' + unit
            op_content.append( line )
            
    op_content.append('end-parameter-section')
    op_content.append('\n')
    
    for line in ham_sec :
        if len(line) < 2 :
            key = None
        elif line.split()[0][:2] == 'I*' :
            key = line.split()[0][2:]
        else :
            key = line.split()[0]
            
        if key in keys :
            if para[key] != 0 :
                op_content.append( line )
        else :
            op_content.append( line )
            
    op_content.append('\n')
    op_content.append('end-operator')
    return op_content
    
def long_op(op_name, para={}, ham_sec=[], unit='eV'):
    op_content = op_head(op_name)
    op_content.append( '\n' )
    op_content.append( 'PARAMETER-SECTION' )
    
    # keys = sorted(para.keys())
    keys = para.keys()
    for key in keys:
        n = 25 - len(key)
        s_val = str(para[key])
        n2 = 25 - len(s_val)
        line = key + ' '*n + '=' + ' '*n2 + s_val + ' , ' + unit
        op_content.append( line )
    op_content.append('end-parameter-section')
        
    op_content.append('\n')
    op_content.extend(ham_sec)
    
    op_content.append('\n')
    op_content.append('end-operator')    
    return op_content

def op_head(op_name):
    op_content = []

    op_content.append( '''OP_DEFINE-SECTION
title
%s
end-title
end-op_define-section''' % op_name )
    return op_content

def op_out(op_content, op_name = 'test'):
    op_name += '.op'
    f = open(op_name, 'w')
    for i in op_content :
        if i == '\n' :
            print(i, end='', file=f)
        else :
            print(i, file=f)
    f.close()
    


def iinput():
    n_single = int(input('n_single:\n').split()[0])
    n_triple = int(input('n_triple:\n').split()[0])
    n_mode = int(input('n_mode:\n').split()[0])
    op_name = input('op_name:\n').split()[0]
    line = input('op_type: "s: short" or "l: long"? \n')
    op_type = line.split()[0].lower()

    return n_single, n_triple, n_mode, op_name, op_type
    
#n_single = 2
#n_triple = 3
#n_mode = 6
#op_name = 'spin_vibronic'

#n_single, n_triple, n_mode, op_name, op_type = iinput()

#conf = [n_single, n_triple, n_mode]
def generOp(
        op_type = 's',
        n_triple = 0,
        op_name = 'a',
        fnm_kappa = 'kappa.dat',
        fnm_omega = 'omega_eV.dat',
        fnm_vmat = 'vmat.dat',
        fnm_lambda = 'lambda.dat',
    ):
    # print('generOp')
    gen_op = {'s': short_op, 'l': long_op}

    rp = read_para.read_para_lvc(fnm_kappa, fnm_omega, fnm_vmat, fnm_lambda)
    #rp.iinput(*conf)
    n_single, n_mode, para = rp.run()

    conf = [n_single, n_triple, n_mode]

    gh = gener_ham.ham_gen_lvc()
    gh.iinput(*conf)
    ham_sec = gh.run()

    op_content = gen_op[op_type](op_name, para, ham_sec)
    op_out(op_content, op_name)
if __name__=='__main__':
    generOp()






