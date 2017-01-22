from Tkinter import *


class Application(Frame):
    """ GUI class """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.frequency = 0
        self.amplitude_h = 0
        self.amplitude_v = 0
        self.phase_v = 0
        self.phase_h = 0

    def create_widgets(self):
        self.instruction1 = Label(self,
                                  text="Please enter values before choosing a gait:")
        self.instruction1.pack(anchor=N)

        self.freq_label = Label(self, text="Frequency:")
        self.freq_label.pack(anchor=N)

        self.freq = Entry(self)
        self.freq.pack(anchor=N)

        self.amp_label = Label(self, text="Amplitude:")
        self.amp_label.pack(anchor=N)

        self.amp = Entry(self)
        self.amp.pack(anchor=N)

        self.space1 = Label(self, text='')
        self.space1.pack(anchor=CENTER)

        self.instruction2 = Label(self, text="Please choose the desired gait:")
        self.instruction2.pack(anchor=CENTER)

        self.button1 = Button(self, text="Rolling", command=self.rolling)
        self.button1.config(height=2, width=5)
        self.button1.pack(anchor=CENTER)

        self.button2 = Button(self, text="Forward", command=self.forward)
        self.button2.config(height=2, width=5)
        self.button2.pack(anchor=CENTER)

        self.button3 = Button(self, text="Reset", command=self.reset)
        self.button3.config(height=2, width=5)
        self.button3.pack(anchor=CENTER)

        self.button4 = Button(self, text="Hold", command=self.hold)
        self.button4.config(height=2, width=5)
        self.button4.pack(anchor=CENTER)

        self.space2 = Label(self, text='')
        self.space2.pack(anchor=S)

        labelText = ''
        self.instruction3 = Label(self, text=labelText)
        self.instruction3.pack(anchor=S)

    # callbacks
    def rolling(self):
        self.frequency = int(self.freq.get())
        self.amplitude_h = int(self.amp.get())
        self.amplitude_v = int(self.amp.get())
        self.phase_v = 0
        self.phase_h = 0
        self.instruction3.config(text='Rolling')

    def forward(self):
        self.frequency = int(self.freq.get())
        self.amplitude_h = 0
        self.amplitude_v = int(self.amp.get())
        self.phase_v = 120
        self.phase_h = 60
        self.instruction3.config(text='Moving Forward')

    def reset(self):
        self.frequency = 0
        self.amplitude_h = 0
        self.amplitude_v = 0
        self.phase_v = 0
        self.phase_h = 0

        self.instruction3.config(text='Resetted')

    def hold(self):
        self.frequency = 0
        self.instruction3.config(text='Paused')

        ##def rotating(self):
        ##def lateral_shifting(self):
        ##def turning(self):

def gui_thread_aux():
    root = Tk()
    root.title("Snake Robot GUI")
    root.geometry("400x333")
    root.resizable(width=False, height=False)
    return root