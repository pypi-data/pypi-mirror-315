import numpy as np
from tqdm import tqdm
import pickle

class QuantumState:
    def __init__(self, state_vector):
        self.state_vector = np.array(state_vector, dtype=complex)
        self.normalize()

    def normalize(self):
        norm = np.linalg.norm(self.state_vector)
        if norm == 0:
            raise ValueError("State vector cannot be zero.")
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
            raise ValueError("Gate dimensions must match the quantum state vector size.")
        self.state_vector = np.dot(gate, self.state_vector)

    def compose_gates(self, *gates):
        combined_gate = np.eye(len(self.state_vector))
        for gate in gates:
            if gate.shape[0] != combined_gate.shape[0]:
                raise ValueError("All gates must have dimensions matching the quantum state vector.")
            combined_gate = np.dot(gate, combined_gate)
        self.apply_gate(combined_gate)

    def convert_to_qubit(self, classical_data):
        """
        Converts classical data (strings or numerical) into a quantum state representation.
        For strings, each unique string is mapped to a basis state, and the state is initialized
        to an equal superposition of these basis states.
        """
        if isinstance(classical_data[0], str):
            unique_strings = list(set(classical_data))
            mapping = {string: idx for idx, string in enumerate(unique_strings)}
            num_states = len(unique_strings)
            state_vector = np.ones(num_states, dtype=complex)  # Initialize non-zero vector
            self.state_vector = state_vector / np.linalg.norm(state_vector)
        elif isinstance(classical_data[0], (int, float)):
            if not np.isclose(sum(classical_data), 1):
                raise ValueError("Probabilities must sum to 1.")
            self.state_vector = np.sqrt(np.array(classical_data, dtype=complex))
        else:
            raise ValueError("Unsupported data type. Provide strings or numerical probabilities.")

    def save(self, filename):
        """
        Saves the quantum state vector to a file using pickle.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.state_vector, f)

    @staticmethod
    def load(filename):
        """
        Loads the quantum state vector from a file and initializes a QuantumState object.
        """
        with open(filename, 'rb') as f:
            state_vector = pickle.load(f)
        return QuantumState(state_vector)

    def __repr__(self):
        return f"QuantumState({self.state_vector})"

# Define standard quantum gates
class QuantumGates:
    @staticmethod
    def tensor_gate(single_qubit_gate, num_qubits, target_qubit):
        """
        Builds a tensor product gate for multi-qubit systems.
        """
        if target_qubit >= num_qubits:
            raise ValueError("Target qubit index exceeds the number of qubits.")
        gate = 1
        for qubit in range(num_qubits):
            if qubit == target_qubit:
                gate = np.kron(gate, single_qubit_gate) if qubit > 0 else single_qubit_gate
            else:
                gate = np.kron(gate, np.eye(2)) if qubit > 0 else np.eye(2)
        return gate

    I = np.eye(4)  # Identity gate (adjusted for 2-qubit systems)
    X = tensor_gate.__func__(np.array([[0, 1], [1, 0]]), 2, 0)  # Pauli-X gate on qubit 0
    Z = tensor_gate.__func__(np.array([[1, 0], [0, -1]]), 2, 0)  # Pauli-Z gate on qubit 0
    H = tensor_gate.__func__((1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]]), 2, 0)  # Hadamard on qubit 0
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])  # CNOT gate

# Define a basic quantum training framework
class QuantumTrainer:
    def __init__(self, model, training_data):
        self.model = model  # Parameterized quantum circuit
        self.training_data = training_data  # Data for training (input-output pairs)
        self.loss_history = []

    def align_target_state(self, target_state):
        """
        Aligns the target state to match the shape of the model's state vector.
        If the target state has fewer elements, it is padded with zeros.
        If it has more elements, it is truncated.
        """
        current_size = len(self.model.state_vector)
        target_size = len(target_state)
        if target_size < current_size:
            target_state = np.pad(target_state, (0, current_size - target_size), mode='constant')
        elif target_size > current_size:
            target_state = target_state[:current_size]
        return target_state

    def compute_loss(self, target_state):
        """
        Computes loss as the Euclidean distance between the current state
        and the target quantum state.
        """
        target_state = self.align_target_state(target_state)
        current_state = self.model.state_vector
        loss = np.linalg.norm(current_state - target_state)
        return loss

    def train(self, target_state, epochs=100, learning_rate=0.1):
        """
        Trains the model by applying small parameter updates to minimize loss.
        Uses tqdm for progress tracking.
        """
        target_state = self.align_target_state(target_state)
        for epoch in tqdm(range(epochs), desc="Training Progress"):
            # Compute the loss
            loss = self.compute_loss(target_state)
            self.loss_history.append(loss)

            # Simulate parameter update (for demonstration purposes, no actual parameters here)
            perturbation = (target_state - self.model.state_vector) * learning_rate
            self.model.state_vector += perturbation
            self.model.normalize()

class QuantumChatbot:
    def __init__(self):
        self.state = None  # QuantumState instance
        self.response_map = {}  # Maps measurement outcomes to responses

    def initialize_state(self, input_data):
        """
        Initializes the quantum state based on user input.
        """
        self.state = QuantumState([1] * len(set(input_data)))  # Create a valid non-zero state
        self.state.convert_to_qubit(input_data)

    def add_response_map(self, mapping):
        """
        Adds a mapping of measurement outcomes to responses.
        Example: {0: "Hello!", 1: "How can I help you?", ...}
        """
        self.response_map = mapping

    def respond(self, input_data):
        """
        Responds to user input by processing quantum state and measuring the outcome.
        """
        if self.state is None:
            self.initialize_state(input_data)

        # Apply quantum processing (customize gates or logic here)
        self.state.apply_gate(QuantumGates.H)  # Example: Apply Hadamard gate

        # Measure the quantum state
        outcome = self.state.measure()

        # Return the response based on the measurement outcome
        return self.response_map.get(outcome, "I'm not sure how to respond.")

# Example usage
if __name__ == "__main__":
    # Create a quantum state |0> (represented as [1, 0])
    qs = QuantumState([1, 0, 0, 0])
    print("Initial state:", qs)

    # Apply Hadamard gate
    qs.apply_gate(QuantumGates.H)
    print("After Hadamard:", qs)

    # Apply a sequence of gates: H, CX, then H again
    qs.compose_gates(QuantumGates.H, QuantumGates.CX, QuantumGates.H)
    print("After H-CX-H sequence:", qs)

    # Convert classical data (strings) to quantum state
    classical_data = ["hello", "world", "hello", "how are u"]
    qs.convert_to_qubit(classical_data)
    print("Quantum state from classical data (strings):", qs)

    # Measure the quantum state
    outcome = qs.measure()
    print("Measurement outcome:", outcome)
    print("State after measurement:", qs)

    # Save the quantum state
    qs.save("quantum_state.pkl")
    print("Quantum state saved.")

    # Load the quantum state
    loaded_qs = QuantumState.load("quantum_state.pkl")
    print("Loaded quantum state:", loaded_qs)

    # Training example
    target_state = np.array([0.5 + 0j, 0.5 + 0j, 0.5 + 0j, 0.5 + 0j])  # Example target state
    trainer = QuantumTrainer(qs, training_data=None)
    trainer.train(target_state, epochs=10, learning_rate=0.05)

    # Predict the outcome of a measurement
    print("Predicted outcome of measurement:", loaded_qs.measure())

    # Create the chatbot
    chatbot = QuantumChatbot()

    # Initialize with some sample data
    user_inputs = ["hello", "help", "info", "goodbye"]
    chatbot.initialize_state(user_inputs)

    # Define response mapping
    chatbot.add_response_map({
        0: "Hello! How can I assist you?",
        1: "I'm here to help!",
        2: "Here's some information for you.",
        3: "Goodbye! Have a great day!"
    })

    # Simulate a conversation
    user_message = "hello"
    print("User:", user_message)
    response = chatbot.respond(user_inputs)
    print("Chatbot:", response)
