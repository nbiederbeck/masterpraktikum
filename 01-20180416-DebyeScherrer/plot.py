import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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
    dsc = sc.all_struc_fac(5)

    bcc = body_cubic_cristal()   
    dbcc = bcc.all_struc_fac(5)

    fcc = face_cubic_cristal()   
    dfcc = fcc.all_struc_fac(5)
    
    diamant = composite_structure()   
    diamant.add_structure(face_cubic_cristal())
    diamant.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25]))
    dd = diamant.all_struc_fac(5)
    
    zinkblende = composite_structure()   
    zinkblende.add_structure(face_cubic_cristal())
    zinkblende.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=5/3))
    dz = zinkblende.all_struc_fac(5)
    
    steinsalz = composite_structure()   
    steinsalz.add_structure(face_cubic_cristal())
    steinsalz.add_structure(face_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=5/6))
    ds = steinsalz.all_struc_fac(5)
    
    caesium = composite_structure()   
    caesium.add_structure(prim_cubic_cristal())
    caesium.add_structure(prim_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=5/6))
    dc = caesium.all_struc_fac(5)

    fluorit= composite_structure()   
    fluorit.add_structure(prim_cubic_cristal())
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=5/6))
    fluorit.add_structure(prim_cubic_cristal(
        bias=[0.75,0.75,0.75], formfaktor=5/6))
    df = fluorit.all_struc_fac(5)

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
    

    radius = 57.3
    print('Die Kammer besitzt einen Radius von {} mm.'.format(radius))
    umfang_to_deg = np.round(360 / (2 * np.pi * radius),4)
    print('Damit betraegt gemessener Millimeter auf der Trommel den \
    Winkel {} Grad.'.format(umfang_to_deg))
    
    theta_1 = 0.5*np.array([4.35, 5.05, 7.4, 9.0, 9.5, 11.7, 13.6, 14.4])*10 #mm
    theta_1 =np.radians(theta_1)
    theta_2 = 0.5*np.array([2.7, 4.5, 5.5, 6.8, 7.5, 8.7, 9.4, 10.5, 11.2, 12.5, 13.5, 15.4])*10 #mm
    theta_2 =np.radians(theta_2)

    rho = 0.8*10**(-3)      # meter
    R = 57.3*10**(-3)       # meter
    F = 130*10**(-3)        # meter

    def gittertest(m, theta):
        # print('m:', m)
        # print('theta:', theta)
        # print('len: ', len(m), len(theta))
        return m / (np.sin(theta)**2)

    def delta_a_A(theta, a):
        return a*rho/(2 * R)*(1 - R/F)*(np.cos(theta)**2)/theta

    def gitterabstand(lam, m, theta):
        return np.sqrt(m)*(lam/2)/np.sin(theta)

    def linear_func(x, a, b):
        return a*x + b

    lam = 1.6*10**(-10)

    print('Probe 1:')
    def output(n_refl, gitter, theta, lam, pathrefl, pathfig, rem=0): 
        theta = theta[:n_refl]
        for x in new_m:
            print(gittertest(x[:n_refl],theta))
        abstand = gitterabstand(lam, new_m[gitter][:n_refl],theta)
        print('Abstand: ', abstand)

        x = np.cos(theta)**2
        popt, pcov = curve_fit(linear_func, x[rem:], abstand[rem:])

        plt.plot(x, abstand, 'x')
        plt.plot(np.linspace(0,1,10), linear_func(np.linspace(0,1,10), *popt), '--')
        plt.xlabel(r'$\cos^2(x)$')
        plt.xlabel(r'$a$ / nm')
        plt.savefig(pathfig)
        plt.close()
        print('Parameter: ', popt)
        
        with open(pathrefl, "w") as text_file:
            i = 1
            for theta, m in zip(theta, new_m[gitter][:n_refl]):
                theta_deg = round(np.degrees(theta), 3)
                m_sin = round(gittertest(m,theta), 3)
                cosinus = round(np.cos(theta)**2, 3)
                abstand = round(10**10*gitterabstand(lam, m, theta), 3) 
                text_file.write('{} & {} & {} & {} & {} & {} \\\\ '.format(i,
                    theta_deg, m, m_sin, cosinus, abstand))
                i += 1

    output(8,2,theta_1,lam,"build/reflexe1.txt",'build/test1.pdf',rem=0)
#    print('leange output 2', len(theta_2))
    output(12,6,theta_2,lam,"build/reflexe2.txt",'build/test2.pdf', rem=1)

#    n_refl1= 8
#    gitter = 2
#    theta_1 = theta_1[:n_refl1]
#    for x in new_m:
#        print(gittertest(x[:n_refl1],theta_1))
#    abstand_1 = gitterabstand(lam, new_m[gitter][:n_refl1],theta_1)
#    print('Abstand 1: ', abstand_1)
#    
#    x = np.cos(theta_1)**2
#    popt, pcov = curve_fit(linear_func, x, abstand_1)
#
#    plt.plot(x, abstand_1, 'x')
#    plt.plot(x, linear_func(x, *popt), '--')
#    plt.show()
#    print('Parameter: ', popt)
#    
#    with open("build/reflexe1.txt", "w") as text_file:
#        i = 1
#        for theta_1, m in zip(theta_1, new_m[gitter][:n_refl1]):
#            theta = np.degrees(theta_1)
#            m_sin = round(gittertest(m,theta_1), 3)
#            cosinus = round(np.cos(theta_1), 3)
#            abstand = round(10**10*gitterabstand(lam, m, theta_1), 3) 
#            text_file.write('{} & {} & {} & {} & {} & {} \\\\ '.format(i, theta, m, m_sin, cosinus, abstand))
#            i += 1
#    
#    print('Probe 2:')
#    n_refl2= 9
#    gitter = 6
#    theta_2 = theta_2[:n_refl2]
#    for x in new_m:
#        print(gittertest(x[:n_refl2],theta_2))
#    abstand_2 = gitterabstand(lam, new_m[gitter][:n_refl2],theta_2)
#    print('Abstand 2: ', abstand_2)
#    plt.plot(np.cos(theta_2)**2, 1/abstand_2)
#    plt.show()
#    
#    with open("build/reflexe2.txt", "w") as text_file:
#        i = 1
#        for theta_2, m in zip(theta_2, new_m[gitter][:n_refl2]):
#            theta = np.degrees(theta_2)
#            m_sin = round(gittertest(m,theta_2), 3)
#            cosinus = round(np.cos(theta_2), 3)
#            abstand = round(10**10*gitterabstand(lam, m, theta_2), 3) 
#            text_file.write('{} & {} & {} & {} & {} & {} \\\\ '.format(i, theta, m, m_sin, cosinus, abstand))
#            i += 1


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
