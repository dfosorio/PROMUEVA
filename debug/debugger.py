import subprocess
import re
import sys
import time

#recieves the raw string from the console and obtains the state, contained in <>
def extractState(string):	
    pattern = r'result State: <([\s\S]+?)>'
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

def runSimulation(seed):
    #open the maude console with random seed
    process = subprocess.Popen(["../Maude/maude.linux64", f"-random-seed={seed}", "simulation.maude"], stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    counter = 0
    #rewrite the first state
    command = f"rew experiment1 .\n"
    output, error = process.communicate(command.encode()) 
    #get decoded output and the state
    output = output.decode()
    stateString = extractState(output) 
    #eliminate special characters
    stateString = ''.join(stateString.split())
    #add space before ">"
    stateString = stateString.replace(">", " >")
    #eliminate resultState:
    stateString = stateString.replace("resultState:", "")
    
    print(f"State {counter}: {stateString}")

    for i in range(310031):
        counter += 1
        #open the maude console with random seed
        process = subprocess.Popen(["../Maude/maude.linux64", f"-random-seed={str(seed + i)}", "simulation.maude"], stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #rewrite the state
        command = f"rew tick({stateString}) .\n"
        output, error = process.communicate(command.encode()) 
        #get decoded output and the state
        output = output.decode()
        stateString = extractState(output)
        #eliminate special characters
        stateString = ''.join(stateString.split())
        #add space before ">"
        stateString = stateString.replace(">", " >")
        #eliminate resultState:
        stateString = stateString.replace("resultState:", "")
        
        if(counter % 31 == 0):
            print("####################################################3")
            print(f"State {counter}: {stateString}")




#print(extractNetwork(extractState("rewrite in SIMULATIONS : tick(<{((((((((ag(9, -1, -1.0), ag(10, -1, -5.0e-1)), ag(8, -1, -1.0)), ag(7, -1, -5.0e-1)), ag(6, -1, -1.0)), ag(5, 1, 5.0e-1)), ag(4, 1, 5.0061798095703125e-1)), ag(3, 1, 9.8876953125e-3)), ag(2, 1, 1.0)), ag(1, 1, 1.0)},{((((((((ag(9, -1, -1.0), ag(10, -1, -5.0e-1)), ag(8, -1, -1.0)), ag(7, -1, -5.0e-1)), ag(6, -1, -1.0)), ag(5, 1, 5.0e-1)), ag(4, 1, 5.0061798095703125e-1)), ag(3, 1, 9.8876953125e-3)), ag(2, 1, 1.0)), ag(1, 1, 1.0)},9999,4,3.0,4.0,false >) . rewrites: 1774 in 0ms cpu (0ms real) (~ rewrites/second) result State: <{ag(1, 1, 1.0), ag(2, 1, 1.0), ag(3, 1, 9.8876953125e-3), ag(4, 1, 5.0061798095703125e-1), ag(5, 1, 7.2190809736352413e-1), ag(6, -1, -1.0), ag(7, -1, -5.0e-1), ag(8, -1, -1.0), ag(9, -1, -1.0), ag(10, -1, -5.0e-1)},{ag(1, 1, 1.0), ag(2, 1, 1.0), ag(3, 1, 9.8876953125e-3), ag(4, 1, 5.0061798095703125e-1), ag(5, 1, 7.2190809736352413e-1), ag(6, -1, -1.0), ag(7, -1, -5.0e-1), ag(8, -1, -1.0), ag( 9, -1, -1.0), ag(10, -1, -5.0e-1)},9998,4,3.0,4.0,false >")))
runSimulation(45670)