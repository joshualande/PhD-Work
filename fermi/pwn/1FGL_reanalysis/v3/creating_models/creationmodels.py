#R.Rousseau 16/12/2010
#Module de creation des sources models a rentrer dans gtsrcmaps pour l'analyse.

import os
import re,sys,pyfits,os
from math  import *
import string

#Chemin du template (version borlin55)
#path='/data/astro17g/rousseau/Data/scripts/Template/Templates/'
#Chemin du template (version noric)
path='sourcemdl/Template/Templates/'
Frac=1.0

def XML_EC_PL(Name, InputsFile, OutputFile, emin,emax):
	"""Creation du fichier xml source model pour des Lois de puissances avec coupure exponentielle et lois de puissances"""

	#On commence par afficher ce qu'on fait
	print " Build xml file "
	print InputsFile
	#ouverture du fichier dans lequel on place le source model
	try:
		fresult = open(OutputFile, 'w')
	except:
		print "Coucou"
    	#ecriture des premieres lignes invariantes
	fresult.write('<?xml version="1.0" ?>')
	fresult.write("<source_library title=\"source library\">\n")

    	#ouverture du fichier avec les entrees
	f = open(InputsFile,"r")
	lines = f.readlines()
	
    	#Ajout des sources detectees dans le catalogue
	#Pour chaque ligne du fichier d'entree
	for line in range(len(lines)):
		#Lire les donnees de la ligne		
		data = lines[line].split()
		name = data[0]

		#Verification : est on en train de traiter la source que l'on veut etudier ou une autre ?
		if str(name) == Name :
			mysource = 1
		else:
			mysource = 0

		#recuperation des donnees
		RA = data[1]
		DEC = data[2]
		Integral = float(data[3])*float(Frac)
		Gamma= data[4]

		
		try:
			#essai de definition des donnees pour un PL avec ExpCut
			Prefactor = float(data[5])*float(Frac)
			Energy =  float(data[6])
	#		Prefactor = Prefactor/pow(Energy/100., float(Gamma)) #Densite de flux calculee a Epivot
	#		Prefactor = Prefactor*pow(1000./100., float(Gamma)) #We do the calculation with (E/1000.)^Gamma
			variabilite=float(data[8])

#			print variabilite




			cut = float(data[7]) # Cut est la variable qui nous permettra de savoir si il faut utiliser un cut off (1) ou une loi de puissance normale (2)
		except:
			try:
				cut = float(data[5])
			except:
				print " Wrong size of list "
				sys.exit()
            	#Si on considere un ccut off exponentiel pour la source :
		if cut == 1:
			#ecriture du nom de la source consideree
			result_line="  <source "
			result_line += "name=\""+name+"\""
			result_line += " type=\"PointSource\">\n"
			spectrum_type = "PLSuperExpCutoff"
			#Utilisation de la modelisation PLSuperExpCutoff car plus simple et plus intuitive pour nous et pour la modelisation des pulsars si il faut en modeliser

			#definition des parametres spectraux a prendre en comtpe et de la chaine de caractere a integrer



			if variabilite==0.0 or variabilite==2.0:
				spectrum_lines  = "     <parameter free=\"0\" max=\"10000000.0\" min=\"0.0000001\""

				#d'ou vient ce 1e-12
				Integral = float(Prefactor)*1.0e10
				scale = 1.0e-10

				spectrum_lines += " name=\"Prefactor\" scale=\""+str(scale)+"\" value=\""
				spectrum_lines += str(Integral)+"\" />\n"
            
				spectrum_lines += "       <parameter free=\"1\" max=\"5.0\" min=\"0.\""
				spectrum_lines += " name=\"Index1\" scale=\"-1.0\" value=\""
				spectrum_lines += str(Gamma)+"\"/>\n"
            
				spectrum_lines += "        <parameter free=\"0\" max=\"20000.0\" min=\"1.0\""
				spectrum_lines += " name=\"Scale\" scale=\"1.0\" value=\""+str(Energy)+"\"/>\n"
            
				spectrum_lines += "        <parameter free=\"1\" max=\"100.0\" min=\"0.001\""
				spectrum_lines += " name=\"Cutoff\" scale=\"1000.0\" value=\"30.0\"/>\n"

				spectrum_lines += "        <parameter free=\"0\" max=\"5.0\" min=\"0.0\""
				spectrum_lines += " name=\"Index2\" scale=\"1.0\" value=\"1.0\"/>\n"
			elif variabilite==1.0 :
				spectrum_lines  = "     <parameter free=\"1\" max=\"10000000.0\" min=\"0.0\""

				#d'ou vient ce 1e-12
				Integral = float(Prefactor)*1.0e10
				scale = 1.0e-10

				spectrum_lines += " name=\"Prefactor\" scale=\""+str(scale)+"\" value=\""
				spectrum_lines += str(Integral)+"\" />\n"
            
				spectrum_lines += "       <parameter free=\"1\" max=\"5.0\" min=\"0.\""
				spectrum_lines += " name=\"Index1\" scale=\"-1.0\" value=\""
				spectrum_lines += str(Gamma)+"\"/>\n"
            
				spectrum_lines += "        <parameter free=\"0\" max=\"20000.0\" min=\"1.0\""
				spectrum_lines += " name=\"Scale\" scale=\"1.0\" value=\""+str(Energy)+"\"/>\n"
            
				spectrum_lines += "        <parameter free=\"1\" max=\"100.0\" min=\"0.0001\""				spectrum_lines += " name=\"Cutoff\" scale=\"1000.0\" value=\"30.0\"/>\n"
            
				spectrum_lines += "        <parameter free=\"0\" max=\"5.0\" min=\"0.0\""
				spectrum_lines += " name=\"Index2\" scale=\"1.0\" value=\"1.0\"/>\n"


            

#      <spectrum type="PLSuperExpCutoff">
#        <parameter free="1" max="100000" min="0" name="Prefactor" scale="1e-10" value="Prefactor*1e-10"/>
#        <parameter free="1" max="0" min="5" name="Index1" scale="-1" value="valeur du catalogue"/>
#        <parameter free="0" max="20000" min="1.0" name="Scale" scale="1" value="Epivot"/>
#        <parameter free="1" max="300000" min="100" name="Cutoff" scale="1" value="3000"/>
#        <parameter free="0" max="5" min="0" name="Index2" scale="1" value="1.5"/>
#      </spectrum>


		else:
		#Sinon (si on considere une loi de puissance simple)
		#definition de la chaine de caractere comportant le nom de la source
			result_line="  <source "
			result_line += "name=\""+name+"\""
			if mysource == 0:				result_line += " type=\"PointSource\">\n"
			else:
				result_line += " type=\"PointSource\">\n"				

			#definition de la chaine de caractere correspondant a la forme de fit que l'on souhaite utiliser (Loi de puissance)
			spectrum_type = "PowerLaw2"

			if mysource == 0 and variabilite!=1.0:
			#si ce n'est pas la source que l'on etudie on fige le parametre Integrale
				spectrum_lines  = "     <parameter free=\"0\" max=\"1000000.0\" min=\"0.0\""
			else:
			#sinon on le libere
				spectrum_lines  = "     <parameter free=\"1\" max=\"1000000.0\" min=\"0.0\""





			#Toujours ce facteur....
			Integral = float(Integral)*1e10
			scale = 1e-10


	

			spectrum_lines += " name=\"Integral\" scale=\""+str(scale)+"\" value=\""
			spectrum_lines += str(Integral)+"\" />\n"

			if mysource == 0 and variabilite!=1.0:
				#si ce n'est pas la source que l'on etudie on fige le parametre gamma
		 		spectrum_lines += "       <parameter free=\"0\" max=\"5.0\" min=\"0.\""
			else:
				#si c'est pas la source que l'on etudie on le laisse libre
		 		spectrum_lines += "       <parameter free=\"1\" max=\"5.0\" min=\"0.\""

			#fin de la chaine de parametres sur le modele spectral
			spectrum_lines += " name=\"Index\" scale=\"-1.0\" value=\""
			spectrum_lines += str(Gamma)+"\"/>\n"
             
			if mysource == 0 and variabilite!=1.0:
	     
			    spectrum_lines += "        <parameter free=\"0\" max=\"200000.0\" min=\"20.0\""
			    spectrum_lines += " name=\"LowerLimit\" scale=\"1.0\" value=\"1000.0\"/>\n"
             
			    spectrum_lines += "        <parameter free=\"0\" max=\"1000000.0\" min=\"20.0\""
			    spectrum_lines += " name=\"UpperLimit\" scale=\"1.0\" value=\"100000.0\"/>\n"
			else:
				spectrum_lines += "        <parameter free=\"0\" max=\"200000.0\" min=\"20.0\""
				spectrum_lines += " name=\"LowerLimit\" scale=\"1.0\" value=\"100\"/>\n"

				spectrum_lines += "        <parameter free=\"0\" max=\"100000.0\" Min =\"20.0\""
				spectrum_lines += " name=\"UpperLimit\" scale=\"1.0\" value=\"100000.0\"/>\n"

 		#ajout du modele spectral a la liste de parametres           
		result_line += "   <spectrum type=\""+spectrum_type+"\">\n"		result_line += spectrum_lines
		result_line += "   </spectrum>\n"

		

		if mysource==0 and variabilite!=1.0:
 			#ajout du modele spatial a la liste de parametres  
			result_line += "   <spatialModel type=\"SkyDirFunction\">\n"
			result_line += "     <parameter free=\"0\" max=\"360\" min=\"-360\""
			result_line += " name=\"RA\" scale=\"1\" value=\""+RA+"\"/>\n"
			result_line += "     <parameter free=\"0\" max=\"90\" min=\"-90\""
			result_line += " name=\"DEC\" scale=\"1\" value=\""+DEC+"\"/>\n"
			result_line += "   </spatialModel>\n"
		elif mysource==0 and variabilite==1.0:
 			#ajout du modele spatial a la liste de parametres  
			result_line += "   <spatialModel type=\"SkyDirFunction\">\n"
			result_line += "     <parameter free=\"1\" max=\"360\" min=\"-360\""
			result_line += " name=\"RA\" scale=\"1\" value=\""+RA+"\"/>\n"
			result_line += "     <parameter free=\"1\" max=\"90\" min=\"-90\""
			result_line += " name=\"DEC\" scale=\"1\" value=\""+DEC+"\"/>\n"
			result_line += "   </spatialModel>\n"
		else:
                        #ajout du modele spatial a la liste de parametres  
			result_line += "   <spatialModel type=\"SkyDirFunction\">\n"
			result_line += "     <parameter free=\"1\" max=\"360\" min=\"-360\""
			result_line += " name=\"RA\" scale=\"1\" value=\""+RA+"\"/>\n"
			result_line += "     <parameter free=\"1\" max=\"90\" min=\"-90\""
			result_line += " name=\"DEC\" scale=\"1\" value=\""+DEC+"\"/>\n"
			result_line += "   </spatialModel>\n"
			
		result_line += "  </source>\n"
		fresult.write(result_line+"\n")
    #Ajout du fond diffus galactique
	result_line="  <source "
	result_line += "name=\"gal_v02\""
	result_line += " type=\"DiffuseSource\">\n"
	spectrum_type = "ConstantValue"

	spectrum_lines  = "     <parameter free=\"1\" max=\"10.0\" min=\"0\""
	spectrum_lines += " name=\"Value\" scale=\"1.0\" value=\""+str(Frac)+"\" />\n"

	result_line += "   <spectrum type=\""+spectrum_type+"\">\n"
	result_line += spectrum_lines
	result_line += "   </spectrum>\n"

	result_line += "   <spatialModel file=\"/nfs/farm/g/glast/u31/marianne/VelaX/July09_Pointed/gll_iem_v02.fit\" type=\"MapCubeFunction\">\n"
	result_line += "     <parameter free=\"0\" max=\"1000.0\" min=\"0.0\""
	result_line += " name=\"Normalization\" scale=\"1\" value=\"1.0\"/>\n"
	result_line += "   </spatialModel>\n"
	result_line += "  </source>\n"
	fresult.write(result_line+"\n")

    	#Ajout du fond diffus extragalactique
	result_line="  <source "
	result_line += "name=\"eg_v02\""
	result_line += " type=\"DiffuseSource\">\n"
	spectrum_type = "FileFunction"
	spectrum_lines  = "     <parameter free=\"1\" max=\"10.0\" min=\"0\""
	spectrum_lines += " name=\"Normalization\" scale=\"1.0\" value=\""+str(Frac)+"\" />\n"

	result_line += "   <spectrum file=\"/nfs/farm/g/glast/u31/marianne/VelaX/July09_Pointed/isotropic_iem_v02.txt\" type=\""+spectrum_type+"\">\n"
	result_line += spectrum_lines
	result_line += "   </spectrum>\n"
   
	result_line += "   <spatialModel type=\"ConstantValue\">\n"
	result_line += "     <parameter free=\"0\" max=\"100.0\" min=\"0.0\""
	result_line += " name=\"Value\" scale=\"1\" value=\"1.0\"/>\n"
	result_line += "   </spatialModel>\n"
	result_line += "  </source>\n"
	fresult.write(result_line+"\n")

    	#Fermeture des fichiers  
	f.close() 
	fresult.write("\n</source_library>\n")
	fresult.close()
	return

# Main
if __name__ == '__main__':

	print "Je ne fais rien tout seul !"
