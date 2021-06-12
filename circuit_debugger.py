import cirq
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import test_circuit
import shor_code
import math

# Given two sequences of length n, calculate hamming distance between the two.
def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

'''
Given a circuit, visualize the qubit relationships via repeated simulation
iterations is the number of times simulation is run, higher yields better results
measure_insert is default to None; supply a moment index to have the debugger insert measurement gates at that moment
'''
def debug(circuit, iterations=1000, measure_insert=None, kind = "qubit_entanglement" ):
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

    print(qubits)

    if kind == "qubit_entanglement":
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
      ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, xticklabels=labels, yticklabels=labels, vmin = -0.1, vmax = 1.0)
      plt.title("Qubit Pairwise Entanglement")
      plt.show()

    if kind == "qubit_superposition":
      # visualize the heatmap
      num_qubits = len(qubits)
      # 1D array to compare qubits against themselves
      matrix = [-0.1 for i in range(num_qubits)]
      #probability qubit being 1
      for i in range(num_qubits):
        accum = 0
        for s in qubits[i]:
          accum += int(s)
        matrix[i] = accum/iterations

      heatmap = np.matrix(matrix)
      # using seaborn
      labels = [f'q{x}' for x in range(1, num_qubits+1)]
      # get rid of mask parameter to stop masking out upper triangular
      ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, xticklabels=labels, yticklabels=["%q == 1"], vmin = 0.0, vmax = 1.0)
      plt.title("Qubit Superposition")
      plt.show()

    if kind == "state_superposition":
      num_qubits = len(qubits)
      num_states = math.pow(2, len(qubits))
      row = math.ceil(math.sqrt(num_states))
      col = math.ceil(num_states/row)

      dic = {}
      for i in range(row*col):
        if i < num_states:
          dic[i] = 0.0
        else:
          dic[i] = -0.1

      for i in range(iterations):
        s = ""
        for q in range(len(qubits)):
          s += qubits[q][i]
        state_num = int(s[::-1], 2)
        dic[state_num] += 1.0/iterations

      matrix = [[dic[r + c*row] for r in range(row)] for c in range(col)]

      #print(dic)
      #print(matrix)

      heatmap = np.matrix(matrix)
      # using seaborn
      labels_x = [x for x in range(col)]
      labels_y = [x for x in range(row)]
      # get rid of mask parameter to stop masking out upper triangular
      ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, xticklabels=labels_x, yticklabels=labels_y, vmin = -0.1, vmax = 1.0)
      plt.title("State Superposition")
      plt.show()



# weird measurements inserted, but there were no measurements to begin with...
# debug(shor_code.make_circuit(), measure_insert=6)

# result, t, dj = test_circuit.run_DJ(5)
# debug(dj)

debug(test_circuit.simon_circuit(4), iterations = 20, kind = "state_superposition")
