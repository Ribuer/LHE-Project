from LHEevent import LHEEvent
from LHEfile import LHEFile
from array import array
from plotTools import transverse_momentum

import sys
import ROOT as rt

if __name__ == '__main__':

    # find events in file
    my_lhe_file = LHEFile(sys.argv[1])
    my_lhe_file.set_max(10000)

    events_read_in = my_lhe_file.read_events()

    t = rt.TTree('events', 'tree with events from LHE file' )
    n_part =  array('i', [50])

    ident = array('f', [0])
    e = array('f', [0])
    px = array('f', [0])
    py = array('f', [0])
    pz = array('f', [0])
    pt = array('f', [0])    

    t.Branch("nPart", n_part, "nPart/I")
    t.Branch("ID", ident, "ID/F")
    t.Branch("Px", px, "Px/F")
    t.Branch("Py", py, "Py/F")
    t.Branch("Pz", pz, "Pz/F")
    t.Branch("E", e, "E/F")
    t.Branch("Pt", pt, "Pt/F")
	
    
    for one_event in events_read_in:
	

        my_lhe_event = LHEEvent()
        my_lhe_event.fill_event(one_event)
        w = my_lhe_event.weights
	n_part[0] = int(len(my_lhe_event.particles))
	
        for i,p  in enumerate(my_lhe_event.particles):
	    if isinstance(p, dict):	#Sorting out unnecessary data
		ident[0] = p['ID']
		e[0] = p['E']   
		px[0] = p['Px']
		py[0] = p['Py']
		pz[0] = p['Pz']
		pt[0] = transverse_momentum(p)
		
		t.Fill()
	

    fout =  rt.TFile(sys.argv[2],"RECREATE") 
    t.Write()
