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

## Use Examples

