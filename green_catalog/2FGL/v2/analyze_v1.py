# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike

import IntegralUpperLimit
from LikelihoodState import LikelihoodState

from setup_snr import setup_roi, get_snr
from uw.like.roi_plotting import ROISmoothedSource

from argparse import ArgumentParser
import pylab as P
import yaml
from toolbag import tolist,sourcedict



parser = ArgumentParser()
parser.add_argument("--snrdata", required=True)
parser.add_argument("--name", required=True)
args=parser.parse_args()

name=args.name
snrdata=args.snrdata

results=dict(name=name)

# *) Build the ROI
roi=setup_roi(name,snrdata)

# get the SNR as an extended source object.

snr=get_snr(name, snrdata)
snrsize = snr.spatial_model['sigma']


# *) modify the ROI to remove overlaping background sources. 
deleted_sources = []
for source in roi.get_sources():
    if source.skydir.difference(snr.skydir) < snrsize + 0.1:
        deleted_sources.append(roi.del_source(source))

roi.print_summary()

def plot_extra_stuff(axes,header):
    # overlay the SNR
    ROISmoothedSource.overlay_extension(snr, axes, header, extension_color='red')
    for source in deleted_sources:
        axes['gal'].plot([source.skydir.l()],[source.skydir.b()], marker='*', color='blue', markeredgecolor='white')


# *) make a smoothed counts map + tsmap

plot_size = max(snrsize*4, 3)
smooth=roi.plot_sources(size = plot_size, 
                        kernel_rad=0.25, label_psf=False,
                        show_extensions=False,
                        title='Smoothed Counts %s' % name)
plot_extra_stuff(smooth.axes, smooth.header)
P.savefig('sources_%s.png' % name)

tsmap=roi.plot_tsmap(size = plot_size, 
                     pixelsize = 1./8,
                     show_extensions=False,
                     title='TS Map %s' % name)
plot_extra_stuff(tsmap.axes, tsmap.header)
P.savefig('tsmap_%s.png' % name)


#    Then add in the SNR as a new source.

roi.add_source(snr)

# *) perform spectral fit + get out the best fit values.

try:
    roi.fit(use_gradient=True)
except Exception, ex:
    print 'ERROR spectral fitting: ', ex

results.update(sourcedict(roi,name,extra='_prelocalize_pointlike',emin=1e4,emax=1e5))


# *) Perform spatial analysis (?)
#    if TS > 20 (or something):
#      do some extension fitting and stuff

results.update(sourcedict(roi,name,extra='_postlocalize_pointlike',emin=1e4,emax=1e5))

roi.print_summary()

# *) Convert to Gtlike object

gtlike=Gtlike(roi,binsz=1./8)
like=gtlike.like

# *) perform spectral fit with gtlike + get out the best fit values

like.fit(covar=True)
results.update(sourcedict(like,name,extra='_postlocalize_gtlike',emin=1e4,emax=1e5))

# *) Perform upper limits assuming spectral idnex 2

def upper_limit(like,name, powerlaw_index=-2):
    """ Wrap up calculating the flux upper limit, for simplicity. """
    saved_state = LikelihoodState(like)

    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(powerlaw_index)
    like.logLike.syncSrcParams(name) # not sure if this is needed

    ul_scipy, results_scipy = IntegralUpperLimit.calc(like, name, ul=0.95, emin=1e4, emax=1e5)

    saved_state.restore()
    return ul_scipy

results['upper_limit_gtlike'] = upper_limit(like,name)

f=open('results_%s.yaml' % name,'w')
yaml.dump(tolist(results),f)
