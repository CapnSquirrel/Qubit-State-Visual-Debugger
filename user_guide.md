# Qubit State Visual Debugger

## What is This Tool For?

This is a Python 3 (3.7+) visual debugging tool for Cirq circuits. Use it to visualize qubit superposition, check for entanglement, ensure that your circuit behavior matches your intuition for what you are trying to code, and understand the state of your qubits at specific moments.

## Tool Dependencies

This tool makes use of Numpy, seaborn, Matplotlib, and Cirq. Please make sure to install these dependencies to use the tool.

- https://numpy.org/install/

- https://seaborn.pydata.org/installing.html

- https://matplotlib.org/stable/users/installing.html

- https://quantumai.google/cirq/install

## How to Use?

The tool is a function with the following signature:

```python
def debug(circuit, iterations=1000, measure_insert=None, kind="qubit_entanglement" )
```

Given a Cirq `circuit` object, this function will visualize the qubit relationships via repeated simulation.

`iterations` is the number of times simulation is run; a higher number yields more data, so the default is set to 1000.

`measure_insert` is default to `None`; supply a moment index (integer) to have the debugger insert measurement gates at that moment (other measurement gates will be removed, since more than one per qubit is not allowed).

`kind` specifies the type of visualization you would like to see; there are three options: `state_superposition`, `qubit_superposition`, and `qubit_entanglement`.

## Debugging Operations

### 1. Qubit Entanglement

### 2. Qubit Superposition

The state of a qubit is oftentimes nondeterministic, especially when the circuit is composed of superposition operations such as a Hadamard gate, and/or entanglement operations such as a CNOT gate.  These operations compound as the circuit grows, making tracking the superposition state of a single qubit at a given moment difficult. Having access to such information can provide useful insight while debugging or verifying a circuit's correctness.

We run the circuit `iterations` times gathering all the measurements. For each qubit, we compute the probability $\alpha$ of measuring 1 from frequency, reported on the graph. We can then deduce the state of the qubit q:
&emsp; q =  (1.0 -  $\alpha$) |0> + $\alpha$ |1>

### 3. State Superposition

Similar to the qubit case, the whole state of the quantum circuit at a given moment is nondeterministic. Being able to visualize the state distribution can also prove useful in inspecting a circuit.

We run the circuit `iterations` times gathering all the measurements. Measurements are stored in in the following format:
&emsp; m$_{state}$ = m$_{n-1}$ ... m$_1$m$_0$,
&emsp; such that $measurement(q$_i$)$ =  m$_i$ $\in$ {0,1},
making of m$_{state}$ a $n$  long binary bitstring representing the whole state of the circuit.

We then compute the frequency of every measurement, giving us the probability of each possible circuit state for the measured moment. The frequencies are then placed in a 2D matrix, of dimension $row$ x $col$ such that:
&emsp; $number\_states \le row \times col$

The matrix entries are numbered from left to right, and top to bottom, with the top left being index 0, bottom right being index  $(row \times col) - 1$.

Therefore each matrix entry has a probability value, and an integer index. From there we extract the following information:
&emsp; m$_{state}$ = index as binary value
&emsp; $P($m$_{state})$ = matrix[index]
