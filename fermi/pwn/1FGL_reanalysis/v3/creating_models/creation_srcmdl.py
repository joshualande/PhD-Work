#R.Rousseau 16/12/2010
#Module de lecture du catalogue en pyfits et de creation du sourcmodel
#import des outils necessaires
import os
import re,sys,pyfits,os
from math  import *
import string
from creationmodels import *

#Definition des numeros de colonnes des differentes donnees necessaires
#nom de la source :
name_col='NickName'
#Ra :
ra_col='RA'
#Dec
dec_col='DEC'
#Indice spectral
ind_col='Spectral_Index'
#Indice de courbure
cour_col='Curvature_Index'
#E pivot
Epivot_col='Pivot_Energy'
#Integral
Inte_col='Flux100'
#Prefactor
pref_col='Flux_Density'
#error on prefactor
err_pref_col='Unc_Flux_Density'
#indice de cutoff
varia_cut='Pivot_Energy'

#definition du seuil de variabilite
varia_seuil=11.34

raymax=10.0

#Definition des bornes minimum et maximum de la zone considereee minimum en ra,#max en ra,#min en dec,#max en dec
def lect_ca(dir_cat,SourceRA,SourceDec,SourceROI,distmin,name,outputfile,namesource):
	"""Lecture du catalogue pour en retirer les sources interessantes pour le fit
		la fonction s'appelle de la maniere suivante : lect_ca(dir_cat,SourceRA,SourceDec,SourceROI,distmin)
		dir_cat est la direction du catalogue utilise
		SourceRA est l'ascension droite de la source etudiee
		SourceDec est la declinaison de la source etudiee
		SourceROI (Region of Interest) est le rayon du cercle considere autour de la source
		distmin est la distance pour laquelle on considerera que la source n'est pas etendue.
		name est le nom de l'objet que l'on souhaite etudier
		Outputfile est le nom de fichier de sortie qui va contenir toutes les donnees sur les sources
		namesource is the name of the source of interest"""
	print "SourceROI="+str(SourceROI)
	fcal= open(outputfile,"w");
	
	#fcat=pyfits.open(dir_cat)

	donnees=pyfits.getdata(dir_cat,1)
	names=donnees.field(name_col)
	print names
	ra=donnees.field(ra_col)
	dec=donnees.field(dec_col)
	ind=donnees.field(ind_col)
	cour=donnees.field(cour_col)
	Epiv=donnees.field(Epivot_col)	
	Integ=donnees.field(Inte_col)
	Prefact=donnees.field(pref_col)
	Err_prefact=donnees.field(err_pref_col)
	variabilite=donnees.field(varia_cut)

    #Loop on the LAT Catalog
	for p in range(0,len(names)-1):
			#Calcul de la distance angulaire separant la source p et la source que l'on etudie
		dist = (180./3.14159)*acos(cos(3.14159/2. - float(SourceDec)*3.14159/180.)*cos(3.14159/2.- float(dec[p])*3.14159/180.)+sin(3.14159/2. - float(SourceDec)*3.14159/180.)*sin(3.14159/2.- float(dec[p])*3.14159/180.)*cos((float(SourceRA) - float(ra[p]))*3.14159/180.))
			
			#These Marie-Helene Grondin p.
		#nom=names[p].split(" ")
		#names[p]=nom[0]+"_"+nom[1]


#		if (dist< float(SourceROI)):
#			print str(dist)+str(names[p])                 
		if (dist < float(SourceROI) and dist > float(distmin) ): #SI la source est dans la region d'interet mais n'est pas confondu avec la source elle meme. 0.2 est subjectif, compromis qui marche dans la pluspart des cas mais pas dans tous. Faire attention parfois il faut remplacer ce 0.2 par 0.3
			if float(cour[p]!="NULL") and float(Integ[p]) > 1e-8 and dist < 5: #cut-off
				print "curvature = ", float(cour[p])
				txt = str(names[p])+" "+str(ra[p])+" "+str(dec[p])+" "+str(Integ[p])+" "+str(ind[p])+" "+str(Prefact[p])+" "+str(Epiv[p])+" 1"
#				if variabilite[p]>varia_seuil:
                                txt+=" 1 "+str(dist)
#				else :
#			   txt+=" 0 "+str(dist)
			else: #no cut off with flux level high enough
				txt = str(names[p])+" "+str(ra[p])+" "+str(dec[p])+" "+str(Integ[p])+" "+str(ind[p])+" "+str(Prefact[p])+" "+str(Epiv[p])+" 0"
#				if variabilite[p]>varia_seuil:
			    	txt+=" 1 "+str(dist)
#				else :
#					txt+=" 0 "+str(dist)
			fcal.write(txt)
			fcal.write("\n")
		elif (dist < float(raymax) and names[p]!=namesource) :

			if float(cour[p]) > 11.34 and float(Integ[p]) > 1e-8 and dist < 5: #cut-off
				print "curvature = ", float(cour[p])
				txt = str(names[p])+" "+str(ra[p])+" "+str(dec[p])+" "+str(Integ[p])+" "+str(ind[p])+" "+str(Prefact[p])+" "+str(Epiv[p])+" 1 2 "+str(dist)

			else: #no cut off with flux level high enough
				txt = str(names[p])+" "+str(ra[p])+" "+str(dec[p])+" "+str(Integ[p])+" "+str(ind[p])+" "+str(Prefact[p])+" "+str(Epiv[p])+" 0 2 "+str(dist)                           
			fcal.write(txt)
			fcal.write("\n")
	#On ajoute l'objet de l'etude
	pwn = name
	txt = str(pwn)+" "+str(SourceRA)+" "+str(SourceDec)+" 1e-10 2 0"
	fcal.write(txt)
	fcal.write("\n")

	fcal.close()

	

def creation_srcmdl(dir_cat,SourceRA,SourceDec,SourceROI,distmin,name,outputfile,emin,emax):
	"""Lecture du catalogue pour en retirer les sources interessantes pour le fit
		la fonction s'appelle de la maniere suivante : lect_ca(dir_cat,SourceRA,SourceDec,SourceROI,distmin)
		dir_cat est la direction du catalogue utilise
		SourceRA est l'ascension droite de la source etudiee
		SourceDec est la declinaison de la source etudiee
		SourceROI (Region of Interest) est le rayon du cercle considere autour de la source
		distmin est la distance pour laquelle on considerera que la source n'est pas etendue.
		name est le nom de l'objet que l'on souhaite etudier
		Outputfile est le nom de fichier de sortie sourcemap.xml
		Frac la fraction de periode du pulsar utilisee
		f_liste_source est le nom du fichier de liste des sources"""
	f_liste_sour="a.txt"

	lect_ca(dir_cat,SourceRA,SourceDec,SourceROI,distmin,name,f_liste_sour,name)
	XML_EC_PL(name, f_liste_sour, outputfile, emin,emax)
	os.system("rm -rf a.txt")
#if __name__ == '__main__':

	#dir_cat="/data/astro17g/rousseau/Data/catalogue/gll_psc18month_uw8_assoc.fits"

 #   if len(sys.argv)==10:
 #   creation_srcmdl(dir_cat,sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
  #  else:
   #     print "Usage: python creation_srcmdl.py SourceRA SourceDec SourceROI distmin name outputfile nom_template frac: Try again !!!" 
