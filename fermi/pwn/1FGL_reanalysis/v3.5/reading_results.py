import glob
import yaml

energyrange=[]
names=[]
for name in glob.iglob("*"):
    for name2 in glob.iglob("%s/*"%name):
        if len(energyrange)!=0:
            test=0
            for i in range(len(energyrange)):
                if energyrange[i]==name:
                    test=1
            if test==0:
                energyrange.append(name)
        else :
            energyrange.append(name)


#for erange in energyrange:
sources={}
for name2 in glob.iglob("%s/*"%energyrange[0]):
    
    if name2.find("PSR")!=-1:
        source={}
        source['name']=name2[len(energyrange[0])+1:len(name2)]
        structu=yaml.load(open("%s/results_%s"%(name2,name2[len(energyrange[0])+1:len(name2)])))
        for erange in energyrange:
            
            erangedat={}
            erangedat['tsgtlike']=structu['gtlike']['ts_at_pulsar']
            erangedat['tspointlike']=structu['pointlike']['ts_at_pulsar']
            erangedat['fluxgtlike']=structu['gtlike']['flux_at_pulsar']
            erangedat['fluxpointlike']=structu['pointlike']['flux_at_pulsar']
            if erangedat['tsgtlike']<25.0:
                erangedat['limsup']=structu['gtlike_ul']
            else :
                erangedat['limsup']=-1
            erangedat['gammagtlike']=structu['gtlike']['Index_at_pulsar']
            erangedat['gammapointlike']=structu['pointlike']['Index_at_pulsar']
            source[erange]=erangedat
        sources[source['name']]=source


f1=open("gtlike.out","w")
f2=open("pointlike.out","w")
chain="|\tSource\t\t|"
for i in range(len(energyrange)):
    chain+="|\t%s\tTS\tFlux\tGamma\t|"%energyrange[i]
chain+="\n"
f1.write(chain)
f2.write(chain)
for name1 in glob.iglob("%s/*"%energyrange[0]):
    name2=name1[len(energyrange[0])+1:len(name1)]
    if name2.find("PSR")!=-1:
        chain1="|\t%s\t|"%name2
        chain2="|\t%s\t|"%name2
        source=sources[name2]
        for energ in energyrange:
            gamme=source[energ]
            if gamme['limsup']==-1:
                chain1+="|\t%.2f\t%.2e\t%.2f\t|"%(gamme['tsgtlike'],gamme['fluxgtlike'],gamme['gammagtlike'])
            else :
                chain1+="|\t<%.2f\t%.2e\t%.2f\t|"%(gamme['limsup'],gamme['fluxgtlike'],gamme['gammagtlike'])


            
            chain2+="|\t%.2f\t%.2e\t%.2f\t|"%(gamme['tspointlike'],gamme['fluxpointlike'],gamme['gammapointlike'])
        f1.write(chain1+"\n")
        f2.write(chain2+"\n")

f1.close()
f2.close()
