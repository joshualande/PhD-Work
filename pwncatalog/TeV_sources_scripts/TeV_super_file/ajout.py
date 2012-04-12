import os,sys
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
