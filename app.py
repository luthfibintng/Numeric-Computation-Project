from flask import Flask, request, jsonify, render_template
import numpy as np
import traceback

app = Flask(__name__)

# Fungsi untuk mengevaluasi ekspresi matematika yang aman
def safe_eval(expr, x_val):
    """Mengevaluasi ekspresi f(x) dengan aman."""
    allowed_names = {
        "x": x_val,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs
    }
    allowed_names.update(np.__dict__)
    
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Penggunaan '{name}' tidak diizinkan.")
    return eval(code, {"__builtins__": {}}, allowed_names)

@app.route('/')
def index():
    """Menampilkan halaman utama."""
    return render_template('index.html')

@app.route('/hitung', methods=['POST'])
def hitung():
    """Endpoint untuk melakukan perhitungan iterasi."""
    try:
        data = request.json
        fx_str = data['fx']
        gx_str = data['gx']
        x0 = float(data['x0'])
        toleransi = float(data['toleransi'])
        max_iter = int(data['max_iter'])

        hasil_iterasi = []
        x_sekarang = x0
        
        for i in range(1, max_iter + 1):
            # Hitung g(x) untuk iterasi berikutnya
            x_berikutnya = safe_eval(gx_str, x_sekarang)
            
            # --- PERUBAHAN DIMULAI DI SINI ---
            # Cek apakah hasilnya bilangan kompleks
            if isinstance(x_berikutnya, complex):
                # Jika ya, hentikan iterasi dan kirim pesan error yang jelas
                raise ValueError(
                    f"Pada iterasi ke-{i}, perhitungan g(x) menghasilkan bilangan kompleks: {x_berikutnya}.\n"
                    "Ini biasanya terjadi karena akar dari bilangan negatif. Periksa kembali fungsi g(x) atau tebakan awal Anda."
                )
            
            # Hitung f(x)
            fx_val = safe_eval(fx_str, x_sekarang)
            # --- PERUBAHAN SELESAI ---

            # Hitung galat (error)
            error = abs(x_berikutnya - x_sekarang)
            
            hasil_iterasi.append({
                "iterasi": i,
                "x": round(x_sekarang, 6),
                "gx": round(x_berikutnya, 6),
                "fx": round(fx_val.real, 6), # Tampilkan bagian real dari f(x) jika kompleks
                "error": round(error, 6)
            })

            if error < toleransi:
                break
            
            x_sekarang = x_berikutnya
        
        return jsonify({"hasil": hasil_iterasi, "akar": round(x_sekarang, 6)})

    except Exception as e:
        # Mengembalikan pesan error yang lebih informatif
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
