import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

class QuantumGates:
    @staticmethod
    def tensor_gate(single_qubit_gate, num_qubits, target_qubit):
        # Ensures the number of qubits and target qubit index are valid
        if num_qubits <= 0:
            raise ValueError("Number of qubits must be greater than zero.")
        if target_qubit >= num_qubits:
            raise ValueError("Target qubit index exceeds the number of qubits.")

        # Create identity gates for all qubits, replacing the target qubit gate
        gates = [np.eye(2) for _ in range(num_qubits)]
        gates[target_qubit] = single_qubit_gate

        # Compute the full tensor product of gates
        full_gate = gates[0]
        for gate in gates[1:]:
            full_gate = np.kron(full_gate, gate)
        return full_gate

    # Predefined single-qubit gates
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

    @staticmethod
    def RX(theta):
        # Rotation around the X-axis by angle theta
        return np.array([
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)]
        ])

    @staticmethod
    def RY(theta):
        # Rotation around the Y-axis by angle theta
        return np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)]
        ])

    @staticmethod
    def RZ(theta):
        # Rotation around the Z-axis by angle theta
        return np.array([
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)]
        ])


class QuantumCircuit:
    def __init__(self, num_qubits):
        # Initialize the quantum circuit with a specified number of qubits
        self.num_qubits = num_qubits
        self.state_vector = np.zeros(2 ** num_qubits, dtype=complex)
        self.state_vector[0] = 1.0  # Start in the |0...0> state

    def apply_gate(self, gate, target_qubit):
        # Apply a single-qubit gate to the specified qubit
        full_gate = QuantumGates.tensor_gate(gate, self.num_qubits, target_qubit)
        self.state_vector = np.dot(full_gate, self.state_vector)

    def measure(self):
        # Measure the quantum state, collapsing it to a single basis state
        probabilities = np.abs(self.state_vector) ** 2
        outcome = np.random.choice(len(self.state_vector), p=probabilities)
        self.state_vector = np.zeros_like(self.state_vector)
        self.state_vector[outcome] = 1.0
        return outcome


class QuantumNeuralNetwork:
    def __init__(self, n_qubits, n_layers):
        # Initialize a parameterized quantum neural network
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.params = np.random.uniform(0, 2 * np.pi, (n_layers, n_qubits))

    def forward(self, inputs):
        # Forward pass through the quantum neural network
        qc = QuantumCircuit(self.n_qubits)

        # Apply input data as rotations on the qubits
        for i, inp in enumerate(inputs):
            qc.apply_gate(QuantumGates.RY(inp), target_qubit=i)

        # Apply parameterized rotations for each layer
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                qc.apply_gate(QuantumGates.RY(self.params[layer, qubit]), target_qubit=qubit)
        return np.abs(qc.state_vector) ** 2

    def predict(self, inputs):
        # Predict the class based on the highest probability
        probabilities = self.forward(inputs)
        return np.argmax(probabilities)


class ClassicalNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ClassicalNN, self).__init__()
        # Define the layers of the classical neural network
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Forward pass through the classical neural network
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


class QuantumAI:
    def __init__(self, input_size, n_qubits, n_layers, hidden_size, output_size):
        # Combine quantum and classical models
        self.qnn = QuantumNeuralNetwork(n_qubits, n_layers)
        self.classical_model = ClassicalNN(input_size, hidden_size, output_size)

    def forward(self, quantum_inputs, classical_inputs):
        # Forward pass through quantum and classical components
        quantum_outputs = self.qnn.forward(quantum_inputs)
        classical_outputs = self.classical_model(torch.tensor(classical_inputs, dtype=torch.float32))
        # Combine outputs from quantum and classical models
        combined_outputs = torch.cat((torch.tensor(quantum_outputs, dtype=torch.float32), classical_outputs), dim=0)
        return combined_outputs

    def predict(self, quantum_inputs, classical_inputs):
        # Predict the class based on combined model outputs
        outputs = self.forward(quantum_inputs, classical_inputs)
        return torch.argmax(outputs, dim=0).item()


# Existing QuantumGates, QuantumCircuit, QuantumNeuralNetwork, ClassicalNN, and QuantumAI classes remain the same.

class QuantumChatBot(QuantumAI):
    def __init__(self, input_size, n_qubits, n_layers, hidden_size, output_size):
        super(QuantumChatBot, self).__init__(input_size, n_qubits, n_layers, hidden_size, output_size)
        self.responses = ["Hello! How can I help you?", 
                          "I'm here to assist you.", 
                          "Goodbye! Take care.", 
                          "Let me look into that for you."]

    def process_input(self, text):
        """
        Converts text input into embeddings for quantum and classical processing.
        """
        quantum_input = np.random.uniform(0, np.pi, 4)  # Simulated quantum embedding
        classical_input = np.random.uniform(0, 1, 4)  # Simulated classical embedding
        return quantum_input, classical_input

    def generate_response(self, quantum_inputs, classical_inputs):
        """
        Generates a chatbot response based on model predictions.
        """
        response_index = self.predict(quantum_inputs, classical_inputs)
        return self.responses[response_index]

if __name__ == "__main__":
    # Training setup remains the same
    quantum_data = [np.random.uniform(0, np.pi, 4) for _ in range(100)]
    classical_data = [np.random.uniform(0, 1, 4) for _ in range(100)]
    labels = [np.random.randint(0, 4) for _ in range(100)]

    chatbot = QuantumChatBot(input_size=4, n_qubits=4, n_layers=2, hidden_size=8, output_size=4)

    optimizer = optim.Adam(chatbot.classical_model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    for epoch in tqdm(range(10), desc="Training Chatbot"):
        total_loss = 0
        for classical_inputs, target in zip(classical_data, labels):
            classical_inputs = torch.tensor(classical_inputs, dtype=torch.float32)
            target = torch.tensor([target], dtype=torch.long)

            optimizer.zero_grad()
            outputs = chatbot.classical_model(classical_inputs)
            loss = criterion(outputs.unsqueeze(0), target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        print(f"Epoch {epoch + 1}: Loss = {total_loss / len(classical_data):.4f}")

    # Interactive chatbot mode
    print("Chatbot is ready! Type your message or 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        q_input, c_input = chatbot.process_input(user_input)
        response = chatbot.generate_response(q_input, c_input)
        print(f"Chatbot: {response}")