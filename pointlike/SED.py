"""
Implements a Module to calculate SEDs using the pyLikelihood framework.

The primary benefit to this implementation is that it requires no
temporary files and automatically saves the output in
a nice format. All you need is a BinnedAnalysis and
you can directly generate the SED.

Usage:

name='Vela'
like=BinnedAnalysis(...)
sed = SED(like,name)
sed.save('sed_Vela.dat') # save data points
sed.plot('sed_Vela.png') # requires matplotlib

# Later on the SED can be replotted from the file:
import pylab
# axes is a matplotlib object which can
# be later modified
axes=plot_from_file('sed_Vela.dat')
pylab.savefig('sed_Vela.png')

@author J. Lande <lande@slac.stanford.edu>

Todo:
* Add energy flux to file output
* Allow saving/plotting SED in different units (eV, TeV, ergs).

$Header:$
"""
from os.path import join
import csv
import math
import pprint

import pylab as P
import numpy as np

from LikelihoodState import LikelihoodState
from pyLikelihood import dArg, ParameterVector, FunctionFactory

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
        self.energies = like.energies

        # dN/dE in units of ph/cm^2/s/MeV
        self.dnde=np.empty_like(self.energies)
        self.dnde_err=np.empty_like(self.energies)
        self.ts=np.empty_like(self.energies)
        self.ul=-1*np.ones_like(self.energies) # -1 is no UL
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
        index.setTrueValue(self.powerlaw_index)
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
            self.dnde[i] = prefactor.getTrueValue()
            self.dnde_err[i] = prefactor.error()*prefactor.getScale()
            if verbosity:
                print lower,upper,self.dnde[i],self.dnde_err[i],self.ts[i],self.ul[i]

        # revert to old model
        like.setEnergyRange(self.bin_edges[0],self.bin_edges[-1])
        like.setSpectrum(name,old_spectrum)
        saved_state.restore()

    def __str__(self,precision=1):
        """ Pack up values into a nicely formatted string.

            If self.verbosity=False, only include energy, flux, and flux_err 
            where flux is replaced by the upper limit if there is 
            a < 3sigma detection. If verbosity=False, also include
            a column of TS values, upper limits, Lower and Upper
            energies, and fluxes + flux errors (even when
            insignificant. """

        # convert list to scientific notation
        conv_science = lambda vals: ['%.*e' % (precision,i) \
                                 if not isinstance(i,str) else i \
                                 for i in vals]
        conv_float   = lambda vals: ['%.*f' % (precision,i) for i in vals]

        sed_vals = []
        sed_vals.append(['Energy', '[MeV]'] + conv_float(self.energies))

        # contains flux + UL if TS < min_ts 
        sed_vals.append(['Flux', '[ph/cm^2/s/MeV]'] + \
                        conv_science([f if ts>=self.min_ts else '<%.*e' % (precision,ul) \
                                  for f,ul,ts in zip(self.dnde,self.ul,self.ts)]))

        # contains flux error if TS > min_ts
        sed_vals.append(['Flux_Err', ''] + \
                        conv_science([ferr if ts>=self.min_ts else '' \
                                  for ferr,ts in zip(self.dnde_err,self.ts)]))

        if self.verbosity:
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
        ]) + '\n' # this last newline is helpful for genfromtxt


    @staticmethod
    def spectrum_to_string(spectrum, precision):
        """ Create a simple text representation
            of a gtlike spectrum object which
            can be saved to a file. """
        parameters=ParameterVector()
        spectrum.getParams(parameters)

        d = dict(name = spectrum.genericName())

        class nice_float(float):
            """ Overload __repr__ for better formatting. """
            def __repr__(self): return '%.*e' % (precision,self)

        for p in parameters:
            d[p.getName()]= nice_float(p.getTrueValue())
        return pprint.pformat(d,width=1e10)

    @staticmethod
    def string_to_spectrum(spectrum):
        """ Load back as a pyLikelihood spectrum object
            a spectrum that has been saved by the spectrum_to_string
            object. """
        d = eval(spectrum)
        spectrum=FunctionFactory().create(d.pop('name'))
        for k,v in d.items(): spectrum.getParam(k).setTrueValue(v)
        return spectrum

    def get_comments(self, precision):

        spectrum = self.like.logLike.getSource(self.name).spectrum()

        comments = [
            "# SED for %s: %s" % (
                self.name,pprint.pformat(dict(
                    ul_algorithm=self.ul_algorithm,
                    powerlaw_index=self.powerlaw_index,
                    min_ts=self.min_ts))),
            '# '+ SED.spectrum_to_string(spectrum, precision=precision)
        ]
        return '\n'.join(comments)

    def save(self,filename,precision=3,**kwargs):
        """ Save SED data points to a file.
            By default, save with 5 points of
            precision and save out everything that
            can be saved out. """
        output=self.get_comments(precision=precision) + '\n' + self.__str__(precision=precision,**kwargs)
        if hasattr(filename,'write'):
            filename.write(output)
        else:
            f=open(filename,'w')
            f.write(output)
            f.close()

    @staticmethod 
    def _plot_data(energies, dnde, dnde_err, ul, significant,
                   axes=None, fignum=None, figsize=(4,4),
                   plot_spectral_fit=True, spectrum=None,
                   spectral_kwargs=dict(color='red'),
                  ):
        """ Plot SED points and upper limits. 

            spectrum: pyLikelihood spectrum object (required if plot_spectral_fit=True)
            """

        if axes is None:
            fig = P.figure(fignum,figsize)
            axes = fig.add_axes((0.2,0.15,0.75,0.8))

        e=energies
        s = significant

        # recreate bin edges from geometric
        # mean of energy bins
        bin_edges=np.empty((len(e)+1,))
        le=np.log10(e)
        bin_edges[:-2] = 10**(le[:-1] - (le[1:]-le[:-1])/2)
        bin_edges[2:] = 10**(le[1:]  + (le[1:]-le[:-1])/2)

        elow=bin_edges[:-1]
        ehi=bin_edges[1:]

        delo=e-elow
        dehi=ehi-e

        # plot data points
        if sum(s)>0:
            axes.errorbar(e[s], e[s]**2*dnde[s],
                          xerr=[delo[s],dehi[s]],
                          yerr=e[s]**2*dnde_err[s], 
                          linestyle='none',  
                          color='black', capsize=0)
        
        # and upper limits
        if sum(~s)>0:
            axes.errorbar(e[~s], e[~s]**2*ul[~s], 
                          xerr=[delo[~s],dehi[~s]],
                          yerr=[ 0.4*e[~s]**2*ul[~s], np.zeros(sum(~s))],
                          linestyle='none',
                          lolims=True, 
                          color='black')

        l,h=np.log10(elow[0]),np.log10(ehi[-1])

        low_lim=10**(l - 0.1*(h-l))
        hi_lim =10**(h + 0.1*(h-l))

        # overlay best fit spectra.
        if plot_spectral_fit:
            elist = np.logspace(np.log10(low_lim), np.log10(hi_lim), 100)
            flist = np.asarray([spectrum(dArg(i)) for i in elist])
            axes.plot(elist,elist**2*flist, zorder=1, **spectral_kwargs)

        axes.set_xlim(low_lim,hi_lim)

        axes.set_xscale('log');
        axes.set_xlabel('MeV')

        axes.set_yscale('log')
        axes.set_ylabel(r'Energy Flux $(\mathrm{MeV}\,\mathrm{cm}^{-2}\,\mathrm{s}^{-1})$')

        return axes

    def plot(self, filename=None, **kwargs):

        significant = self.ts>=self.min_ts

        source = self.like.logLike.getSource(self.name)
        spectrum=source.spectrum()

        axes = SED._plot_data(self.energies, self.dnde, self.dnde_err, self.ul, 
                              significant, spectrum=spectrum, **kwargs)

        if filename is not None: P.savefig(filename)

    @staticmethod
    def plot_from_file(filename,**kwargs):
        """ Plots the SED points from a file saved
        by the SED.save function. """

        r=np.genfromtxt(filename, names=True, invalid_raise=False, dtype=object, delimiter=20, autostrip=True,
                       skip_header=2)

        if r['Energy'][0] != '[MeV]' or r['Flux'][0] != '[ph/cm^2/s/MeV]':
            raise Exception("Wrong Units in File!")

        energies = r['Energy'][1:].astype(float)

        flux_char = np.char.array(r['Flux'][1:])

        significant = flux_char.find('<') == -1

        # strip out the limits + convert to float
        temp = flux_char.replace('<', '')
        dnde = np.array(temp).astype(float)

        temp = r['Flux_Err'][1:]
        temp = np.where( temp != '', temp, 0)
        dnde_err = np.array(temp).astype(float)

        ul = np.where(~significant,dnde,0)

        spectrum=SED.string_to_spectrum(
            open(filename).readlines()[1].replace('#',''))

        # plot the SED
        SED._plot_data(energies, dnde, dnde_err, ul, significant, 
                       spectrum=spectrum,
                       **kwargs)
                             
plot_from_file = SED.plot_from_file
