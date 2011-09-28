# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike


from setup_snr import setup_roi, get_snr
from uw.like.roi_plotting import ROISmoothedSource

from toolbag import tolist,sourcedict,powerlaw_upper_limit

from uw.like.Models import PowerLaw
import numpy as np
import pylab as P
import pyfits

from argparse import ArgumentParser
import yaml
import os

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

snr = get_snr(name, snrdata)
snrsize = snr.spatial_model['sigma']


# *) modify the ROI to remove overlaping background sources. 
deleted_sources = []
for source in roi.get_sources():
    if np.degrees(source.skydir.difference(snr.skydir)) < snrsize + 0.1:
        deleted_sources.append(roi.del_source(source))

for source in roi.get_sources():
    # Freeze the spectrum (but not flux) of all other sources in the ROI.
    if np.any(source.model.free):
        free=np.asarray([True]+[False]*(len(source.model._p)-1))
        roi.modify(which=source,free=free)

roi.print_summary()

def plot_extra_stuff(axes,header):
    """ Overlay pruned 2FGL sources + the SNR extension. 
    
        TODO: overlay multiwavelenth contours. """
    for source in deleted_sources:
        axes['gal'].plot([source.skydir.l()],[source.skydir.b()], marker='*', color='blue', 
                         markeredgecolor='white', markersize=12)
    ROISmoothedSource.overlay_extension(snr, axes, header, extension_color='red',
                                       extension_zorder=10)

    temp=yaml.load(open(snrdata))[name]
    if temp.has_key('contour'):
        contour = temp['contour']
        p = pyfits.open(os.path.expandvars(contour['file']))
        hdu = p[contour['hdu']]
        levels = eval(contour['levels'])
        axes[hdu.header].contour(hdu.data, levels, colors='lightblue')

# *) make a smoothed counts map + tsmap

plot_size = max(snrsize*4, 3)

for kernel_rad in [0.1,0.25]:
    smooth=roi.plot_sources(size = plot_size, 
                            kernel_rad=kernel_rad, label_psf=False,
                            colorbar_radius = max(snrsize, 1),
                            title='Smoothed Counts %s' % name)
    plot_extra_stuff(smooth.axes, smooth.header)
    P.savefig('sources_kernel_%g_%s.png' % (kernel_rad,name))

tsmap=roi.plot_tsmap(size = plot_size, 
                     pixelsize = 1./8,
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

results['prelocalize_pointlike']=sourcedict(roi,name,emin=1e4,emax=1e5)
roi.save('roi_prelocalize.dat')

# *) Perform spatial analysis (?)
#    if TS > 20 (or something):
#      do some extension fitting and stuff

results['postlocalize_pointlike']=sourcedict(roi,name,emin=1e4,emax=1e5)
roi.save('roi_postlocalize.dat')

roi.print_summary()
print roi

print results

# *) Convert to Gtlike object

gtlike=Gtlike(roi,binsz=1./8)
like=gtlike.like

# *) perform spectral fit with gtlike + get out the best fit values

like.fit(covar=True)
results['postlocalize_gtlike']=sourcedict(like,name,emin=1e4,emax=1e5)

# *) Perform upper limits assuming spectral index 2

# N.B., for the E>10GeV analysis we are very much in the Poisson instead
# of Gaussian regime. The likelihood function will be VERY linear. As a result,
# delta_log_like_limits = 50 should be much more reasonable (not quite sure
# how to quantify this right now...)
results['upper_limit_gtlike'] = powerlaw_upper_limit(like,name, delta_log_like_limits=50, verbosity=2)

f=open('results_%s.yaml' % name,'w')
yaml.dump(tolist(results),f)
