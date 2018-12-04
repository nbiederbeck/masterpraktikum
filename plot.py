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
        return np.round(structurfactor, 2)

    def all_struc_fac(self, order):
        h, k, l = 1, 0, 0
        storage = {'hkl':[], 'm':[], 'structurfactor':[]}
        while(h<=order):
            while(k<=h):
                while(l<=k):
                    storage['hkl'].append('{}{}{}'.format(h, k, l))
                    storage['m'].append('{}'.format(h**2 + k**2 + l*2))
                    storage['structurfactor'].append('{}'.format(
                            self.structurfactor(h, k, l)))
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
    print('sc:')
    sc = prim_cubic_cristal()   
    dsc = sc.all_struc_fac(3)
    print(dsc)

    print('bcc:')
    bcc = body_cubic_cristal()   
    dbcc = bcc.all_struc_fac(3)
    print(dbcc)

    print('fcc:')
    fcc = face_cubic_cristal()   
    dfcc = fcc.all_struc_fac(3)
    print(dfcc)
    
    print('diamant:')
    diamant = composite_structure()   
    diamant.add_structure(face_cubic_cristal())
    diamant.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25]))
    dd = diamant.all_struc_fac(3)
    print(dd)
    
    print('zinkblende:')
    zinkblende = composite_structure()   
    zinkblende.add_structure(face_cubic_cristal())
    zinkblende.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=2/3))
    dz = zinkblende.all_struc_fac(3)
    print(dz)
    
    print('Steinsalz:')
    steinsalz = composite_structure()   
    steinsalz.add_structure(face_cubic_cristal())
    steinsalz.add_structure(face_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=2/3))
    ds = steinsalz.all_struc_fac(3)
    print(ds)
    
    print('Caesiumchlorid:')
    caesium = composite_structure()   
    caesium.add_structure(prim_cubic_cristal())
    caesium.add_structure(prim_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=2/3))
    dc = caesium.all_struc_fac(3)
    print(dc)

    print('Fluorit:')
    fluorit= composite_structure()   
    fluorit.add_structure(prim_cubic_cristal())
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=2/3))
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.75,0.75,0.75], formfaktor=2/3))
    df = fluorit.all_struc_fac(3)
    print(df)
#    radius = 57.3
#    print('Die Kammer besitzt einen Radius von {} mm.'.format(radius))
#    umfang_to_deg = np.round(360 / (2 * np.pi * radius),4)
#    print('Damit betraegt gemessener Millimeter auf der Trommel den \
#    Winkel {} Grad.'.format(umfang_to_deg))
#    
#    def netzebenen_abstand(n, lam, theta):
#        return n * lam / (2 * np.sin(theta))
#    
#    print('Probe 1:')
#    reflexe_1 = np.array([2.1,4.3,5.1,7.4,9.0,11.7,13.6,14.4])*10 #mm
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
