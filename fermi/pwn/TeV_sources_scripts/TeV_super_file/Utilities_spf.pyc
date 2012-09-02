import yaml
import os,sys
import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
import numpy as num
import pylab


def type_list(filename,type,assoc=True):
    nb =0
    sources=yaml.load(open(filename))
    for name in sources.keys():
        if sources[name]["type"].lower().find(type.lower())!=-1:
            nb+=1
            print "\n"
            print name
            if assoc:
                print "-------assoc %s type : %s:"%(name,sources[name]["type"])
                print sources[name]['association']

    print "%d sources found"%nb

def get_assoc(filename,name):
    sources=yaml.load(open(filename))
    print sources[name]['association']

def PLSuperExpCutoff(Prefactor,Index1,Scale,Cutoff,Index2,x):
    from math import pow,exp
    y=Prefactor*pow((x/Scale),(-1.0)*Index1)*exp((-1.0)*pow((x/Cutoff),Index2))
    return y
                    

def update_pulsars(inputfile, psrfile):
    sources=yaml.load(open(inputfile))
    for name in sources.keys():
        try:
            pulsar_name=sources[name]["psrname"]
        except:
            pulsar_name=None
        
        if pulsar_name is not None:
            indice=-1

            import pyfits
            fic=pyfits.open(psrfile)
            pulsars=fic[1].data
            for i in range(len(pulsars)-1):
                if pulsars[i]["PSR"].lower()==pulsar_name.lower().replace(" ",''):
                    indice=i
            if indice!=-1:
                Prefact=float(pulsars[indice]["ECPL1PRE"])*1e-12
                gamma1=float(pulsars[indice]["ECPL1IN1"])
                gamma2=float(pulsars[indice]["ECPL1IN2"])
                pivot=float(pulsars[indice]["ECPL1PIV"])
                cutoff=float(pulsars[indice]["ECPL1CO"])
                print "Prefact=%.2e gamma1=%.2f gamma2=%.2f pivot=%.2e cutoff=%.2e"%(Prefact,gamma1,gamma2,pivot,cutoff)
                
                emean=num.logspace(2.0,5.5,1e2)
                E2dNdE=[]
                emean_2=[]

                for i in range(len(emean)):
                    #print "emean=%.2e"%(emean[i])
                    #print "PLS=%.2e"%(emean[i]*emean[i]*PLSuperExpCutoff(Prefact,gamma1,pivot,cutoff,gamma2,emean[i]))
                    sources[name]["pulsar_SED_energy"].append(float(emean[i]))
                    sources[name]["pulsar_SED"].append(float(1.60217646e-6*emean[i]*emean[i]*PLSuperExpCutoff(Prefact,gamma1,pivot,cutoff,gamma2,emean[i])))
                print emean
                print E2dNdE
                print emean_2
#                sources[name]["pulsar_SED_energy"]=emean_2
#                sources[name]["pulsar_SED"]=E2dNdE
                f=open(inputfile,"w")
                f.write(yaml.dump(sources))
                f.close()

def update_super_file(inputfile,outputfile,directory,hypothesis="at_tev"):
    #os.system("cp %s %s"%(inputfile,outputfile))
    sources=yaml.load(open(inputfile))
    for name in sources.keys():
        try:
            source_ind=yaml.load(open("%s/%s/seds/sed_gtlike_2bpd_%s_%s.yaml"%(directory,name,hypothesis,name)))
            
            emin=[]
            emax=[]
            emean=[]
            point=[]
            error=[]
            emin_ul=[]
            emax_ul=[]
            emean_ul=[]
            Uls=[]
            Signif=source_ind["Test_Statistic"]
            


            for i in range(len(Signif)):
                if Signif[i]>=9.0:
                    emin.append(float(source_ind["Energy"]["Lower"][i]))
                    emax.append(float(source_ind["Energy"]["Upper"][i]))
                    emean.append(float(source_ind["Energy"]["Value"][i]))
                    point.append(float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["dNdE"]["Value"][i]))
                    error.append(float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["dNdE"]["Error"][i]))
                else:
                    emin_ul.append(float(source_ind["Energy"]["Lower"][i]))
                    emax_ul.append(float(source_ind["Energy"]["Upper"][i]))
                    emean_ul.append(float(source_ind["Energy"]["Value"][i]))
                    Uls.append(float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["Energy"]["Value"][i])*1.602e-6*float(source_ind["dNdE"]["Upper_Limit"][i]))

            sources[name]["Fermi"]["SED"]["points"]["Emin"]=emin
            sources[name]["Fermi"]["SED"]["points"]["Emax"]=emax
            sources[name]["Fermi"]["SED"]["points"]["Emean"]=emean
            sources[name]["Fermi"]["SED"]["points"]["E2dNdE"]=point
            sources[name]["Fermi"]["SED"]["points"]["E2dNdE_Err"]=error
            

            sources[name]["Fermi"]["SED"]["ULs"]["Emin"]=emin_ul
            sources[name]["Fermi"]["SED"]["ULs"]["Emax"]=emax_ul
            sources[name]["Fermi"]["SED"]["ULs"]["Emean"]=emean_ul
            sources[name]["Fermi"]["SED"]["ULs"]["E2dNdE"]=Uls
            
        except:
            print "pas trouve le fichier yaml SED : %s"%name
        
    f=open(outputfile,"w")
    f.write(yaml.dump(sources))
    f.close()
            
def plot_seds(filename,output="plots",pulsars=False):
    sources=yaml.load(open(filename))
    try :
        os.system("mkdir %s"%output)
    except:
        print "%s already exists"%output
    for name in sources.keys():
    
        print name
        pylab.figure(1);pylab.clf()
        oldlw = pylab.rcParams['axes.linewidth']
        pylab.rcParams['axes.linewidth'] = 2
        axes = pylab.gca()
        axes.grid(True)
        axes.set_xscale('log')
        axes.set_yscale('log')
        
        pylab.ylabel(r'$\mathsf{E^{2} \frac{dN}{dE}(ergs\ cm^{-2}\ s^{-1})}$',fontsize=18)
        pylab.xlabel(r'$\mathsf{Energy\ (MeV)}$',fontsize=18)
        pylab.title('SED of %s'%name,fontsize='small')
    

        pylab.grid(True)
        
        Ranges=["X-Ray","Radio","Fermi","TeV"]
        for energ_r in Ranges:
            if energ_r=="X-Ray":
                fmtc='g'
            elif energ_r=="Radio":
                fmtc='k'
            elif energ_r=="Fermi":
                fmtc='r'
            elif energ_r=="TeV":
                fmtc='b'
            emin=sources[name][energ_r]["SED"]["points"]["Emin"]
            emax=sources[name][energ_r]["SED"]["points"]["Emax"]
            e=sources[name][energ_r]["SED"]["points"]["Emean"]
            f=sources[name][energ_r]["SED"]["points"]["E2dNdE"]
            err=sources[name][energ_r]["SED"]["points"]["E2dNdE_Err"]
            if len(e)!=0:
                if emin[0]!=e[0]:
                    errormin=[]
                    errormax=[]
                    for i in range(len(e)):
                        errormin.append(e[i]-emin[i])
                        errormax.append(emax[i]-e[i])
                    pylab.errorbar(e, f, xerr=[errormin,errormax],yerr=err, fmt=fmtc+'+',label=energ_r)
                else:
                    pylab.errorbar(e, f, xerr=0.0,yerr=err, fmt=fmtc,label=energ_r)
                    
            emin=sources[name][energ_r]["SED"]["ULs"]["Emin"]
            emax=sources[name][energ_r]["SED"]["ULs"]["Emax"]
            e=sources[name][energ_r]["SED"]["ULs"]["Emean"]
            f=sources[name][energ_r]["SED"]["ULs"]["E2dNdE"]
            if len(e)!=0:
                errormin=[]
                errormax=[]
                dinf=[]
                dsup=[]
                for i in range(len(e)):
                    errormin.append(e[i]-emin[i])
                    errormax.append(emax[i]-e[i])
                    dinf.append(f[i]/2.0)
                    dsup.append(0.0)
                if emin[0]!=e[0]:
                    pylab.errorbar(e, f, xerr=[errormin,errormax],yerr=[dinf,dsup], fmt=fmtc+'+',label=energ_r)
                else:
                    pylab.errorbar(e, f, xerr=0.0,yerr=[dinf,dsup], fmt=fmtc+'+',label=energ_r)
                pylab.errorbar(e,dinf,xerr=0.0,yerr=0.0,fmt=fmtc+'v')


        #Galactic and extra-gal_sensitivity
        E_Gal_Center=[1.333521e+02,2.371374e+02,4.216965e+02,7.498942e+02,1.333521e+03,2.371374e+03,4.216965e+03,7.498942e+03,1.333521e+04,2.371374e+04,4.216965e+04,7.498942e+04,1.333521e+05]
        F_Gal_Center=[4.00336E-11,2.91153E-11,2.28477E-11,1.86270E-11,1.51850E-11,1.25372E-11,1.04837E-11,9.95361E-12,1.04586E-11,1.20124E-11,1.45149E-11,2.01676E-11,3.79969E-11]
        E_Gal_Pole=[1.333521e+02,2.371374e+02,4.216965e+02,7.498942e+02,1.333521e+03,2.371374e+03,4.216965e+03,7.498942e+03,1.333521e+04,2.371374e+04,4.216965e+04,7.498942e+04,1.333521e+05]
        F_Gal_Pole=[4.92969E-12,3.19788E-12,2.18257E-12,1.60750E-12,1.26150E-12,1.13832E-12,1.22700E-12,1.83975E-12,3.33679E-12,5.82638E-12,1.03031E-11,1.89262E-11,3.61147E-11]
        E_intermed=[1.333521e+02,2.371374e+02,4.216965e+02,7.498942e+02,1.333521e+03,2.371374e+03,4.216965e+03,7.498942e+03,1.333521e+04,2.371374e+04,4.216965e+04,7.498942e+04,1.333521e+05]
        F_intermed=[7.88487E-12,5.45022E-12,4.11703E-12,3.27224E-12,2.60095E-12,2.25907E-12,2.20006E-12,2.43230E-12,3.55555E-12,6.36779E-12,1.12605E-11,2.09498E-11,3.94729E-11]

        pylab.loglog(E_Gal_Center,F_Gal_Center,'c--',label="Sensitivity_Gal_Center")
        pylab.loglog(E_Gal_Pole,F_Gal_Pole,'m--',label="Sensitivity_Gal_Pole")
        pylab.loglog(E_intermed,F_intermed,'y--',label="Sensitivity_intermed")
        
        if pulsars:
            try:
                pulsar_name=sources[name]["psrname"]
                e_puls=sources[name]["pulsar_SED_energy"]
                SED_puls=sources[name]["pulsar_SED"]
                pylab.loglog(e_puls,SED_puls,'r-',label="Pulsar %s"%pulsar_name)
            except:
                print "pas de pulsar a traiter"
        pylab.ylim(1.0e-13,1.0e-10)
        pylab.legend(loc="best")
        pylab.savefig("%s/%s.png"%(output,name))

if __name__ == '__main__':

    if len(sys.argv)==1:
        filename="Super_File.yaml"
        output="plots"
        plot_seds(filename,output=output)
    elif len(sys.argv)==3:
        filename=sys.argv[1]
        output=sys.argv[2]
        plot_seds(filename,output=output)
    else:
        print "Usage python Super_file_utilities.py filename output"
