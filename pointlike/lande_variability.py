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
from likelihood_tools import paranoid_gtlike_fit,flux_dict,gtlike_upper_limit,pointlike_upper_limit


class VariabilityTester(object):

    defaults = (
        ('f',                   0.02, """ percent systematic correction factor. 
                                  Set to 0.02 for 2FGL. See Section 3.6
                                  of 2FGL paper http://arxiv.org/pdf/1108.1435v1. """),
        ("savedir",             None, """ Directory to put output files into. 
                                  Default is to use a temporary file and 
                                  delete it when done."""),
        ("nbins",               None, """ Number of time bins. """),
        ("always_upper_limit", False, """ Always compute an upper limit. """),
        ("min_ts",                 4, """ minimum ts in which to quote a SED points instead of an upper limit."""),
        ("ul_confidence",       0.95, """ confidence level for upper limit."""),
        ("gtlike_kwargs",         {}, """ Kwargs to specify creating of gtlike object. """),
        ("do_gtlike",           True, """ Run gtlike varaibility test. """),
    )

    @keyword_options.decorate(defaults)
    def __init__(self, roi, which, **kwargs):
        keyword_options.process(self, kwargs)

        self.roi = roi
        self.which = roi.get_source(which).name
        saved_state = PointlikeState(roi)

        if self.savedir is not None:
            self.tempdir=self.savedir
            if not exists(self.tempdir):
                os.makedirs(self.savedir)
        else:
            self.tempdir=mkdtemp()

        # Divide into several time bins
        ft1files=roi.sa.pixeldata.ft1files
        self.earliest_time, self.latest_time = VariabilityTester.get_time_range(ft1files)

        # round to nearest second, for simplicity
        self.time_bins = np.round(np.linspace(self.earliest_time, self.latest_time, self.nbins+1)).astype(int)
        self.tstarts = self.time_bins[:-1]
        self.tstops = self.time_bins[1:]

        self._test_variability()

        saved_state.restore()


    def all_time_fit_gtlike(self, roi):
        print 'First, computing best all-time parameters using gtlike.'
        gtlike=Gtlike(roi, 
                      savedir=join(self.tempdir,'gtlike_all_time') if self.savedir is not None else None,
                      **self.gtlike_kwargs)
        like=gtlike.like

        like.fit(covar=True)

        self.best_gtlike_state = LikelihoodState(like)

        return like


    def each_time_fit_pointlike(self, smaller_roi, tstart, tstop):

        print 'Performing Pointlike analysis from %s to %s' % (tstart, tstop)
        which=self.which

        smaller_roi.print_summary()

        ll = lambda: -smaller_roi.logLikelihood(smaller_roi.parameters())

        results = dict()
        results['ll_0'] = ll()

        # * freeze everything but normalization of source

        for source in list(smaller_roi.psm.point_sources) + list(smaller_roi.dsm.diffuse_sources):
            smaller_roi.modify(which=source,free=False)

        free=np.zeros_like(smaller_roi.get_model(which).free).astype(bool)
        free[0]=True
        smaller_roi.modify(which=which, free=free)

        # * fit prefactor of source
        smaller_roi.fit(use_gradient=False)
        smaller_roi.print_summary()

        # * calcualte likelihood for the fit flux
        results['ll_1'] = ll()
        results['flux'] = flux_dict(smaller_roi,which)
        results['TS'] = TS = smaller_roi.TS(which,quick=True)

        if TS < self.min_ts or self.always_upper_limit:
            results['upper_limit'] = pointlike_upper_limit(smaller_roi, which, cl=0.95)
        else:
            results['upper_limit'] = None

        return results

    def each_time_fit_gtlike(self, smaller_roi, tstart, tstop):

        print 'Performing gtlike analysis from %s to %s' % (tstart, tstop)

        name=self.which

        results = dict()

        gtlike=Gtlike(smaller_roi, 
                      savedir=join(self.tempdir,'gtlike_%s_%s' % (tstart, tstop)) if self.savedir is not None else None,
                      **self.gtlike_kwargs)
        like=gtlike.like

        ll = lambda: like.logLike.value()

        results['ll_0'] = ll()

        # update gtlike object with best fit gtlike parameters
        state = self.best_gtlike_state
        state.old_like = state.like
        state.like = like
        state.restore()
        state.old_like = state.old_like

        # freeze everything but normalization of source

        for i in range(len(like.model.params)):
            like.freeze(i)

        # Free the prefactor of our source
        like.thaw(like.par_index(name, 'Prefactor'))


        # fit prefactor for source
        paranoid_gtlike_fit(like)

        # * calcualte likelihood for the fit flux
        results['ll_1'] = ll()
        results['flux'] = flux_dict(like,name)

        results['TS'] = TS = like.Ts(name,reoptimize=False)

        if TS < self.min_ts or self.always_upper_limit:
            results['upper_limit'] = gtlike_upper_limit(like, name, cl=0.95)
        else:
            results['upper_limit'] = None

        return results

    def _test_variability(self):

        roi = self.roi
        which = self.which

        F0p = flux_dict(roi, which, error=False)
        self.flux_0 = dict(pointlike = F0p, error=False)

        if self.do_gtlike:
            all_time_like = self.all_time_fit_gtlike(roi)
            self.flux_0['gtlike'] = F0g = flux_dict(all_time_like,which)

        empty = lambda: np.empty_like(self.tstarts).astype(float)

        self.bands = []

        for i,(tstart,tstop) in enumerate(zip(self.tstarts, self.tstops)):

            days = (tstop-tstart)/(60*60*24)
            print  '%s/%s Looping from time %s to %s (%.1f days)' % (i+1, self.nbins, tstart, tstop, days)

            band = dict(
                tstart = tstart, 
                tstop = tstop,
                days = days)

            self.bands.append(band)

            smaller_roi = VariabilityTester.time_cut(roi, self.tempdir, tstart, tstop)

            band['pointlike'] = self.each_time_fit_pointlike(smaller_roi, tstart, tstop)
            if self.do_gtlike:
                band['gtlike'] = self.each_time_fit_gtlike(smaller_roi, tstart, tstop)

        self.TS_var = dict(
            pointlike = self.compute_TS_var('pointlike')
        )
        if self.do_gtlike:
            self.TS_var['gtlike'] = self.compute_TS_var('gtlike')

    def compute_TS_var(self,type):
        a=np.asarray
        ll1 = a([b[type]['ll_1'] for b in self.bands])
        ll0 = a([b[type]['ll_0'] for b in self.bands])

        f = self.f

        F = a([b[type]['flux']['flux'] for b in self.bands])
        F0 = self.flux_0[type]['flux']

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
    def time_cut(roi, tempdir, tstart, tstop):
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

        evfile=Gtlike.make_evfile(ft1files,tempdir)

        cut_evfile=join(tempdir,"cut_ft1_%s_%s.fits" % (tstart, tstop))

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
        ds_kwargs['binfile'] = join(tempdir,'binned_%s_%s.fits' % (tstart, tstop))

        # save this to see if it has been phased by 
        # the function uw.utilities.phasetools.phase_ltcube
        all_time_ltcube = ds_kwargs['ltcube']

        new_ltcube = join(tempdir,'ltcube_%s_%s.fits' % (tstart, tstop))

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

            phased_ltcube = join(tempdir,'phased_ltcube_%s_%s.fits' % (tstart, tstop))
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

    def summary_dict(self, type):
        """ Condense information into more useful arrays. """
        bands=self.bands
        d = dict(
            TS=[b[type]['TS'] for b in bands],
            TS_var = self.TS_var[type],
            flux = dict(
                value=[b[type]['flux']['flux'] for b in bands],
                error=[b[type]['flux']['flux_err'] for b in bands],
                upper_limit=[b[type]['upper_limit']['flux']
                             if b[type]['upper_limit'] is not None
                             else None for b in bands]),
            flux_0=self.flux_0[type],
            ll_0=[b[type]['ll_0'] for b in bands],
            ll_1=[b[type]['ll_1'] for b in bands])
        return d

    def todict(self):
        d = dict(
            time_bins = self.time_bins,
            tstarts = self.tstarts,
            tstops = self.tstops)

        d['pointlike'] = self.summary_dict('pointlike')
        if self.do_gtlike:
            d['gtlike'] = self.summary_dict('gtlike')

        return tolist(d)

    @staticmethod
    def _plot(d, filename=None, figsize=(8,4)):
        """ Create a plot from a dictionary. """

        fig = P.figure(None,figsize)
        axes = fig.add_subplot(111)

        a=np.asarray

        starts=a(d['tstops'])
        stops=a(d['tstarts'])
        x=(starts+stops)/2
        xerr=(stops-starts)/2
        y=a(d['gtlike']['flux']['value'])
        yerr=a(d['gtlike']['flux']['error'])
        axes.errorbar(x,y,xerr=xerr,yerr=yerr, linestyle='none')

        axes.set_xlabel('Time (MET)')
        axes.set_ylabel('Flux (ph$\,$cm$^{-2}$s$^{-1}$)')

        if filename is not None: P.savefig(filename)
        return axes

    def plot(self, *args, **kwargs):
        return self._plot(self.todict(), *args, **kwargs)

    def __del__(self):
        if self.savedir is None:
            if not self.roi.quiet: print 'Removing tempdir',self.tempdir
            shutil.rmtree(self.tempdir)
