from os.path import join
import math
import numpy as np

from LikelihoodState import LikelihoodState
import IntegralUpperLimit    # This requires scipy

class SED(object):
    """ object to make SEDs using pointlike. """

    def __init__(self,
                 like, # pyLike object
                 name, # Name of the source to make an SED of
                 verbosity=0, # Prints more stuff out
                 freeze_background=True, # don't refit background sources when making SED
                 #minos=False, # Compute minos errors
                 #always_upper_limit=False, # Compute
                 **kwargs
                ):

        self.like              = like
        self.name              = name
        self.verbosity         = verbosity
        self.freeze_background = freeze_background

        self.bin_edges = like.energies
        self.e_vals = like.e_vals

        # dN/dE in units of ph/cm^2/s/MeV
        self.dnde=np.empty_like(self.e_vals)
        self.dnde_err=np.empty_like(self.e_vals)
        self.ts=np.empty_like(self.e_vals)
        self.ul=-1*np.ones_like(self.e_vals) # -1 is no UL
        self.calculate(**kwargs)

    @staticmethod
    def upper_limit(like,name,verbosity):
        # do the integral approximatly: don't fit background parameters during fit
        ul_flux,results = IntegralUpperLimit.calc_int(like, name, 
                                                      freeze_all=True,
                                                      skip_global_opt=True,
                                                      cl=0.95,
                                                      verbosity=verbosity)
        return results['xlim']

    def calculate(self):

        like    = self.like
        name    = self.name
        verbosity = self.verbosity

        # Freeze all sources except one to make sed of.
        all_sources = like.sourceNames()

        if name not in all_sources:
            raise Exception("Cannot find source %s in list of sources" % name)

        # make copy of parameter values + free parameters
        
        saved_state = LikelihoodState(like)

        if verbosity: print 'Freezeing all parameters'

        if self.freeze_background:
            # freeze all other sources
            for i in range(len(like.model.params)):
                like.freeze(i)

        # convert source to a PowerLaw of (frozen) index 2

        source = like.logLike.getSource(name)
        old_spectrum=source.spectrum()
        like.setSpectrum(name,'PowerLaw')

        index=like[like.par_index(name, 'Index')]
        prefactor=like[like.par_index(name, 'Prefactor')]
        scale=like[like.par_index(name, 'Scale')]

        index.setValue(-2/index.getScale())
        index.setFree(0)
        prefactor.setScale(1e-11)
        prefactor.setBounds(1e-10,1e10)

        like.syncSrcParams(name)

        for i,(lower,upper) in enumerate(zip(self.bin_edges[:-1],self.bin_edges[1:])):

            if verbosity: print 'Calculating spectrum from %.0dMeV to %.0dMeV' % (lower,upper)

            # goot starting guess for source
            like.syncSrcParams(name)
            prefactor.setValue(1e-11/prefactor.getScale())
            scale.setValue(math.sqrt(lower*upper)/scale.getScale())
            like.syncSrcParams(name)

            like.setEnergyRange(float(lower)+1, float(upper)-1)
            like.fit(covar=True,verbosity=3 if verbosity else 0)
            self.ts[i]=like.Ts(name,reoptimize=False)

            if self.ts[i] < 9: 
                if verbosity: print 'Calculating upper limit from %.0dMeV to %.0dMeV' % (lower,upper)
                self.ul[i] = SED.upper_limit(like,name,verbosity)

            prefactor=like[like.par_index(name, 'Prefactor')]
            self.dnde[i] = prefactor.getValue()*prefactor.getScale()
            self.dnde_err[i] = prefactor.error()*prefactor.getScale()
            if verbosity:
                print lower,upper,self.dnde[i],self.dnde_err[i],self.ts[i] ,self.ul[i]

        # revert to old source model
        like.setEnergyRange(self.bin_edges[0],self.bin_edges[-1])
        like.setSpectrum(name,old_spectrum)
        saved_state.restore()

    def __str__(self,terse=True,precision=1):
        """ Pack up the values into a nicely formatted string.
            If terse, only include energy, flux, flux_err where flux is
            replaced by the upper limit if there is only 3 sigma source
            detection for a given energy. """

        # convert list to scientific notation
        conv_science = lambda vals: ['%.*e' % (precision,i) \
                                 if isinstance(i,str) else i \
                                 for i in vals]
        conv_float   = lambda vals: ['%.*f' % (precision,i) for i in vals]

        sed_vals = []
        sed_vals.append(['Energy', '[MeV]'] + conv_float(self.e_vals))

        # contains flux + UL if TS < 9
        sed_vals.append(['Flux', '[ph/MeV/cm^2/s]'] + \
                        conv_science([f if ts>=9 else '>'+'%.*e' % (precision,ul) \
                                  for f,ul,ts in zip(self.dnde,self.ul,self.ts)]))

        # contains flux error if TS > 9
        sed_vals.append(['Flux_Err', '[ph/MeV/cm^2/s]'] + \
                        conv_science([ferr if ts>9 else '' \
                                  for ferr,ts in zip(self.dnde_err,self.ts)]))

        if not terse:
            # add into the list everything else somebody might want.
            sed_vals.append(['Lower_Energy', '[MeV]'] + conv_float(self.bin_edges[:-1]))
            sed_vals.append(['Upper_Energy', '[MeV]'] + conv_float(self.bin_edges[1:]))
            sed_vals.append(['Raw_Flux', ''] + conv_science(self.dnde))
            sed_vals.append(['Raw_Flux_Err', ''] + conv_science(self.dnde_err))
            sed_vals.append(['Test_Statistic', ''] + conv_float(self.ts))
            # only include when upper limit was calculated
            sed_vals.append(['Upper_Limit', ''] + \
                            conv_science([u if u >= 0 else '' for u in self.ul]))

        sed_transpose = zip(*sed_vals)

        return '\n'.join([
            ''.join(['%15s' % j for j in i]) for i in sed_transpose
        ])

    def save(self,file,precision=5,terse=False,**kwargs):
        output=self.__str__(precision=precision,**kwargs)
        if hasattr(file,'write'):
            file.write()
        else:
            f=open(file,'w')
            f.write(output)
            f.close()

    def plot(self,filename):
        import pylab as P

        P.set_xscale('log')
        P.xlabel('MeV')
        P.set_yscale('log')
        P.ylabel('MeV')
        P.ylabel(r'$\mathsf{Energy\ Flux\ (MeV\ cm^{-2}\ s^{-1})}$')

        P.plot(self.e_vals,self.e_vals**2*self.dnde)

        source = like.logLike.getSource(self.name)
        spectrum=source.spectrum()
        elist = np.logspace(self.like.energies[0],self.like.energies[-1])
        flist = spectrum(elist)
        P.plot(elist,elist**2*flist)

        # figure out how to plot the source fit also.

        P.savefig(filename)
