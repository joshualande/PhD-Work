import os,sys
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

def modify_roi(name,roi):

    modify_psr_base.modify_roi(name,roi)

    pass # nothing for now
