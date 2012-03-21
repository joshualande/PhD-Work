import yaml
import os,sys
import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
import numpy as num
import pylab
sources=yaml.load(open("tev_super_file.yaml"))
os.system("rm -rf plots/*")

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
        #print e
        #print f
        #print err
        if len(e)!=0:
            pylab.errorbar(e, f, xerr=0.0,yerr=err, fmt='b+')

    pylab.savefig("plots/%s.png"%name)
