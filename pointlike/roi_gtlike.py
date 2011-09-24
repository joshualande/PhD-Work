"""
    Usage:

    # roi is a pointlike ROIAnalysis object
    roi=sa.roi_from_xml(...)

    from roi_gtlike import Gtlike

    # like is a pyLikelihood object
    like = Gtlike(roi) 

    # like is a BinnedAnalysis pyLikelihood object
    # the most relevant parameters are 
    like = Gtlike(roi,
                  binsz       = 1/8.,             # spatial bins in gtliek
                  bigger_roi  = False,            # bigger_roi=True => put pointlike circular ROI inside gtlike square ROI
    )
    
"""
import os
from os.path import join
import shutil
import math
import numpy as np
from tempfile import mkdtemp

# pointlike
from uw.like.SpatialModels import Disk
from skymaps import SkyDir
from uw.utilities import keyword_options

# pylikelihood
from GtApp import GtApp
from BinnedAnalysis import BinnedObs,BinnedAnalysis
from pyLikelihood import ParameterVector
from SED import SED


class Gtlike(object):

    defaults = (
            ('binsz',                   1/8., "bin size"),
            ("bigger_roi",             False, "If false, enscribe gtlike ROI in pointlike ROI. If True, enscribe pointlike ROI in gtlike ROI"),
            ("proj",                   "ZEA", "Projection"),
            ("coordsystem",SkyDir.EQUATORIAL, "Coordinate system"),
            ("emin",                    None, "Minimum energy. Default is to get from ROI."),
            ("emax",                    None, "Maximum energy. Default is to get from ROI."),
            ("enumbins",                None, "Number of bins. Defualt is to get from ROI."),
            ("savedir",                 None, "Directory to put output files into. Default is to use a temporary file and delete it when done."),
    )


    @keyword_options.decorate(defaults)
    def __init__(self, roi, **kwargs):
        """ Build a gtlike pyLikelihood object
            which is consistent with a pointlike roi. """
        keyword_options.process(self, kwargs)

        self.roi = roi

        if not roi.quiet: print 'Running a gtlike followup'

        self.old_dir=os.getcwd()
        if self.savedir is not None:
            self.tempdir=self.savedir
            if not os.path.exists(self.tempdir):
                os.makedirs(self.savedir)
        else:
            self.tempdir=mkdtemp()

        # put pfiles into savedir
        os.environ['PFILES']=self.tempdir+';'+os.environ['PFILES'].split(';')[-1]

        if not roi.quiet: print 'Saving files to ',self.tempdir

        if self.emin==None and self.emax==None and self.enumbins==None:
            self.emin,self.emax=roi.bin_edges[0],roi.bin_edges[-1]
            self.enumbins=len(roi.bin_edges)-1
        elif self.emin is not None and \
                self.emax is not None and \
                self.enumbins is not None:
            # all set
            pass
        else:
            raise Exception("emin, emax, and enumbins must all be set.")

        # Note that this formulation makes the gtlike slightly smaller than
        # the pointlike ROI (so the gtlike ROI is inside the pointlike ROI)
        roi_radius=np.degrees(max(_.radius_in_rad for _ in roi.bands))
        if self.bigger_roi:
            npix=int(math.ceil(2.0*roi_radius/self.binsz))
        else:
            npix=int(math.ceil(np.sqrt(2.0)*roi_radius/self.binsz))

        cmap_file=join(self.tempdir,'ccube.fits')
        srcmap_file=join(self.tempdir,'srcmap.fits')
        bexpmap_file=join(self.tempdir,'bexpmap.fits')
        input_srcmdl_file=join(self.tempdir,'srcmdl.xml')
        optimizer="MINUIT"

        pd=roi.sa.pixeldata

        # for now, only one ft1/ft2 file.
        if len(pd.ft2files) > 1:
            raise Exception("Only 1 ft2 file at a time, for now")

        scfile=pd.ft2files[0]
        expcube_file=pd.ltcube 

        irfs=roi.sa.irf
        if pd.conv_type == 0 and 'FRONT' not in irfs: irfs += '::FRONT'
        if pd.conv_type == 1 and 'BACK' not in irfs: irfs += '::BACK'


        if self.coordsystem==SkyDir.GALACTIC:
            x,y,coordsys_str=roi.roi_dir.l(),roi.roi_dir.b(),'GAL'
        else:
            x,y,coordsys_str=roi.roi_dir.ra(),roi.roi_dir.dec(),'CEL'


        # shirnk all disk sources which are smaller than 0.02 degrees.
        # Otherwise, gtlike will crash. Anyway, no reason
        # to have extended source smaller than the binsize.
        shrink_list = [ source for source in roi.get_sources() if \
                       hasattr(source,'spatial_model') and \
                       isinstance(source.spatial_model,Disk) and \
                       source.spatial_model['sigma'] < self.binsz ]
        for src in shrink_list: src.spatial_model.shrink(size=self.binsz)

        roi.toXML(input_srcmdl_file,convert_extended=True,expand_env_vars=True)

        for src in shrink_list: src.spatial_model.unshrink()

        if isinstance(pd.ft1files,str):
            evfile=pd.ft1files
        elif len(pd.ft1files) == 1:
            evfile=pd.ft1files[0]
        else:
            ft1list = join(self.tempdir,'ft1files.lst')
            if not os.path.exists(ft1list):
                temp=open(ft1list,'w')
                temp.write('\n'.join(pd.ft1files))
                temp.close()
            evfile='@'+ft1list

        cut_evfile=join(self.tempdir,"ft1_cut.fits")
        if not os.path.exists(cut_evfile):
            if not roi.quiet: print 'Running gtselect'
            gtselect=GtApp('gtselect','dataSubselector')
            gtselect.run(infile=evfile,
                         outfile=cut_evfile,
                         ra=0, dec=0, rad=180,
                         tmin=0, tmax=0,
                         emin=self.emin, emax=self.emax,
                         zmax=180)
        else:
            if not roi.quiet: print 'Skip... gtselect'

        if not os.path.exists(cmap_file):
            if not roi.quiet: print 'Running gtbin (ccube)'
            gtbin=GtApp('gtbin','evtbin')
            gtbin.run(algorithm='ccube',
                      nxpix=npix, nypix=npix, binsz=self.binsz,
                      evfile=cut_evfile,
                      outfile=cmap_file,
                      scfile=scfile,
                      xref=x, yref=y, axisrot=0, proj=self.proj,
                      ebinalg='LOG', emin=self.emin, emax=self.emax, enumbins=self.enumbins,
                      coordsys=coordsys_str)
        else:
            if not roi.quiet: print 'Skip... gtbin (ccube)'

        if not os.path.exists(bexpmap_file):
            # https://confluence.slac.stanford.edu/display/ST/Science+Tools+Development+Notes?focusedCommentId=99484083#comment-99484083
            # Use the default binning all sky, 1deg/pixel
            if not roi.quiet: print 'Running gtexpcube'
            gtexpcube=GtApp('gtexpcube2')
            gtexpcube.run(infile=expcube_file,
                          cmap='none',
                          ebinalg='LOG', emin=self.emin, emax=self.emax, enumbins=self.enumbins,
                          outfile=bexpmap_file,
                          irfs=irfs)
        else:
            if not roi.quiet: print 'Skip... gtexpcube'

        if not os.path.exists(srcmap_file):
            if not roi.quiet: print 'Running gtsrcmaps'
            gtsrcmaps=GtApp('gtsrcmaps','Likelihood')
            gtsrcmaps.run(scfile=scfile,
                          expcube=expcube_file,
                          cmap=cmap_file,
                          srcmdl=input_srcmdl_file,
                          bexpmap=bexpmap_file,
                          outfile=srcmap_file,
                          irfs=irfs)
        else:
            if not roi.quiet: print 'skip... gtsrcmaps'

        if not roi.quiet: print 'Creating LIKE'
        obs=BinnedObs(srcmap_file,expcube_file,bexpmap_file,irfs)

        self.like = BinnedAnalysis(obs,input_srcmdl_file,optimizer)


        if not roi.quiet: print 'LIKE Created!'

    def fit(self):
        """ perform a gtlike spectral fit. """
        if not self.roi.quiet: print 'Fitting ROI'
        self.like.fit(covar=True)
        if not self.roi.quiet: print 'Done ROI'

    def plot_sed(self,which=None,filename=None, **kwargs):

        if not self.roi.quiet: print 'Plotting SED of %s' % which
        sed=SED(self.like,which,verbosity=not self.roi.quiet,**kwargs)
        if not self.roi.quiet: print sed
        print sed
        sed.plot(filename)

    def __del__(self):
        if self.savedir is None:
            if not self.roi.quiet: print 'Removing tempdir',self.tempdir
            shutil.rmtree(self.tempdir)

    def get_gtlike_info_dict(self,which):
        """ get a bunch of gtlike stuff and
            pack it nicely into a dictionary. """
        like = self.like
        roi  = self.roi

        src_info={}
        src_info['logLikelihood']={'spectral':float(like.logLike.value())}

        try:
            manager,index=roi.mapper(which)
        except:
            try:
                # Two point sources
                roi.mapper('%s (first)' % which)
                roi.mapper('%s (second)' % which)

            except:
                # Source doesn't exist
                return src_info

            results1=self.get_gtlike_info_dict('%s (first)' % which)
            results1 = dict((k+'_first' if k!='logLikelihood' else k,v) for k,v in results1.items())

            results2=self.get_gtlike_info_dict('%s (second)' % which)
            results2 = dict((k+'_second' if k!='logLikelihood' else k,v) for k,v in results2.items())

            results1.update(results2)
            return results1

        source=roi.get_source(which)
        name=source.name
        src_info['TS']={'quick':like.Ts(name,reoptimize=False),
                       'slow':like.Ts(name,reoptimize=True)}

        src_info['other_sources']={}
        for source in roi.get_sources():
            try:
                other_name=str(source.name)
                emin=float(roi.bin_edges[0])
                emax=float(roi.bin_edges[-1])
                src_info['other_sources'][other_name]={}
                src_info['other_sources'][other_name]['TS']=float(like.Ts(other_name,reoptimize=False))
                src_info['other_sources'][other_name]['Flux']=[float(like.flux(other_name,emin=emin,emax=emax)),
                                                               float(like.fluxError(other_name,emin=emin,emax=emax))]
            except:
                pass # sometimes the flux function doesn't work

        if not roi.quiet: print 'gtlike TS =',src_info['TS']

        spectralparameters=ParameterVector()
        like.model[name]['Spectrum'].getParams(spectralparameters)

        for p in spectralparameters:
            src_info[str(p.getName())]=[float(p.getValue()),float(p.error())]

        for flux_name,emin,emax in [['Flux_100',100,100000],['Flux_1000',1000,100000],
                ['Flux',min(roi.bin_edges),max(roi.bin_edges)]]:
                          
            src_info[flux_name]=[float(like.flux(name,emin=emin,emax=emax)),
                              float(like.fluxError(name,emin=emin,emax=emax))]
        return src_info


