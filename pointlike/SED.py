"""
Implements a Module to calculate SEDs using the pyLikelihood framework.

The primary benefit to this implementation is that it requires no
temporary files. All you need is a BinnedAnalysis and
you can directly generate the SED.

Usage:

name='Vela'
like=BinnedAnalysis(...)
sed = SED(like,name)
sed.save('sed_Vela.dat')
sed.plot('sed_Vela.png') # requires matplotlib

@author J. Lande <lande@slac.stanford.edu>

$Header:$
"""
from os.path import join
import math
import numpy as np

from LikelihoodState import LikelihoodState
from pyLikelihood import dArg

class SED(object):
    """ object to make SEDs using pyLikelihood. 
    
        Currently, this object only allows the SED
        points to be the same as the binning in
        the FT1 file. """

    ul_choices = ['frequentist', 'bayesian']

    def __init__(self, like, name, verbosity=0, 
                 freeze_background=True,
                 always_upper_limit=False,
                 ul_algorithm='bayesian',
                 powerlaw_index=-2,
                 min_ts=4):
        """ Parameters:
            * like - pyLikelihood object
            * name - source to make an SED for
            * verbosity - how much output
            * freeze_background - don't refit background sources.
            * always_upper_limit - Always compute an upper limit. Default 
                                   is only when source is not significant. 
            * ul_algorithm - choices = 'frequentist', 'bayesian' 
            * powerlaw_index - fixed spectral index to assume when
                               computing SED.
            * min_ts - minimum ts in which to quote a SED points instead of an upper limit.
        """
        self.like               = like
        self.name               = name
        self.verbosity          = verbosity
        self.freeze_background  = freeze_background
        self.always_upper_limit = always_upper_limit
        self.ul_algorithm       = ul_algorithm
        self.powerlaw_index     = powerlaw_index
        self.min_ts             = min_ts

        if ul_algorithm not in self.ul_choices:
            raise Exception("Upper Limit Algorithm %s not in %s" % (ul_algorithm,str(self.ul_choices)))

        self.bin_edges = like.energies
        self.e_vals = like.e_vals

        # dN/dE in units of ph/cm^2/s/MeV
        self.dnde=np.empty_like(self.e_vals)
        self.dnde_err=np.empty_like(self.e_vals)
        self.ts=np.empty_like(self.e_vals)
        self.ul=-1*np.ones_like(self.e_vals) # -1 is no UL
        self._calculate()

    @staticmethod
    def frequentist_upper_limit(like,name,verbosity,emin,emax):
        """ Calculate a frequentist upper limit on the
            prefactor. """
        import UpperLimits
        ul = UpperLimits.UpperLimits(like)
        ul_prof, par_prof = ul[name].compute(emin=emin, emax=emax, verbosity=verbosity)
        prefactor=like[like.par_index(name, 'Prefactor')]
        return par_prof*prefactor.getScale()

    @staticmethod
    def bayesian_upper_limit(like,name,verbosity):
        """ Calculate a baysian upper limit.
            Return the fit prefactor value (which is dN/dE
            in the geometric mean of the energy bin
            since scale is set to the geometric mean
            of the energy bin). """
        import IntegralUpperLimit
        ul_flux,results = IntegralUpperLimit.calc_int(like, name, 
                                                      freeze_all=True,
                                                      skip_global_opt=True,
                                                      cl=0.95,
                                                      verbosity=verbosity)
        prefactor=like[like.par_index(name, 'Prefactor')]
        return results['ul_value']*prefactor.getScale()

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
        index.setValue(self.powerlaw_index/index.getScale())
        index.setFree(0)

        prefactor=like[like.par_index(name, 'Prefactor')]

        # assume a canonical dnde=1e-11 at 1GeV index 2 starting value
        dnde = lambda e: 1e-11*(e/1e3)**-2

        like.syncSrcParams(name)

        optverbosity = max(verbosity-1, 0) # see IntegralUpperLimit.py

        for i,(lower,upper) in enumerate(zip(self.bin_edges[:-1],self.bin_edges[1:])):

            e = math.sqrt(lower*upper)

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

            like.fit(optverbosity,covar=True)
            self.ts[i]=like.Ts(name,reoptimize=False)

            if self.ts[i] < self.min_ts or self.always_upper_limit: 
                if verbosity: print 'Calculating upper limit from %.0dMeV to %.0dMeV' % (lower,upper)
                if self.ul_algorithm == 'frequentist':
                    self.ul[i] = SED.frequentist_upper_limit(like,name,verbosity,lower,upper)
                elif self.ul_algorithm == 'bayesian':
                    self.ul[i] = SED.bayesian_upper_limit(like,name,verbosity)

            prefactor=like[like.par_index(name, 'Prefactor')]
            self.dnde[i] = prefactor.getValue()*prefactor.getScale()
            self.dnde_err[i] = prefactor.error()*prefactor.getScale()
            if verbosity:
                print lower,upper,self.dnde[i],self.dnde_err[i],self.ts[i] ,self.ul[i]

        # revert to old model
        like.setEnergyRange(self.bin_edges[0],self.bin_edges[-1])
        like.setSpectrum(name,old_spectrum)
        saved_state.restore()

    def __str__(self,terse=True,precision=1):
        """ Pack up values into a nicely formatted string.

            If terse=True, only include energy, flux, and flux_err 
            where flux is replaced by the upper limit if there is 
            a < 3sigma detection. If terse=False, also include
            a column of TS values, upper limits, Lower and Upper
            energies, and fluxes + flux errors (even when
            insignificant. """

        # convert list to scientific notation
        conv_science = lambda vals: ['%.*e' % (precision,i) \
                                 if not isinstance(i,str) else i \
                                 for i in vals]
        conv_float   = lambda vals: ['%.*f' % (precision,i) for i in vals]

        sed_vals = []
        sed_vals.append(['Energy', '[MeV]'] + conv_float(self.e_vals))

        # contains flux + UL if TS < min_ts 
        sed_vals.append(['Flux', '[ph/cm^2/s/MeV]'] + \
                        conv_science([f if ts>=self.min_ts else '<%.*e' % (precision,ul) \
                                  for f,ul,ts in zip(self.dnde,self.ul,self.ts)]))

        # contains flux error if TS > min_ts
        sed_vals.append(['Flux_Err', ''] + \
                        conv_science([ferr if ts>=self.min_ts else '' \
                                  for ferr,ts in zip(self.dnde_err,self.ts)]))

        if not terse:
            # add into the list everything else somebody might want.
            sed_vals.append(['Lower_Energy',   ''] + conv_float(self.bin_edges[:-1]))
            sed_vals.append(['Upper_Energy',   ''] + conv_float(self.bin_edges[1:]))
            sed_vals.append(['Raw_Flux',       ''] + conv_science(self.dnde))
            sed_vals.append(['Raw_Flux_Err',   ''] + conv_science(self.dnde_err))
            sed_vals.append(['Test_Statistic', ''] + conv_float(self.ts))
            # only include when upper limit was calculated
            sed_vals.append(['Upper_Limit', ''] + \
                            conv_science([u if u >= 0 else '' for u in self.ul]))

        sed_transpose = zip(*sed_vals)

        return '\n'.join([
            ''.join(['%20s' % j for j in i]) for i in sed_transpose
        ])

    def save(self,filename,precision=5,**kwargs):
        """ Save SED data points to a file.
            By default, save with 5 points of
            precision and save out everything that
            can be saved out. """
        output=self.__str__(precision=precision,**kwargs)
        if hasattr(filename,'write'):
            filename.write(output)
        else:
            f=open(filename,'w')
            f.write(output)
            f.close()

    def plot(self,filename=None,plot_spectral_fit=True, axes=None, fignum=None, figsize=(4,4)):
        try:
            import pylab as P
        except:
            raise Exception("SED.plot() requires pylab.")

        if axes is None:
            fig = P.figure(fignum,figsize)
            axes = fig.add_subplot(111)

        # Plot SED points

        elow=self.bin_edges[:-1]
        ehi=self.bin_edges[1:]

        e=self.e_vals
        de=[(self.e_vals-elow),
            (ehi-self.e_vals)
           ]

        significant = self.ts>=self.min_ts
        f=self.e_vals**2*\
                np.where(significant,self.dnde,self.ul)

        df = [
            # lower error
            self.e_vals**2*\
            np.where(significant,self.dnde_err,0.4*self.ul),
            # upper error
            self.e_vals**2*\
            np.where(significant,self.dnde_err,0)
        ]
           
        P.errorbar(e,f, xerr=de, yerr=df, linestyle='none',  
                   lolims=self.ts<self.min_ts, zorder=3)

        if plot_spectral_fit:
            source = self.like.logLike.getSource(self.name)
            spectrum=source.spectrum()
            elist = np.logspace(np.log10(self.like.energies[0]),
                                np.log10(self.like.energies[-1]))
            flist = np.asarray([spectrum(dArg(i)) for i in elist])
            P.plot(elist,elist**2*flist, zorder=2)

        P.xscale('log')
        P.xlabel('MeV')

        P.yscale('log')
        P.ylabel(r'Energy Flux $(\mathrm{MeV}\ \mathrm{cm}^{-2}\ \mathrm{s}^{-1})$')

        if filename is not None: P.savefig(filename)
