import glob
import yaml
from uw.pulsar.phase_range import PhaseRange
import os,sys
import asciitable
import re
from os.path import join,exists
from collections import defaultdict

debug=0
debug2=0
def create_sources_list(folder,pwnphase,hypothesis):
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
                print "%s/%s/results_%s.yaml"%(folder,name,name)
                results1=yaml.load(open("%s/%s/results_%s.yaml"%(folder,name,name)))
                if debug ==1:
                    print "opening results 1"
                results=results1[hypothesis]
                if debug ==1:
                    print "results"
                try :
                    source['gtlike_TS']=results['TS_gtlike']
                except :
                    try :
                        source['gtlike_TS']=results['gtlike']['TS']
                    except :
                        source['gtlike_TS']=-1.0
                if debug ==1:
                    print "TS_gtlike"
                try :
                    source['pointlike_TS']=results['TS_pointlike']
                except :
                    try :
                        source['pointlike_TS']=results['pointlike']['TS']
                    except :
                        source['gtlike_TS']=-1.0
                if debug ==1:
                    print "try except"
                try :
                    source['gtlike_Prefactor']=results['gtlike']['Prefactor']
                except :
                    try :
                        source['gtlike_Prefactor']=results['gtlike']['Integral']
                    except :
                        try :
                            source['gtlike_Prefactor']=results['gtlike']['Norm']
                        except :
                            source['gtlike_Prefactor']=-1.0
                try :
                    source['gtlike_Prefactor_Error']=results['gtlike']['Prefactor_err']
                except :
                    try :
                        source['gtlike_Prefactor_Error']=results['gtlike']['Integral_err']
                    except :
                        try :
                            source['gtlike_Prefactor_Error']=results['gtlike']['Norm_err']
                        except :
                            source['gtlike_Prefactor_Error']=-1.0
                try :
                    source['pointlike_Prefactor']=results['pointlike']['Norm']
                except :
                    try :
                        source['pointlike_Prefactor']=results['pointlike']['Int_Flux']
                    except :
                        source['pointlike_Prefactor']=-1.0
                try :
                    source['pointlike_Prefactor_Error']=results['pointlike']['Norm_err']
                except :
                    try :
                        source['pointlike_Prefactor_Error']=results['pointlike']['Int_Flux']
                    except :
                        source['pointlike_Prefactor_Error']=-1.0
                source['pointlike_Index']=results['pointlike']['Index']
                if debug ==1:
                    print "source['pointlike_Index']=results['pointlike']['Index_at_pulsar']"
                try :
                    source['pointlike_Index_Error']=results['pointlike']['Index_err']
                except :
                    source['pointlike_Index_Error']=-1.0
                if debug ==1:
                    print "source['pointlike_Index_Error']=results['pointlike']['Index_err_at_pulsar']"
                try :
                    source['gtlike_Index']=results['gtlike']['Index']
                except :
                    source['gtlike_Index']=-1.0
                if debug ==1:
                    print "source['gtlike_Index']=results['gtlike']['Index_at_pulsar']"
                try :
                    source['gtlike_Index_Error']=results['gtlike']['Index_err']
                except :
                    source['gtlike_Index_Error']=-1.0
                if debug ==1:
                    print "source['gtlike_Index_Error']=results['gtlike']['Index_err_at_pulsar']"
                try :
                    source['gtlike_flux']=results['gtlike']['flux']
                except :
                    source['gtlike_flux']=-1.0
                if debug ==1:
                    print "source['gtlike_flux']=results['gtlike']['flux_at_pulsar']"
                try :
                    source['gtlike_flux_Error']=results['gtlike']['flux_err']
                except :
                    source['gtlike_flux_Error']=-1.0
                if debug ==1:
                    print "source['gtlike_flux_Error']=results['gtlike']['flux_err_at_pulsar']"
                try :
                    source['pointlike_flux']=results['pointlike']['flux']
                except :
                    source['pointlike_flux']=-1.0
                if debug ==1:
                    print "source['pointlike_flux']=results['pointlike']['flux']"
                try :
                    source['pointlike_flux_Error']=results['pointlike']['flux_err']
                except :
                    source['pointlike_flux_Error']=-1.0
                if debug ==1:
                    print "source['pointlike_flux_Error']=results['pointlike']['flux_err']"
                source['counts_file']="%s/%s/counts_0.2_%s_%s.png"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['counts_file']="
                source['input_pointlike_srcmodel']="%s/%s/srcmodel_prefit_%s_%s.xml"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['input_pointlike_srcmodel']"
                source['input_pointlike_srcmodel_renormalized']="%s/%s/srcmodel_prefit_renorm_%s_%s.xml"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['input_pointlike_srcmodel_renormalized']"
                source['output_pointlike_srcmodel']="%s/%s/srcmodel_res_%s_%s.xml"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['output_gtlike_srcmodel_phased']"
                source['output_gtlike_srcmodel']="%s/%s/output_model_gtlike_%s_%s.xml" %(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['output_gtlike_srcmodel']"
                txt="farith %s/%s/counts_0.1_%s_%s.fits"%(folder,name,hypothesis,name)
                txt+=" %s/%s/model_0.1_%s_%s.fits"%(folder,name,hypothesis,name)
                txt+=" %s/%s/residuals_0.1_%s_%s.fits -"%(folder,name,hypothesis,name)
                try :
                    os.system("rm -rf %s/%s/residuals_0.1_%s_%s.fits"%(folder,name,hypothesis,name))
                except :
                    print " "
                    os.system(txt)
                
                source['residual_counts']="%s/%s/residuals_0.1_%s_%s.fits"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['residual_counts']"
                txt="farith %s/%s/counts_excess_0.1_%s_%s.fits"%(folder,name,hypothesis,name)
                txt+=" %s/%s/model_excess_0.1_%s_%s.fits"%(folder,name,hypothesis,name)
                txt+=" %s/%s/excess_0.1_%s_%s.fits -"%(folder,name,hypothesis,name)
                try :
                    os.system("rm -rf %s/%s/excess_0.1_%s_%s.fits"%(folder,name,hypothesis,name))
                except :
                    print " "
                    os.system(txt)
                source['excess_counts']="%s/%s/excess_0.1_%s_hypothesis.fits"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['excess_counts']"
                source['residual_tsmap']="%s/%s/residual_tsmap_%s_%s.png"%(folder,name,hypothesis,name)
                if debug ==1:
                    print " source['residual_tsmap']"
                source['excess_tsmap']="%s/%s/source_tsmap_%s_%s.png"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['excess_tsmap']="
                source['smoothed_cmap']="%s/%s/sources_%s_%s.png"% (folder,name,hypothesis,name)
                if debug ==1:
                    print "source['smoothed_cmap']"
                source['residual_tsmap_fits']="%s/%s/residual_tsmap_%s_%s.fits"%(folder,name,hypothsesis,name)
                if debug ==1:
                    print "source['residual_tsmap_fits']"
                source['excess_tsmap_fits']="%s/%s/source_tsmap_%s_%s.fits"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['excess_tsmap_fits']"
                source['spectrum_plot']="%s/%s/Spectra_%s_%s.png"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['spectrum_plot']"
                source['Slice']="%s/%s/outslice_%s_%s.png"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['Slice']"
                source['SED']="%s/%s/sed_pointlike_%s_%s.pdf"%(folder,name,hypothesis,name)
                if debug ==1:
                    print "source['SED']"
                source['region']="%s/%s/Region_file_%s.reg"%(folder,name,name)
                if debug ==1:
                    print "ource['region']"
                source['allsed']="%s/%s/allsed_%s.png"%(folder,name,name)
                if debug ==1:
                    print source['allsed']
                source['logfile']="%s/%s/log_%s.txt"%(folder,name,name)
                if debug ==1:
                    print "source['logfile']"
                try :
                    source['gal_gtlike']=results1['gal_gtlike']
                except :
                    source['gal_gtlike']=-1.0
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

def format_table(lines,sources,sourcelist,image_folder,pagename):
    lines.append('')
    if debug2==1:
        print "append"
    while pagename.find('/')!=-1:
        pagename2=pagename[pagename.find('/')+1:len(pagename)]
        pagename=pagename2
    if debug2==1:
        print "pagenam"
    pagename+=".html"
    if debug2==1:
        print "pagename+"
    table=defaultdict(list)
    if debug2==1:
        print "table"
    format = '| [%30s %30s] | %30s | %30s | %30s | %30s | %30s |%30s | %30s | %30s | %30s | %30s |'
    if debug==2:
        print "format"
    lines.append('')
    if debug2==1:
        print "append2"
    for i in range(len(sourcelist)+1) :
        if debug2==1:
            print "loop"
        if i==0:
            if debug2==1:
                print "i=0"
            lines.append(
                   '|'+format % ('Name', pagename, 'Phase Range','TS pointlike','TS gtlike','Prefactor Pointlike','Prefactor gtlike','Gamma pointlike','Gamma gtlike','Flux pointlike','Flux gtlike','Gal_norm_gtlike')
                    )
            if debug2==1:
                print "premier ligne"
        else :
            if debug2==1:
                print "else"
            name=sourcelist[i-1]
            if debug2==1:
                print "name=sourcelist[i-1]"
            phaserange=' '
            if debug2==1:
                print "phaserange"
            try:
                if debug2==1:
                    print "try"
                for i in range(len(sources[name]['phasemin'])):
                    if debug2==1:
                        print "loop2"
                    if i!=0:
                        if debug2==1:
                            print "i!=0"
                        phaserange+='U'
                        if debug2==1:
                            print "U"
                    phaserange+='[%.2f,%.2f]'%(sources[name]['phasemin'][i],sources[name]['phasemax'][i])
                    if debug2==1:
                        print "phaserange3"
            except:
                if debug2==1:
                    print "except"
                phaserange+='[%.2f,%.2f]'%(sources[name]['phasemin'],sources[name]['phasemax'])
                if debug2==1:
                    print "phaserange4"
            phaserange+="->%.2f"%sources[name]['deltaphi']
            if debug2==1:
                print "phaserange+=->"
                print "name"
                print name
                print "(image_folder,name)"
                print "%s/%s.html"%(image_folder,name)
                print "phaserange"
                print phaserange
                print "sources[name]['pointlike_TS']"
                print "%.2f"%(sources[name]['pointlike_TS'])
                print "sources[name]['gtlike_TS']"
                print "%.2f"%(sources[name]['gtlike_TS'])
                print "pointlike_Prefactor"
                print "%.2e +/- %.2e"%(sources[name]['pointlike_Prefactor'],sources[name]['pointlike_Prefactor_Error'])
                print "gtlike_Prefactor"
                print "%.2e +/- %.2e"%(sources[name]['gtlike_Prefactor'],sources[name]['gtlike_Prefactor_Error'])
                print "sources[name]['pointlike_Index'],sources[name]['pointlike_Index_Error']"
                print "%.2f +/- %.2f"%(sources[name]['pointlike_Index'],sources[name]['pointlike_Index_Error'])
                print "sources[name]['gtlike_Index'],sources[name]['gtlike_Index_Error']"
                print "%.2f +/- %.2f"%(sources[name]['gtlike_Index'],sources[name]['gtlike_Index_Error'])
                print "pointlike_flux"
                print "%.2e +/- %.2e"%(sources[name]['pointlike_flux'],sources[name]['pointlike_flux_Error'])
                print "gtlike_flux"
                print "%.2e +/- %.2e"%(sources[name]['gtlike_flux'],sources[name]['gtlike_flux_Error'])
                print "gal_gtlike"
                print sources[name]['gal_gtlike']
                print "%.2f"%sources[name]['gal_gtlike']
            lines.append(
                format % (name, "%s/%s.html"%(image_folder,name),phaserange,"%.2f"%(sources[name]['pointlike_TS']),"%.2f"%(sources[name]['gtlike_TS']),"%.2e +/- %.2e"%(sources[name]['pointlike_Prefactor'],sources[name]['pointlike_Prefactor_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_Prefactor'],sources[name]['gtlike_Prefactor_Error']),"%.2f +/- %.2f"%(sources[name]['pointlike_Index'],sources[name]['pointlike_Index_Error']),"%.2f +/- %.2f"%(sources[name]['gtlike_Index'],sources[name]['gtlike_Index_Error']),"%.2e +/- %.2e"%(sources[name]['pointlike_flux'],sources[name]['pointlike_flux_Error']),"%.2e +/- %.2e"%(sources[name]['gtlike_flux'],sources[name]['gtlike_flux_Error']),"%.2f"%sources[name]['gal_gtlike']
                          )
                )
            if debug2==1:
                print "append_encore"
    lines.append('')
    if debug2==1:
        print "append_last"
    return lines

def copy_and_create_pages(folder,sourcelist,pagename,image_folder,sources,webpage):
    """creates the page with all the plots concerning one source"""
    fold=image_folder
    for name in sourcelist:
        
        lines=[' Control page %s'%name]

        format='ln -s %s  %s/%s'
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

def one_folder(folder,pagename,website,hypothesis='point'):
    """Action to do for one folder of tests"""
    try :
        #creating source list and page of results
        if debug2==1:
            print "one_folder_try"
        lines=['=PWN cat results %s='%pagename]
        if debug2==1:
            print "setting lines"
        sources,sourcelist=create_sources_list(folder,pwnphase,hypothesis)
        if debug2==1:
            print "sources,sourcelist"
            print sourcelist
            print sources
        sourcelist.sort()
        if debug2==1:
            print "sourcelist.sort()"
        image_folder="%s%s_images"%(website,pagename)
        if debug2==1:
            print "image_folder"
        try :
            os.system("mkdir %s"%image_folder)
        except :
            os.system("rm -rf %s"%image_folder)
            os.system("mkdir %s"%image_folder)
        if debug2==1:
            print "try again"
        fold=copy_and_create_pages(folder,sourcelist,pagename,image_folder,sources,website)
        if debug2==1:
            print "fold"
        lines=format_table(lines,sources,sourcelist,fold,pagename)
        if debug2==1:
            print "lines"
        t2t(lines,pagename)
        if debug2==1:
            print "t2t"
    except :
        print "No page %s created"%pagename
    

if __name__ == '__main__':
    website="/afs/slac.stanford.edu/u/gl/rousseau/public_html/pwncat2fgl/"
    pwnphase="/afs/slac/g/glast/users/rousseau/svn/trunk/pwncatalog/1FGL_reanalysis/v3/pwndata/pwnphase_v1.yaml"
    base="/afs/slac/g/glast/users/rousseau/PWN_cat/website/website_v2/"
    try :
        os.system("rm -rf %s"%website)
        os.system("mkdir %s"%website)
    except :
        os.system("mkdir %s"%website)
        
    test=1
    
    try :
        f=open('submit_all.py',"r")
    except :
        test=0
    if test==0 :
        line2=[]
        line2.append('')
        line2.append('= Summary of available results file for reanalysis of PWN cat 1 =')
        for direct in glob.iglob("%s/*"%base):
            print "folder : %s"%direct
            test2=0
            try :
                ftest=open(direct+'/non','r')
                ftest.close()
                print "je ne traite pas ce dossier"
            except :
                test2=1
                print "je traite ce dossier"
            if test2==1:
                hyp=["at_pulsar","point","extended"]
                for hypothesis in hyp:
                    one_folder(direct,"%s_%s"%(direct[len(base):len(direct)],hypothesis),website,hypothesis=hypothesis)
                    line2.append('[%s_%s %s_%s.html]'%(direct[len(base):len(direct)],hypothesis,direct[len(base):len(direct)],hypothesis))
            line2.append('')
        line2.append('Question ? Comment ? rousseau@cenbg.in2p3.fr')
        line2.append('')
        t2t(line2,'index')
        for sorties in glob.iglob("%s*/*.html"%website):
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
        
