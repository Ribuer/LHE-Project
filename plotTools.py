import ROOT as rt
import math

def invariant_mass_sq(p1, p2):
    v1 = rt.TLorentzVector(p1['Px'], p1['Py'], p1['Pz'], p1['E'])
    v2 = rt.TLorentzVector(p2['Px'], p2['Py'], p2['Pz'], p2['E'])
    return (v1+v2).Mag2()

def transverse_momentum(p1):
    v1 = rt.TLorentzVector(p1['Px'], p1['Py'], p1['Pz'], p1['E'])
    
    if v1.X() == 0 and v1.Y() == 0:
	return 0

    return v1.P()*math.sin(v1.Eta())
