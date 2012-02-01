

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--pwnphase")




name='PSRJ0534+2200'
roi = load('$pwndata/spectral/v9/analysis_no_plots/%s/roi_at_pulsar_%s.dat' % (name,name))

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

import lande_variability
reload(lande_variability);v = lande_variability.VariabilityTester(roi,name,nbins=36, always_upper_limit=True, savedir='savedir')

print v
print v.todict()

open('results_%s.yaml' % name,'w').write(yaml.dump(v.todict()))

