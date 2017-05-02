"""Making changes to the program for different plots:,

Increase number of allowed plots: Add entries in color_list, Ln 12
"""

from ROOT import *
import sys
import string

alphabet = [0]*(len(sys.argv)-1)
color_list = [634, 418, 882, 434, 618, 402, 602, 628, 412, 876, 428, 612, 396, 596]
leg_list = [0]*8
var_list = ["E", "Pt"]
part_num_list = [18, 55, 6, 5]
part_list = ["DM", "Med", "Top", "Bot"]
canv_list = [0]*8

leg_size = (len(sys.argv)-1)*.07

x_e_min = 0
x_e_max = 1400
x_pt_min = 0
x_pt_max = 850

if len(sys.argv)-1 > len(color_list):
	sys.exit("Please use less than "+str(len(color_list)+" files. Too little colors assigned(-> Color_list)"))


def make_plot(counter, num, histo, information):
	if num % 2 == 0:
		varia = var_list[0]
	else:
		varia = var_list[1]

	part = part_num_list[num/2]

	if counter == 1:	
		leg_list[num] = TLegend(.6, .85-leg_size, 0.85, 0.88)
		leg_list[num].SetTextSize(0.03)
		histo.Draw(varia, "PdgID=="+str(part), "norm")			
		gPad.SetLogy()
		htemp1 = gPad.GetPrimitive("htemp")
		if num % 2 == 0:
			htemp1.GetXaxis().SetTitle("Energy [GeV]")
			htemp1.GetXaxis().SetRangeUser(x_e_min, x_e_max)
		else:
			htemp1.GetXaxis().SetTitle("Momentum [GeV]")
			htemp1.GetXaxis().SetRangeUser(x_pt_min, x_pt_max)
		gPad.Update()
		del htemp1
	else:	
		histo.Draw(varia, "PdgID=="+str(part), "normsame")
	
	leg_list[num].AddEntry(histo, "#splitline{Chi: "+str(int(information.MChi))+" Phi: "+str(int(information.MPhi))+"}{GDM: "+str(int(information.Gdm))+" GQ: "+str(information.Gq)+"}", "l")
	if counter == len(sys.argv)-1:
		leg_list[num].Draw()

for i in range(1, 9):
	canv_list[i-1] = TCanvas("canvas"+str(i), "Histplots", 800, 600)

gStyle.SetOptStat(0)	#hide statbox
gStyle.SetOptTitle(0)

for count in range(1,len(sys.argv)):
	alphabet[count-1] = TFile(sys.argv[count]) 

	#Getting information for legend entries
	nEntries = information.GetEntries()
	entry = information.GetEntry(0)

	events.SetLineColor(color_list[count])
	

	for i in range(0, len(canv_list)):
		canv_list[i].cd()
		make_plot(count, i, events, information)
	
	del events
	del information
	
for i in range(0, 8):
	part_check = i/2
	if i % 2 == 0:
		vari = 0
	else:
		vari = 1
	canv_list[i].Print(part_list[part_check]+"_"+var_list[vari]+"_Normed.pdf")
