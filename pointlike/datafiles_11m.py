""" Here is an example datafiles script It sets up a standard Fermi data
    analysis using 11 months of data. """

datafiles_basedir = "/nfs/slac/g/ki/ki03/lande/allsky/11month_pointlike"

ft2file  = datafiles_basedir + "/ft2_11months.fits"
ltcube   = datafiles_basedir + "/ltcube_11months.fits"
catalog = datafiles_basedir + "/gll_psc_v03.fit"
ft1files = [
    datafiles_basedir + "/ft1_11months.fits"
]

galactic = datafiles_basedir+"/gll_iem_v02.fit"
extragalactic = datafiles_basedir+"/isotropic_iem_v02.txt"

emin,emax,binsperdecade=100,100000,8
binfile = datafiles_basedir+'/binned_100_100000_8.fits'
