from ROOT import *
import sys



f = TFile(sys.argv[1]);

c1 = TCanvas("canvas1", "Energy", 800, 600)
events_dm = events.Clone()
events_med = events.Clone()

events_med.SetLineColor(kRed)
events_dm.SetLineColor(kBlue)

events_dm.Draw("E", "ID==18")
events_med.Draw("E", "ID==55", "same")
htemp.SetTitle("Energy Distribution of DM and Mediator ; Energy ; Number of entries")

legend = TLegend(0.6, 0.7, 0.75, 0.85)
legend.AddEntry(events_med, "Mediator", "l")
legend.AddEntry(events_dm, "DM", "l")
legend.Draw()

c1.Print("DM_Mediator Energy.pdf")


del htemp #Deleting htemp for setting new title

c2 = TCanvas("canvas2", "Transverse Momentum", 800, 600)

events_dm.Draw("Pt", "ID==18")
events_med.Draw("Pt", "ID==55", "same")
htemp.SetTitle("Transverse Momentum of DM and Mediator ; Pt ; Number of entries")

legend = TLegend(.15, 0.7, 0.3, 0.85)
legend.AddEntry(events_med, "Mediator", "l")
legend.AddEntry(events_dm, "DM", "l")
legend.Draw()

c2.Print("DM_Mediator Transverse Momentum.pdf")


