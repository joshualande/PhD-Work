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
sed = SED(like,name, flux_units='erg')
# To quote the (x-axis energy in 'GeV'):
sed = SED(like,name, energy_units='GeV')


# save data points. The default file is very terse
sed.save('sed_Vela.dat') 

# to save out additional values (like TS, energy ranges):
sed.verbosity=True
sed.save('sed_Vela.dat')

sed.plot('sed_Vela.png') # requires matplotlib

# If you are doing something fancy with Matplotlib,
# you can give the axes you want the data points added to.

sed.plot(axes=axes)
# do something else to the plot ...
pylab.savefig('fancy_sed.png')

# Later on the SED can be replotted from the saved file:

import pylab
# axes is a matplotlib object which can
# be later modified
axes=plot_from_file('sed_Vela.dat')

# here, additional things could be done with the
# axes object.
pylab.savefig('sed_Vela.png')

@author J. Lande <lande@slac.stanford.edu>

Todo:
* Add energy flux to file output
* Allow larger energy bins than those in the BinnedAnalysis
  object.
* Merge upper limits at either edge in energy.

$Header:$
"""
from os.path import join
import csv
import math
import pprint

import pylab as P
import numpy as np

from LikelihoodState import LikelihoodState
import pyLikelihood
_funcFactory = pyLikelihood.SourceFactory_funcFactory()

class PrettyTable(object):
    """ Define a very simple file format for saving
        SED points. """
    def __init__(self,precision,colwidth): 
        self.precision, self.colwidth = precision, colwidth

    def fmt(self,i,fmt='s', ul=False):
        """ Format a number to have a fixed width and precision.
            ul = format as upper limit with a < in front of number. 
            If input is None or nan, leave a blank in the file. """
        print i,i is None,np.isnan(i)
        if fmt == 's': return '%*s' % (self.colwidth,i)
        if i is None or np.isnan(i): return ' '*self.colwidth

        if ul:
            temp=('<%.*'+fmt) % (self.precision,i)
            return '%*s' % (self.colwidth,temp)
        return ('%*.*'+fmt) % (self.colwidth, self.precision, i)

    def dump(self,data,comments=[]):
        """ Writes data structure of the from:
            [ dict(name='energy', unit='[MeV]', data=[1,2,3],                          fmt='e'), 
              dict(name='flux',   unit='[GeV]', data=[1,2,3], ul=[False, False, True], fmt='f')] . """
        lines = ['# '+c for c in comments] # comments
        lines.append(''.join([self.fmt(d['name']) for d in data])) #names
        lines.append(''.join([self.fmt(d['unit']) for d in data])) # nnits
        for i in range(len(data[0]['data'])): # data
            lines.append(''.join([self.fmt(d['data'][i], fmt=d['fmt'],
                                           ul=d['ul'][i] if d.has_key('ul') else False) 
                                  for d in data]))

        return '\n'.join(lines)

    def load(self,filename):
        """ Parses the saved data back into data structure. """
        cw=self.colwidth

        lines = [i.rstrip() for i in open(filename).readlines()]

        data,comments = [],[]
        for i in reversed(range(len(lines))):
            if lines[i][0]=='#': comments.insert(0,lines.pop(i).replace('#','').strip())

        for i,line in enumerate(lines):
            if len(line) % cw !=0: raise Exception("Wrong colwidth for line %s." % i)

        for i in range(len(lines[0])/cw):
            l=cw*i; u=l+cw
            d=dict(
                name=lines[0][l:u].strip(),
                unit=lines[1][l:u].strip())
            d['data']=[line[l:u].strip() for line in lines[2:]]

            if '<' in ''.join(d['data']): d['ul']=['<' in i for i in d['data']]
            d['data']=[i.replace('<','') for i in d['data']]

            d['data']=[i if i !='' else None for i in d['data']]
            data.append(d)

        return data,comments


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
                 min_ts=4,
                 flux_units='erg',
                 energy_units='MeV'):
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
            * flux_units - desired units to quote energy flux (y axis) in.
            * energy_units - desired units to quote energy (x axis) in. """
        self.like               = like
        self.name               = name
        self.verbosity          = verbosity
        self.freeze_background  = freeze_background
        self.always_upper_limit = always_upper_limit
        self.ul_algorithm       = ul_algorithm
        self.powerlaw_index     = powerlaw_index
        self.min_ts             = min_ts

        self.flux_units  = flux_units
        self.energy_units       = energy_units

        if self.flux_units not in [ 'eV', 'MeV', 'GeV', 'TeV', 'erg']:
            raise Exception('flux_units must be eV, Mev TeV, or erg')
        if self.energy_units not in [ 'eV', 'MeV', 'GeV', 'TeV', 'erg']:
            raise Exception('energy_units must be eV, Mev TeV, or erg')
        if ul_algorithm not in self.ul_choices:
            raise Exception("Upper Limit Algorithm %s not in %s" % (ul_algorithm,str(self.ul_choices)))

        # These energies are always in MeV
        self.bin_edges = like.energies
        self.energies = like.e_vals

        # dN/dE, dN/dE_err and upper limits (ul)
        # always in units of ph/cm^2/s/MeV
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

    # functions for unit conversions.
    # These functions could be cleanded up.
    # For example: convert(energy=100,from='MeV',to='erg')
    @staticmethod
    def energy_from_MeV(energy, energy_units):
        """ Converts energy from MeV to specified output. """
        return energy*dict(eV=1e6, MeV=1, GeV=1e-3, TeV=1e-6, erg=1.60217646e-6)[energy_units]

    @staticmethod
    def energy_to_MeV(*args,**kwargs): 
        """ Convert energy to MeV. """
        return SED.flux_from_MeV(*args,**kwargs)

    @staticmethod
    def flux_from_MeV(flux, flux_units):
        """ Converts from ph/cm^2/s/MeV to desired output. """
        return flux*dict(eV=1e-6, MeV=1, GeV=1e3, TeV=1e6, erg=6.24150974e5)[flux_units]

    @staticmethod
    def flux_to_MeV(*args,**kwargs): 
        """ Convert flux to MeV. """
        return SED.energy_from_MeV(*args,**kwargs)

    def __str__(self,precision=1, colwidth=20, comments=[]):
        """ Pack up values into a nicely formatted string.

            If self.verbosity=False, only include energy, flux, and flux_err 
            where flux is replaced by the upper limit if there is 
            a < 3sigma detection. If verbosity=False, also include
            a column of TS values, upper limits, Lower and Upper
            energies, and fluxes + flux errors (even when
            insignificant. """

        significant=self.ts>=self.min_ts

        cf=lambda f: SED.flux_from_MeV(f,self.flux_units)
        ce=lambda e: SED.energy_from_MeV(e, self.energy_units)

        eu = '[%s]' % self.energy_units
        fu = '[ph/cm^2/s/%s]' % self.flux_units

        # note, set empty columns to nan

        data = [
            dict(name='Energy',        unit=eu,           fmt='f', data=ce(self.energies)),
            dict(name='Flux',          unit=fu, fmt='e',
                 data=cf(np.where(significant, self.dnde, self.ul)), ul=~significant),
            dict(name='Flux_Err',      unit=fu, fmt='e', 
                 data=cf(np.where(significant,self.dnde_err,np.nan).astype(float)))
        ]

        if self.verbosity:
            data += [
                dict(name='Lower_Energy',   unit=eu, fmt='f', data=ce(self.bin_edges[:-1])),
                dict(name='Upper_Energy',   unit=eu, fmt='f', data=ce(self.bin_edges[1:])),
                dict(name='Raw_Flux',       unit=fu, fmt='e', data=cf(self.dnde)),
                dict(name='Raw_Flux_Err',   unit=fu, fmt='e', data=cf(self.dnde_err)),
                dict(name='Test_Statistic', unit='', fmt='f', data=self.ts),
                dict(name='Upper_Limit',    unit=fu, fmt='e', 
                     data=cf(np.where(~significant,self.ul,np.nan).astype(float)))
            ]

        table=PrettyTable(precision=precision, colwidth=colwidth)
        return table.dump(data,comments=comments)

    @staticmethod
    def spectrum_to_string(spectrum, precision):
        """ Create a simple text representation
            of a gtlike spectrum object which
            can be saved to a file. Always
            create this object with the same
            units as pyLikelihood. """
        parameters=pyLikelihood.ParameterVector()
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
        spectrum=_funcFactory.create(d.pop('name'))
        for k,v in d.items(): spectrum.getParam(k).setTrueValue(v)
        return spectrum

    def get_comments(self, precision):
        """ Pack up the source name and spectrum for a nice header. """
        spectrum = self.like.logLike.getSource(self.name).spectrum()
        return [ "SED for %s" % self.name,
                 SED.spectrum_to_string(spectrum, precision=precision)]

    def save(self,filename,precision=3,**kwargs):
        """ Save SED data points to a file.
            By default, save with 5 points of
            precision and save out everything that
            can be saved out. """
        output=self.__str__(precision=precision,
                            comments=self.get_comments(precision),
                            **kwargs)
        if hasattr(filename,'write'):
            filename.write(output)
        else:
            f=open(filename,'w')
            f.write(output)
            f.close()

    @staticmethod 
    def _plot_data(energies, dnde, dnde_err, ul, significant,
                   energy_units, flux_units,
                   axes=None, fignum=None, figsize=(4,4),
                   plot_spectral_fit=True, spectrum=None,
                   spectral_kwargs=dict(color='red'),
                  ):
        """ Plot SED points and upper limits. 
            
            energies must be in MeV
            dnde, dnde_err, and ul must be in ph/cm^2/s/MeV

            energy_units - unit to plot energy in (x axis)
            flux_units - unit to plot flux in (y axis)

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


        # map x values (in MeV) to desired units
        x = lambda e: SED.energy_from_MeV(e,energy_units)
        # map y values (in MeV*2 * ph/cm^2/s/MeV) to desired units
        y = lambda f: SED.energy_from_MeV(f,flux_units)

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
                          y(e[~s]**2*ul[~s]),
                          yerr=[y(0.4*e[~s]**2*ul[~s]),np.zeros(sum(~s))],
                          **ul_kwargs)

            # plot horizontal line (no caps)
            axes.errorbar(x(e[~s]),
                          y(e[~s]**2*ul[~s]),
                          xerr=[x(delo[~s]),x(dehi[~s])],
                          capsize=0, **ul_kwargs)

        l,h=np.log10(elow[0]),np.log10(ehi[-1])

        low_lim=10**(l - 0.1*(h-l))
        hi_lim =10**(h + 0.1*(h-l))

        # overlay best fit spectra.
        if plot_spectral_fit:
            elist = np.logspace(np.log10(low_lim), np.log10(hi_lim), 100)
            # remember that gtlike always returns ph/cm^2/s/MeV
            flist = np.asarray([spectrum(pyLikelihood.dArg(i)) for i in elist])
            axes.plot(x(elist), y(elist**2*flist), zorder=1, **spectral_kwargs)

        axes.set_xlim(low_lim,hi_lim)

        axes.set_xscale('log');
        axes.set_xlabel('Energy (%s)' % energy_units)

        axes.set_yscale('log')
        axes.set_ylabel(r'Energy Flux (%s cm$^{-2}$ s$^{-1}$)' % flux_units)

        return axes

    def plot(self, filename=None, **kwargs):

        significant = self.ts>=self.min_ts

        source = self.like.logLike.getSource(self.name)
        spectrum=source.spectrum()

        axes = SED._plot_data(self.energies, self.dnde, 
                              self.dnde_err, self.ul, 
                              significant,
                              energy_units = self.energy_units,
                              flux_units = self.flux_units,
                              spectrum=spectrum, **kwargs)

        if filename is not None: P.savefig(filename)

    @staticmethod
    def plot_from_file(filename,precision=3,colwidth=20,
                       energy_units='MeV', flux_units='erg',
                       **kwargs):
        """ Plots the SED points from a file created 
            by SED.save(). Regardless of what units 
            are saved in the log file, the units of
            the plotted energy and flux can be modified
            by the input parameters. """

        table=PrettyTable(precision=precision, colwidth=colwidth)
        data,comments=table.load(filename)

        energy=next(d for d in data if d['name']=='Energy')
        flux=next(d for d in data if d['name']=='Flux')
        flux_err=next(d for d in data if d['name']=='Flux_Err')

        file_energy_units = energy['unit'].replace('[','').replace(']','')
        if flux['unit'] != flux_err['unit']:
            raise Exception("Flux and Flux_Err must be the same units")
        file_flux_units = flux['unit'].replace('[ph/cm^2/s/','').replace(']','')

        # convert whatever units are in the file for energy and flux to
        # MeV and ph/cm^2/s/MeV to injest into _plot_data
        e = SED.energy_to_MeV(np.asarray(energy['data'],dtype=float), file_energy_units)

        significant = ~np.asarray(flux['ul']) if flux.has_key('ul') else np.asarray([True]*len(e))

        flux=SED.flux_to_MeV(np.asarray(flux['data'],dtype=float),file_flux_units)
        dnde = np.where(significant,flux,0)
        ul = np.where(~significant,flux,0)
        dnde_err = SED.flux_to_MeV(np.asarray(flux_err['data'],dtype=float),file_flux_units)

        spectrum=SED.string_to_spectrum(comments[1])

        # plot the SED
        SED._plot_data(e, dnde, dnde_err, ul, significant, 
                       spectrum=spectrum, 
                       energy_units = energy_units,
                       flux_units = flux_units,
                       **kwargs)
                             
plot_from_file = SED.plot_from_file
