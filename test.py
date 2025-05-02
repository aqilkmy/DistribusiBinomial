import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

n = 100  # jumlah percobaan
p = 0.5  # peluang sukses
k_values = np.arange(0, n + 1)  # Nilai k dari 0 hingga 100
probabilities = binom.pmf(k_values, n, p)  # Hitung probabilitas untuk setiap k

# Buat grafik
plt.figure(figsize=(10, 6))
plt.bar(k_values, probabilities, color='skyblue')
plt.title(f'Distribusi Binomial (n={n}, p={p})')
plt.xlabel('Jumlah Sukses (k)')
plt.ylabel('Probabilitas')

# Menambahkan grid untuk membantu visualisasi
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Menampilkan grafik
plt.show()
