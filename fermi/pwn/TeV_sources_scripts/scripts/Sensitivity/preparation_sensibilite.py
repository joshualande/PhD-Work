
import yaml
from os.path import expandvars as e
from os.path import join
import os,sys
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-d", "--data", required=True)
parser.add_argument("-t", "--tevdata", required=True)
parser.add_argument("-m", "--hypothese", default="at_tev")
args,remaining_args = parser.parse_known_args()
data=args.data
nom=data
hypothese=args.hypothese
while nom.find("/")!=-1:
#    print nom
    nom2=nom[nom.find("/")+1:len(nom)]
    nom=nom2
    
print nom

reference="/afs/slac/g/glast/users/rousseau/TeV_sources/scripts/Sensitivity/Modele/"

test=True
output=args.output
folder="%s/%s"%(output,nom)

try:
    os.system("mkdir %s/"%(folder))
    os.system("mkdir %s/detectes"%(folder))
    os.system("mkdir %s/lim_sup_globale"%(folder))
    os.system("mkdir %s/lim_sup_SED"%(folder))
    os.system("cp %sSensitivity* %s/detectes/"%(reference,folder))
    os.system("cp %sSensitivity* %s/lim_sup_globale/"%(reference,folder))
    os.system("cp %sSensitivity* %s/lim_sup_SED/"%(reference,folder))

except:
    test=False

tev_sed="/afs/slac/g/glast/users/rousseau/TeV_sources/scripts/Sensitivity/version_MH/"
erg_en_MeV=1.0/1.6e-6

if test:
    sources=yaml.load(open(args.tevdata))
    for name in sources.keys():
        try:
            print name
            results=yaml.load(open("%s/%s/results_%s.yaml"%(data,name,name)))
            TS=float(results[hypothese]['gtlike']['TS'])
            if TS>25.0:
                direction=["%s/detectes/%s/"%(folder,name)]
            else :
                direction=["%s/lim_sup_globale/%s/"%(folder,name),"%s/lim_sup_SED/%s/"%(folder,name)]
            for direct in direction:
                try:
                    os.system("rm -rf %s"%direct)
                except:
                    print " "
                os.system("mkdir %s"%direct)

                os.system("cp %s/modele/plot.C %s"%(reference,direct))

                if direct.find("detectes")!=-1 or direct.find("lim_sup_SED")!=-1:
                    try :
                        SED=yaml.load(open("%s/%s/seds/sed_gtlike_2bpd_%s_%s.yaml"%(data,name,hypothese,name)))
                    except :
                        SED=yaml.load(open("%s/%s/seds/sed_gtlike_%s_%s.yaml"%(data,name,hypothese,name)))
                    points=SED['dNdE']['Value']
                    error=SED['dNdE']['Error']
                    UL=SED['dNdE']['Upper_Limit']
                    significant=SED['Significant']
                    min_E=SED['Energy']['Lower']
                    max_E=SED['Energy']['Upper']
                    unit_E=SED['Energy']['Units']
                    unit_dNdE=SED['dNdE']['Units']
                    mean_E=[]
                    from math import log10,pow
                    #conversion de E en erg
                    for i in range(len(max_E)):
                        mean_E.append(pow(10.0,(log10(float(min_E[i]))+log10(float(max_E[i])))/2.0)/624150.974)

                
                    print significant
                    car1=[]
                    car2=[]
                    for i in range(len(significant)):
                        if significant[i]:
                            car1.append("%.2e %.2e %.2e %.2e"%(float(min_E[i]),float(max_E[i]),float(points[i])*mean_E[i]*mean_E[i],float(error[i])*mean_E[i]*mean_E[i]))
                        else:
                            car2.append("%.2e %.2e %.2e 0.0"%(float(min_E[i]),float(max_E[i]),float(UL[i]*mean_E[i]*mean_E[i])))
                
                
                    if len(car1)==0:
                        car1.append(' ')
                    elif len(car2)==0:
                        car2.append(' ')
                    
                    for i in range(len(car1)):
                        if i!=0:
                            traitement="\n"+car1[i]
                            car1[i]=traitement
                    for i in range(len(car2)):
                        if i!=0:
                            traitement="\n"+car2[i]
                            car2[i]=traitement

                    f=open("%s/GeV.txt"%direct,"w")
                    for text in car1:
                        f.write(text)
                    f.close()
                    f=open("%s/GeV_UL.txt"%direct,"w")
                    for text in car2:
                        f.write(text)
                    f.close()
                    f=open("%s/liste"%tev_sed,"r")
                    lignes=f.readlines()
                    f.close()
                    test_file=False
                    for nom2 in lignes:
                        nom3=nom2.lower()
                        if nom3.find(name.lower())!=-1:
                            test_file=True
                            try:
                                os.system("cp %s/%s %s/TeV.txt"%(tev_sed,nom2[0:len(nom2)-1],direct))
                            except:
                                os.system("cp %s/TeV.txt %s/TeV.txt"%(tev_sed,direct))
                                print "pas trouve %s/%s.txt"%(tev_sed,nom2[0:len(nom2)-1])
                    if not test_file:
                        os.system("cp %s/TeV.txt %s/TeV.txt"%(tev_sed,direct))
                else:
                    try :
                        SED=yaml.load(open("%s/%s/seds/sed_gtlike_1bin_%s_%s.yaml"%(data,name,hypothese,name)))
                    except :
                        SED=yaml.load(open("%s/%s/seds/sed_gtlike_%s_%s.yaml"%(data,name,hypothese,name)))
                    points=SED['dNdE']['Value']
                    error=SED['dNdE']['Error']
                    UL=SED['dNdE']['Upper_Limit']
                    significant=SED['Significant']
                    min_E=SED['Energy']['Lower']
                    max_E=SED['Energy']['Upper']
                    unit_E=SED['Energy']['Units']
                    unit_dNdE=SED['dNdE']['Units']
                    mean_E=[]
                    from math import log10,pow
                    #conversion de E en erg
                    f=open("%s/GeV_UL.txt"%direct,"w")
                
                    for i in range(len(max_E)):
                        mean_E.append(pow(10.0,(log10(float(min_E[i]))+log10(float(max_E[i])))/2.0)/624150.974)
                        f.write("%.2e %.2e %.2e 0.0"%(float(min_E[i]),float(max_E[i]),float(UL[i])*mean_E[i]*mean_E[i]))
                    f.close()
                            
                    f=open("%s/GeV.txt"%direct,"w")
                    f.write(" ")
                    f.close()
                    f=open("%s/liste"%tev_sed,"r")
                    lignes=f.readlines()
                    f.close()
                
                    for nom2 in lignes:
                        nom3=nom2.lower()
                        if nom3.find(name.lower())!=-1:
                            try:
                                os.system("cp %s/%s %s/TeV.txt"%(tev_sed,nom2[0:len(nom2)-1],direct))
                            except:
                                print "pas trouve %s/%s.txt"%(tev_sed,nom2[0:len(nom2)-1])

        except:
            print "pas reussi a traiter"
