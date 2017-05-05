"""Making changes to the program for different plots:,

Increase number of allowed plots: Add entries in color_list, Ln 12
"""

from ROOT import *
import sys
import string

#TH1.SetDefaultSumw2(True)

alphabet = [0]*(len(sys.argv)-1)	#Storage for opening files
color_list = [634, 418, 882, 434, 618, 402, 602, 628, 412, 876, 428, 612, 396, 596]
var_list = ["E", "Pt"]
part_num_list = [9100022, 9100000, 6, 5]
part_list = ["DM", "Med", "Top", "Bot"]
canv_list = [0]*8	#Storage of canvases
leg_list = [0]*8	#Storage of legends
hist_list = [0]*8	#Storage of histograms to be compared with
dm_e_list = [0]*(len(sys.argv)-2)	#Storage of normed histograms

leg_size = (len(sys.argv)-1)*.07

x_e_min = 0
x_e_max = 3000
x_pt_min = 0
x_pt_max = 850
y_min = 10e-6
y_max = 5

if len(sys.argv)-1 > len(color_list):
	sys.exit("Please use less than "+str(len(color_list)+" files. Too little colors assigned(-> Color_list)"))


def make_plot(counter, num, tree, information):
	if num % 2 == 0:
		varia = var_list[0]
	else:
		varia = var_list[1]

	part = part_num_list[num/2]

	hist_name = "histo_"+str(num)+"_"+str(counter-1)  #canvas-nr_file-nr

	if counter == 1:	
		leg_list[num] = TLegend(.6, .85-leg_size, 0.85, 0.88)
		leg_list[num].SetTextSize(0.03)
		tree.Draw(varia+">>"+hist_name, "PdgID=="+str(part), "norm")			
		gPad.SetLogy()
		htemp1 = gPad.GetPrimitive(hist_name)
		if num % 2 == 0:
			htemp1.GetXaxis().SetTitle("Energy [GeV]")
			htemp1.GetXaxis().SetRangeUser(x_e_min, x_e_max)
			htemp1.GetYaxis().SetRangeUser(y_min, y_max)
		else:
			htemp1.GetXaxis().SetTitle("Momentum [GeV]")
			htemp1.GetXaxis().SetRangeUser(x_pt_min, x_pt_max)
			htemp1.GetYaxis().SetRangeUser(y_min, y_max)
		hist_list[num] = htemp1
		gPad.Update()
		del htemp1
	else:	
		tree.Draw(varia+">>"+hist_name, "PdgID=="+str(part), "normsame")
		if num == 0:
			htemp2 = gPad.GetPrimitive(hist_name)
			dm_e_list[counter-2] = htemp2.Clone()

			dm_e_list[counter-2].Divide(hist_list[num])
			dm_e_list[counter-2].Draw("same")

	m_chi = "Chi: "+str(int(information.MChi))
	m_phi = " Phi: "+str(int(information.MPhi))
	g_dm = "GDM: "+str(int(information.Gdm))
	g_q = "GQ: "+str(round(information.Gq*10)/10.) #Issue with root float storage.

	if information.Gdm == 0 and information.Gq == 0:
		leg_list[num].AddEntry(tree, "#splitline{"+m_chi+m_phi+"}", "l")
	elif information.Gdm == 0:
		leg_list[num].AddEntry(tree, "#splitline{"+m_chi+m_phi+"}{"+g_q+"}", "l")
	elif information.Gq == 0:
		leg_list[num].AddEntry(tree, "#splitline{"+m_chi+m_phi+"}{"+g_dm+"}", "l")
	else: 
		leg_list[num].AddEntry(tree, "#splitline{"+m_chi+m_phi+"}{"+g_dm+g_q+"}", "l")

	if counter == len(sys.argv)-1:
		leg_list[num].Draw()

"""Creating canvases and setting Statbox and Title to 0"""

for i in range(1, 9):
	canv_list[i-1] = TCanvas("canvas"+str(i), "Histplots", 800, 600)

gStyle.SetOptStat(0)	#hide statbox
gStyle.SetOptTitle(0)

for count in range(1,len(sys.argv)):
	alphabet[count-1] = TFile(sys.argv[count]) 

	nEntries = information.GetEntries()	#Getting information for legend entries
	entry = information.GetEntry(0)

	events.SetLineColor(color_list[count])

	for i in range(0, len(canv_list)):
		canv_list[i].cd()
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



