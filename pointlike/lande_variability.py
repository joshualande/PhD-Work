""" Code to compute the variability of a source
    using pointlike. 
"""
from tempfile import mkdtemp
from os.path import join, exists
import os
import shutil
 
import pyfits
import numpy as np

from GtApp import GtApp

from uw.utilities import keyword_options

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.utilities.phasetools import phase_ltcube

from roi_gtlike import Gtlike

from lande_toolbag import tolist


class VariabilityTester(object):

    defaults = (
        ('f', 0.02, """ percent systematic correction factor. 
                        Set to 0.02 for 2FGL. See Section 3.6
                        of 2FGL paper http://arxiv.org/pdf/1108.1435v1. """),
        ("savedir", None, """ Directory to put output files into. 
                              Default is to use a temporary file and 
                              delete it when done."""),
        ("nbins", None, """ Number of time bins. """),
    )

    @keyword_options.decorate(defaults)
    def __init__(self, roi, which, **kwargs):
        keyword_options.process(self, kwargs)

        self.roi = roi
        saved_state = PointlikeState(roi)

        if self.savedir is not None:
            self.tempdir=self.savedir
            if not exists(self.tempdir):
                os.makedirs(self.savedir)
        else:
            self.tempdir=mkdtemp()

        ft1files=roi.sa.pixeldata.ft1files

        self.earliest_time, self.latest_time = VariabilityTester.get_time_range(ft1files)

        # round to nearest second, for simplicity
        self.time_bins = np.round(np.linspace(self.earliest_time, self.latest_time, self.nbins+1)).astype(int)
        self.tstarts = self.time_bins[:-1]
        self.tstops = self.time_bins[1:]

        empty = lambda: np.empty_like(self.tstarts).astype(float)

        def ll(roi):
            return -roi.logLikelihood(roi.parameters())

        def F(roi):
            emin, emax = roi.bin_edges[0], roi.bin_edges[-1]
            return roi.get_model(which).i_flux(emin, emax)

        self.ll_0 = ll_0 = ll(roi)
        self.F_0 = F_0 = F(roi)

        self.ll_1 = ll_1 = empty()
        self.F_1 = F_1 = empty()


        for i,(tstart,tstop) in enumerate(zip(self.tstarts, self.tstops)):
            
            days = (tstop-tstart)/(60*60*24)
            print  '%s/%s Looping from time %s to %s (%.1f days)' % (i+1, self.nbins, tstart, tstop, days)

            smaller_roi = VariabilityTester.time_cut(roi, self.tempdir, tstart, tstop)
            self.smaller_roi = smaller_roi

            # * freeze everything but normalization of source

            for source in list(smaller_roi.psm.point_sources) + list(smaller_roi.dsm.diffuse_sources):
                smaller_roi.modify(which=source,free=False)

            free=np.zeros_like(smaller_roi.get_model(which).free).astype(bool)
            free[0]=True
            smaller_roi.modify(which=which, free=free)

            # * fit prefactor of source

            smaller_roi.fit(use_gradient=False)
            smaller_roi.print_summary()

            # * calcualte likelihood for fit flux

            self.ll_1[i], self.F_1[i] = ll(smaller_roi), F(smaller_roi)


        # * compute TS_var

        self.delta_flux = df = F_1 - F_0

        f = self.f

        self.TS_var = 2*np.sum(
            df**2/(df**2 + f**2*F_0**2) *
            (ll_1-ll_0)
        )

        saved_state.restore()

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


        # * cut ft1file on time using gtmktime

        ft1files=roi.sa.pixeldata.ft1files
        ft2files=roi.sa.pixeldata.ft2files
        if len(ft2files) > 1: raise Exception("...")
        ft2file=ft2files[0]

        evfile=Gtlike.make_evfile(ft1files,tempdir)

        cut_evfile=join(tempdir,"cut_ft1_%s_%s.fits" % (tstart, tstop))

        if not exists(cut_evfile):
            if not roi.quiet: print 'Running gtmktime'
            gtmktime=GtApp('gtmktime', 'dataSubselector')
            gtmktime.run(scfile=ft2file,
                         evfile=evfile,
                         outfile=cut_evfile,
                         roicut='no',
                         filter="(START>=%s)&&(STOP<=%s)" % (tstart,tstop))
        else:
            print 'Skiping gtmktime for %s to %s' % (tstart,tstop)

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
            print 'Skiping gtltcube for %s to %s' % (tstart,tstop)

        # next, check if ltcube is phased
        f = pyfits.open(all_time_ltcube)
        if f['exposure'].header.has_key('PHASE'):
            assert f['exposure'].header['PHASE'] == f['weighted_exposure'].header['PHASE']
            phase = f['exposure'].header['PHASE']

            phased_ltcube = join(tempdir,'phased_ltcube_%s_%s.fits' % (tstart, tstop))
            if not exists(phased_ltcube):
                phase_ltcube(new_ltcube, phased_ltcube, phase)
            else:
                print 'Skiping gtltcube phasing for %s to %s' % (tstart,tstop)

            ds_kwargs['ltcube'] = phased_ltcube
        else:
            ds_kwargs['ltcube'] = new_ltcube

        # * create new ds object

        new_ds = DataSpecification(**ds_kwargs)

        # * create new ds object

        sa = SpectralAnalysis(new_ds, **sa_kwargs)

        # * create new ROI object

        smaller_roi = sa.roi(
            point_sources = point_sources,
            diffuse_sources = diffuse_sources,
            **roi_kwargs)
        
        return smaller_roi

    def todict(self):
        return tolist(
            dict(
                pointlike=dict(
                    ll_0 = self.ll_0,
                    ll_1 = self.ll_1,
                    F_0 = self.F_0,
                    F_1 = self.F_1,
                    TS_var = self.TS_var
                )
            )
        )

    def __del__(self):
        if self.savedir is None:
            if not self.roi.quiet: print 'Removing tempdir',self.tempdir
            shutil.rmtree(self.tempdir)
