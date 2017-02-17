#!/usr/bin/env python

"""
GUI.py:
Module to handle Graphical User Interface to control V-REP snake simulation according to an XML file of predefined gaits.
"""

__author__      = "Rotem Mordoch"


from Tkinter import *
import tkFileDialog
from xml.dom import minidom


NUM_OF_JOINTS = 8
LARGE_FONT = ("Verdana", 12)


class Application(Frame):
    """
    GUI class
    """
    def __init__(self, parent):
        """
        Initialize some GUI widgets and parameters
        """
        Frame.__init__(self, parent)
        self.pack()
        title = Label(self, text="Please select the XML file of the defined gaits parameters:", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        self.xml_button = Button(self, text="Browse...", command=self.load_xml)
        self.xml_button.config(height=2, width=10)
        self.xml_button.pack()
        self.speed_value = DoubleVar()
        self.speed_value.set(1)
        self.slider = Scale(self, orient=HORIZONTAL, length=250, from_=0.2, to=2, tickinterval=0.2, resolution=0.2,
                            variable=self.speed_value)
        self.valid = False  # boolean to check whether application is valid (xml file was loaded)
        self.gaits = []  # available gaits in xml file
        # current gaits parameters
        self.sim_frequency = [0] * NUM_OF_JOINTS
        self.sim_amplitude_v = [0] * (NUM_OF_JOINTS / 2)
        self.sim_amplitude_h = [0] * (NUM_OF_JOINTS / 2)
        self.sim_phase_v = [0] * (NUM_OF_JOINTS / 2)
        self.sim_phase_h = [0] * (NUM_OF_JOINTS / 2)

    def load_xml(self):
        """
        Load xml file and parse gaits widgets
        """
        fileName = tkFileDialog.askopenfilename(filetypes=(("XML Files", "*.xml"), ("All Files", "*")))
        self.xml_button['state'] = 'disabled'
        # parse xml file
        xml_doc = minidom.parse(fileName)
        self.gaits = xml_doc.getElementsByTagName('gait')
        if len(self.gaits) == 0:
            print 'Error: wrong XML format - no <gait> nodes. Please follow the format definition in the README file.'
            sys.exit()
        title = Label(self, text="Please select the desired gait:", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        self.create_gaits_widgets()
        self.create_const_widgets()
        self.valid = True  # application marked as valid after xml file was loaded

    def create_gaits_widgets(self):
        """
        Create gaits widgets according to xml file
        """
        for gait in self.gaits:
            gait_id = gait.getAttribute('id')
            if not gait_id:
                print 'Warning: id attribute is not defined (gait without a name). Can cause to unexpected behaviour.'
            widget = Button(self, text=gait_id, command=lambda gait_id=gait_id: self.callback(gait_id))
            widget.config(height=2, width=15)
            widget.pack()

    def create_const_widgets(self):
        """
        Create some constant widgets (not defined in xml file)
        """
        slider_title = Label(self, text="Speed")
        slider_title.pack(pady=10, padx=10)
        self.slider.pack()
        curr_gait_title = Label(self, text='Current Gait Activated:')
        curr_gait_title.pack()
        self.gait_title = Label(self, text='')
        self.gait_title.pack()

    def callback(self, gait_name):
        """
        Widgets callback
        This function is called whenever a gait widget is selected
        """
        self.parse_sim_gait_parameters(gait_name)
        self.gait_title.config(text=gait_name)

    def parse_sim_gait_parameters(self, gait_name):
        """
        Fetch corresponding gait parameters from xml file and update application parameters
        """
        for gait in self.gaits:
            gait_id = gait.getAttribute('id')
            if gait_id == gait_name:  # find which gait widget is selected
                sim_freq_elements = gait.getElementsByTagName('freq_sim')
                sim_amp_v_elements = gait.getElementsByTagName('amp_v_sim')
                sim_amp_h_elements = gait.getElementsByTagName('amp_h_sim')
                sim_phase_v_elements = gait.getElementsByTagName('phase_v_sim')
                sim_phase_h_elements = gait.getElementsByTagName('phase_h_sim')
                # gaits where all joints have the same parameters
                if (len(sim_freq_elements) == 1 and len(sim_amp_v_elements) == 1 and len(sim_amp_h_elements) == 1 and
                    len(sim_phase_v_elements) == 1 and len(sim_phase_h_elements) == 1):
                    # duplicate parameters values for all joints
                    sim_freq_elements *= NUM_OF_JOINTS
                    sim_amp_v_elements *= (NUM_OF_JOINTS / 2)
                    sim_amp_h_elements *= (NUM_OF_JOINTS / 2)
                    sim_phase_v_elements *= (NUM_OF_JOINTS / 2)
                    sim_phase_h_elements *= (NUM_OF_JOINTS / 2)
                # convert strings to integers
                if (len(sim_freq_elements) == NUM_OF_JOINTS and
                    len(sim_amp_v_elements) == NUM_OF_JOINTS / 2 and
                    len(sim_amp_h_elements) == NUM_OF_JOINTS / 2 and
                    len(sim_phase_v_elements) == NUM_OF_JOINTS / 2 and
                    len(sim_phase_h_elements) == NUM_OF_JOINTS / 2):
                    self.sim_frequency = map(lambda x: int(x.firstChild.data), sim_freq_elements)
                    self.sim_amplitude_v = map(lambda x: int(x.firstChild.data), sim_amp_v_elements)
                    self.sim_amplitude_h = map(lambda x: int(x.firstChild.data), sim_amp_h_elements)
                    self.sim_phase_v = map(lambda x: int(x.firstChild.data), sim_phase_v_elements)
                    self.sim_phase_h = map(lambda x: int(x.firstChild.data), sim_phase_h_elements)
                # handle HOLD gait separately
                elif (len(sim_freq_elements) == 1 and len(sim_amp_v_elements) == 0 and len(sim_amp_h_elements) == 0 and
                      len(sim_phase_v_elements) == 0 and len(sim_phase_h_elements) == 0):
                    sim_freq_elements *= NUM_OF_JOINTS
                    self.sim_frequency = map(lambda x: int(x.firstChild.data), sim_freq_elements)
                else:
                    print ('Error: wrong XML format - the selected gait has either too many or too less parameters.\n'
                           'Please follow the format definition in the README file.')
                    sys.exit()

    # application getters
    def is_valid(self):
        return self.valid

    def get_speed_scalar(self):
        return self.speed_value.get()

    def get_sim_frequency(self):
        return self.sim_frequency

    def get_sim_amplitude_v(self):
        return self.sim_amplitude_v

    def get_sim_amplitude_h(self):
        return self.sim_amplitude_h

    def get_sim_phase_v(self):
        return self.sim_phase_v

    def get_sim_phase_h(self):
        return self.sim_phase_h


def init_gui_aux():
    """
    Auxiliary function to initialize GUI
    """
    root = Tk()
    root.title("Snake Robot GUI")
    root.geometry("600x633")
    root.resizable(width=False, height=False)
    return root
