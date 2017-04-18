from ROOT import *
import sys
import string

alphabet = [0]*(len(sys.argv)-1)
color_list = [600, 632, 416, 880, 432, 800, 400]
str_list = ["dm","med", "top", "bot"]

hist_dict = {}

def scale_hist(hist_name):
	scale = hist_name.Integral()
	hist_name.Scale(100./scale)

def draw_print_hists(dictionary):
	for k in str_list:
		for i in range(1,len(dictionary)/8+1):	
			scale_hist(dictionary[str(i)+"_"+k+"_e"])
			scale_hist(dictionary[str(i)+"_"+k+"_pt"])

		for l in ["e", "pt"]:
			c1 = TCanvas("canvas1", "Histplots", 800, 600)
			legend = TLegend(.7, .7, 0.85, 0.85)

			for i in range(1,len(dictionary)/8+1):	
				if i == 1:
					dictionary[str(i)+"_"+k+"_"+l].Draw()
				else: 
					dictionary[str(i)+"_"+k+"_"+l].Draw("same")
				
				legend.AddEntry(dictionary[str(i)+"_"+k+"_"+l], "File "+str(i), "l")				
			legend.Draw()
			c1.Print(k.upper()+" "+l.upper()+" Normed.pdf")
			c1.Close()
			del legend	
    
    
def make_hists(counter):
	"""Setting boundaries, number of bins and hist colors."""

	x_e_min = 0
	x_e_max = 1400
	e_bins = (x_e_max - x_e_min)/40	#each bin containing 40Gev

	dm_e_hist = TH1F("hist1_"+str(counter), "Dark Matter ; Energy [GeV] ; Number of entries in %", e_bins, x_e_min, x_e_max)
	med_e_hist = TH1F("hist2_"+str(counter), "Mediator ; Energy [GeV] ; Number of entries in %", e_bins, x_e_min, x_e_max)
	top_e_hist = TH1F("hist3_"+str(counter), "T Quark ; Energy [GeV] ; Number of entries in %", e_bins, x_e_min, x_e_max)	
	bot_e_hist = TH1F("hist4_"+str(counter), "B Quark ; Energy [GeV] ; Number of entries in %", e_bins, x_e_min, x_e_max)	


	x_pt_min = -1550
	x_pt_max = 850
	pt_bins = (x_pt_max - x_pt_min)/40

	dm_pt_hist = TH1F("hist5_"+str(counter), "Dark Matter ; Momentum [GeV] ; Number of entries in %", pt_bins, x_pt_min, x_pt_max)
	med_pt_hist = TH1F("hist6_"+str(counter), "Mediator ; Momentum [GeV] ; Number of entries in %", pt_bins, x_pt_min, x_pt_max)
	top_pt_hist = TH1F("hist7_"+str(counter), "T Quark ; Momentum [GeV] ; Number of entries in %", pt_bins, x_pt_min, x_pt_max)
	bot_pt_hist = TH1F("hist8_"+str(counter), "B Quark ; Momentum [GeV] ; Number of entries in %", pt_bins, x_pt_min, x_pt_max)

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

	return dm_e_hist, dm_pt_hist, med_e_hist, med_pt_hist, top_e_hist, top_pt_hist, bot_e_hist, bot_pt_hist


def set_color(hist_dictionary, arg_length):
	for i in range(1, arg_length):
		for k in str_list:
			hist_dict[str(i)+"_"+k+"_e"].SetLineColor(color_list[i-1])
			hist_dict[str(i)+"_"+k+"_pt"].SetLineColor(color_list[i-1])
		


if len(sys.argv)-1 > len(color_list):
	sys.exit("Please use less than "+str(len(color_list)+" files. Too little colors assigned(-> Color_list)"))

for count in range(1,len(sys.argv)):
	alphabet[count-1] = TFile(sys.argv[count]) 
	gStyle.SetOptStat(0)	#hide statbox
	
	hist_dict[str(count)+'_dm_e'], hist_dict[str(count)+'_dm_pt'], hist_dict[str(count)+'_med_e'], hist_dict[str(count)+'_med_pt'], hist_dict[str(count)+'_top_e'], hist_dict[str(count)+'_top_pt'], hist_dict[str(count)+'_bot_e'], hist_dict[str(count)+'_bot_pt'] = make_hists(count)

	del events
	
set_color(hist_dict, len(sys.argv))
draw_print_hists(hist_dict)



