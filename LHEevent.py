import ROOT as rt
                     
class LHEEvent(object):
    
    def __init__(self):
        self.particles = []
        self.weights = []
        self.model = "none"

    def fill_event(self, lhe_lines):
        # check that this is a good event

        if lhe_lines[0].find("<event") == -1 or lhe_lines[-1].find("</event>") == -1:
            print "THIS IS NOT AN LHE EVENT"
            return 0

        # read the model
        for i in range(2,len(lhe_lines)-3):
            if "wgt" in lhe_lines[i]:
                
		self.weights.append(self.read_weights(lhe_lines[i]))
            else:
                self.particles.append(self.read_particle(lhe_lines[i]))

        return 1

    def read_particle(self, lhe_line):
        data_in = lhe_line[:-1].split(" ")
        data_in_good = []
        for entry in data_in:
            if entry != "": data_in_good.append(entry)
	
	
        if len(data_in_good) > 10:
	    if len(data_in_good[0])>5:	#Checking elements ID
		return

	    if len(data_in_good[2])>5:
		return

            return {'ID': int(data_in_good[0]),
                    'mIdx': int(data_in_good[2])-1,
                    'Px' : float(data_in_good[6]),
                    'Py' : float(data_in_good[7]),
                    'Pz' : float(data_in_good[8]),
                    'E' : float(data_in_good[9]),
                    'M' : float(data_in_good[10])}

	return

    def read_weights(self, lhe_line):
        data_in = lhe_line[:-1].split(" ")
        data_in_good = []

        for entry in data_in:
            if entry != "": 
		data_in_good.append(entry)

        if len(data_in_good) > 3:
            return {'WeightID': data_in_good[1][data_in_good[1].find("='")+2:data_in_good[1].find("'>")],
                    'Weight' :  float(data_in_good[2])}
            
