import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import imageio

# Funcție pentru crearea unui circuit Grover
def grover_circuit(n, oracle):
    qc = QuantumCircuit(n)
    
    # 1. Inițializare în suprapunere
    qc.h(range(n))
    
    # Aplicăm Grover
    qc.append(oracle, range(n))
    
    # Operatorul de difuzie Grover
    qc.h(range(n))
    qc.append(oracle, range(n))
    qc.h(range(n))
    
    return qc

# 2. Creăm un oracol simplu (marchează |101⟩ ca soluție)
def oracle_101(n):
    qc = QuantumCircuit(n)
    qc.cz(0, 2)  # Aplica un CZ pe qubitul 2 dacă primul este 1
    return qc.to_gate(label="Oracle")

# 3. Simulăm algoritmul și salvăm probabilitățile după fiecare pas
n = 3
simulator = Aer.get_backend("aer_simulator")
oracle = oracle_101(n)

# Inițializăm probabilitățile
probabilities = []

# Generăm și rulăm circuitul pentru fiecare iterație
for i in range(4):  # 4 pași pentru a vedea evoluția
    qc = grover_circuit(n, oracle)
    qc.measure_all()
    
    # Rulăm circuitul pe simulator
    transpiled_qc = transpile(qc, simulator)
    qobj = assemble(transpiled_qc)
    result = simulator.run(qobj).result()
    counts = result.get_counts()
    
    # Salvăm probabilitățile
    probabilities.append(counts)

# 4. Creăm animația cu Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))

def update(frame):
    ax.clear()
    plot_histogram(probabilities[frame], ax=ax)
    ax.set_title(f"Step {frame + 1} of Grover's Algorithm")
    ax.set_xlabel("Quantum States", fontsize=12)
    ax.set_ylabel("Probability", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)  # Rotim etichetele X pentru lizibilitate

ani = animation.FuncAnimation(fig, update, frames=len(probabilities), interval=1000)

# 5. Salvăm animația ca GIF
ani.save("grover_animation.gif", writer="pillow")

print("GIF creat: grover_animation.gif 🎉")
