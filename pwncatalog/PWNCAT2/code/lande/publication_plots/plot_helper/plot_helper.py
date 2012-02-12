from matplotlib import rc

rc('ps',usedistiller='xpdf')
rc('text', usetex=True)
rc('font', family='serif', serif="Computer Modern Roman")

import pylab as P


def get_bw():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--bw", action="store_true", default=False)
    args=parser.parse_args()
    global bw
    bw=args.bw
    return bw


def save(base):
    if bw:
        P.savefig('%s_bw.pdf' % base)
        P.savefig('%s_bw.eps' % base)
    else:
        P.savefig('%s_color.pdf' % base)
        P.savefig('%s_color.eps' % base)
