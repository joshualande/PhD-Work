from Utilities_spf import *
import os,sys

try:
    os.system("rm -rf Super_File_test_pulsar.yaml")
except:
    print " "
input="Super_File.yaml"
output="Super_File_test_pulsar.yaml"

file=open(input,"r")
file2=open(output,"w")
lignes=file.readlines()

for i in range(len(lignes)):
    if lignes[i].find("  ")==-1 and lignes[i].find("#")==-1:
        file2.write(lignes[i])
        file2.write("  pulsar_SED_energy: []\n  pulsar_SED: []\n")
    else:
        file2.write(lignes[i])
file2.close()                                    

#os.system("cp Super_File.yaml Super_File_test_pulsar.yaml")
update_pulsars("Super_File_test_pulsar.yaml","Ozlem_fit_results.fits")
