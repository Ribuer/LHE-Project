import ROOT as rt

class LHEFile(object):
    
    def __init__(self, filename):
        self.event_list = []
        self.filename = filename
        self.max_ev = -99

    def set_max(self, max_val):
        self.max = max_val
        
    def read_events(self):
        new_event = False
        one_event = []
        
        with open(self.filename, "r") as x_file:
            lines = x_file.readlines()
        
        print 'Found %i lines in %s' %(len(lines),self.filename)      

        for line in lines:                                                                                                            
            if line[0] == '#': continue      
                                                                                          
            if new_event: 
                one_event.append(line)
                
            if line.find("</event>") != -1:
                new_event = False
                self.event_list.append(one_event)
                one_event = []

                if len(self.event_list) >= self.max and self.max > 0: break
            
            if line.find("<event") != -1:
                new_event = True
                one_event.append(line)

        return self.event_list

    
