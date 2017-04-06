from LHEevent import *
from LHEfile import *
from array import array

import sys
import plotTools
import numpy as n
import ROOT as rt
import math

if __name__ == '__main__':

    # find events in file
    my_lhe_file = LHEFile(sys.argv[1])
    my_lhe_file.set_max(10000)

    events_read_in = my_lhe_file.read_events()

    t = rt.TTree( 'events', 'tree with events from LHE file' )
    n_part =  array('i',[50])

    np = 0
    ident = array('f',n_part[0]*[0])
    id_nP = ident[np]


    t.Branch("nPart", n_part, "nPart/I")
    t.Branch("ID", ident, "IDnp/F")
#    t.Branch("E",E,"E[n_part]/F")
#    t.Branch("Px",Px,"Px[n_part]/F")
#    t.Branch("Py",Py,"Py[n_part]/F")
#    t.Branch("Pz",Pz,"Pz[n_part]/F")

#    tree.Branch( 'staff', staff, '' )
    
    for one_event in events_read_in:

        my_lhe_event = LHEEvent()
        my_lhe_event.fill_event(one_event)
        w = my_lhe_event.weights
        n_part[0] = int(len(my_lhe_event.particles))
        np = int(len(my_lhe_event.particles))

	print n_part
	
        for i,p  in enumerate(my_lhe_event.particles):
            ident[i] = p['ID']

        print ident

        t.Fill()


            

        #del one_event, my_lhe_event

    fout =  rt.TFile(sys.argv[2],"RECREATE") 
    t.Write()
