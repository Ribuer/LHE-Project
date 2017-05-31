"""Making changes to the program for different plots:,

Increase number of allowed plots: Add entries in color_list, Ln 12
"""

from ROOT import *
import sys
import string
import math as mt
from array import array

save_file_as = ".pdf"


alphabet = [0]*(len(sys.argv)-1)	#Storage for opening files
color_list = [633, 434, 419, 877, 618, 402, 602, 628, 414, 882, 428, 612, 396, 596]
var_list = ["E", "Pt"]
part_num_list = [9100022, 9100000, 6, 5, 10000]		#Last entrance in the following 3 lists is for DM1+DM2 comparing reasons and has a single own plot
part_list = ["DM", "Med", "Top", "Bot", "DM_Comp"]	#Naming pdfs
part_xtitle_list = ["Dark Matter", "Mediator", "Top Quark", "Bottom Quark", "Dark Matter 1+2"]	#Naming x axis

test = ((2*len(part_list))-1)

canv_list = [0]*test	#Storage of canvases
leg_list = [0]*test	#Storage of legends
hist_list = [0]*test	#Storage of histograms to be compared with
normed_list = [] 	#Storage of normed histograms
top_pad_list = [0]*test	#Storage of upper pads
bot_pad_list = [0]*test	#Storage of lower pads
line_list = [0]*test	#Storage of line at y = 1 in lower pad
bin_list_e = array('f', {0})
bin_list_pt = array('f', {0})

info_list = []

leg_size = (len(sys.argv)-1)*.06

x_e_min = 0
x_e_max = 720
x_pt_min = 0
x_pt_max = 720
bin_width = 40
bin_e = (x_e_max-x_e_min)/bin_width
bin_pt = (x_pt_max-x_pt_min)/bin_width

for i in range(1, int(bin_e)+1):		# The following lines are built to set different bin sizes later on
	bin_list_e.append(i*bin_width)

if x_e_max % bin_width != 0:
	bin_list_e.append(x_e_max)

for i in range(1, int(bin_pt)+1):
	bin_list_pt.append(i*bin_width)

if x_pt_max % bin_width != 0:
	bin_list_pt.append(x_pt_max)

set_title_font = 63
set_label_font = set_title_font-20
set_size = 18

if len(sys.argv)-1 > len(color_list):
	sys.exit("Please use less than "+str(len(color_list)+" files. Too little colors assigned(-> Color_list)"))

def make_plot(counter, num, tree, information):
	top_pad_list[i].cd()
	if num % 2 == 0:
		varia = var_list[0]
	else:
		varia = var_list[1]

	if num == len(canv_list)-1:		#Naming DM1+DM2 Plot
		varia = var_list[1]
	
	if varia == var_list[0]:		#Set which set to take for histogram(e or pt)
		max_bin = len(bin_list_e)-1	#For setting different bin sizes
		x_min = x_e_min
		x_max = x_e_max
		bin_list = bin_list_e
	else:	
		max_bin = len(bin_list_pt)-1
		x_min = x_pt_min
		x_max = x_pt_max
		bin_list = bin_list_pt

	part = part_num_list[num/2]

	hist_name = "histo_"+str(num)+"_"+str(counter-1)  #canvas-nr_file-nr

	if counter == 1:	
		leg_list[num] = TLegend(.65, .82-leg_size, .78, .85)
		leg_list[num].SetTextSize(0.04)
		
		tree.SetLineWidth(3)	

		#tree.Draw(varia+">>"+hist_name+"("+str(max_bin)+","+str(bin_list)+")", "PdgID=="+str(part), "Enorm")	
		tree.Draw(varia+">>"+hist_name+"("+str(max_bin)+","+str(x_min)+","+str(x_max)+")", "PdgID=="+str(part), "Enorm")	
		gPad.SetLogy()

		htemp1 = gPad.GetPrimitive(hist_name)	
		htemp1.GetYaxis().SetTitle("Normalized events / 40 GeV")
		htemp1.GetXaxis().SetLabelSize(set_size)
		
		htemp1.GetYaxis().SetLabelFont(set_label_font)
		htemp1.GetYaxis().SetLabelSize(set_size)
		htemp1.GetYaxis().SetTitleFont(set_title_font)
		htemp1.GetYaxis().SetTitleSize(set_size)
		htemp1.GetYaxis().SetTitleOffset(1.3)

		htemp1.SetBinContent(max_bin, htemp1.GetBinContent(max_bin+1)+htemp1.GetBinContent(max_bin))
		htemp1.SetBinError(max_bin, mt.sqrt(htemp1.GetBinError(max_bin+1)**2+htemp1.GetBinError(max_bin)**2))

		try:		#Checking if there is data. To avoid ZeroDivisionError
			htemp1.Scale(1./htemp1.Integral())
		except ZeroDivisionError:
			print "Could not Scale "+sys.argv[counter]+" for "+part_xtitle_list[num/2]+" "+varia+" because there is no data."

		htemp1.Draw("histnormsame")
		hist_list[num] = gDirectory.Get(hist_name)
		gPad.Update()
		del htemp1

	else:	
		tree.SetLineWidth(2)
		tree.SetLineStyle(2)

		tree.Draw(varia+">>"+hist_name, "PdgID=="+str(part), "Enormsame")
		htemp2 = gPad.GetPrimitive(hist_name)
		htemp2.SetBinContent(max_bin,  htemp2.GetBinContent(max_bin+1)+htemp2.GetBinContent(max_bin))
		htemp2.SetBinError(max_bin,  mt.sqrt(htemp2.GetBinError(max_bin+1)**2+htemp2.GetBinError(max_bin)**2))
		htemp2.Draw("histnormsame")

		try:		#Checking if there is data. To avoid ZeroDivisionError
			htemp2.Scale(1./htemp2.Integral())
		except ZeroDivisionError:
			print "Could not Scale "+sys.argv[counter]+" for "+part_xtitle_list[num/2]+" "+varia+" because there is no data."

		bot_pad_list[num].cd()
		normed_list.append(htemp2.Clone())
		normed_list[-1].Divide(hist_list[num])
		del htemp2

		if counter == 2:			
			normed_list[num].Draw()
			normed_list[num].Draw("histsame")
			normed_list[num].GetYaxis().SetRangeUser(.5, 1.5)
			if num == len(canv_list)-1:
				normed_list[num].GetXaxis().SetTitle(part_xtitle_list[num/2]+" p_{T} (GeV)")
			elif num % 2 == 0:
				normed_list[num].GetXaxis().SetTitle(part_xtitle_list[num/2]+" Energy (GeV)")
			else:
				normed_list[num].GetXaxis().SetTitle(part_xtitle_list[num/2]+" p_{T} (GeV)")

			normed_list[num].GetYaxis().SetTitle("g = x / g = 1")

			normed_list[num].GetXaxis().SetTitleFont(set_title_font)	#Set and make the title/label size/font equal
			normed_list[num].GetXaxis().SetTitleSize(set_size)
			normed_list[num].GetYaxis().SetTitleFont(set_title_font)
			normed_list[num].GetYaxis().SetTitleSize(set_size)
			normed_list[num].GetXaxis().SetLabelFont(set_label_font)
			normed_list[num].GetXaxis().SetLabelSize(set_size)
			normed_list[num].GetYaxis().SetLabelFont(set_label_font)
			normed_list[num].GetYaxis().SetLabelSize(set_size)

			normed_list[num].GetYaxis().SetNdivisions(503)		#Set Y axis divisions
			normed_list[num].GetXaxis().SetTitleOffset(4)		#Offset X title to bottom(not covered by label anymore)
			normed_list[num].GetYaxis().SetTitleOffset(1.3)		#Offset Y title to left
			normed_list[num].GetYaxis().SetLabelOffset(.01)
			gPad.SetBottomMargin(0.3)				#Set Margin for y title	
				
		else:
			normed_list[(counter-2)*test+num].Draw("same")						
			normed_list[(counter-2)*test+num].Draw("histsame")

		if counter == len(sys.argv)-1:
			if num % 2 == 0:
				line_list[num] = TLine(x_e_min, 1, x_e_max, 1)
			else: 
				line_list[num] = TLine(x_pt_min, 1, x_pt_max, 1)
			line_list[num].SetLineWidth(2)
			line_list[num].SetLineColor(kGray+2)
			line_list[num].Draw("same")

	top_pad_list[num].cd()
	m_chi = " Mchi "+str(int(information.MChi))
	m_phi = " Mdm "+str(int(information.MPhi))
	g_dm = "GDM "+str(int(information.Gdm))
	g_q = "GQ "+str(round(information.Gq*10)/10.) #Issue with root float storage.
	g_both = " g"+str(round(information.Gdm*10)/10.)

	leg_list[num].SetHeader(" Model: #splitline{"+m_chi+" GeV}{"+m_phi+" Gev}")

	if information.Gdm == information.Gq:
		leg_list[num].AddEntry(tree, g_both, "l")
	else: 
		leg_list[num].AddEntry(tree, g_both, "l")

	if counter == len(sys.argv)-1:
		leg_list[num].SetBorderSize(0)
		leg_list[num].Draw()
		if num == len(canv_list)-1:
			info_list.append(m_chi)
			info_list.append(m_phi)
			info_list.append(g_dm)
			info_list.append(g_q)	

low_pad_up_tresh = .3025

"""Creating canvases and setting Statbox and Title to 0"""
for i in range(1, len(canv_list)+1):
	canv_list[i-1] = TCanvas("canvas"+str(i), "Histplots", 800, 600)
	canv_list[i-1].cd()
	top_pad_list[i-1] = TPad("upperPad"+str(i), "Test", .005, low_pad_up_tresh-.07, .995, .995)
	top_pad_list[i-1].Draw()
	bot_pad_list[i-1] = TPad("lowerPad"+str(i), "Test", .005, .005, .995, low_pad_up_tresh)
	bot_pad_list[i-1].Draw()

gStyle.SetOptStat(0)	#hide statbox
gStyle.SetOptTitle(0)

for count in range(1,len(sys.argv)):
	alphabet[count-1] = TFile(sys.argv[count]) 

	nEntries = information.GetEntries()	#Getting information for legend entries
	entry = information.GetEntry(0)

	events.SetLineColor(color_list[count-1])
	for i in range(0, len(canv_list)):
		make_plot(count, i, events, information)
	del events
	del information

"""Printing all the different canvases to pdf"""
for i in range(0, len(canv_list)-1):
	part_check = i/2
	if i % 2 == 0:
		vari = 0
	else:
		vari = 1

	canv_list[i].Print(sys.argv[1].split("_")[0]+"_"+info_list[1][5:]+"_"+info_list[0][6:]+"_"+part_list[part_check]+"_"+var_list[vari]+"_Normed"+save_file_as)

canv_list[-1].Print(sys.argv[1].split("_")[0]+"_"+info_list[1][5:]+"_"+info_list[0][6:]+"_"+part_list[-1]+"_Pt_Normed"+save_file_as)
