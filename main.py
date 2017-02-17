#!/usr/bin/env python

"""
main.py:
Module to start the Graphical User Interface and perform V-REP snake simulation in parallel.
"""

__author__      = "Rotem Mordoch"


import vrep
import math
import time
import sys
import GUI
from threading import Thread


global gui_thread


def init_gui():
    """
    Initialize GUI
    """
    global app
    root = GUI.init_gui_aux()
    app = GUI.Application(root)
    root.mainloop()


class Simulation():
    """
    V-REP simulation class
    """
    def __init__(self):
        self.client_id = -1
        self.snake_joint_v_handle = []
        self.snake_joint_h_handle = []
        self.number_of_joints = 8

    def init_simulation(self):
        """
        Initialize simulation parameters
        """
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.client_id = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # connect to vrep
        if self.client_id != -1:
            print ('Connected to remote API server')
        else:
            print ('Connection to remote API server failed.\n'
                    'Make sure the simulation in V-REP has been started before running the program.')
            sys.exit('Error: could not connect')
        # fetch simulation joint objects
        for i in xrange(self.number_of_joints / 2):
            return_code, snake_joint_h = vrep.simxGetObjectHandle(self.client_id,
                                                                  'snake_joint_h' + str(i + 1),
                                                                  vrep.simx_opmode_blocking)
            return_code, snake_joint_v = vrep.simxGetObjectHandle(self.client_id,
                                                                  'snake_joint_v' + str(i + 1),
                                                                  vrep.simx_opmode_blocking)
            self.snake_joint_h_handle += [snake_joint_h]
            self.snake_joint_v_handle += [snake_joint_v]

    def perform_simulation(self):
        """
        Simulate gaits by updating joints positions
        """
        t = 0  # simulation time step
        prev_time = time.time()
        # simulate as long as the GUI is running
        while gui_thread.isAlive():
           if app.is_valid():
               speed = app.get_speed_scalar()
               F = [int(round(x * speed)) for x in app.get_sim_frequency()]  # update frequency according to speed scalar
               coef = math.pi / 180  # degree to radian coefficient
               # fetch current parameters from GUI
               A_V = list(app.get_sim_amplitude_v())
               A_H = list(app.get_sim_amplitude_h())
               P_V = list(app.get_sim_phase_v())
               P_H = list(app.get_sim_phase_h())
               # apply conversion on parameters
               A_V = [item * coef for item in A_V]
               A_H = [item * coef for item in A_H]
               P_V = [item * coef for item in P_V]
               P_H = [item * coef for item in P_H]
               # update time step
               t += time.time() - prev_time
               prev_time = time.time()
               # compute new joints positions
               for i in xrange(self.number_of_joints / 2):
                   return_code = vrep.simxSetJointTargetPosition(self.client_id,
                                                                 self.snake_joint_v_handle[i],
                                                                 A_V[i] * math.sin(t * F[i] + i * P_V[i]),
                                                                 vrep.simx_opmode_streaming)
                   return_code = vrep.simxSetJointTargetPosition(self.client_id,
                                                                 self.snake_joint_h_handle[i],
                                                                 A_H[i] * math.cos(t * F[i] + i * P_H[i]),
                                                                 vrep.simx_opmode_streaming)


if __name__ == '__main__':
    gui_thread = Thread(target=init_gui, args=())  # initialize GUI thread
    gui_thread.setDaemon(True)  # set daemon = True, to terminate GUI thread when main thread dies
    gui_thread.start()
    sim = Simulation()
    sim.init_simulation()
    sim.perform_simulation()
