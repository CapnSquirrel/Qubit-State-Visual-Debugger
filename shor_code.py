""" Shor's code is a stabilizer code for quantum error correction.
It uses 9 qubits to encode 1 logic qubit and is able to correct
at most one bit flip and one sign flip or their combination.
(0, 0): ───@───@───H───@───@───@───@───X───H───@───@───X───M───
           │   │       │   │   │   │   │       │   │   │
(0, 1): ───┼───┼───────X───┼───X───┼───@───────┼───┼───┼───M───
           │   │           │       │   │       │   │   │
(0, 2): ───┼───┼───────────X───────X───@───────┼───┼───┼───M───
           │   │                               │   │   │
(0, 3): ───X───┼───H───@───@───@───@───X───H───X───┼───@───M───
               │       │   │   │   │   │           │   │
(0, 4): ───────┼───────X───┼───X───┼───@───────────┼───┼───M───
               │           │       │   │           │   │
(0, 5): ───────┼───────────X───────X───@───────────┼───┼───M───
               │                                   │   │
(0, 6): ───────X───H───@───@───@───@───X───H───────X───@───M───
                       │   │   │   │   │
(0, 7): ───────────────X───┼───X───┼───@───────────────────M───
                           │       │   │
(0, 8): ───────────────────X───────X───@───────────────────M───
reference: P. W. Shor, Phys. Rev. A, 52, R2493 (1995).
"""

import random

import cirq


class OneQubitShorsCode:
    def __init__(self):
        self.num_physical_qubits = 9
        self.physical_qubits = cirq.LineQubit.range(self.num_physical_qubits)

    def encode(self):
        yield cirq.ops.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[3])])
        yield cirq.ops.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[6])])
        yield cirq.ops.Moment(
            [
                cirq.H(self.physical_qubits[0]),
                cirq.H(self.physical_qubits[3]),
                cirq.H(self.physical_qubits[6]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[1]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[4]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[7]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[2]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[5]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[8]),
            ]
        )

    def apply_gate(self, gate: cirq.Gate, pos: int):
        if pos > self.num_physical_qubits:
            raise IndexError
        else:
            return gate(self.physical_qubits[pos])

    def correct(self):
        yield cirq.ops.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[1]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[4]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[7]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(self.physical_qubits[0], self.physical_qubits[2]),
                cirq.CNOT(self.physical_qubits[3], self.physical_qubits[5]),
                cirq.CNOT(self.physical_qubits[6], self.physical_qubits[8]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CCNOT(
                    self.physical_qubits[1], self.physical_qubits[2], self.physical_qubits[0]
                ),
                cirq.CCNOT(
                    self.physical_qubits[4], self.physical_qubits[5], self.physical_qubits[3]
                ),
                cirq.CCNOT(
                    self.physical_qubits[7], self.physical_qubits[8], self.physical_qubits[6]
                ),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.H(self.physical_qubits[0]),
                cirq.H(self.physical_qubits[3]),
                cirq.H(self.physical_qubits[6]),
            ]
        )
        yield cirq.ops.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[3])])
        yield cirq.ops.Moment([cirq.CNOT(self.physical_qubits[0], self.physical_qubits[6])])
        yield cirq.ops.Moment(
            [cirq.CCNOT(self.physical_qubits[3], self.physical_qubits[6], self.physical_qubits[0])]
        )

def AppendMoment(moment, circuit):
    circuit.append(moment, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    moment = []
    return moment

def make_circuit():
    # coverage: ignore

    # create circuit with 9 physical qubits
    code = OneQubitShorsCode()

    circuit = cirq.Circuit(code.apply_gate(cirq.X ** (1 / 4), 0))
    # print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    circuit += cirq.Circuit(code.encode())
    # print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    # create error
    circuit += cirq.Circuit(
        code.apply_gate(cirq.X, random.randint(0, code.num_physical_qubits - 1))
    )
    # print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    # correct error and decode
    circuit += cirq.Circuit(code.correct())
    # print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    moment = []
    for i in range(9):
        moment.append(cirq.measure(code.physical_qubits[i]))
    moment = AppendMoment(moment, circuit)
    return circuit