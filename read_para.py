
import numpy as np


class read_para:
    def __init__(self, fnm_kappa, fnm_omega, fnm_vmat):
        self.fnm_kappa = fnm_kappa
        self.fnm_omega = fnm_omega
        self.fnm_vmat = fnm_vmat
        self.para = {}
    def read_para(self):
        self.ele_part()
        self.vib_part()
    def ele_part(self):
        self.vmat = np.loadtxt(self.fnm_vmat)
    def vib_part(self):
        self.omega = np.loadtxt(self.fnm_omega)
        self.kappa = np.loadtxt(self.fnm_kappa)
    def check(self):
        # print(self.vmat.shape, self.kappa.shape, self.omega.shape)
        if self.vmat.shape[0] != self.kappa.shape[1]:
            print('Please check "' + self.fnm_vmat + '" and "' + self.fnm_kappa + '".')
            print('The numbers of states in the two files are different!')
            exit()
        if self.omega.shape[0] != self.kappa.shape[0]:
            print('Please check "' + self.fnm_omega + '" and "' + self.fnm_kappa + '".')
            print('The numbers of modes in the two files are different!')
            exit()
        self.n_sate = self.vmat.shape[0]
        self.n_mode = self.omega.shape[0]
    def gen_para(self):
        self.gen_ele()
        self.gen_vib()
    def gen_ele(self):
        for i in range(self.n_sate):
            for j in range(self.n_sate):
                vij = 'V_S' + str(i+1) + '_S' + str(j+1)
                self.para[vij] = self.vmat[i,j]
    def gen_vib(self):
        for i in range(self.n_mode):
            omega = 'w' + str(i+1) + 'a'
            self.para[omega] = self.omega[i]
        for i in range(self.n_mode):
            for j in range(self.n_sate):
                kappa = 'k' + str(i+1) + 'a' + '_S' + str(j+1)
                self.para[kappa] = self.kappa[i,j]

    def run(self):
        #print self.fnm_kappa
        #print self.fnm_omega
        #print self.fnm_vmat
        self.read_para()
        self.check()
        self.gen_para()
        #print self.omega
        return self.n_sate, self.n_mode, self.para


if __name__ == "__main__":
    fnm_kappa = 'kappa.dat'
    fnm_omega = 'omega_eV.dat'
    fnm_vmat = 'vmat.dat'
    op = read_para(fnm_kappa, fnm_omega, fnm_vmat)
    op.run()
    print(op.para)
#kappa.dat  omega_eV.dat  vmat.dat
