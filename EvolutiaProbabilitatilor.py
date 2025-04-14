import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, transpile, assemble

# Setăm numărul de qubiți
n = 3  # 3 qubiți = 8 stări posibile

# Backend de simulare
simulator = Aer.get_backend('aer_simulator')

# Oracol care marchează starea |101⟩
def oracle_101(n):
    qc = QuantumCircuit(n)
    qc.cz(0, 2)
    return qc.to_gate(label="Oracle")

# Grover step
def grover_iteration(n, oracle):
    qc = QuantumCircuit(n)
    qc.h(range(n))  # Inițializare Hadamard
    qc.append(oracle, range(n))  # Aplicare Oracol
    qc.h(range(n))
    qc.append(oracle, range(n))
    qc.h(range(n))
    return qc

# Simulare algoritm Grover pentru mai multe iterații
oracle = oracle_101(n)
iterations = 4  # Număr de iterații Grover

probabilities = []

for i in range(iterations):
    qc = grover_iteration(n, oracle)
    qc.measure_all()
    
    transpiled_qc = transpile(qc, simulator)
    qobj = assemble(transpiled_qc)
    result = simulator.run(qobj).result()
    counts = result.get_counts()
    
    # Probabilitatea stării corecte |101⟩
    prob_101 = counts.get("101", 0) / sum(counts.values())
    probabilities.append(prob_101)

# Creare grafic evoluție probabilități
plt.figure(figsize=(8,5))
plt.plot(range(1, iterations+1), probabilities, marker='o', linestyle='-', color='b', label="Grover's Algorithm")
plt.axhline(y=1/8, color='r', linestyle='--', label="Random Guess (1/N)")  # Linia de referință pentru căutare aleatoare
plt.xlabel("Number of Grover Iterations")
plt.ylabel("Probability of Correct State")
plt.title("Evolution of Probability in Grover's Algorithm")
plt.legend()
plt.grid()
plt.show()
