from os.path import expandvars, join

import pyfits

import yaml
import numpy as np

from skymaps import SkyDir

from uw.pulsar.phase_range import PhaseRange

from lande.utilities.table import get_confluence
from lande.utilities.tools import OrderedDefaultDict

from lande.fermi.pipeline.pwncat2.table import get_pwnlist,get_results,write_latex, write_confluence, BestHypothesis, savedir



psr_name=[]
phase_min_list=[]
phase_max_list=[]

second_phase_min_list=[]
second_phase_max_list=[]

ra_list=[]
dec_list=[]

glon_list=[]
glat_list=[]

poserr_list = []

ts_point_list=[]
ts_ext_list=[]
ts_cutoff_list =[]

flux_list =[]
unc_flux_list =[]

prefactor_list=[]
scale_list=[]

pulsed_ul_list =[]

index_list =[]
unc_index_list =[]

cutoff_list     =[]
unc_cutoff_list =[]

ts1_list=[]
flux1_list=[]
index1_list=[]

ts2_list=[]
flux2_list=[]
index2_list=[]

ts3_list=[]
flux3_list=[]
index3_list=[]


data = yaml.load(open(expandvars('$pwncode/data/pwncat2_phase_lande.yaml')))

pwnlist=get_pwnlist()
for pwn in pwnlist:
    print pwn

    phase=PhaseRange(data[pwn]['phase'])


    results = get_results(pwn)

    if results is None:
        continue

    point_gtlike = results['point']['gtlike']
    point_pointlike = results['point']['pointlike']

    extended_pointlike = results['extended']['pointlike']
    extended_gtlike = results['extended']['gtlike']
    
    b = BestHypothesis(results)
    gtlike = b.gtlike
    pointlike = b.pointlike
    type = b.type
    cutoff = b.cutoff

    ts_point = b.ts_point
    ts_cutoff = b.ts_cutoff

    psr_name.append(pwn)

    if phase.is_continuous():
        min,max=phase.tolist(dense=True)

        phase_min_list.append(min)
        phase_max_list.append(max)

        second_phase_min_list.append(None)
        second_phase_max_list.append(None)

    else:
        first,second=phase.split_ranges()
        min,max=first.tolist(dense=True)
        phase_min_list.append(min)
        phase_max_list.append(max)

        min,max=second.tolist(dense=True)
        second_phase_min_list.append(min)
        second_phase_max_list.append(max)

    ra_list.append(b.pointlike['position']['equ'][0])
    dec_list.append(b.pointlike['position']['equ'][1])

    glon_list.append(b.pointlike['position']['gal'][0])
    glat_list.append(b.pointlike['position']['gal'][1])

    if b.type == 'upper_limit':
        poserr_list.append(None)
    else:
        ellipse=b.pointlike['spatial_model']['ellipse']
        if ellipse.has_key('lsigma'):
            poserr_list.append(ellipse['lsigma'])
        else:
            print 'ERROR: ELLIPSE FAILED for %s' % pwn
            poserr_list.append(None)

    ts_point_list.append(ts_point)

    if b.type == 'upper_limit':
        ts_ext_list.append(None)
    else:
        ts_ext_list.append(b.ts_ext)

    if b.type == 'upper_limit':
        ts_cutoff_list.append(None)
    else:
        ts_cutoff_list.append(ts_cutoff)


    flux_list.append(None)
    unc_flux_list.append(None)

    prefactor_list.append(None)
    scale_list.append(None)

    index_list.append(None)
    unc_index_list.append(None)

    cutoff_list.append(None)
    unc_cutoff_list.append(None)

    pulsed_ul_list.append(None)

    # band limits

    ts1_list.append(None)
    flux1_list.append(None)
    index1_list.append(None)

    ts2_list.append(None)
    flux2_list.append(None)
    index2_list.append(None)

    ts3_list.append(None)
    flux3_list.append(None)
    index3_list.append(None)


columns = [
    pyfits.Column(name='PSR', format='A', unit=None, array=psr_name),

    pyfits.Column(name='Phase_Min', format='E', unit=None, array=phase_min_list),
    pyfits.Column(name='Phase_Max', format='E', unit=None, array=phase_max_list),
    pyfits.Column(name='Second_Phase_Min', format='E', unit=None, array=second_phase_min_list),
    pyfits.Column(name='Second_Phase_Max', format='E', unit=None, array=second_phase_max_list),

    pyfits.Column(name='RAJ2000', format='E', unit='deg', array=ra_list),
    pyfits.Column(name='DECJ2000', format='E', unit='deg', array=dec_list),

    pyfits.Column(name='GLON', format='E', unit='deg', array=glon_list),
    pyfits.Column(name='GLAT', format='E', unit='deg', array=glat_list),

    pyfits.Column(name='POSITION_ERROR', format='E', unit='deg', array=poserr_list),

    # TS Values
    pyfits.Column('TS_point', format='E', unit=None, array=ts_point_list),
    pyfits.Column('TS_ext', format='E', array=ts_ext_list),
    pyfits.Column('TS_cutoff', format='E', array=ts_cutoff_list),

    # Broadband spectral analysis
    pyfits.Column('Flux_100_316228', format='E', unit='ph/cm**2/s', array=flux_list),
    pyfits.Column('Unc_Flux_100_316228', format='E', unit='ph/cm**2/s', array=unc_flux_list),

    pyfits.Column('Prefator', format='E', unit='ph/cm**2/s/MeV', array=prefactor_list),
    pyfits.Column('Energy_Scale', format='E', unit='MeV', array=scale_list),

    # Pulsed upper limit
    pyfits.Column('PULSED_UL_100_316228', format='E', unit='ph/cm**2/s', array=pulsed_ul_list),

    # TODO: put in prefactor, and E0

    pyfits.Column('Spectral_Index', format='E', array=index_list),
    pyfits.Column('Unc_Spectral_Index', format='E', array=unc_index_list),

    pyfits.Column('E_cutoff', format='E', unit='MeV', array=cutoff_list),
    pyfits.Column('Unc_E_cutoff', format='E', unit='MeV', array=unc_cutoff_list),


    # Bin by bin fitting
    pyfits.Column('TS_100_1000', format='E', array=ts1_list),
    pyfits.Column('Flux_100_1000', format='E', unit='ph/cm**2/s', array=flux1_list),
    pyfits.Column('Index_100_1000', format='E', array=index1_list),

    pyfits.Column('TS_1000_10000', format='E', array=ts2_list),
    pyfits.Column('Flux_1000_10000', format='E', unit='ph/cm**2/s', array=flux2_list),
    pyfits.Column('Index_1000_10000', format='E', array=index2_list),

    pyfits.Column('TS_10000_316228', format='E', array=ts3_list),
    pyfits.Column('Flux_10000_316228', format='E', unit='ph/cm**2/s', array=flux3_list),
    pyfits.Column('Index_10000_316228', format='E', array=index3_list),
]



cols=pyfits.ColDefs(columns)
hdu=pyfits.PrimaryHDU()
tbhdu=pyfits.new_table(cols)
tbhdu.name = '2PC_OFF_PEAK_ANALYSIS'
thdulist = pyfits.HDUList([hdu, tbhdu])

filename=join(savedir,"off_peak_table.fits")
thdulist.writeto(filename, clobber=True)
