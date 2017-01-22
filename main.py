import vrep
import math
import time
import GUI
import thread
import sys


def gui_thread():
    global app
    root = GUI.gui_thread_aux()
    app = GUI.Application(root)
    root.mainloop()


if __name__ == '__main__':
    thread.start_new_thread(gui_thread, ())

    vrep.simxFinish(-1) # just in case, close all opened connections
    client_id = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # Connect to V-REP
    if client_id != -1:
        print 'Connected to remote API server'
    else:
        print 'Connection failed'
        sys.exit('Could not connect')

    snake_joint_h_handle = []
    snake_joint_v_handle = []
    for i in xrange(4):
        return_code, snake_joint_h = vrep.simxGetObjectHandle(client_id,
                                                              'snake_joint_h'+str(i+1),
                                                              vrep.simx_opmode_blocking)
        return_code, snake_joint_v = vrep.simxGetObjectHandle(client_id,
                                                              'snake_joint_v'+str(i+1),
                                                              vrep.simx_opmode_blocking)
        snake_joint_h_handle += [snake_joint_h]
        snake_joint_v_handle += [snake_joint_v]

    t = 0
    prev_time = time.time()
    while True:
        # update parameters from GUI
        frequency = app.frequency
        amplitude_h = app.amplitude_h
        amplitude_v = app.amplitude_v
        phase_v = app.phase_h
        phase_h = app.phase_v
        # apply conversion on the parameters
        A_H = amplitude_h * math.pi / 180
        A_V = amplitude_v * math.pi / 180
        P_V = phase_v * math.pi / 180
        P_H = phase_h * math.pi / 180
        t += time.time() - prev_time # update timestep
        prev_time = time.time()
        for i in xrange(4):
            return_code = vrep.simxSetJointTargetPosition(client_id,
                                                          snake_joint_v_handle[i],
                                                          A_V * math.sin(t * frequency + i * P_V),
                                                          vrep.simx_opmode_streaming)
            return_code = vrep.simxSetJointTargetPosition(client_id,
                                                          snake_joint_h_handle[i],
                                                          A_H * math.cos(t * frequency + i * P_H),
                                                          vrep.simx_opmode_streaming)

	  
