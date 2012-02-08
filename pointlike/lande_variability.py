""" Code to compute the variability of a source
    using pointlike. 

    Author: Joshua Lande <joshualande@gmail.com>
"""
# N.B. Have to import gtlike stuff first
from roi_gtlike import Gtlike
from LikelihoodState import LikelihoodState
from SED import SED

from tempfile import mkdtemp
from os.path import join, exists
import os
import shutil
 
import pylab as P
import pyfits
import numpy as np

from GtApp import GtApp

from uw.utilities import keyword_options

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.utilities.phasetools import phase_ltcube

from roi_gtlike import Gtlike

from lande_toolbag import tolist
from likelihood_tools import paranoid_gtlike_fit,fluxdict,gtlike_upper_limit,\
        pointlike_upper_limit,diffusedict,fit_only_prefactor,get_background,get_sources,gtlike_modify


class VariabilityTester(object):
    """ Code to compute varability for for a pointlike ROI
    using the method described in 2FGL:

        arXiv:1108.1435v1

    A nice description of this method is:

        https://confluence.slac.stanford.edu/display/SCIGRPS/How+to+-+Variability+test
    """

    defaults = (
        ('f',                    0.02, """ percent systematic correction factor. 
                                           Set to 0.02 for 2FGL. See Section 3.6
                                           of 2FGL paper http://arxiv.org/pdf/1108.1435v1. """),
        ("savedir",              None, """ Directory to put output files into. 
                                           Default is to use a temporary file and 
                                           delete it when done."""),
        ("nbins",                None, """ Number of time bins. """),
        ("always_upper_limit",  False, """ Always compute an upper limit. """),
        ("min_ts",                  4, """ minimum ts in which to quote a SED points instead of an upper limit."""),
        ("ul_confidence",        0.95, """ confidence level for upper limit."""),
        ("gtlike_kwargs",          {}, """ Kwargs to specify creating of gtlike object. """),
        ("do_gtlike",            True, """ Run gtlike varaibility test. """),
        ("refit_background",     True, """ Fit the background sources in each energy bin."""),
        ("refit_other_sources", False, """ Fit other sources in each energy bin. """),
        ("filename",             None, """ Filename to save data to. """),
    )

    @keyword_options.decorate(defaults)
    def __init__(self, roi, which, **kwargs):
        self.roi = roi
        keyword_options.process(self, kwargs)

        self.pointlike_fit_kwargs = dict(use_gradient=False)

        self.which = roi.get_source(which).name

        self._setup_savedir()

        self._setup_time_bins()

        saved_state = PointlikeState(roi)

        self._test_variability()

        saved_state.restore()


    def _setup_savedir(self):
        if self.savedir is not None:
            self.save_data = True
            if not exists(self.savedir):
                os.makedirs(self.savedir)
        else:
            self.save_data = False
            self.savedir = mkdtemp()


    def _setup_time_bins(self):
        roi = self.roi

        # Divide into several time bins
        ft1files=roi.sa.pixeldata.ft1files
        self.earliest_time, self.latest_time = VariabilityTester.get_time_range(ft1files)

        # round to nearest second, for simplicity
        self.time_bins = np.round(np.linspace(self.earliest_time, self.latest_time, self.nbins+1)).astype(int)
        self.tstarts = self.time_bins[:-1]
        self.tstops = self.time_bins[1:]


    def all_time_fit(self):
        print 'First, computing best all-time parameters'

        roi = self.roi
        which = self.which

        # first, spectral fit in gtlike

        roi.fit(**self.pointlike_fit_kwargs)

        F0p = fluxdict(roi, which, error=False)
        diffp = diffusedict(roi)

        all_time = dict(
            pointlike = dict(
                flux = F0p,
                diffuse = diffp,
            )
        )

        if self.do_gtlike:

            savedir = join(self.savedir,'all_time') if self.save_data else None

            gtlike=Gtlike(roi, 
                          savedir=savedir,
                          **self.gtlike_kwargs)
            like=gtlike.like

            like.fit(covar=True)

            self.best_gtlike_state = LikelihoodState(like)

            F0g =  fluxdict(like,which)
            diffg = diffusedict(like)

            all_time['gtlike'] = dict(
                flux = F0g,
                diffuse = diffg,
            )

        return all_time


    def each_time_fit_pointlike(self, smaller_roi, tstart, tstop):

        results = dict()

        print 'Performing Pointlike analysis from %s to %s' % (tstart, tstop)
        which=self.which

        smaller_roi.print_summary()
        ll = lambda: -smaller_roi.logLikelihood(smaller_roi.parameters())

        if not self.refit_background:
            for source in get_background(smaller_roi):
                    roi.modify(which=source,free=False)

        if not self.refit_other_sources:
            for source in get_sources(smaller_roi):
                smaller_roi.modify(which=source,free=False)

        # Freeze source of interest
        smaller_roi.modify(which=which, free=False)

        smaller_roi.fit(**self.pointlike_fit_kwargs)

        results['ll_0'] = ll()

        # Fit prefactor of source of interest
        fit_only_prefactor(smaller_roi, which)

        # * fit prefactor of source
        smaller_roi.fit(**self.pointlike_fit_kwargs)

        smaller_roi.print_summary()

        # * calcualte likelihood for the fit flux
        results['ll_1'] = ll()
        results['flux'] = fluxdict(smaller_roi,which)
        results['TS'] = TS = smaller_roi.TS(which,quick=True)
        results['diffuse'] = diffusedict(smaller_roi)


        if TS < self.min_ts or self.always_upper_limit:
            results['upper_limit'] = pointlike_upper_limit(smaller_roi, which, cl=0.95)
        else:
            results['upper_limit'] = None

        return results

    def each_time_fit_gtlike(self, smaller_roi, tstart, tstop, subdir):

        print 'Performing gtlike analysis from %s to %s' % (tstart, tstop)

        name=self.which

        results = dict()

        gtlike=Gtlike(smaller_roi, 
                      savedir=subdir,
                      **self.gtlike_kwargs)
        like=gtlike.like

        ll = lambda: like.logLike.value()

        # update gtlike object with best fit gtlike parameters
        state = self.best_gtlike_state
        state.old_like = state.like
        state.like = like
        state.restore()
        state.old_like = state.old_like

        if not self.refit_background:
            for source in get_background(like):
                gtlike_modify(like, source, free=False)

        if not self.refit_other_sources:
            for source in get_sources(like):
                gtlike_modify(like,source, free=False)

        # Freeze source of interest
        gtlike_modify(like, name, free=False)

        paranoid_gtlike_fit(like)

        results['ll_0'] = ll()

        # Fit prefactor of source of interest
        fit_only_prefactor(like, name)
        like.thaw(like.par_index(name, 'Prefactor'))

        paranoid_gtlike_fit(like)

        results['ll_1'] = ll()
        results['flux'] = fluxdict(like,name)

        results['TS'] = TS = like.Ts(name,reoptimize=False)
        results['diffuse'] = diffusedict(like)

        if TS < self.min_ts or self.always_upper_limit:
            results['upper_limit'] = gtlike_upper_limit(like, name, cl=0.95)
        else:
            results['upper_limit'] = None

        return results

    def _test_variability(self):
        roi = self.roi

        # Perform all-time analysis
        self.all_time = self.all_time_fit()

        self.bands = []

        for i,(tstart,tstop) in enumerate(zip(self.tstarts, self.tstops)):

            subdir = join(self.savedir,'time_%s_%s' % (tstart, tstop))
            print 'Subdir = ',subdir
            if not exists(subdir):
                os.makedirs(subdir)

            days = (tstop-tstart)/(60*60*24)
            print  '%s/%s Looping from time %s to %s (%.1f days)' % (i+1, self.nbins, tstart, tstop, days)

            band = dict(
                tstart = tstart, 
                tstop = tstop,
                days = days)

            self.bands.append(band)

            smaller_roi = VariabilityTester.time_cut(roi, tstart, tstop, subdir)

            band['pointlike'] = self.each_time_fit_pointlike(smaller_roi, tstart, tstop)
            if self.do_gtlike:
                band['gtlike'] = self.each_time_fit_gtlike(smaller_roi, tstart, tstop, subdir)

            if not self.save_data:
                print 'Removing subdir',subdir
                shutil.rmtree(subdir)

            if self.filename is not None: self.save(self.filename)

        self.TS_var = dict(
            pointlike = self.compute_TS_var('pointlike')
        )
        if self.do_gtlike:
            self.TS_var['gtlike'] = self.compute_TS_var('gtlike')

        if self.filename is not None: self.save(self.filename)

    def compute_TS_var(self,type):
        a=np.asarray
        ll1 = a([b[type]['ll_1'] for b in self.bands])
        ll0 = a([b[type]['ll_0'] for b in self.bands])

        f = self.f

        F = a([b[type]['flux']['flux'] for b in self.bands])
        F0 = self.all_time[type]['flux']['flux']

        df = F - F0
        TS_var = 2*np.sum(
            df**2/(df**2 + f**2*F0**2)*
            (ll1-ll0)
        )
        return TS_var 

    @staticmethod
    def get_time_range(ft1files):
        """ Get the largest time range (in MET) from an ft1 file
            or a list of ft1 files. """
        if isinstance(ft1files,list):
            tmins,tmaxs = zip(*[VariabilityTester.get_time_range(i) for i in ft1files])
            return min(tmins),max(tmaxs)

        f=pyfits.open(ft1files)
        tmin = min(f[2].data.field('START'))
        tmax = max(f[2].data.field('STOP'))
        return tmin, tmax

    @staticmethod
    def time_cut(roi, tstart, tstop, subdir):
        """ Create a new ROI given a time cut. """

        sa = roi.sa
        ds = sa.dataspec

        get_defaults=lambda obj: [k[0] for k in obj.defaults if not isinstance(k,str)]
        get_kwargs=lambda obj: {k:obj.__dict__[k] for k in get_defaults(obj)}

        ds_kwargs, sa_kwargs, roi_kwargs = map(get_kwargs,[ds,sa,roi])

        point_sources = [i.copy() for i in roi.psm.point_sources]
        diffuse_sources = [i.copy() for i in roi.dsm.diffuse_sources]

        if sa_kwargs['tstart'] !=0 or sa_kwargs['tstop'] !=0:
            raise Exception("sanity check")

        # * cut ft1file on time using gtselect

        ft1files=roi.sa.pixeldata.ft1files
        ft2files=roi.sa.pixeldata.ft2files
        if len(ft2files) > 1: raise Exception("...")
        ft2file=ft2files[0]

        evfile=Gtlike.make_evfile(ft1files,subdir)

        cut_evfile=join(subdir,"cut_ft1_%s_%s.fits" % (tstart, tstop))

        if not exists(cut_evfile):
            if not roi.quiet: print 'Running gtselect'
            gtselect=GtApp('gtselect', 'dataSubselector')
            gtselect.run(infile=evfile,
                         outfile=cut_evfile,
                         ra=0, dec=0, rad=180,
                         tmin=tstart, tmax=tstop,
                         emin=1, emax=1e7,
                         zmax=180)

        else:
            print '... Skiping gtselect for %s to %s' % (tstart,tstop)

        ds_kwargs['ft1files'] = cut_evfile

        # * create new binfile and ltcube
        ds_kwargs['binfile'] = join(subdir,'binned_%s_%s.fits' % (tstart, tstop))

        # save this to see if it has been phased by 
        # the function uw.utilities.phasetools.phase_ltcube
        all_time_ltcube = ds_kwargs['ltcube']

        new_ltcube = join(subdir,'ltcube_%s_%s.fits' % (tstart, tstop))

        if not exists(new_ltcube):
            if not roi.quiet: print 'Running gtltcube for %s to %s' % (tstart,tstop)
            gtltcube=GtApp('gtltcube', 'Likelihood')
            gtltcube.run(evfile=cut_evfile,
                         scfile=ft2file,
                         outfile=new_ltcube,
                         dcostheta=0.025, 
                         binsz=1)
        else:
            print '... Skiping gtltcube for %s to %s' % (tstart,tstop)

        # next, check if ltcube is phased, kind of a kluge
        f = pyfits.open(all_time_ltcube)
        if f['exposure'].header.has_key('PHASE'):
            assert f['exposure'].header['PHASE'] == f['weighted_exposure'].header['PHASE']
            # If so, phase new ltcube
            phase = f['exposure'].header['PHASE']

            phased_ltcube = join(subdir,'phased_ltcube_%s_%s.fits' % (tstart, tstop))
            if not exists(phased_ltcube):
                phase_ltcube(new_ltcube, phased_ltcube, phase)
            else:
                print '... Skiping gtltcube phasing for %s to %s' % (tstart,tstop)

            ds_kwargs['ltcube'] = phased_ltcube
        else:
            ds_kwargs['ltcube'] = new_ltcube

        # * create new ds, sa, and roi
        new_ds = DataSpecification(**ds_kwargs)
        sa = SpectralAnalysis(new_ds, **sa_kwargs)
        return sa.roi(
            point_sources = point_sources,
            diffuse_sources = diffuse_sources,
            **roi_kwargs)

    def todict(self):
        d = dict(
            time_bins = self.time_bins,
            tstarts = self.tstarts,
            tstops = self.tstops,
            bands=self.bands,
            all_time=self.all_time)

        return tolist(d)

    def save(self, filename):
        f=open(filename,'w')
        f.write(self.todict())
        f.close()

    @staticmethod
    def _plot_points(axes, x, xerr, y, yerr, yup, significant, 
                     ul_fraction=0.4, label=None, **kwargs):

        plot_kwargs = dict(linestyle='none')
        plot_kwargs.update(kwargs)

        s = significant
        if sum(s) > 0:
            axes.errorbar(x[s],y[s],
                          xerr=xerr[s], yerr=yerr[s], 
                          capsize=0,
                          label=label,
                          **plot_kwargs)

        ns = not_significant = ~s & ~np.isnan(yup) # possibly, some UL failed

        if sum(ns) > 0:
            axes.errorbar(x[ns], yup[ns], 
                          yerr=[ul_fraction*yup[ns], np.zeros(sum(ns))],
                          lolims=True,
                          **plot_kwargs)

            if sum(s) == 0: 
                plot_kwargs['label'] = label

            axes.errorbar(x[ns], yup[ns], 
                          xerr=xerr[ns],
                          capsize=0,
                          **plot_kwargs)

    @staticmethod
    def _plot(d, min_ts, 
              filename=None, 
              figsize=(7,4), 
              gtlike_color='black',
              pointlike_color='red',
              time_scale = None,
              flux_scale = None,
              **kwargs):
        """ Create a plot from a dictionary. """

        fig = P.figure(None,figsize)
        axes = fig.add_subplot(111)

        # astype(float) converts None to nan
        a=lambda x: np.asarray(x).astype(float)

        starts=a(d['tstops'])
        stops=a(d['tstarts'])
        time=(starts+stops)/2
        time_err=(stops-starts)/2

        if time_scale is None:
            time_scale = 10**np.floor(np.log10(np.average(time)))
        if flux_scale is None:
            fg=np.mean(a(d['gtlike']['flux']['value']))
            flux_scale = 10**np.floor(np.log10(fg))

        for t,color in [
            ['gtlike',gtlike_color],
            ['pointlike',pointlike_color]
        ]:

            results = d[t]

            f0 = results['flux_0']['flux']

            flux = results['flux']

            ts = a(results['TS'])
            significant = ts >= min_ts

            f=a(flux['value'])
            ferr=a(flux['error'])
            fup=a(flux['upper_limit'])

            #from matplotlib.ticker import ScalarFormatter
            #formatter = ScalarFormatter(useMathText=True, useOffset=False)
            #formatter.set_scientific(True)
            #formatter.set_powerlimits((-1,1))
            #axes.xaxis.set_major_formatter(formatter)
            #axes.yaxis.set_major_formatter(formatter)

            VariabilityTester._plot_points(
                axes,
                x=time/time_scale,
                xerr=time_err/time_scale,
                y=f/flux_scale,
                yerr=ferr/flux_scale,
                yup=fup/flux_scale, 
                significant=significant,
                color=color,
                label=t,
                **kwargs)
            
            axes.axhline(f0/flux_scale, color=color, dashes=[5,2])

        t = np.log10(time_scale)
        assert t == int(t)

        f = np.log10(flux_scale)
        assert f == int(f)

        axes.set_xlabel('MET (10$^{%d}$ s)' % t)
        axes.set_ylabel('Flux (10$^{%d}$ ph$\,$cm$^{-2}$s$^{-1}$)' % f)

        # Kluge legend due to buggy legend impolementaiton
        # for errorbar in matplotlib
        from matplotlib.lines import Line2D
        l=lambda c:Line2D([0],[0],linestyle='-', color=c)
        axes.legend(
            (l(gtlike_color), l(pointlike_color)),
            ('gtlike','pointlike')
            )

        if filename is not None: P.savefig(filename)
        return axes

    def plot(self, *args, **kwargs):
        return self._plot(self.todict(), self.min_ts, *args, **kwargs)

    def __del__(self):
        if not self.save_data:
            if not self.roi.quiet: print 'Removing savedir',self.savedir
            shutil.rmtree(self.savedir)
