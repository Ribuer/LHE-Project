from ROOT import *
import sys

f = TFile(sys.argv[1]);
gStyle.SetOptStat(0)	#hide statbox

"""Setting boundaries, number of bins and hist colors."""

x_e_min = 0
x_e_max = 800
e_bins = (x_e_max - x_e_min)/10	#each bin containing 10Gev

dm_e_hist = TH1F("hist1", "Energy Distribution ; GeV ; Number of entries", e_bins, x_e_min, x_e_max)
med_e_hist = TH1F("hist2", "Energy Distribution ; GeV ; Number of entries", e_bins, x_e_min, x_e_max)
top_e_hist = TH1F("hist3", "Energy Distribution ; GeV ; Number of entries", e_bins, x_e_min, x_e_max)	
bot_e_hist = TH1F("hist4", "Energy Distribution ; GeV ; Number of entries", e_bins, x_e_min, x_e_max)	


x_pt_min = -800
x_pt_max = 800
pt_bins = (x_pt_max - x_pt_min)/10

dm_pt_hist = TH1F("hist5", "Transverse Momentum Distribution ; GeV ; Number of entries", pt_bins, x_pt_min, x_pt_max)
med_pt_hist = TH1F("hist6", "Transverse Momentum Distribution ; GeV ; Number of entries", pt_bins, x_pt_min, x_pt_max)
top_pt_hist = TH1F("hist7", "Transverse Momentum Distribution ; GeV ; Number of entries", pt_bins, x_pt_min, x_pt_max)
bot_pt_hist = TH1F("hist8", "Transverse Momentum Distribution ; GeV ; Number of entries", pt_bins, x_pt_min, x_pt_max)

med_e_hist.SetLineColor(kRed)
med_pt_hist.SetLineColor(kRed)
top_e_hist.SetLineColor(kViolet)
top_pt_hist.SetLineColor(kViolet)
bot_e_hist.SetLineColor(kGreen)
bot_pt_hist.SetLineColor(kGreen)

"""Filling the histograms"""

nEntries = events.GetEntries()

for i in range(0,nEntries):
    entry = events.GetEntry(i)
    if abs(events.ID) == 18:	#18 resembles DM, abs for particles+antiparticles
	dm_e_hist.Fill(events.E)
        dm_pt_hist.Fill(events.Pt)

    if abs(events.ID) == 55:	#55 resembles mediator
	med_e_hist.Fill(events.E)
	med_pt_hist.Fill(events.Pt)

    if abs(events.ID) == 6:	#6 resembles t-quark
	top_e_hist.Fill(events.E)
	top_pt_hist.Fill(events.Pt)

    if abs(events.ID) == 5:	#5 resembles b-quark
	bot_e_hist.Fill(events.E)
	bot_pt_hist.Fill(events.Pt)

"""Drawing and saving histograms to files"""

c1 = TCanvas("canvas1", "Histplots", 800, 600)
dm_e_hist.Draw()
med_e_hist.Draw("same")
top_e_hist.Draw("same")
bot_e_hist.Draw("same")

legend = TLegend(.7, 0.7, 0.85, 0.85)
legend.AddEntry(dm_e_hist, "DM", "l")
legend.AddEntry(med_e_hist, "Mediator", "l")
legend.AddEntry(top_e_hist, "T-Quark", "l")
legend.AddEntry(bot_e_hist, "B-Quark", "l")
legend.Draw()
    
c1.Print("DM_Mediator_T_B Energy Hist.pdf")

del legend

dm_pt_hist.Draw()
med_pt_hist.Draw("same")
top_pt_hist.Draw("same")
bot_pt_hist.Draw("same")

legend = TLegend(.7, 0.7, 0.85, 0.85)
legend.AddEntry(dm_pt_hist, "DM", "l")
legend.AddEntry(med_pt_hist, "Mediator", "l")
legend.AddEntry(top_pt_hist, "T-Quark", "l")
legend.AddEntry(bot_pt_hist, "B-Quark", "l")
legend.Draw()

c1.Print("DM_Mediator_T_B Transverse Momentum Hist.pdf")
