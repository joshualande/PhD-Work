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

def plot_seds(filename,output="plots"):
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
            e=sources[name][energ_r]["SED"]["points"]["Emean"]
            f=sources[name][energ_r]["SED"]["points"]["E2dNdE"]
            err=sources[name][energ_r]["SED"]["points"]["E2dNdE_Err"]
            if len(e)!=0:
                pylab.errorbar(e, f, xerr=0.0,yerr=err, fmt='b+')

        pylab.savefig("plots/%s.png"%name)

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
