#!/usr/bin/python

class ham_gen:
    '''
    Used for generate hamiltonian-section in mctdh's op file!
    '''
    ham_sec = []
    
    def iinput(self, n_single=0, n_triple=0, n_mode=0):
        self.n_single = n_single
        self.n_triple = n_triple
        self.n_mode = n_mode
        self.n_state = self.n_single + self.n_triple * 3
        self.states = []

        for i in range(1, self.n_single + 1):
            self.states.append( "S"+str(i) )

        for i in range(1, self.n_triple + 1):
            for it in range(1, 4):
                self.states.append( "T"+str(i)+"_"+str(it) )

    def head(self):
        self.ham_sec.append("HAMILTONIAN-SECTION")
        self.ham_sec.append( """
# %d singlet states
# %d triplet states
# %d modes
""" % (self.n_single, self.n_triple, self.n_mode))
        tt = "modes  | el "
        for imode0 in range(self.n_mode):
            imode = imode0 + 1
            im = imode % 10
            if imode == self.n_mode + 1 :
                tt += "| %da \n" % (imode)
            elif imode == 1 :
                tt += "| %da " % (imode)
            elif im == 0 :
                tt += "| %da \n" % (imode)
            elif im == 1 :
                tt += "modes  | %da " % (imode)
            else :
                tt += "| %da " % (imode)

        self.ham_sec.append(tt)
        self.ham_sec.append( '\n' )
        
    def ele_part(self):
        self.ham_sec.append( "#electronic part" )

        states = self.states

        #print states
        istates = list(range(1, self.n_state + 1))
        for i, name_i in zip(istates, states):
            for j, name_j in zip(istates, states):
                vij = 'V_' + name_i + '_' + name_j
                n = 25 - len(vij)
                if i <  j <= self.n_single :
                    line = vij + ' '*n + '|1 S' + str(i) + '&' + str(j)
                elif j < i <= self.n_single :
                    continue
                elif i == j :
                    line = vij + ' '*n + '|1 S' + str(i) + '&' + str(j)
                else :
                    vij = 'V_' + name_i + '_' + name_j + 'r'
                    n = 25 - len(vij)
                    line1 = vij + ' '*n + '|1 Z' + str(i) + '&' + str(j)
                    vij = 'V_' + name_i + '_' + name_j + 'i'
                    n = 23 - len(vij)
                    line2 = 'I*' + vij + ' '*n + '|1 Z' + str(i) + '&' + str(j)
                    line = line1 + '\n' + line2
                self.ham_sec.append( line )
        self.ham_sec.append( '\n' )

    def vib_part(self):
        self.vib_tuning()
        #self.vib_coupling()
    def vib_tuning(self):
        self.ham_sec.append( "#vibronic part" )
        self.ham_sec.append( "#tuning" )
        istates = list(range(1, self.n_state + 1))
        for i, name_i in zip(istates, self.states):
            for j in range(1, self.n_mode + 1):
                kappa = 'k' + str(j) + 'a_' + name_i
                n = 25 - len(kappa)
                sym_mat = '|1 S' + str(i) + '&' + str(i)
                n1 = 12 - len(sym_mat)
                imode = j + 1
                n2 = 4 - len(str(imode))

                line = kappa + ' '*n + sym_mat + ' '*n1 + '|' \
                       + str(imode) + ' '*n2 + 'q'
                self.ham_sec.append( line )
        self.ham_sec.append( '\n' )
    def vib_coupling(self):
        istates = list(range(1, self.n_state + 1))
        self.ham_sec.append( '#coupling' )
        for i, name_i in zip(istates, self.states):
            for j, name_j in zip(istates, self.states):
                for ivmode in range(1, self.n_mode + 1):
                    if i>=j :
                        continue

                    lam = 'la' + str(ivmode) + 'a_' + name_i + '_' + name_j
                    n = 25 - len(lam)

                    sym_mat = '|1 S' + str(i) + '&' + str(j)
                    n1 = 12 - len(sym_mat)
                    
                    imode = ivmode + 1
                    n2 = 4 - len(str(imode))

                    line = lam + ' '*n + sym_mat + ' '*n1 + '|' \
                           + str(imode) + ' '*n2 + 'q'
                    self.ham_sec.append( line )
        self.ham_sec.append( '\n' )


    def Tn_part(self):
        self.ham_sec.append( "#Tn  part" )
        istates = list(range(1, self.n_state + 1))
        for j in range(1, self.n_mode + 1):
            omega = 'w' + str(j) + 'a'
            n = 25 - len(omega)
            imode = j + 1
            n2 = 4 - len(str(imode))

            line = omega + ' '*n  + '|' + str(imode) + ' '*n2 + 'KE'
            self.ham_sec.append( line )
        self.ham_sec.append( '\n' )

    def gs_pes_part(self):
        self.ham_sec.append( "#ground state PES part" )
        for j in range(1, self.n_mode + 1):
            omega = '0.5*w' + str(j) + 'a'
            n = 25 - len(omega)
            imode = j + 1
            n2 = 4 - len(str(imode))

            line = omega + ' '*n  + '|' + str(imode) + ' '*n2 + 'q^2'
            self.ham_sec.append( line )
        self.ham_sec.append( '\n' )

    def tail(self):
        self.ham_sec.append( 'end-hamiltonian-section' )

    def run(self):
        self.head()
        self.Tn_part()
        self.gs_pes_part()
        self.ele_part()
        self.vib_part()
        self.tail()
        return self.ham_sec
        
    def output(self):
        self.run()
        for i in self.ham_sec :
            if i == '\n' :
                print(i, end=' ')
            else :
                print(i)


        
if __name__ == "__main__":
    ham = ham_gen()
    ham.iinput(2, 0, 6)
    ham.output()
