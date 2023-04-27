import subprocess
import re
import sys
import time

#recieves the raw string from the console and obtains the state, contained in <>
def extractState(string):	
    pattern = r'<([\s\S]+?)>'
    match = re.search(pattern, string)
    if match:
        return match.group(0)
    else:
        return None

#recieve a state string and returns only the network
def extractNetwork(string):
	pattern = r'\{([^}]*)\}'
	match = re.search(pattern, string)
	if match:
		return match.group(0)
	else:
		return None



#recieves a seed for the simulation and runs it
#returns the string of the resulting state

def runSimulation(seed, numExp):
	#open the maude console with random seed
	process = subprocess.Popen(["../Maude/maude.linux64", f"-random-seed={seed}", "simulation.maude"], stdin=subprocess.PIPE, 
	                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	#rewrite the experiment
	command = f"rew experiment{str(numExp)} .\n"
	output, error = process.communicate(command.encode()) 

	#get decoded output and the state
	output = output.decode()
	stateString = extractState(output) 
	#eliminate special characters
	stateString = ''.join(stateString.split())
	#add space before ">"
	stateString = stateString.replace(">", " >")

	return stateString 


def evaluateState(stateString, equation):

	#open the maude console
	process = subprocess.Popen(["../Maude/maude.linux64", "simulation.maude"], stdin=subprocess.PIPE, 
	                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	command = ""
	if equation == "moderate": command = f"red moderateConcensus({stateString}) .\n"
	elif equation == "extreme": command = f"red extremeConcensus({stateString}) .\n"
	elif equation == "polarization": command = f"red biPolarization({stateString}) .\n"

	output, error = process.communicate(command.encode()) 
	#get decoded output and the state
	output = output.decode()

	#check if it is true or false and return the value
	answer = None
	if "false" in output: answer = False
	elif "true" in output: answer = True 

	return answer

def main():

	#start counting time
	start_time = time.time()
	
	#number of simulations
	arg1 = int(sys.argv[1])
	#initial seed
	arg2 = int(sys.argv[2])
	#number of the experiment
	arg3 = int(sys.argv[3])

	
	#count occurences
	moderate = 0
	extreme = 0
	polarization = 0
	
	#make simulations
	for i in range(arg1):
		state = runSimulation(arg2 + i, arg3)
		print(extractNetwork(state))
		if(evaluateState(state,"moderate")): moderate += 1
		elif(evaluateState(state,"extreme")): extreme += 1
		elif(evaluateState(state,"polarization")): polarization += 1
		
		print("############################################")
		print(f"Number of moderate concesus: {str(moderate)}")
		print(f"Number of extreme concesus: {str(extreme)}")
		print(f"Number of bi-polarization: {str(polarization)}")
	
	#get total time
	end_time = time.time()
	total_time = end_time - start_time
	#print results
	print("############################################")
	print("Final Results:")
	print("############################################")
	print(f"Simulation time: {str(total_time)} seconds")
	print(f"Number of moderate concesus: {str(moderate)}")
	print(f"Number of extreme concesus: {str(extreme)}")
	print(f"Number of bi-polarization: {str(polarization)}")



if __name__ == "__main__":
    main()

#command example: python3 runSimulations.py 10 38 1

