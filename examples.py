import cirq
import circuit_debugger

# circuit helper functionality
def AppendMoment(moment, circuit):
  circuit.append(moment, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
  moment = []
  return moment

def entangled_circuit():
    circuit = cirq.Circuit()
    (q0, q1) = cirq.LineQubit.range(2)
    # Apply the X-Pauli gate to each qubit
    circuit.append([cirq.X(q0), cirq.X(q1)])
    # Apply the Hadamard gate to first qubit and CNOT gate to both qubits
    circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])
    circuit.append([cirq.measure(q0), cirq.measure(q1)])

    return circuit

def hadamard_circuit(N):
  qubits = cirq.LineQubit.range(N)
  circuit = cirq.Circuit()
  moment = []
  for i in range(N):
      moment.append(cirq.H(qubits[i]))
      moment.append(cirq.measure(qubits[i]))
  moment = AppendMoment(moment, circuit)

  return circuit


circuit_debugger.debug(entangled_circuit())

circuit_debugger.debug(hadamard_circuit(5), kind="state_superposition")