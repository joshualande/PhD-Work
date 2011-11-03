"""
A Module to calculate SEDs using the pyLikelihood framework.

The primary benefit to this implementation is that it requires no
temporary files and automatically saves the output in a nice format. All
you need is a BinnedAnalysis and you can directly generate the SED.

The SED is created by modifying the source of interest to have
a fixed spectral index and in each energy band fitting
the flux of the source.

Usage:

name='Vela'
like=BinnedAnalysis(...)
sed = SED(like,name)

# by default, energy is quoted in MeV and
# flux is quted in erg/cm^2/s:
sed = SED(like,name)


# save data points to a file
sed.save('sed_Vela.dat') 

# plot the SED
sed.plot('sed_Vela.png') 

To pase the outptu file,

results_dictionary=eval(open('sed_vela.data').read())

@author J. Lande <lande@slac.stanford.edu>

Todo:
* Merge upper limits at either edge in energy.
"""
from os.path import join
import csv
from pprint import pformat
from StringIO import StringIO
from collections import OrderedDict

import pylab as P
import numpy as np

from LikelihoodState import LikelihoodState
from pyLikelihood import ParameterVector
import pyLikelihood
_funcFactory = pyLikelihood.SourceFactory_funcFactory()



class SED(object):
    """ object to make SEDs using pyLikelihood. 
    
        Currently, this object only allows the SED
        points to be the same as the binning in
        the FT1 file. """

    ul_choices = ['frequentist', 'bayesian']

    def __init__(self, like, name, 
                 bin_edges=None,
                 verbosity=0, 
                 freeze_background=True,
                 always_upper_limit=False,
                 ul_algorithm='bayesian',
                 powerlaw_index=-2,
                 min_ts=4):
        """ Parameters:
            * like - pyLikelihood object
            * name - source to make an SED for
            * bin_edges - if specified, calculate the SED in these bins.
            * verbosity - how much output
            * freeze_background - don't refit background sources.
            * always_upper_limit - Always compute an upper limit. Default 
                                   is only when source is not significant. 
            * ul_algorithm - choices = 'frequentist', 'bayesian' 
            * powerlaw_index - fixed spectral index to assume when
                               computing SED.
            * min_ts - minimum ts in which to quote a SED points instead of an upper limit. """
        self.like               = like
        self.name               = name
        self.verbosity          = verbosity
        self.freeze_background  = freeze_background
        self.always_upper_limit = always_upper_limit
        self.ul_algorithm       = ul_algorithm
        self.powerlaw_index     = powerlaw_index
        self.min_ts             = min_ts

        self.spectrum = self.like.logLike.getSource(self.name).spectrum()

        if bin_edges is not None:

            for e in bin_edges:
                if np.alltrue(np.abs(e - like.energies) > 0.5):
                    raise Exception("energy %.1f in bin_edges is not commensurate with the energy binning of pyLikelihood." % e)
            
            self.bin_edges = np.asarray(bin_edges)
            self.energies = np.sqrt(self.bin_edges[1:]*self.bin_edges[:-1])
        else:
            # These energies are always in MeV
            self.bin_edges = like.energies
            self.energies = like.e_vals

        self.lower_energy=self.bin_edges[:-1]
        self.upper_energy=self.bin_edges[1:]

        if ul_algorithm not in self.ul_choices:
            raise Exception("Upper Limit Algorithm %s not in %s" % (ul_algorithm,str(self.ul_choices)))

        # dN/dE, dN/dE_err and upper limits (ul)
        # always in units of ph/cm^2/s/MeV
        self.dnde=np.empty_like(self.energies)
        self.dnde_err=np.empty_like(self.energies)
        self.dnde_ul=-1*np.ones_like(self.energies) # -1 is no UL

        self.flux=np.empty_like(self.energies)
        self.flux_err=np.empty_like(self.energies)
        self.flux_ul=-1*np.ones_like(self.energies)

        self.eflux=np.empty_like(self.energies)
        self.eflux_err=np.empty_like(self.energies)
        self.eflux_ul=-1*np.ones_like(self.energies)

        self.ts=np.empty_like(self.energies)


        self._calculate()

    @staticmethod
    def frequentist_upper_limit(like,name,emin,emax,verbosity):
        """ Calculate a frequentist upper limit on the prefactor. 
            Returns the unscaled prefactor upper limit. """
        import UpperLimits
        ul = UpperLimits.UpperLimits(like)
        flux_ul, pref_ul = ul[name].compute(emin=emin, emax=emax, verbosity=verbosity)
        return pref_ul

    @staticmethod
    def bayesian_upper_limit(like,name,emin,emax,verbosity):
        """ Calculate a baysian upper limit on the prefactor.
            Return the unscaled prefactor upper limit. """
        import IntegralUpperLimit
        flux_ul,results = IntegralUpperLimit.calc_int(like, name, 
                                                      freeze_all=True,
                                                      skip_global_opt=True,
                                                      emin=emin, emax=emax,
                                                      verbosity=verbosity)
        pref_ul = results['ul_value']
        return pref_ul

    @staticmethod
    def upper_limit(like,name,ul_algorithm,emin,emax,*args,**kwargs):
        """ Calculates the upper limit. Returns the dN/dE, Flux, and eergy
            flux upper limit. """
        if ul_algorithm == 'frequentist': 
            f = SED.frequentist_upper_limit
        elif ul_algorithm == 'bayesian':  
            f = SED.bayesian_upper_limit

        pref_ul = f(like,name,emin,emax,*args,**kwargs)

        prefactor=like[like.par_index(name, 'Prefactor')]
        pref_ul *= prefactor.getScale() # scale prefactor
        prefactor.setTrueValue(pref_ul)

        flux_ul = like.flux(name,emin,emax)
        eflux_ul = like.energyFlux(name,emin,emax)

        return pref_ul,flux_ul, eflux_ul

    def _calculate(self):
        """ Compute the flux data points for each energy. """

        like    = self.like
        name    = self.name
        verbosity = self.verbosity

        # Freeze all sources except one to make sed of.
        all_sources = like.sourceNames()

        if name not in all_sources:
            raise Exception("Cannot find source %s in list of sources" % name)

        # make copy of parameter values + free parameters
        
        saved_state = LikelihoodState(like)

        if self.freeze_background:
            if verbosity: print 'Freezeing all parameters'
            # freeze all other sources
            for i in range(len(like.model.params)):
                like.freeze(i)

        # convert source to a PowerLaw of frozen index 

        source = like.logLike.getSource(name)
        old_spectrum=source.spectrum()
        like.setSpectrum(name,'PowerLaw')

        index=like[like.par_index(name, 'Index')]
        index.setTrueValue(self.powerlaw_index)
        index.setFree(0)

        # assume a canonical dnde=1e-11 at 1GeV index 2 starting value
        dnde = lambda e: 1e-11*(e/1e3)**-2

        like.syncSrcParams(name)

        optverbosity = max(verbosity-1, 0) # see IntegralUpperLimit.py

        for i,(lower,upper) in enumerate(zip(self.lower_energies,self.upper_energies)):

            e = np.sqrt(lower*upper)

            if verbosity: print 'Calculating spectrum from %.0dMeV to %.0dMeV' % (lower,upper)

            # goot starting guess for source
            prefactor=like[like.par_index(name, 'Prefactor')]
            prefactor.setScale(dnde(e))
            prefactor.setValue(1)
            prefactor.setBounds(1e-10,1e10)

            scale=like[like.par_index(name, 'Scale')]
            scale.setScale(1)
            scale.setValue(e)
            like.syncSrcParams(name)

            like.setEnergyRange(float(lower)+1, float(upper)-1)

            try:
                like.fit(optverbosity,covar=True)
            except Exception, ex:
                if verbosity: print 'ERROR gtlike fit: ', ex

            self.ts[i]=like.Ts(name,reoptimize=False)

            prefactor=like[like.par_index(name, 'Prefactor')]
            self.dnde[i] = prefactor.getTrueValue()
            self.dnde_err[i] = prefactor.error()*prefactor.getScale()

            self.flux[i] = like.flux(name, lower, upper)
            self.flux_err[i] = like.fluxError(name, lower, upper)

            self.eflux[i] = like.energyFluxError(name, lower, upper)
            self.eflux_err[i] = like.energyFluxError(name, lower, upper)

            if self.ts[i] < self.min_ts or self.always_upper_limit: 
                if verbosity: print 'Calculating upper limit from %.0dMeV to %.0dMeV' % (lower,upper)
                self.dnde_ul[i], self.flux_ul[i], self.eflux_ul[i] = SED.upper_limit(like,name,self.ul_algorithm,lower,upper,verbosity)

            if verbosity:
                print lower,upper,self.dnde[i],self.dnde_err[i],self.ts[i],self.dnde_ul[i]

        self.significant=self.ts>=self.min_ts

        # revert to old model
        like.setEnergyRange(self.bin_edges[0],self.bin_edges[-1])
        like.setSpectrum(name,old_spectrum)
        saved_state.restore()

    def todict(self):
        """ Create a dictionary of the SED results, entirely
            in gtlike units [MeV] and [ph/cm^2/s/MeV]. """

        data = OrderedDict()

        data['Lower_Energy']=self.lower_energy
        data['Upper_Energy']=self.upper_energy
        data['Energy']=self.energies
        data['Energy_Units'] = '[MeV]'

        data['dN/dE']=self.dnde
        data['dN/dE_Err']=self.dnde_err
        data['dN/dE_UL']=self.dnde_ul
        data['dN/dE_Units'] = '[ph/cm^2/s/MeV]'

        data['Ph_Flux']=self.dnde
        data['Ph_Flux_Err']=self.dnde_err
        data['Ph_Flux_UL']=self.dnde_ul
        data['Ph_Flux_Units'] = '[ph/cm^2/s]'

        data['En_Flux']=self.dnde
        data['En_Flux_Err']=self.dnde_err
        data['En_Flux_UL']=self.dnde_ul
        data['En_Flux_Units'] = '[MeV/cm^2/s]'

        data['Test_Statistic']=self.ts
        data['Significant']=self.significant

        data['Spectrum']=SED.spectrum_to_dict(self.spectrum)

    def __str__(self):
        """ Pack up values into a nicely formatted string. """
        results = self.todict()
        return pformat(results)

    @staticmethod
    def spectrum_to_dict(spectrum):
        """ Convert a pyLikelihood object to a python 
            dictionary which can be easily saved to a file. """
        parameters=ParameterVector()
        spectrum.getParams(parameters)
        d = dict(name = spectrum.genericName())
        for p in parameters: d[p.getName()]= p.getTrueValue()
        return d

    def save(self,filename,**kwargs):
        """ Save SED data points to a file. """
        if hasattr(filename,'write'):
            filename.write(self.__str__())
        else:
            f=open(filename,'w')
            f.write(self.__str__())
            f.close()

    @staticmethod 
    def plot_spectrum(axes,spectrum, npts=100, **kwargs):
        """ This function overlays a pyLikleihood spectrum
            object onto a Matplotlib axes assumign that
            (a) the x-axis is in MeV and (b) that
            the y-axis is E^2 dN/dE (MeV/cm^2/s) """
        low_lim, hi_lim = axes.get_xlim()
        elist = np.logspace(np.log10(low_lim), np.log10(hi_lim), npts)
        # remember that gtlike always returns ph/cm^2/s/MeV
        flist = np.asarray([spectrum(pyLikelihood.dArg(i)) for i in elist])
        axes.plot(elist, elist**2*flist, **kwargs)

    def plot(axes=None, filename=None):
        """ Plot the SED using matpotlib. """
        if axes is None:
            fig = P.figure(fignum,figsize)
            axes = fig.add_axes((0.2,0.15,0.75,0.8))

        e=self.energies
        s = self.significant

        delo=e-self.lower_energy
        dehi=self.upper_energy-e

        # plot data points
        if sum(s)>0:
            axes.errorbar(x(e[s]),
                          y(e[s]**2*dnde[s]),
                          xerr=[x(delo[s]),x(dehi[s])],
                          yerr=y(e[s]**2*dnde_err[s]),
                          linestyle='none',  color='black', capsize=0)
        
        # and upper limits
        if sum(~s)>0:
            ul_kwargs = dict(linestyle='none', lolims=True, color='black')

            # plot veritical lines (with arrow)
            axes.errorbar(x(e[~s]),
                          y(e[~s]**2*dnde_ul[~s]),
                          yerr=[y(0.4*e[~s]**2*dnde_ul[~s]),np.zeros(sum(~s))],
                          **ul_kwargs)

            # plot horizontal line (no caps)
            axes.errorbar(x(e[~s]),
                          y(e[~s]**2*dnde_ul[~s]),
                          xerr=[x(delo[~s]),x(dehi[~s])],
                          capsize=0, **ul_kwargs)

        l,h=np.log10(lower_energy[0]),np.log10(upper_energy[-1])
        low_lim=10**(l - 0.1*(h-l))
        hi_lim =10**(h + 0.1*(h-l))
        axes.set_xlim(low_lim,hi_lim)

        if plot_spectral_fit:
            SED.plot_spectrum(axes,self.spectrum)

        axes.set_xscale('log');
        axes.set_xlabel('Energy (MeV)')

        axes.set_yscale('log')
        axes.set_ylabel(r'Energy Flux (MeV cm$^{-2}$ s$^{-1}$)')

        if filename is not None: P.savefig(filename)
