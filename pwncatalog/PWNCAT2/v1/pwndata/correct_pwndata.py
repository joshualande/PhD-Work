f=open("pwncat2_data_v2.yaml","r")
lignes=f.readlines()
f.close()
f2=open("pwncat2_data_v3.yaml","w")
name=''
for ligne in lignes:
    if ligne[0]!=' ':
        name=ligne[0:len(ligne)-2]
        ligne2=ligne
    elif ligne.find('ltcube')!=-1:
        ligne2='  ltcube: /afs/slac/g/glast/groups/pulsar/2ndPulsarcatalog/psue/General/%s/ltcube_%s.fits\n'%(name[3:len(name)],name[3:len(name)])
    else :
        ligne2=ligne

    f2.write(ligne2)
f2.close()
