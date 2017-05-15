"""Making changes to the program for different plots:,

Increase number of allowed plots: Add entries in color_list, Ln 12
"""

from ROOT import *
import sys
import string


TH1.StatOverflows(True)	#Doesnt overflow

alphabet = [0]*(len(sys.argv)-1)	#Storage for opening files
color_list = [634, 418, 882, 434, 618, 402, 602, 628, 412, 876, 428, 612, 396, 596]
var_list = ["E", "Pt"]
part_num_list = [9100022, 9100000, 6, 5]
part_list = ["DM", "Med", "Top", "Bot"]
canv_list = [0]*8	#Storage of canvases
leg_list = [0]*8	#Storage of legends
hist_list = [0]*8	#Storage of histograms to be compared with
normed_list = [] 	#Storage of normed histograms
top_pad_list = [0]*8
bot_pad_list = [0]*8

leg_size = (len(sys.argv)-1)*.06

x_e_min = 0
x_e_max = 1000
x_pt_min = 0
x_pt_max = 1000
bin_width = 40
bin_e = (x_e_max-x_e_min)/bin_width
bin_pt = (x_pt_max-x_pt_min)/bin_width

line1_e = TLine(-1, 0, x_e_max, 0)
line1_e.SetLineWidth(2)
line1_pt = TLine(-1, 0, x_pt_max, 0)

if len(sys.argv)-1 > len(color_list):
	sys.exit("Please use less than "+str(len(color_list)+" files. Too little colors assigned(-> Color_list)"))

def make_plot(counter, num, tree, information):
	top_pad_list[i].cd()
	if num % 2 == 0:
		varia = var_list[0]
	else:
		varia = var_list[1]

	part = part_num_list[num/2]

	hist_name = "histo_"+str(num)+"_"+str(counter-1)  #canvas-nr_file-nr

	if counter == 1:	
		leg_list[num] = TLegend(.7, .85-leg_size, .83, .88)
		leg_list[num].SetTextSize(0.03)
		
		tree.Draw(varia+">>"+hist_name+"("+str(bin_e)+","+str(x_e_min)+","+str(x_e_max)+")", "PdgID=="+str(part), "Enorm")	
		tree.Draw(varia, "PdgID=="+str(part), "normsame")
		gPad.SetLogy()

		htemp1 = gPad.GetPrimitive(hist_name)
		if num % 2 == 0:
			htemp1.GetXaxis().SetTitle("Energy (GeV)")
		else:
			htemp1.GetXaxis().SetTitle("Momentum (GeV)")
		
		htemp1.GetYaxis().SetTitle("Normalized events / 40 GeV")

		hist_list[num] = gDirectory.Get(hist_name)
		gPad.Update()
		del htemp1

	else:	
		tree.Draw(varia+">>"+hist_name, "PdgID=="+str(part), "Enormsame")
		tree.Draw(varia, "PdgID=="+str(part), "normsame")
		htemp2 = gPad.GetPrimitive(hist_name)
		
		line1_e.Draw("same")

		bot_pad_list[num].cd()
		normed_list.append(htemp2.Clone())
		normed_list[-1].Divide(hist_list[num])
		del htemp2

		if counter == 2:
			normed_list[num].Draw()
			normed_list[num].Draw("histsame")
			normed_list[num].GetYaxis().SetRangeUser(.5, 1.5)
			normed_list[num].GetXaxis().SetTitle("Test")
			normed_list[num].GetYaxis().SetTitle("Ratio")
		else:
			normed_list[(counter-2)*8+num].Draw("same")
			normed_list[(counter-2)*8+num].Draw("histsame")

	top_pad_list[num].cd()
	m_chi = " Mchi "+str(int(information.MChi))
	m_phi = " Mdm "+str(int(information.MPhi))
	g_dm = "GDM "+str(int(information.Gdm))
	g_q = "GQ "+str(round(information.Gq*10)/10.) #Issue with root float storage.
	g_both = " g"+str(round(information.Gdm*10)/10.)

	leg_list[num].SetHeader("Model: #splitline{"+m_chi+"}{"+m_phi+"}")

	if information.Gdm == information.Gq:
		leg_list[num].AddEntry(tree, g_both, "l")
	else: 
		leg_list[num].AddEntry(tree, g_both, "l")

	if counter == len(sys.argv)-1:
		leg_list[num].SetBorderSize(0)
		leg_list[num].Draw()

"""Creating canvases and setting Statbox and Title to 0"""
for i in range(1, len(canv_list)+1):
	canv_list[i-1] = TCanvas("canvas"+str(i), "Histplots", 800, 600)
	canv_list[i-1].cd()
	top_pad_list[i-1] = TPad("upperPad"+str(i), "Test", .005, .2625, .995, .995)
	top_pad_list[i-1].Draw()
	bot_pad_list[i-1] = TPad("lowerPad"+str(i), "Test", .005, .005, .995, .2575)
	bot_pad_list[i-1].Draw()
	

gStyle.SetOptStat(0)	#hide statbox
gStyle.SetOptTitle(0)

for count in range(1,len(sys.argv)):
	alphabet[count-1] = TFile(sys.argv[count]) 

	nEntries = information.GetEntries()	#Getting information for legend entries
	entry = information.GetEntry(0)

	events.SetLineColor(color_list[count])

	for i in range(0, len(canv_list)):
		make_plot(count, i, events, information)
	
	del events
	del information

"""Printing all the different canvases to pdf"""

for i in range(0, 8):
	part_check = i/2
	if i % 2 == 0:
		vari = 0
	else:
		vari = 1
	canv_list[i].Print(part_list[part_check]+"_"+var_list[vari]+"_Normed.pdf")
