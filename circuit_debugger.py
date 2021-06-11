import cirq
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import test_circuit
import shor_code

# Given two sequences of length n, calculate hamming distance between the two. 
def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

'''
Given a circuit, visualize the qubit relationships via repeated simulation
iterations is the number of times simulation is run, higher yields better results
measure_insert is default to None; supply a moment index to have the debugger insert measurement gates at that moment
'''
def debug(circuit, iterations=1000, measure_insert=None):
    # simulate the circuit
    print(circuit)

    if measure_insert != None:
        qs = circuit.all_qubits()

        # remove existing measurement gates
        for i, gate in enumerate(circuit.moments):
            if 'M' in str(gate):
                circuit.clear_operations_touching(qs, [i])

        # add new measurement gates and show updated circuit
        measurements = [cirq.measure(q) for q in qs]
        circuit.insert(measure_insert, measurements)
        print("Updated measurement gates: ")
        print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=iterations)
    
    # extract the measurement results per qubit
    qubits = []
    for q in result.measurements.values():
        bit_string = ""
        for measurement in q:
            # randomly flip measurement to simulate error
            bit_string += str(measurement[0])
        qubits.append(bit_string)

    # visualize the heatmap
    num_qubits = len(qubits)
    # 2D array to compare qubits against each other, but not against themselves
    matrix = [[-0.1 for i in range(num_qubits)] for j in range(num_qubits)]

    for r in range(0, num_qubits):
        for c in range(0, num_qubits):
            if r != c: 
                matrix[r][c] = hamming_distance(qubits[r], qubits[c]) / iterations # division to place values between 0 and 1

    heatmap = np.matrix(matrix)
    mask = np.triu(heatmap) # this masks out the upper triangular 

    # using seaborn
    labels = [f'q{x}' for x in range(1, num_qubits+1)]
    # get rid of mask parameter to stop masking out upper triangular
    ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, xticklabels=labels, yticklabels=labels)
    plt.show()

# weird measurements inserted, but there were no measurements to begin with...
# debug(shor_code.make_circuit(), measure_insert=6)

# result, t, dj = test_circuit.run_DJ(5)
# debug(dj)

# debug(test_circuit.simon_circuit(4))