import glob
import yaml
from uw.pulsar.phase_range import PhaseRange
import os,sys
import asciitable
import re
from os.path import join,exists
from collections import defaultdict

debug=0

def create_sources_list(folder,pwnphase,version="2"):
    """Define a dict to include all the directory and values needed for each sources in a directory"""

    sources={}
    sourcelist=[]
    for name2 in glob.iglob("%s/*"%folder):
        try :
            source={}

            name=name2[len(folder)+1:len(name2)]
            if name.find('PSRJ')!=-1:
                source['name']=name
                phase=yaml.load(open(pwnphase))
                source['phasemin']=phase[name]['phase'][0]
                if debug ==1:
                    print "source['phasemin']"
                source['phasemax']=phase[name]['phase'][1]
                if debug ==1:
                    print "source['phasemax']"
                source['deltaphi']=PhaseRange(phase[name]['phase'][0],phase[name]['phase'][1]).phase_fraction
                if debug ==1:
                    print "source['deltaphi']"
                results=yaml.load(open("%s/%s/results_%s.yaml"%(folder,name,name)))
                if debug ==1:
                    print "results"
                try :
                    source['gtlike_TS']=results['TS_gtlike']
                except :
                    source['gtlike_TS']=results['gtlike']['ts_at_pulsar']
                try :
                    source['pointlike_TS']=results['TS_pointlike']
                except :
                    source['pointlike_TS']=results['pointlike']['ts_at_pulsar']
                if debug ==1:
                    print "try except"
                try :
                    source['gtlike_Prefactor']=results['gtlike']['Prefactor_at_pulsar']
                except :
                    source['gtlike_Prefactor']=results['gtlike']['Integral_at_pulsar']
                try :
                    source['gtlike_Prefactor_Error']=results['gtlike']['Prefactor_err_at_pulsar']
                except :
                    source['gtlike_Prefactor_Error']=results['gtlike']['Integral_err_at_pulsar']
                try :
                    source['pointlike_Prefactor']=results['pointlike']['Norm_at_pulsar']
                except :
                     source['pointlike_Prefactor']=results['pointlike']['Int_Flux_at_pulsar']
                try :
                    source['pointlike_Prefactor_Error']=results['pointlike']['Norm_err_at_pulsar']
                except :
                    source['pointlike_Prefactor_Error']=results['pointlike']['Int_Flux_err_at_pulsar']
                source['pointlike_Index']=results['pointlike']['Index_at_pulsar']
                if debug ==1:
                    print "source['pointlike_Index']=results['pointlike']['Index_at_pulsar']"
                source['pointlike_Index_Error']=results['pointlike']['Index_err_at_pulsar']
                if debug ==1:
                    print "source['pointlike_Index_Error']=results['pointlike']['Index_err_at_pulsar']"
                source['gtlike_Index']=results['gtlike']['Index_at_pulsar']
                if debug ==1:
                    print "source['gtlike_Index']=results['gtlike']['Index_at_pulsar']"
                source['gtlike_Index_Error']=results['gtlike']['Index_err_at_pulsar']
                if debug ==1:
                    print "source['gtlike_Index_Error']=results['gtlike']['Index_err_at_pulsar']"
                source['gtlike_flux']=results['gtlike']['flux_at_pulsar']
                if debug ==1:
                    print "source['gtlike_flux']=results['gtlike']['flux_at_pulsar']"
                source['gtlike_flux_Error']=results['gtlike']['flux_err_at_pulsar']
                if debug ==1:
                    print "source['gtlike_flux_Error']=results['gtlike']['flux_err_at_pulsar']"
                source['pointlike_flux']=results['pointlike']['flux_at_pulsar']
                if debug ==1:
                    print "source['pointlike_flux']=results['pointlike']['flux_at_pulsar']"
                source['pointlike_flux_Error']=results['pointlike']['flux_err_at_pulsar']
                if debug ==1:
                    print "source['pointlike_flux_Error']=results['pointlike']['flux_err_at_pulsar']"
                source['counts_file']="%s/%s/cnts_0.25%s.png"%(folder,name,name)
                if debug ==1:
                    print "source['counts_file']="
                source['input_pointlike_srcmodel']="%s/%s/srcmodel_prefit_%s.xml"%(folder,name,name)
                if debug ==1:
                    print "source['input_pointlike_srcmodel']"
                source['input_pointlike_srcmodel_renormalized']="%s/%s/srcmodel_prefit_renorm_%s.xml"%(folder,name,name)
                if debug ==1:
                    print "source['input_pointlike_srcmodel_renormalized']"
                source['output_pointlike_srcmodel']="%s/%s/srcmodel_output_pointlike_%s.xml"%(folder,name,name)
                if debug ==1:
                    print "source['output_pointlike_srcmodel']"
                source['output_gtlike_srcmodel_phased']="%s/%s/output_model_gtlike_renorm_%s.xml" %(folder,name,name)
                if debug ==1:
                    print "source['output_gtlike_srcmodel_phased']"
                source['output_gtlike_srcmodel']="%s/%s/output_model_gtlike_%s.xml" %(folder,name,name)
                if debug ==1:
                    print "source['output_gtlike_srcmodel']"
                txt="farith %s/%s/counts_file_0.1_%s.fits"%(folder,name,name)
                txt+=" %s/%s/model_file_0.1_%s.fits"%(folder,name,name)
                txt+=" %s/%s/residuals_0.1_%s.fits -"%(folder,name,name)
                try :
                    os.system("rm -rf %s/%s/residuals_0.1_%s.fits"%(folder,name,name))
                except :
                    print " "
                    os.system(txt)
                
                source['residual_counts']="%s/%s/residuals_0.1_%s.fits"%(folder,name,name)
                if debug ==1:
                    print "source['residual_counts']"
                txt="farith %s/%s/counts_file_excess_0.1_%s.fits"%(folder,name,name)
                txt+=" %s/%s/model_file_excess_0.1_%s.fits"%(folder,name,name)
                txt+=" %s/%s/excess_0.1_%s.fits -"%(folder,name,name)
                try :
                    os.system("rm -rf %s/%s/excess_0.1_%s.fits"%(folder,name,name))
                except :
                    print " "
                    os.system(txt)
                source['excess_counts']="%s/%s/excess_0.1_%s.fits"%(folder,name,name)
                if debug ==1:
                    print "source['excess_counts']"
                source['residual_tsmap']="%s/%s/residual_tsmap_0.1_%s.png"%(folder,name,name)
                if debug ==1:
                    print " source['residual_tsmap']"
                source['excess_tsmap']="%s/%s/source_tsmap_0.10%s.png"%(folder,name,name)
                if debug ==1:
                    print "source['excess_tsmap']="
                source['smoothed_cmap']="%s/%s/sources_%s.png"% (folder,name,name)
                if debug ==1:
                    print "source['smoothed_cmap']"
                source['residual_tsmap_fits']="%s/%s/residual_tsmap_0.1_%s.fits"%(folder,name,name)
                if debug ==1:
                    print "source['residual_tsmap_fits']"
                source['excess_tsmap_fits']="%s/%s/source_tsmap_0.10%s.fits"%(folder,name,name)
                if debug ==1:
                    print "source['excess_tsmap_fits']"
                source['spectrum_plot']="%s/%s/Spectra_%s.png"%(folder,name,name)
                if debug ==1:
                    print "source['spectrum_plot']"
                source['Slice']="%s/%s/outslice_%s.png"%(folder,name,name)
                if debug ==1:
                    print "source['Slice']"
                source['SED']="%s/%s/sed_%s.png"%(folder,name,name)
                if debug ==1:
                    print "source['SED']"
                source['region']="%s/%s/%s.reg"%(folder,name,name)
                if debug ==1:
                    print "ource['region']"
                source['allsed']="%s/%s/allsed_%s.png"%(folder,name,name)
                if debug ==1:
                    print source['allsed']
                source['logfile']="%s/%s/log_%s.txt"%(folder,name,name)
                if debug ==1:
                    print "source['logfile']"
                if version =="2":
                    source['gal_gtlike']=results['gal_gtlike']
                    if debug ==1:
                        print "source['gal_gtlike']"
                sources[name]=source
                sourcelist.append(name)
        except :
            print "source non cree"
    return sources,sourcelist



def t2t(lines,name):
    """ create the HTML for a given t2t file. """
    filename = join(website,'%s.t2t' % name)
    
    temp=open(filename,'w')
    temp.write(
        '\n'.join(lines))
    temp.close()
    os.system('python /afs/slac/g/glast/users/rousseau/txt2tags-2.6/txt2tags --target html %s' % filename)    
#    os.system('python /afs/slac/g/glast/users/rousseau/txt2tags-2.6/txt2tags --target html --style color.css --css-sugar %s' % filename)

def format_table(lines,sources,sourcelist,image_folder,pagename,version="2"):
    lines.append('')

    while pagename.find('/')!=-1:
        pagename2=pagename[pagename.find('/')+1:len(pagename)]
        pagename=pagename2
    pagename+=".html"
    table=defaultdict(list)
    if version =="2":
        format = '| [%30s %30s] | %30s | %30s | %30s | %30s | %30s |%30s | %30s | %30s | %30s | %30s |'
    else :
        format = '| [%30s %30s] | %30s | %30s | %30s | %30s | %30s |%30s | %30s | %30s | %30s |'
    
    lines.append('')
#        format % ('Name','Phase Range','TS pointlike','TS gtlike','Prefactor Pointlike','Prefactor gtlike','Gamma pointlike','Gamma gtlike','Flux pointlike','Flux gtlike')
#        )

#    format = '| [%30s %30s] | %30s  | %.2f  | %.2f | %.2e +/- %.2e | %.2e +/- %.2e | %.2e +/- %.2e  | %.2e +/- %.2e | %.2e +/- %.2e | %.2e +/- %.2e |'
    for i in range(len(sourcelist)+1) :
        if i==0:
            if version=="2":
                lines.append(
                   '|'+format % ('Name', pagename, 'Phase Range','TS pointlike','TS gtlike','Prefactor Pointlike','Prefactor gtlike','Gamma pointlike','Gamma gtlike','Flux pointlike','Flux gtlike','Gal_norm_gtlike')
                    )
            else :
                lines.append(
                    '|'+format % ('Name', pagename, 'Phase Range','TS pointlike','TS gtlike','Prefactor Pointlike','Prefactor gtlike','Gamma pointlike','Gamma gtlike','Flux pointlike','Flux gtlike')
                    )
        else :
            name=sourcelist[i-1]
            phaserange=' '
            try:
                for i in range(len(sources[name]['phasemin'])):
                    if i!=0:
                        phaserange+='U'
                    phaserange+='[%.2f,%.2f]'%(sources[name]['phasemin'][i],sources[name]['phasemax'][i])
            except:
                phaserange+='[%.2f,%.2f]'%(sources[name]['phasemin'],sources[name]['phasemax'])
                
            phaserange+="->%.2f"%sources[name]['deltaphi']
            if version=="2":
                lines.append(
                    format % (name, "%s/%s.html"%(image_folder,name),phaserange,"%.2f"%(sources[name]['pointlike_TS']),"%.2f"%(sources[name]['gtlike_TS']),"%.2e +/- %.2e"%(sources[name]['pointlike_Prefactor'],sources[name]['pointlike_Prefactor_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_Prefactor'],sources[name]['gtlike_Prefactor_Error']),"%.2f +/- %.2f"%(sources[name]['pointlike_Index'],sources[name]['pointlike_Index_Error']),"%.2f +/- %.2f"%(sources[name]['gtlike_Index'],sources[name]['gtlike_Index_Error']),"%.2e +/- %.2e"%(sources[name]['pointlike_flux'],sources[name]['pointlike_flux_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_flux'],sources[name]['gtlike_flux_Error']),"%.2f"%sources[name]['gal_gtlike'][0]
                              )
                    )
            else :
                lines.append(
                    format % (name, "%s/%s.html"%(image_folder,name),phaserange,"%.2f"%(sources[name]['pointlike_TS']),"%.2f"%(sources[name]['gtlike_TS']),"%.2e +/- %.2e"%(sources[name]['pointlike_Prefactor'],sources[name]['pointlike_Prefactor_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_Prefactor'],sources[name]['gtlike_Prefactor_Error']),"%.2f +/- %.2f"%(sources[name]['pointlike_Index'],sources[name]['pointlike_Index_Error']),"%.2f +/- %.2f"%(sources[name]['gtlike_Index'],sources[name]['gtlike_Index_Error']),"%.2e +/- %.2e"%(sources[name]['pointlike_flux'],sources[name]['pointlike_flux_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_flux'],sources[name]['gtlike_flux_Error'])
                              )
                    )
        
    lines.append('')
    return lines

def copy_and_create_pages(folder,sourcelist,pagename,image_folder,sources,webpage,version="2"):
    """creates the page with all the plots concerning one source"""
    fold=image_folder
    for name in sourcelist:
        
        lines=[' Control page %s'%name]

        format='cp %s  %s/%s'
        liste=['logfile','counts_file','input_pointlike_srcmodel','input_pointlike_srcmodel_renormalized','output_pointlike_srcmodel','output_gtlike_srcmodel_phased','output_gtlike_srcmodel','residual_counts','excess_counts','residual_tsmap','excess_tsmap','smoothed_cmap','residual_tsmap_fits','excess_tsmap_fits','Slice','SED','region','spectrum_plot','allsed']
        #liste=['logfile']
        for element in liste :
            line2=' '
            try :
                nomfic=sources[name][element]
                while nomfic.find('/')!=-1:
                    nomfic2=nomfic[nomfic.find('/')+1:len(nomfic)]
                    nomfic=nomfic2
                fold=image_folder
                while fold.find('/')!=-1:
                    fold2=fold[fold.find('/')+1:len(fold)]
                    fold=fold2
                os.system(format%(sources[name][element],image_folder,nomfic))
                line2+='%s'%nomfic
                line2+=' '
                if nomfic.find('png')!=-1 :
                    #line2+='[[%s] %s]'%(nomfic,nomfic)
                    line2+='</br><a href="%s"><img src="%s" alt="plot not yet avalaible" title="%s"></a></br>'%(nomfic,nomfic,nomfic)
                else :
                    line2+='<a href="%s" target="_blank">%s</a></br>'%(nomfic,nomfic)
                line2+=' '
            except :
                a=0
                print "plante"
            line2+=' '
            lines.append(line2)
        t2t(lines,'%s/%s'%(image_folder,name))
    return fold

def one_folder(folder,pagename,website,version="2"):
    """Action to do for one folder of tests"""
    try :
        #creating source list and page of results
        lines=['=PWN cat results %s='%pagename]
        sources,sourcelist=create_sources_list(folder,pwnphase,version=version)
        sourcelist.sort()
        image_folder="%s%s_images"%(website,pagename)
        try :
            os.system("mkdir %s"%image_folder)
        except :
            os.system("rm -rf %s"%image_folder)
            os.system("mkdir %s"%image_folder)
        fold=copy_and_create_pages(folder,sourcelist,pagename,image_folder,sources,website,version=version)
        lines=format_table(lines,sources,sourcelist,fold,pagename,version=version)
        t2t(lines,pagename)
    except :
        print "No page %s created"%pagename
    

if __name__ == '__main__':
    website="/afs/slac.stanford.edu/u/gl/rousseau/public_html/pwncat/"
    pwnphase="/afs/slac/g/glast/users/rousseau/svn/trunk/pwncatalog/1FGL_reanalysis/v3/pwndata/pwnphase_v1.yaml"
    base="/afs/slac/g/glast/users/rousseau/PWN_cat/website/"
    
    test=1
    
    try :
        f=open('submit_all.py',"r")
    except :
        test=0
    if test==0 :
        line2=[]
        line2.append('')
        line2.append('= Summary of available results file for reanalysis of PWN cat 1 =')
        for direct in glob.iglob("%swebsite_v1/*"%base):
            print "traitement fichier %s"%direct
            test2=0
            try :
                print "je ne traite pas ce dossier"
                ftest=open(direct+'/non','r')
                ftest.close()
            except :
                test2=1
                print "je traite ce dossier"
            if test2==1:
                one_folder(direct,direct[len(base):len(direct)],website,version="1")
            line2.append('[%s %s.html]'%(direct[len(base):len(direct)],direct[len(base):len(direct)]))
            line2.append('')
        for direct in glob.iglob("%swebsite_v2/*"%base):
            print "traitement fichier %s"%direct
            test2=0
            try :
                ftest=open(direct+'/non','r')
                ftest.close()
                print "je ne traite pas ce dossier"
            except :
                test2=1
                print "je traite ce dossier"
            if test2==1:
                one_folder(direct,direct[len(base):len(direct)],website,version="2")
            line2.append('[%s %s.html]'%(direct[len(base):len(direct)],direct[len(base):len(direct)]))
            line2.append('')
        line2.append('Question ? Comment ? rousseau@cenbg.in2p3.fr')
        line2.append('')
        t2t(line2,'index')
        for sorties in glob.iglob("%s*/*/*.html"%website):
            f=open(sorties,"r")
            lignes=f.readlines()
            f.close()
            f=open(sorties,"w")
            for i in range(len(lignes)):
                lignes[i]=lignes[i].replace('&lt;','<')
                lignes[i]=lignes[i].replace('&gt;','>')
                f.write(lignes[i]+'\n')
            f.close()
        
    else :
        nom=base
        while nom.find('/')!=-1:
            nom2=base[base.find('/')+1:len(base)]
            nom=base2
        one_folder(base,'index',website)
        
