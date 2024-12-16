import numpy as np
import torch

class Gate:
    """Class representing a quantum gate."""
    def __init__(self, matrix, name):
        self.matrix = matrix
        self.name = name

    @staticmethod
    def pauli_x():
        return Gate(torch.tensor([[0, 1], [1, 0]], dtype=torch.complex64), "Pauli-X")

    @staticmethod
    def pauli_y():
        return Gate(torch.tensor([[0, -1j], [1j, 0]], dtype=torch.complex64), "Pauli-Y")

    @staticmethod
    def pauli_z():
        return Gate(torch.tensor([[1, 0], [0, -1]], dtype=torch.complex64), "Pauli-Z")

    @staticmethod
    def hadamard():
        return Gate((1 / np.sqrt(2)) * torch.tensor([[1, 1], [1, -1]], dtype=torch.complex64), "Hadamard")

    @staticmethod
    def cnot():
        return Gate(torch.tensor([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0]], dtype=torch.complex64), "CNOT")

    @staticmethod
    def rotation_x(theta):
        return Gate(torch.tensor([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                                  [-1j * np.sin(theta / 2), np.cos(theta / 2)]], dtype=torch.complex64), f"Rx({theta})")

    @staticmethod
    def rotation_y(theta):
        return Gate(torch.tensor([[np.cos(theta / 2), -np.sin(theta / 2)],
                                  [np.sin(theta / 2), np.cos(theta / 2)]], dtype=torch.complex64), f"Ry({theta})")

    @staticmethod
    def rotation_z(theta):
        return Gate(torch.tensor([[np.exp(-1j * theta / 2), 0],
                                  [0, np.exp(1j * theta / 2)]], dtype=torch.complex64), f"Rz({theta})")

    @staticmethod
    def custom(matrix):
        return Gate(torch.tensor(matrix, dtype=torch.complex64), "Custom")


class QuantumRegister:
    """Class representing a quantum register."""
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = torch.zeros((2 ** num_qubits,), dtype=torch.complex64)
        self.state[0] = 1.0  # Start in |0...0>


class ClassicalRegister:
    """Class representing a classical register."""
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bits = [0] * num_bits


class QuantumCircuit:
    """Class representing a quantum circuit."""
    def __init__(self, num_qubits, num_bits):
        self.qreg = QuantumRegister(num_qubits)
        self.creg = ClassicalRegister(num_bits)
        self.operations = []  # List of operations to apply

    def apply(self, gate, qubits):
        """
        Apply a gate to specified qubits.

        Parameters:
            gate (Gate): The quantum gate to apply.
            qubits (list[int]): Indices of the qubits the gate acts on.
        """
        if len(qubits) != int(np.log2(gate.matrix.shape[0])):
            raise ValueError("Gate size does not match the number of qubits.")
        self.operations.append((gate, qubits))

    def measure(self, qubit, cbit):
        """
        Measure a specific qubit into a classical bit.

        Parameters:
            qubit (int): The index of the qubit to measure.
            cbit (int): The index of the classical bit to store the result.
        """
        probabilities = torch.abs(self.qreg.state) ** 2
        outcome = np.random.choice(len(probabilities), p=probabilities.numpy())
        collapsed_state = torch.zeros_like(self.qreg.state)
        collapsed_state[outcome] = 1.0
        self.qreg.state = collapsed_state

        binary_outcome = format(outcome, f"0{self.qreg.num_qubits}b")
        self.creg.bits[cbit] = int(binary_outcome[qubit])

    def measure_all(self):
        """
        Measure all qubits in the computational basis and store results in classical bits.

        Returns:
            list[int]: Measurement outcomes for all qubits.
        """
        probabilities = torch.abs(self.qreg.state) ** 2
        outcome = np.random.choice(len(probabilities), p=probabilities.numpy())
        collapsed_state = torch.zeros_like(self.qreg.state)
        collapsed_state[outcome] = 1.0
        self.qreg.state = collapsed_state

        # Convert integer outcome to binary and store in classical register
        binary_outcome = format(outcome, f"0{self.qreg.num_qubits}b")
        self.creg.bits = [int(x) for x in binary_outcome]
        return self.creg.bits

    def execute(self):
        """Execute the circuit by applying all gates sequentially."""
        for gate, qubits in self.operations:
            self._apply_gate(gate.matrix, qubits)

    def _apply_gate(self, gate, qubits):
        """Internal method to apply a gate to the quantum state."""
        full_gate = self._expand_gate(gate, qubits)
        self.qreg.state = torch.matmul(full_gate, self.qreg.state)
        # Normalize the state
        self.qreg.state /= torch.norm(self.qreg.state)

    def _expand_gate(self, gate, qubits):
        """
        Expand a gate to the full quantum state.

        Parameters:
            gate (torch.Tensor): The unitary gate matrix.
            qubits (list[int]): Indices of the qubits the gate acts on.

        Returns:
            torch.Tensor: The expanded gate matrix.
        """
        full_size = 2 ** self.qreg.num_qubits
        expanded_gate = torch.eye(full_size, dtype=torch.complex64)
        for i in range(full_size):
            binary = format(i, f"0{self.qreg.num_qubits}b")
            indices = [binary[q] for q in qubits]
            local_index = int("".join(indices), 2)
            for j in range(gate.shape[0]):
                target_binary = list(binary)
                local_target = format(j, f"0{len(qubits)}b")
                for idx, qubit in zip(local_target, qubits):
                    target_binary[qubit] = idx
                target_index = int("".join(target_binary), 2)
                expanded_gate[target_index, i] = gate[j, local_index]
        return expanded_gate

# Example Usage
if __name__ == "__main__":
    # Create a 2-qubit circuit with 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Add gates
    qc.apply(Gate.hadamard(), [0])  # Apply Hadamard to qubit 0
    qc.apply(Gate.cnot(), [0, 1])  # Apply CNOT with qubit 0 as control and qubit 1 as target

    # Execute the circuit
    qc.execute()

    # Measure all qubits
    result = qc.measure_all()
    print(f"Measurement outcome: {result}")
