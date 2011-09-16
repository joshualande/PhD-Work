import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from numpy import *


from skymaps import SkyImage, SkyDir
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from uw.like.sed_plotter import plot_sed
from uw.like.roi_analysis import *
from uw.like.roi_extended import ExtendedSource
from uw.like.roi_plotting import *
from uw.like.pointspec_helpers import FermiCatalog
from uw.like.roi_save import *
from uw.like.roi_catalogs import Catalog2FGL

from roi_gtlike import Gtlike

from uw.like.sed_plotter import plot_sed

from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir

from toolbag import sourcedict,tolist
from numpy import pi
import os,sys

#import mathematic library to have function cos,acos,sin,sqrt...
from math import *

def dist(raref,decref,ra,dec):
    return (180.0/pi)*acos(cos(pi/2.0-decref*pi/180.0)*cos(pi/2.0-dec*pi/180.0)+sin(pi/2.0-decref*pi/180.0)*sin(pi/2.-dec*pi/180.0)*cos((raref-ra)*pi/180.0))

def localize_func(roi,name,nb,gradient=True,update=True,bandfits=True):
    """Function to test the position of the source
    name=name of the source
    nb=nb of times we do the loop localize then fit"""
    roi.fit(method="minuit",use_gradient=True)
    if nb>1:
        for i in range(nb):
            roi.localize(which=name,update=update,bandfits=bandfits)
            roi.fit(method="minuit",use_gradient=True)
    else :
        roi.localize(which=name,update=update,bandfits=bandfits)
        roi.fit(method="minuit",use_gradient=True)
        
    ll=-1.0*roi.logLikelihood(roi.parameters())
    return ll,roi.TS(which=name,quick=False,method="minuit")

def test_location(roi,name,nb,distmax,gradient=True,update=True,bandfits=True):
    """Function to determine if the source is too far from the pulsar to be considered as associated"""

    #save previous position of the source.
    roi.save('roi_temp.dat')
    source=source=roi.get_source(which=name)
    ra=source.skydir.ra()
    dec=source.skydir.dec()

    ll,TS=localize_func(roi,name,nb,gradient=True,update=True,bandfits=bandfits)

    source=source=roi.get_source(which=name)

    source=source=roi.get_source(which=name)
    if dist(ra,dec,source.skydir.ra(),source.skydir.dec())<distmax:
        print "Source consistent with the position of the pulsar : distance =%.2f"%dist(ra,dec,source.skydir.ra(),source.skydir.dec())
    else :
        print "Source unconsistent with the position of the pulsar : distance =%.2f"%dist(ra,dec,source.skydir.ra(),source.skydir.dec())
        roi=load("roi_temp.dat")

    os.system("rm -rf roi_temp.dat")

    return roi

