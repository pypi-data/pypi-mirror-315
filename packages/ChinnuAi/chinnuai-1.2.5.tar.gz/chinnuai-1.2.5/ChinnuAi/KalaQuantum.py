import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from termcolor import colored
import pickle
import json

import numpy as np

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
        if target_qubit >= num_qubits:
            raise ValueError("Target qubit index exceeds the number of qubits.")

        gate = 1
        for qubit in range(num_qubits):
            if qubit == target_qubit:
                gate = np.kron(gate, single_qubit_gate) if qubit > 0 else single_qubit_gate
            else:
                gate = np.kron(gate, np.eye(2)) if qubit > 0 else np.eye(2)
        return gate

    # Single-Qubit Gates
    I = np.eye(2)  # Identity gate
    X = np.array([[0, 1], [1, 0]])  # Pauli-X (NOT) gate
    Y = np.array([[0, -1j], [1j, 0]])  # Pauli-Y gate
    Z = np.array([[1, 0], [0, -1]])  # Pauli-Z gate
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard gate

    # Two-Qubit Gates
    CX = np.array([  # Controlled-X (CNOT) gate
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

    CZ = np.array([  # Controlled-Z gate
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ])

    @staticmethod
    def custom_control_gate(control_gate, num_qubits, control_qubit, target_qubit):
        """
        Constructs a custom controlled gate for a multi-qubit system.

        Args:
            control_gate (np.ndarray): The single-qubit gate for the target qubit.
            num_qubits (int): Total number of qubits in the system.
            control_qubit (int): Index of the control qubit.
            target_qubit (int): Index of the target qubit.

        Returns:
            np.ndarray: The controlled gate represented as a tensor product.
        """
        if control_qubit >= num_qubits or target_qubit >= num_qubits:
            raise ValueError("Control or target qubit index exceeds the number of qubits.")

        dim = 2 ** num_qubits
        identity = np.eye(dim)
        gate = np.zeros((dim, dim), dtype=complex)

        for i in range(dim):
            binary = f"{i:0{num_qubits}b}"
            if binary[control_qubit] == "1":
                new_state = list(binary)
                new_state[target_qubit] = str(1 - int(binary[target_qubit]))
                new_state_idx = int("".join(new_state), 2)
                gate[i, new_state_idx] = 1
            else:
                gate[i, i] = 1

        return gate

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
        if gate.shape[0] != gate.shape[1] or gate.shape[0] != len(state_vector):
            raise ValueError("Gate dimensions must match the quantum state vector size.")
        return np.dot(gate, state_vector)

    @staticmethod
    def multi_qubit_hadamard(num_qubits):
        """
        Constructs a multi-qubit Hadamard gate.

        Args:
            num_qubits (int): Number of qubits.

        Returns:
            np.ndarray: The multi-qubit Hadamard gate.
        """
        H = QuantumGates.H
        gate = H
        for _ in range(num_qubits - 1):
            gate = np.kron(gate, H)
        return gate

# QuantumState Class
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

    def compose_gates(self, *gates):
        combined_gate = np.eye(len(self.state_vector))
        for gate in gates:
            if gate.shape[0] != combined_gate.shape[0]:
                raise ValueError(colored("All gates must have dimensions matching the quantum state vector.", "red"))
            combined_gate = np.dot(gate, combined_gate)
        self.apply_gate(combined_gate)

    def convert_to_qubit(self, classical_data):
        if isinstance(classical_data[0], str):
            unique_strings = list(set(classical_data))
            mapping = {string: idx for idx, string in enumerate(unique_strings)}
            num_states = len(unique_strings)
            state_vector = np.ones(num_states, dtype=complex)  # Initialize non-zero vector
            self.state_vector = state_vector / np.linalg.norm(state_vector)
        elif isinstance(classical_data[0], (int, float)):
            if not np.isclose(sum(classical_data), 1):
                raise ValueError(colored("Probabilities must sum to 1.", "red"))
            self.state_vector = np.sqrt(np.array(classical_data, dtype=complex))
        else:
            raise ValueError(colored("Unsupported data type. Provide strings or numerical probabilities.", "red"))

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.state_vector, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            state_vector = pickle.load(f)
        return QuantumState(state_vector)

    def __repr__(self):
        return f"QuantumState({self.state_vector})"

# QuantumTrainer Class
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

# Define a simple neural network using PyTorch
class ChinnuAI(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChinnuAI, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Initialize Chinnu AI model
def initialize_chinnu_ai(input_size, hidden_size, output_size):
    model = ChinnuAI(input_size, hidden_size, output_size)
    return model

# Define training function
def train_chinnu_ai(model, quantum_trainer, target_state, dataloader, epochs, learning_rate):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in tqdm(range(epochs), desc=colored("Training Chinnu AI", "blue"), colour="blue"):
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

# Chat function for Chinnu AI
def chat_with_chinnu_ai(model, quantum_model, json_input):
    """
    Takes JSON data, processes it through Chinnu AI, and responds based on quantum measurements.
    Args:
        model: Trained Chinnu AI model.
        quantum_model: Trained QuantumState model.
        json_input: JSON data containing input and responses.
    Returns:
        str: Chatbot response.
    """
    try:
        # Parse JSON input
        data = json.loads(json_input)
        input_data = np.array(data.get("input", []))
        responses = data.get("responses", [])

        # Validate input and responses
        if input_data.size == 0 or not responses:
            return "Invalid input: JSON must contain an 'input' array and 'responses' list."

        # Convert input to tensor
        input_tensor = torch.tensor(input_data, dtype=torch.float)

        # Process through Chinnu AI model
        _ = model(input_tensor)

        # Measure quantum state to determine response index
        response_index = quantum_model.measure()

        # Debugging output
        print(f"Measured Response Index: {response_index}, Total Responses: {len(responses)}")

        # Return response based on measured index
        return responses[response_index % len(responses)]

    except json.JSONDecodeError:
        return "Invalid JSON format. Please provide a valid JSON string."
    except IndexError:
        return "Error: Response index is out of bounds. Check the 'responses' list."
