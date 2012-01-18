from uw.like.roi_catalogs import Catalog2FGL, FermiCatalog

catalog1=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',latextdir='$FERMI/extended_archives/gll_psc_v05_templates',prune_radius=0)
catalog2=FermiCatalog("/afs/slac/g/glast/users/rousseau/catalogs/hard_source_list/gll_psc3yearhardclean_v2r1.fit")

