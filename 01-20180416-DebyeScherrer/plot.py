import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties.unumpy import uarray
from uncertainties import unumpy


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
            structurfactor += self.formfaktor * unumpy.cos(2*np.pi*(g_1*h + g_2*k + g_3*l))
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
    reflexe_order = 8
    sc = prim_cubic_cristal()   
    dsc = sc.all_struc_fac(reflexe_order)

    bcc = body_cubic_cristal()   
    dbcc = bcc.all_struc_fac(reflexe_order)

    fcc = face_cubic_cristal()   
    dfcc = fcc.all_struc_fac(reflexe_order)
    
    diamant = composite_structure()   
    diamant.add_structure(face_cubic_cristal())
    diamant.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25]))
    dd = diamant.all_struc_fac(reflexe_order)

    # Zusammengestzte Struktur deren Atomformfaktoren
    f_2_atomig = [2, 1] 

    zinkblende = composite_structure()   
    zinkblende.add_structure(face_cubic_cristal(formfaktor=f_2_atomig[0]))
    zinkblende.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=f_2_atomig[1]))
    dz = zinkblende.all_struc_fac(reflexe_order)
    
    steinsalz = composite_structure()   
    steinsalz.add_structure(face_cubic_cristal(formfaktor=f_2_atomig[0]))
    steinsalz.add_structure(face_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=f_2_atomig[1]))
    ds = steinsalz.all_struc_fac(reflexe_order)
    
    caesium = composite_structure()   
    caesium.add_structure(prim_cubic_cristal(formfaktor=f_2_atomig[0]))
    caesium.add_structure(prim_cubic_cristal(
        bias=[0.5,0.5,0.5], formfaktor=f_2_atomig[0]))
    dc = caesium.all_struc_fac(reflexe_order)

    # Zusammengestzte Struktur deren Atomformfaktoren
    f_3_atomig = [2,1,1] 

    fluorit= composite_structure()   
    fluorit.add_structure(face_cubic_cristal(formfaktor=f_3_atomig[0]))
    fluorit.add_structure(face_cubic_cristal(
        bias=[0.25,0.25,0.25], formfaktor=f_3_atomig[1]))
    fluorit.add_structure(face_cubic_cristal(
        bias=[0.75,0.75,0.75], formfaktor=f_3_atomig[2]))
    df = fluorit.all_struc_fac(reflexe_order)

    with open("build/structf.txt", "w") as text_file:
        for hkl, m, sc, bcc, fcc, diamant, zinkblende, steinsalz, caesium, \
            Fluorit in zip(df['hkl'], df['m'], dsc['structurfactor'], \
            dbcc['structurfactor'], dfcc['structurfactor'], dd['structurfactor'],\
            dz['structurfactor'], ds['structurfactor'], dc['structurfactor'], \
            df['structurfactor']):
            text_file.write("{} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\ \n".format(
                hkl, m, abs(sc), abs(bcc), abs(fcc), abs(diamant), abs(zinkblende),
                abs(steinsalz), abs(caesium), abs(Fluorit)))
            if hkl=='444':
                break
   
    m = [dsc, dbcc, dfcc, dd, dz, ds, dc, df]
    new_m = []
    cut_strukturf = 0.4
    print('Cutten des Strukturfactor bis zu {} des maximalen Strf.'\
            .format(cut_strukturf))
    for x in m:
        print('Strukturfactor: ', x['structurfactor'])
        mask = np.array(x['structurfactor']) >= max(x['structurfactor']) \
                * cut_strukturf
        x = np.array(x['m'])[mask]
        x = np.unique(x)
        x = np.sort(x)
        new_m.append(x)

    radius = 57.3
    print('Die Kammer besitzt einen Radius von {} mm.'.format(radius))
    umfang_to_deg = np.round(360 / (2 * np.pi * radius),4)
    print('Damit betraegt gemessener Millimeter auf der Trommel den \
    Winkel {} Grad.'.format(umfang_to_deg))
    
    lam_1 = 1.54093*10**(-10)
    lam_2 = 1.54478*10**(-10)
    lam_m = 1.5415*10**(-10)
    rho = 0.8*10**(-3)      # meter
    R = 57.3*10**(-3)       # meter
    F = 130*10**(-3)        # meter

    def uncertainty_theta(theta):
        print('Delta theta in deg: ', np.degrees(theta*(lam_2 - lam_1)/lam_m*np.tan(theta)))
        return np.radians(1) * np.ones(len(theta)) + theta*(lam_2 - lam_1)/lam_m*np.tan(theta)
    
    theta_1_deg = 0.5*np.array([44.5, 51.5, 75.0, 90.6, 96.6, 117.5, 135.0, 144.6]) #mm
    theta_2_deg = 0.5*np.array([29.0, 47.5, 57.0, 69.6, 76.5, 88.0, 94.7, 106.5,
        113.4, 126.5, 135.5, 156.0]) #mm
    theta_1 = np.radians(theta_1_deg)
    theta_1 = unumpy.uarray(theta_1, uncertainty_theta(theta_1))
    theta_2 = np.radians(theta_2_deg)
    theta_2 = unumpy.uarray(theta_2, uncertainty_theta(theta_2))

    def gittertest(m, theta):
        return m / (unumpy.sin(theta)**2)

    def gitterabstand(lam, m, theta):
        return np.sqrt(m)*(lam/2)/unumpy.sin(theta)

    def linear_func(x, a, b):
        return a*x + b

    def output(n_refl, gitter, theta, lam, pathrefl, pathfig, pathparams, rem=0): 
        theta = theta[:n_refl]
        for x in new_m:
            print(unumpy.nominal_values(gittertest(x[:n_refl],theta)))
        abstand = gitterabstand(lam, new_m[gitter][:n_refl],theta)

        x = unumpy.cos(theta)**2
      
        popt, pcov = curve_fit(linear_func, 
               unumpy.nominal_values(x[rem:]), 
               unumpy.nominal_values(abstand[rem:]))

        print('parameter:' , popt, np.sqrt(np.diag(pcov)))
        with open(pathparams, "w") as text_file:
            text_file.write('\\num{' + '{}'.format(round(popt[1]*10**10,2)) + '+-' + 
                    '{}'.format(np.round(np.sqrt(pcov[1,1])*10**10,2)) + '} & '
                    + '\\num{' + '{}'.format(round(popt[0]*10**10,2)) + '+-' + 
                    '{}'.format(np.round(np.sqrt(pcov[0,0])*10**10,2)) + '} \\\\')

        plt.errorbar(unumpy.nominal_values(x), unumpy.nominal_values(abstand),
                xerr=unumpy.std_devs(x), yerr=unumpy.std_devs(abstand) ,fmt='o')
        plt.plot(np.linspace(0,1,10), linear_func(np.linspace(0,1,10), *popt), '--')
        plt.xlabel(r'$\cos^2(\theta)$')
        plt.ylabel(r'$a$ / m')
        plt.tight_layout(pad=0)
        plt.savefig(pathfig)
        plt.close()
 
        with open(pathrefl, "w") as text_file:
            i = 1
            for theta, m in zip(theta, new_m[gitter][:n_refl]):
                theta_deg = round(np.degrees(unumpy.nominal_values(theta)), 1)
                theta_deg_err = round(np.degrees(unumpy.std_devs(theta)), 0)
                m_sin =round(np.asscalar(unumpy.nominal_values(
                    gittertest(m,theta))))
                cosinus =round(np.asscalar(np.cos(
                    unumpy.nominal_values(theta))**2), 3)
                abstand = round(np.asscalar(unumpy.nominal_values(
                    10**10*gitterabstand(lam,m, theta))), 2) 
                abstand_err = round(np.asscalar(unumpy.std_devs(
                    10**10*gitterabstand(lam, m, theta))), 2) 
                text_file.write('{} &'.format(i) + ' \\num{'+'{}'.format(theta_deg) + 
                        ' +- ' '{}'.format(theta_deg_err) + '} ' + \
                        '& {} & {} & {} & '.format(m, m_sin, cosinus) + '\\num{'
                        + '{}'.format(abstand) + ' +- '+ '{}'.format(abstand_err) + 
                        ' } \\\\ \n')
                i += 1

    output(8, 2, theta_1, lam_m, "build/reflexe1.txt", 'build/lin_fit1.pdf', \
           'build/params1.txt', rem=0)
    output(12, 7, theta_2, lam_m, "build/reflexe2.txt", 'build/lin_fit2.pdf', \
           'build/params2.txt', rem=1)
