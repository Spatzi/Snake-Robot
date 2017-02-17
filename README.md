# Snake-Robot
Task 1 of snake robot lab course - V-REP simulation


1. Open snake.ttt in V-REP.
2. Place vrep.py, vrepConst.py and remoteApi.so (Linux), remoteApi.dll (Windows) or "remoteApi.dylib" (Mac) in your working directory.
3. Add main.py and GUI.py to the same directory.
4. In order to run the simulation, start it first in V-REP (hit the 'play' button), and then run main.py.
5. Select gaits_params.xml or equivalent (explanation below) from your machine.
6. Select the desired gait by clicking the corresponding button. The speed of the gait is adjustable via the slider.


XML file format:
In order to define different gaits, you may create your own XML file. The XML file has to follow the same structure as 
the provided gaits_params.xml.
1. For gaits where all joints have the same parameters, define the following node:

	<gait id="NAME_OF_GAIT">
		<joint>
			<freq_sim> VALUE_OF_FREQUENCY </freq_sim>
			<amp_v_sim> VALUE_OF_VERTICAL_JOINTS_AMPLITUDE </amp_v_sim>
			<amp_h_sim> VALUE_OF_HORIZONTAL_JOINTS_AMPLITUDE </amp_h_sim>
			<phase_v_sim> VALUE_OF_VERTICAL_JOINTS_PHASE </phase_v_sim>
			<phase_h_sim> VALUE_OF_HORIZONTAL_JOINTS_PHASE </phase_h_sim>
		</joint>
	</gait>
	
2. For gaits where each joint has different parameters, define the following 8 nodes:

	<gait id="NAME_OF_GAIT">
		<joint id="1">
			<freq_sim> VALUE_OF_FREQUENCY </freq_sim>
			<amp_v_sim> VALUE_OF_AMPLITUDE </amp_v_sim>
			<phase_v_sim> VALUE_OF_PHASE </phase_v_sim>
		</joint>
		
		...
		
		<joint id="8">
			<freq_sim> VALUE_OF_FREQUENCY </freq_sim>
			<amp_h_sim> VALUE_OF_AMPLITUDE </amp_h_sim>
			<phase_h_sim> VALUE_OF_PHASE </phase_h_sim>
		</joint>
	</gait>
