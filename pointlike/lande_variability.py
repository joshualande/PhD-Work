""" Code to compute the variability of a source
    using pointlike. 
"""
from pointspec import DataSpecification, SpectralAnalysis


class VariabilityTester(object)

    defaults = (
        ('f', 0.02, """percent systematic correction factor. 
                       Set to 0.02 for 2FGL. See Section 3.6
                       of 2FGL paper http://arxiv.org/pdf/1108.1435v1. """
         'tempdir', None, 'Directory to put temporary files into.'
        )


    def __init__(self, which, nbins, tempdir):

        self.roi = roi

        saved_state = PointlikeState(roi)

        time_ranges='XXX'

        for tstart,tstop in time_ranges:

            smaller_roi = self.time_cut(roi, tstart, tstop)

            # * freeze everything but normalization of source

            # * calculate likelihood for flux constant

            # * fit prefactor of source

            # * calcualte likelihood for fit flux

            # * save out TS and prefactor values
            
            # save out original/fit prefactor and flux


        # * compute TSvar

        saved_state.restore()

    def time_cut(tstart, tstop):
        roi = self.roi

        sa = roi.sa
        ds = sa.data_specification

        get_defaults=lambda obj: return [k[0] for k in obj.defaults if not isinstance(k,str)]
        get_kwargs=lambda obj: return {k:obj.__dict__[k] for k in get_defaults(obj)}

        ds_kwargs, sa_kwargs, roi_kwargs = map(get_kwargs,[ds,sa,roi])

        if 'tstart' in sa_kwargs or 'tstop' in sa_kwargs:
            raise Exception("sanity check")


        # * run gtselect
        ft1 = ds_kwargs['ft1files']

        # * create new binfile

        ds_kwargs['binfile'] = 'binned_%s_%s.fits' % (tstart, tstop)

        # * create new ds object

        # * create new ds object

        # * create new ROI object


    def todict():
        pass

