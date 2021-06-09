import cirq
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from test_circuit import simon_circuit

# Given two sequences of length n, calculate hamming distance between the two. 
def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

'''
Given a circuit, visualize the qubit relationships via repeated simulation
'''
def debug(circuit, iterations=1000):
    # simulate the circuit
    print(circuit)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=iterations)
    
    # extract the measurement results per qubit
    qubits = []
    for q in result.measurements.values():
        bit_string = ""
        for measurement in q:
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




debug(simon_circuit(3))