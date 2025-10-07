document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('calculator-form');
    // Ambil elemen pembungkus utama
    const mainContent = document.querySelector('.main-content');
    const hasilContainer = document.getElementById('hasil-container');
    const ringkasanHasil = document.getElementById('ringkasan-hasil');
    const tabelBody = document.querySelector('#hasil-tabel tbody');
    const errorContainer = document.getElementById('error-container');
    const hitungBtn = document.getElementById('hitung-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Sembunyikan hasil sebelumnya jika ada
        mainContent.classList.remove('show-results');
        hasilContainer.classList.remove('visible');
        hasilContainer.classList.add('hidden');

        hitungBtn.textContent = 'Menghitung...';
        hitungBtn.disabled = true;
        errorContainer.classList.add('hidden');
        tabelBody.innerHTML = '';

        const formData = {
            fx: document.getElementById('fx').value,
            gx: document.getElementById('gx').value,
            x0: document.getElementById('x0').value,
            toleransi: document.getElementById('toleransi').value,
            max_iter: document.getElementById('max_iter').value,
        };

        try {
            const response = await fetch('/hitung', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Terjadi kesalahan pada server.');
            }
            
            displayHasil(data);

        } catch (error) {
            errorContainer.textContent = "Terjadi Kesalahan: " + error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            hitungBtn.textContent = 'Hitung Akar';
            hitungBtn.disabled = false;
        }
    });

    function displayHasil(data) {
        ringkasanHasil.innerHTML = `Akar yang ditemukan adalah <strong>${data.akar}</strong> setelah <strong>${data.hasil.length}</strong> iterasi.`;
        
        data.hasil.forEach(iter => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${iter.iterasi}</td>
                <td>${iter.x}</td>
                <td>${iter.gx}</td>
                <td>${iter.fx}</td>
                <td>${iter.error}</td>
            `;
            tabelBody.appendChild(row);
        });

        // --- ▼▼▼ LOGIKA ANIMASI BARU ▼▼▼ ---
        // 1. Tampilkan kontainer hasil (hapus .hidden agar grid bisa melihatnya)
        hasilContainer.classList.remove('hidden');
        
        // 2. Tambahkan kelas ke pembungkus utama untuk memicu transisi grid
        mainContent.classList.add('show-results');
        
        // 3. Tambahkan kelas .visible untuk memicu animasi 'grow-in'
        hasilContainer.classList.add('visible');
    }
});
