from BinnedAnalysis import BinnedObs,BinnedAnalysis
import os

def setup_gtlike(name,roi):

    binsz=0.125
    bigger_roi=False
    proj="ZEA"
    model_file='mmap.fits'
    map_file='cmap.fits'
    enumbins=None
    output_srcmdl_file=None

    print 'Running a gtlike followup'

    emin,emax=roi.bin_edges[0],roi.bin_edges[-1]
    enumbins=len(roi.bin_edges)-1

    # Note that this formulation makes the gtlike slightly smaller than
    # the pointlike ROI (so the gtlike ROI is inside the pointlike ROI)
    roi_radius=N.degrees(max(_.radius_in_rad for _ in roi.bands))

    npix=math.ceil(2.0*roi_radius/binsz)

    cmap_file='ccube.fits'
    srcmap_file='srcmap.fits'
    bexpmap_file='bexpmap.fits'
    input_srcmdl_file='srcmdl.xml'
    optimizer="MINUIT"

    pd=roi.sa.pixeldata

    # for now, only one ft1/ft2 file.
    if len(pd.ft2files) > 1:
        raise Exception("Only 1 ft2 file at a time, for now")


    scfile=pd.ft2files[0]
    expcube_file=pd.ltcube 

    irfs=roi.sa.irf

    x,y,coordsys_str=roi.roi_dir.l(),roi.roi_dir.b(),'GAL'

    
    os.mkdir('files_science_tools')
    os.chdir(tempdir)

    roi.toXML(input_srcmdl_file,convert_extended=True,expand_env_vars=True)

    if isinstance(pd.ft1files,str):
        evfile=pd.ft1files
    elif len(pd.ft1files) == 1:
        evfile=pd.ft1files[0]
    else:
        temp=NamedTemporaryFile(dir='.',delete=False)
        temp.write('\n'.join(pd.ft1files))
        temp.close()
        evfile='@%s' % temp.name

    print 'Running gtbin (ccube)'
    gtbin=GtApp('gtbin','evtbin')
    gtbin.run(algorithm='ccube',
              nxpix=npix, nypix=npix, binsz=binsz,
              evfile=evfile,
              outfile=cmap_file,
              scfile=scfile,
              xref=x, yref=y, axisrot=0, proj=proj,
              ebinalg='LOG', emin=emin, emax=emax, enumbins=enumbins,
              coordsys=coordsys_str)

    print 'Running gtexpcube'
    gtexpcube=GtApp('gtexpcube2')
    gtexpcube.run(infile=expcube_file,
                  cmap=cmap_file,
                  outfile=bexpmap_file,
                  irfs=irfs)

    print 'Running gtsrcmaps'
    gtsrcmaps=GtApp('gtsrcmaps','Likelihood')
    gtsrcmaps.run(scfile=scfile,
                  expcube=expcube_file,
                  cmap=cmap_file,
                  srcmdl=input_srcmdl_file,
                  bexpmap=bexpmap_file,
                  outfile=srcmap_file,
                  irfs=irfs)

    print 'Running pyLikelihood'
    obs=BinnedObs(srcmap_file,expcube_file,bexpmap_file,irfs)

    like=BinnedAnalysis(obs,input_srcmdl_file,optimizer)

    return like
