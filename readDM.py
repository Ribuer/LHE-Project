from LHEevent import LHEEvent
from LHEfile import LHEFile
from array import array
from plotTools import transverse_momentum

import sys
import ROOT as rt
import math as mt

if __name__ == '__main__':
	# find events in file
	my_lhe_file = LHEFile(sys.argv[1])
	my_lhe_file.set_max(10000)

	events_read_in = my_lhe_file.read_events()
	t = rt.TTree('events', 'tree with events from LHE file' )
	f = rt.TTree('information', 'tree with information about MChi, MPhi, gdm, gq')

	file_name = str(sys.argv[1]).lower()
	m_phi = array('f', [float(file_name[file_name.find("mphi")+4:].split("_")[0])])
	m_chi = array('f', [float(file_name[file_name.find("mchi")+4:].split("_")[0])])

	try:
		g_dm = array('f', [float(file_name[file_name.find("gdm")+3:].split("_")[0])])
	except ValueError:
		check = file_name[-12:]	#Excluding the naming at the beginning of the file
		g_dm = array('f', [float((check[check.find("g")+1:].split(".")[0]).replace("p", "."))])
		g_q = array('f', [float((check[check.find("g")+1:].split(".")[0]).replace("p", "."))])

	try:
		g_q = array('f', [float((file_name[file_name.find("gq")+2:].split(".")[0]).replace("p", "."))])
	except ValueError:
		pass

	f.Branch("MChi", m_chi, "MChi/F")
	f.Branch("MPhi", m_phi, "MPhi/F")
	f.Branch("Gdm", g_dm, "Gdm/F")
	f.Branch("Gq", g_q, "Gq/F")
	f.Fill()

	nPart =  array('i', [50])
	PdgID = array('i',nPart[0]*[0])
	mIdx = array('i',nPart[0]*[0])
	E = array('f',nPart[0]*[0])
	Px = array('f',nPart[0]*[0])
	Py = array('f',nPart[0]*[0])
	Pz = array('f',nPart[0]*[0])
	Pt = array('f',nPart[0]*[0])
	M = array('f',nPart[0]*[0])
	Eta = array('f',nPart[0]*[0])
	Phi = array('f',nPart[0]*[0])

	t.Branch("nPart",nPart,"nPart/I")
	t.Branch("PdgID",PdgID,"PdgID[nPart]/I")
	t.Branch("mIdx",mIdx,"mIdx[nPart]/I")
	t.Branch("E",E,"E[nPart]/F")
	t.Branch("Px",Px,"Px[nPart]/F")
	t.Branch("Py",Py,"Py[nPart]/F")
	t.Branch("Pz",Pz,"Pz[nPart]/F")
	t.Branch("Pt",Pt,"Pt[nPart]/F")
	t.Branch("M",Pt,"M[nPart]/F")
	t.Branch("Eta",Eta,"Eta[nPart]/F")
	t.Branch("Phi",Phi,"Phi[nPart]/F")
	    
	for one_event in events_read_in:
        	my_lhe_event = LHEEvent()
		my_lhe_event.fill_event(one_event)
		w = my_lhe_event.weights
		nPart[0] = int(len(my_lhe_event.particles))
		dm_list = []
	
		for i,p  in enumerate(my_lhe_event.particles):
			if isinstance(p, dict):	#Sorting out unnecessary data
				vect = rt.TLorentzVector(0,0,0,0)
				PdgID[i] = p['PdgID']
				mIdx[i] = p['mIdx']
				E[i] = p['E']
				Px[i] = p['Px']
				Py[i] = p['Py']
				Pz[i] = p['Pz']
				vect.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])

				Pt[i] = vect.Pt()
				M[i] = vect.M()	 
				Eta[i] = -999
				Phi[i] = -999

				if vect.Pt() > 0:
					Eta[i] = vect.Eta()
					Phi[i] = vect.Phi()
				if abs(p['PdgID']) == 9100022:
					dm_list.append(vect)
				del vect
				count = i
	
		k = dm_list[0]+dm_list[1]
		mIdx[count+1] = 10000
		Px[count+1] = k.Px()
		Py[count+1] = k.Py()
		Pz[count+1] = k.Pz()
		Pt[count+1] = k.Pt()
		t.Fill()

	fout =  rt.TFile(sys.argv[2],"RECREATE") 
	t.Write()
	f.Write()
