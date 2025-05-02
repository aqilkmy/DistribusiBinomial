from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

# Faktorial
def faktorial(x):
    hasil = 1
    for i in range(1, x + 1):
        hasil *= i
    return hasil

# Kombinasi 
def kombinasi(n, k):
    return faktorial(n) // (faktorial(k) * faktorial(n - k))

# Hitung distribusi binomial
def hitung_binomial(n, p, k):
    comb = kombinasi(n, k)
    prob = comb * (p ** k) * ((1 - p) ** (n - k))
    return prob

# Routing html
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Ambil nilai input dari form
        alat = request.form["alat"]
        n = int(request.form["n"])
        k = int(request.form["k"])
        pil = request.form["pil"]

        # Kondisional koin / dadu
        if alat == "koin":
            p = 0.5  # Probabilitas untuk koin (50%)
        elif alat == "dadu":
            p = 0.1667  # Probabilitas untuk dadu (1/6)

        # Hitung probabilitas berdasarkan input
        probabilitas = hitung_binomial(n, p, k)

        # Membuat grafik distribusi binomial
        x = np.arange(0, n + 1)
        temp_y = [hitung_binomial(n, p, i) for i in x]  # Probabilitas untuk setiap k
        y = [i * 100 for i in temp_y]  # Ubah ke dalam persen

        # Membuat plot
        fig, ax = plt.subplots()

        # Grafik batang
        ax.bar(x, y, color="crimson")

        # Menampilkan angka di atas batang hanya jika n <= 20
        if n <= 20:
            for i in range(len(x)):
                ax.text(x[i], y[i] + 1, f"{y[i]:.1f}%", ha='center', fontsize=8, rotation=90)

        # Menyesuaikan ukuran plot jika n terlalu besar
        if n > 30:
            fig.set_size_inches(12, 6)  # Lebarkan gambar jika n besar
        else:
            fig.set_size_inches(8, 5)

        # Styling grafik
        ax.set_title(f"Distribusi Binomial (n={n}, p={p})")
        ax.set_xlabel(f"Jumlah mendapat {pil} (k)")
        ax.set_ylabel("Presentase probabilitas (%)")
        ax.grid(True, linestyle='--', alpha=0.7)

        # Menghindari angka presentase keluar dari batas jika n besar
        max_y_value = max(y)
        if max_y_value > 30:  # Jika nilai probabilitas besar, buat sedikit ruang di atas sumbu y
            ax.set_ylim(0, max_y_value + 10)

        # Simpan gambar ke dalam base64 agar bisa ditampilkan di HTML
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()

        # Hitung probabilitas dan ubah ke persen
        presentase = probabilitas * 100

        # Kirim data ke template HTML
        return render_template("index.html", probabilitas=probabilitas, img_base64=img_base64, k=k, n=n, pil=pil, presentase=presentase)

    return render_template("index.html", probabilitas=None, img_base64=None)

if __name__ == "__main__":
    app.run(debug=True)