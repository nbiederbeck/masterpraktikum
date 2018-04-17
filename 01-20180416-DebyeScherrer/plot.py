import numpy as np
import matplotlib.pyplot as plt

class cristal:
    def __init__(self, alpha, beta, gamma, formfaktor=1):
        ''' Erstellt einen Kristal
        Params:
        alpha, beta, gamma = float
            Kantenlaengen der Einheitszelle
        '''
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.base_vec = []
        self.formfaktor = formfaktor
    
    def add_base_vec(self, b_1, b_2, b_3):
        self.base_vec.append([b_1, b_2, b_3])

    def structurfactor(self, h, k, l):
        structurfactor = 0
        for g_1, g_2, g_3 in self.base_vec:
            structurfactor += self.formfaktor * np.cos(2*np.pi*(g_1*h + g_2*k + g_3*l))
        return structurfactor

    def all_struc_fac(self, order):
        h, k, l = 1, 0, 0
        storage = {'hkl':[], 'm':[], 'structurfactor':[]}
        while(h<=order):
            while(k<=h):
                while(l<=k):
                    storage['hkl'].append('{}{}{}'.format(h, k, l))
                    storage['m'].append(h**2 + k**2 + l**2)
                    storage['structurfactor'].append(round(self.structurfactor(h, k, l),2))
                    l += 1
                k += 1
                l = 0
            h += 1
            k = 0
            l = 0
        return storage

class cubic_cristal(cristal):
    def __init__(self, a, formfaktor=1):
        cristal.__init__(self, a, a, a, formfaktor)

class prim_cubic_cristal(cubic_cristal):
    def __init__(self, a=1, formfaktor=1, bias=[0,0,0]):
        cubic_cristal.__init__(self, a, formfaktor)
        vecs = np.array([[0,0,0]]) + np.array(bias)
        # print('Sum vecs', bias, vecs)
        for vec in vecs:
            self.add_base_vec(*vec)

class body_cubic_cristal(cubic_cristal):
    def __init__(self, a=1, formfaktor=1, bias=[0,0,0]):
        cubic_cristal.__init__(self, a, formfaktor)
        vecs = np.array([[0,0,0],[0.5,0.5,0.5]]) + np.array(bias)
        for vec in vecs:
            self.add_base_vec(*vec)

class face_cubic_cristal(cubic_cristal):
    def __init__(self, a=1, formfaktor=1, bias=[0,0,0]):
        cubic_cristal.__init__(self, a, formfaktor)
        vecs = np.array([[0,0,0],[0,0.5,0.5],[0.5,0,0.5],[0.5,0.5,0]]) + np.array(bias)
        for vec in vecs:
            self.add_base_vec(*vec)

class composite_structure(cristal):
    def __init__(self, a=1):
        self.a = a
        self.structures = []

    def add_structure(self, structure):
        self.structures.append(structure)

    def structurfactor(self, h, k, l, formfaktor=1):
        sum_st_fa = 0
        for struc in self.structures :
            sum_st_fa += struc.structurfactor(h,k,l)
        return sum_st_fa

if __name__ == '__main__':
    sc = prim_cubic_cristal()   
    dsc = sc.all_struc_fac(4)

    bcc = body_cubic_cristal()   
    dbcc = bcc.all_struc_fac(4)

    fcc = face_cubic_cristal()   
    dfcc = fcc.all_struc_fac(4)
    
    diamant = composite_structure()   
    diamant.add_structure(face_cubic_cristal())
    diamant.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25]))
    dd = diamant.all_struc_fac(4)
    
    zinkblende = composite_structure()   
    zinkblende.add_structure(face_cubic_cristal())
    zinkblende.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=2/3))
    dz = zinkblende.all_struc_fac(4)
    
    steinsalz = composite_structure()   
    steinsalz.add_structure(face_cubic_cristal())
    steinsalz.add_structure(face_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=2/3))
    ds = steinsalz.all_struc_fac(4)
    
    caesium = composite_structure()   
    caesium.add_structure(prim_cubic_cristal())
    caesium.add_structure(prim_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=2/3))
    dc = caesium.all_struc_fac(4)

    fluorit= composite_structure()   
    fluorit.add_structure(prim_cubic_cristal())
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=2/3))
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.75,0.75,0.75], formfaktor=2/3))
    df = fluorit.all_struc_fac(4)

    with open("build/structf.txt", "w") as text_file:
        for hkl, m, sc, bcc, fcc, diamant, zinkblende, steinsalz, caesium, \
            Fluorit in zip(df['hkl'], df['m'], dsc['structurfactor'], \
            dbcc['structurfactor'], dfcc['structurfactor'], dd['structurfactor'],\
            dz['structurfactor'], ds['structurfactor'], dc['structurfactor'], \
            df['structurfactor']):
            text_file.write("{} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\ \n".format(hkl, m, sc, bcc, fcc, diamant, zinkblende, steinsalz, caesium, Fluorit))
   
    m = [dsc, dbcc, dfcc, dd, dz, ds, dc, df]
    new_m = []
    for x in m:
        mask = np.array(x['structurfactor']) != 0
        x = np.array(x['m'])[mask]
        x = np.unique(x)
        x = np.sort(x)
        new_m.append(x)
    

#    radius = 57.3
#    print('Die Kammer besitzt einen Radius von {} mm.'.format(radius))
#    umfang_to_deg = np.round(360 / (2 * np.pi * radius),4)
#    print('Damit betraegt gemessener Millimeter auf der Trommel den \
#    Winkel {} Grad.'.format(umfang_to_deg))
#    
    theta_1 = 0.5*np.array([4.3, 4.9, 7.4, 9.0, 9.5, 11.7, 13.6, 14.4])*10 #mm
    theta_2 = 0.5*np.array([2.6, 4.5, 5.5, 6.8, 7.5, 8.7, 9.4, 10.5, 11.2, 12.5,
        13.5, 15.4])*10 #mm

    rho = 0.8*10**(-3)      # meter
    R = 57.3*10**(-3)       # meter
    F = 130*10**(-3)        # meter

    def gittertest(m, theta):
        return m / (np.sin(np.radians(theta))**2)

    def delta_a_A(theta, a):
        pass

    

    print('Probe 1:')
    for x in new_m:
        print(gittertest(x[:7],theta_1[:7]))

    print('Probe 2:')
    for x in new_m:
        print(gittertest(x[:9],theta_2[:9]))
#    print('Die Reflexe sind im Abstand von {} mm von der Quelle zu \
#    sehen'.format(reflexe_1))
#    print('Dies entspricht gleichzeitig auch derem doppelten Winkel.')
#    
#    theta_1 = reflexe_1/2
#    print('Die Streuwinkel sind {}'.format(theta_1))
#    
#    m = np.array([1,4,6,11,14,24,26,24])
#    print(m / np.sin(np.radians(theta_1))**2)
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.plot(m, np.sin(np.radians(theta_1))**2)
#    fig.savefig('build/probe_1.pdf')
#    plt.close(fig)
