# Chinnu AI with Quantum Integration 
# Gift for my best friend 

Chinnu AI is an advanced quantum-inspired chatbot framework that combines traditional neural networks with quantum computing principles to provide intelligent and interactive user experiences.

## Features

- **Quantum State Representation:** Represent and manipulate quantum states using `QuantumState`.
- **Quantum Training:** Train quantum models using `QuantumTrainer`.
- **Deep Learning Integration:** Incorporate PyTorch models with Chinnu AI for enhanced learning capabilities.
- **JSON-based Interaction:** Live conversation with Chinnu AI using JSON input for flexibility and integration.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kalasaikamesh944/ChinnuAi.git
   cd ChinnuAi
   ```
 2. Using pip:
    ```bash
    pip install ChinnuAi
    ```

## Usage

### Training Chinnu AI

The following example demonstrates training Chinnu AI with a simple dataset:

```python
import torch
from ChinnuAi import QuantumState, QuantumTrainer, initialize_chinnu_ai, train_chinnu_ai

# Initialize Quantum State and Trainer
initial_state = [1, 0, 0, 0]
target_state = [0.5, 0.5, 0.5, 0.5]
quantum_model = QuantumState(initial_state)
quantum_trainer = QuantumTrainer(quantum_model, training_data=None)

# Initialize Neural Network
input_size = 4
hidden_size = 8
output_size = 4
model = initialize_chinnu_ai(input_size, hidden_size, output_size)

# Example Dataset
dataset = [
    (torch.tensor([1, 0, 0, 0]), torch.tensor([0.5, 0.5, 0.5, 0.5])),
    (torch.tensor([0, 1, 0, 0]), torch.tensor([0.5, 0.5, 0.5, 0.5])),
]
dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=True)

# Train the Model
epochs = 10
learning_rate = 0.01
train_chinnu_ai(model, quantum_trainer, target_state, dataloader, epochs, learning_rate)
```

### Live Conversation with Chinnu AI

Chinnu AI can interact with users through JSON input. Here is an example of a live conversation:

```python
from ChinnuAi import chat_with_chinnu_ai

# Example JSON input
json_input = '{"input": [1, 0, 0, 0], "responses": ["Welcome!", "How can I help you?", "Here is your data.", "Goodbye!"]}'
response = chat_with_chinnu_ai(model, quantum_model, json_input)
print("Chinnu AI response:", response)
```

### Quantum State Manipulation

Manipulate quantum states directly with `QuantumState`:

```python
from ChinnuAi import QuantumState

# Initialize a Quantum State
qs = QuantumState([1, 0, 0, 0])

# Apply a Quantum Gate
qs.apply_gate(QuantumGates.H)
print("State after Hadamard Gate:", qs)

# Measure the State
measurement = qs.measure()
print("Measurement Outcome:", measurement)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
