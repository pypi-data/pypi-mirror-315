# Kala_Quantum

**Kala_Quantum** is a Python framework designed for building and training hybrid quantum-classical AI models. This framework integrates quantum neural networks (QNNs) with classical neural networks (NNs) for advanced AI applications, such as conversational chatbots, predictive modeling, and more.

## Features

- **Quantum Neural Network (QNN):** Implements a multi-layer parameterized QNN for quantum processing.
- **Classical Neural Network (NN):** Provides classical deep learning capabilities using PyTorch.
- **Hybrid Quantum-Classical Model:** Combines quantum and classical components for integrated learning.
- **Custom Quantum Gates:** Includes predefined single-qubit gates and supports constructing tensor product gates for multi-qubit systems.
- **Extensible:** Modular design for easy customization and integration.

## Installation
```bash
   pip install Kala-Quantum
```
## Usage

### Quantum and Classical Integration
The framework allows defining a hybrid quantum-classical model:

```python
from kala_quantum import QuantumAI

# Initialize the model
quantum_ai = QuantumAI(input_size=4, n_qubits=4, n_layers=2, hidden_size=8, output_size=4)

# Example inputs
quantum_inputs = [0.5, 0.8, 1.2, 0.3]  # Quantum embeddings
classical_inputs = [0.1, 0.4, 0.7, 0.9]  # Classical features

# Predict output
outputs = quantum_ai.forward(quantum_inputs, classical_inputs)
print("Model Outputs:", outputs)
```

### Chatbot Example
Train a quantum-classical chatbot with conversational capabilities:

```python
from kala_quantum import QuantumChatBot

# Initialize chatbot model
chatbot = QuantumChatBot(input_size=4, n_qubits=4, n_layers=2, hidden_size=8, output_size=4)

# Train the model (example data required)
# chatbot.train(data, labels)

# Interact with the chatbot
response = chatbot.generate_response("Hello, how are you?")
print("Chatbot Response:", response)
```

## Contributing
We welcome contributions! Please submit issues or pull requests for improvements and fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or support, contact [saikamesh.y@gmail.com].
