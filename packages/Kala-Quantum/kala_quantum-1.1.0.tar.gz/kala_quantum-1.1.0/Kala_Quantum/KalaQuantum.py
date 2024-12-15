import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from termcolor import colored
import pickle
import json

class QuantumGates:
    """
    A collection of standard quantum gates and utilities for constructing gates
    for multi-qubit systems.
    """
    @staticmethod
    def tensor_gate(single_qubit_gate, num_qubits, target_qubit):
        """
        Constructs a tensor product gate for a multi-qubit system.

        Args:
            single_qubit_gate (np.ndarray): The 2x2 single-qubit gate.
            num_qubits (int): Total number of qubits in the system.
            target_qubit (int): Index of the qubit to which the gate is applied.

        Returns:
            np.ndarray: A multi-qubit gate represented as a tensor product.
        """
        if num_qubits <= 0:
            raise ValueError("Number of qubits must be greater than zero.")
        if target_qubit >= num_qubits:
            raise ValueError("Target qubit index exceeds the number of qubits.")

        # Start with identity for other qubits
        gates = [np.eye(2) for _ in range(num_qubits)]
        gates[target_qubit] = single_qubit_gate  # Replace target qubit gate

        # Compute the full tensor product
        full_gate = gates[0]
        for gate in gates[1:]:
            full_gate = np.kron(full_gate, gate)
        
        return full_gate

    # Single-Qubit Gates
    I = np.eye(2)  # Identity gate
    X = np.array([[0, 1], [1, 0]])  # Pauli-X (NOT) gate
    Y = np.array([[0, -1j], [1j, 0]])  # Pauli-Y gate
    Z = np.array([[1, 0], [0, -1]])  # Pauli-Z gate
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard gate

    @staticmethod
    def RX(theta):
        return np.array([
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)]
        ])

    @staticmethod
    def RY(theta):
        return np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)]
        ])

    @staticmethod
    def RZ(theta):
        return np.array([
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)]
        ])

    @staticmethod
    def apply_gate(gate, state_vector):
        """
        Applies a quantum gate to a given state vector.

        Args:
            gate (np.ndarray): The quantum gate to apply.
            state_vector (np.ndarray): The current state vector.

        Returns:
            np.ndarray: The new state vector after applying the gate.
        """
        if len(gate.shape) != 2 or gate.shape[0] != gate.shape[1]:
            raise ValueError(
                colored(
                    f"Gate must be a square matrix, got shape {gate.shape}.",
                    "red",
                )
            )
        if gate.shape[0] != len(state_vector):
            raise ValueError(
                colored(
                    f"Gate dimensions {gate.shape} do not match state vector size {len(state_vector)}.",
                    "red",
                )
            )
        return np.dot(gate, state_vector)


class QuantumState:
    def __init__(self, state_vector):
        self.state_vector = np.array(state_vector, dtype=complex)
        self.normalize()

    def normalize(self):
        norm = np.linalg.norm(self.state_vector)
        if norm == 0:
            raise ValueError(colored("State vector cannot be zero.", "red"))
        self.state_vector /= norm

    def measure(self):
        probabilities = np.abs(self.state_vector) ** 2
        outcome = np.random.choice(len(self.state_vector), p=probabilities)
        new_state = np.zeros_like(self.state_vector)
        new_state[outcome] = 1
        self.state_vector = new_state
        return outcome

    def apply_gate(self, gate):
        if gate.shape[0] != gate.shape[1] or gate.shape[0] != len(self.state_vector):
            raise ValueError(colored("Gate dimensions must match the quantum state vector size.", "red"))
        self.state_vector = np.dot(gate, self.state_vector)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.state_vector, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            state_vector = pickle.load(f)
        return QuantumState(state_vector)


class QuantumCircuit:
    def __init__(self, num_qubits):
        if num_qubits <= 0:
            raise ValueError("Number of qubits must be greater than zero.")
        self.num_qubits = num_qubits
        self.state_vector = np.zeros(2 ** num_qubits, dtype=complex)
        self.state_vector[0] = 1.0  # Initialize to |0...0>

    def apply_gate(self, gate, qubit):
        full_gate = QuantumGates.tensor_gate(gate, self.num_qubits, qubit)
        self.state_vector = QuantumGates.apply_gate(full_gate, self.state_vector)

    def reset(self):
        self.state_vector = np.zeros(2 ** self.num_qubits, dtype=complex)
        self.state_vector[0] = 1.0

    def measure(self):
        probabilities = np.abs(self.state_vector) ** 2
        outcome = np.random.choice(len(self.state_vector), p=probabilities)
        self.reset()
        self.state_vector[outcome] = 1.0
        return outcome


class QuantumTrainer:
    def __init__(self, model, training_data):
        self.model = model
        self.training_data = training_data
        self.loss_history = []

    def align_target_state(self, target_state):
        current_size = len(self.model.state_vector)
        target_size = len(target_state)
        if target_size < current_size:
            target_state = np.pad(target_state, (0, current_size - target_size), mode='constant')
        elif target_size > current_size:
            target_state = target_state[:current_size]
        return target_state

    def compute_loss(self, target_state):
        target_state = self.align_target_state(target_state)
        current_state = self.model.state_vector
        loss = np.linalg.norm(current_state - target_state)
        return loss

    def train(self, target_state, epochs=100, learning_rate=0.1):
        target_state = self.align_target_state(target_state)
        for epoch in tqdm(range(epochs), desc=colored("Training Progress", "green"), colour="green"):
            loss = self.compute_loss(target_state)
            self.loss_history.append(loss)
            perturbation = (target_state - self.model.state_vector) * learning_rate
            self.model.state_vector += perturbation
            self.model.normalize()


class QuantumOptimizer:
    def __init__(self, learning_rate):
        """
        Initializes the QuantumOptimizer with a given learning rate.

        Args:
            learning_rate (float): The step size for optimization.
        """
        if learning_rate <= 0:
            raise ValueError("Learning rate must be greater than zero.")
        self.learning_rate = learning_rate

    def optimize(self, circuit, target_function, target_state):
        """
        Optimizes the given quantum circuit to minimize the target function.

        Args:
            circuit (QuantumCircuit): The quantum circuit to optimize.
            target_function (function): A function that calculates the loss.
            target_state (np.ndarray): The target state vector.

        Returns:
            float: The final loss value after optimization.
        """
        if not callable(target_function):
            raise ValueError("target_function must be a callable function.")

        loss_history = []
        for epoch in tqdm(range(100), desc=colored("Optimization Progress", "blue"), colour="blue"):
            # Calculate current loss
            loss = target_function(circuit.state_vector, target_state)
            loss_history.append(loss)

            # Apply gradient descent (simplified for demonstration purposes)
            gradient = (circuit.state_vector - target_state) * 2
            circuit.state_vector -= self.learning_rate * gradient
            circuit.state_vector /= np.linalg.norm(circuit.state_vector)  # Normalize the state vector

            print(f"Epoch {epoch + 1}: Loss = {loss:.6f}")

            # Early stopping condition
            if loss < 1e-6:
                print(colored("Optimization converged!", "green"))
                break

        return loss_history[-1]

class KalaAI(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(KalaAI, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


def initialize_kala_ai(input_size, hidden_size, output_size):
    model = KalaAI(input_size, hidden_size, output_size)
    return model


def train_kala_ai(model, quantum_trainer, target_state, dataloader, epochs, learning_rate):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in tqdm(range(epochs), desc=colored("Training Kala AI", "blue"), colour="blue"):
        epoch_loss = 0.0
        for data in dataloader:
            inputs, labels = data
            inputs, labels = inputs.float(), labels.float()

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        quantum_trainer.train(target_state, epochs=1, learning_rate=learning_rate)

        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {epoch_loss:.4f}")