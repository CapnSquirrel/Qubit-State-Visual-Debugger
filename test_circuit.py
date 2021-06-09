import cirq
import numpy as np
import random
import time

# circuit helper functionality
def AppendMoment(moment, circuit):
  circuit.append(moment, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
  moment = []
  return moment

def AppendUf(uf_gate, qubits, circuit):
    circuit.append(uf_gate(*qubits))

def dj_circuit(N, uf_gate):
    moment = []
    N += 1 #Add helper
    qubits = cirq.LineQubit.range(N)
    circuit = cirq.Circuit()

    #Negate last Qubit
    circuit.append(cirq.X(qubits[N-1]))

    #Apply Hadamard to all 
    for i in range(N):
        moment.append(cirq.H(qubits[i]))
    moment = AppendMoment(moment, circuit)

    #Apply Oracle
    AppendUf(uf_gate, qubits, circuit)

    #Apply Hadamard to all N first 
    for i in range(N-1):
        moment.append(cirq.H(qubits[i]))
    moment = AppendMoment(moment, circuit)

    #Measure all N-1 first
    for i in range(N-1):
        moment.append(cirq.measure(qubits[i]))
    moment = AppendMoment(moment, circuit)

    return circuit

#Generates Uf for DJ and BV 
def generate_Uf(f, n):
  Uf = []
  for x in range(0, 2**(n+1)):
    xb = format(x, f'0{n+1}b')
    x = xb[0:-1]
    b = xb[-1]
    b_xor_fx = format(int(b, 2) ^ int(f[x], 2), f'0b')
    index = int(x + b_xor_fx, 2)
    row = [0]*(2**(n+1))
    row[index] = 1
    Uf.append(row)
  return Uf

class Uf(cirq.Gate):
    def __init__(self, matrix, nQubits):
        super(Uf, self)
        self.nQubits = nQubits
        self.matrix = matrix

    def _num_qubits_(self):
        return self.nQubits

    def _unitary_(self):
        return np.array(self.matrix)

    def _circuit_diagram_info_(self, args):
        return ["Uf"]*self.nQubits

#Generates functions for DJ 
def generate_DJf(n, constant):
  keys = []
  
  for x in range(0, 2**(n)):
    keys.append(format(x, f'0{n}b'))

  f = dict.fromkeys(keys, '0')
  if constant: return f

  for key in f.keys(): 
    if key[-1] == '1':
      f[key] = '1'
  return f

#Run DJ with a given n, f (optional), and number of repetitions (optional)
def run_DJ(n, f=None, repetitions=1):

  if f == None:
    constant = random.choice([True, False])
    f = generate_DJf(n, constant)

  uf_gate = Uf(generate_Uf(f, n), n+1)

  dj = dj_circuit(n, uf_gate)
  # print("DJ, n = {}".format(n))
  # print(f"Using f={f}")
  # print(dj)
  simulator = cirq.Simulator()
  tic = time.perf_counter()
  result = simulator.run(dj, repetitions=repetitions)
  # print(result)

  # measurement = []
  # for q in result.measurements.values():
  #   measurement.append(str(q[0][0]))
  # if ''.join(measurement) == '0'*n:
  #   print("constant")
  # else:
  #   print("balanced")
  toc = time.perf_counter()
  t = toc - tic
  return result, t, dj

# N=10
# result, t, dj = run_DJ(N)
# print(result)
# print("time: ", t)

def simon_circuit(N):
  moment = []
  
  qubits = []
  # qubits = cirq.LineQubit.range(2*N)
  qubits.append(cirq.GridQubit(3,3))
  qubits.append(cirq.GridQubit(1,4))
  qubits.append(cirq.GridQubit(2,3))
  qubits.append(cirq.GridQubit(3,4))
  qubits.append(cirq.GridQubit(1,5))
  qubits.append(cirq.GridQubit(2,4))
  
  circuit = cirq.Circuit()

  #Apply Hadamar to first N Qubits
  for i in range(N):
    moment.append(cirq.H(qubits[i]))
  moment = AppendMoment(moment, circuit)
  
  # HARD CODED, example from qiskit. Code = '110'
  moment.append(cirq.CNOT(qubits[0], qubits[3]))
  moment = AppendMoment(moment, circuit)

  moment.append(cirq.CNOT(qubits[1], qubits[4]))
  moment = AppendMoment(moment, circuit)
  
  moment.append(cirq.CNOT(qubits[2], qubits[5]))
  moment = AppendMoment(moment, circuit)
  
  moment.append(cirq.CNOT(qubits[1], qubits[4]))
  moment = AppendMoment(moment, circuit)
  
  moment.append(cirq.CNOT(qubits[1], qubits[5]))
  moment = AppendMoment(moment, circuit)

  #Apply Hadamar to first N Qubits
  for i in range(N):
    moment.append(cirq.H(qubits[i]))
  moment = AppendMoment(moment, circuit)

  #Edit: Only need to measure first N bits
  #Measure all N first
  for i in range(N):
    moment.append(cirq.measure(qubits[i]))
  moment = AppendMoment(moment, circuit)

  return circuit