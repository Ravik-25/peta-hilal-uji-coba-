from skyfield.api import load, wgs84
from skyfield import almanac
from datetime import datetime, timezone

# Load data dan timescale
eph = load('de421.bsp')
ts = load.timescale()

# Lokasi pengamatan: Semarang
lokasi_nama = "Lhokseumawe, Aceh"
latitude = 5.1881
longitude = 97.1467
lokasi = wgs84.latlon(latitude, longitude)

# Waktu prediksi
start_date = datetime(2025, 5, 1, tzinfo=timezone.utc)
end_date = datetime(2025, 5, 31, tzinfo=timezone.utc)

t0 = ts.utc(start_date)
t1 = ts.utc(end_date)

# Fungsi prediksi fase bulan
def prediksi_fase_bulan(t0, t1):
    f = almanac.moon_phases(eph)
    times, phases = almanac.find_discrete(t0, t1, f)

    hasil = []
    for t, p in zip(times, phases):
        if p == 0:  # Bulan Baru
            hasil.append((t.utc_strftime('%Y-%m-%d %H:%M'), '🌑 Bulan Baru (Potensi Rob)', lokasi_nama))
        elif p == 2:  # Bulan Purnama
            hasil.append((t.utc_strftime('%Y-%m-%d %H:%M'), '🌕 Bulan Purnama (Potensi Rob)', lokasi_nama))
    return hasil

# Jalankan prediksi
hasil_prediksi = prediksi_fase_bulan(t0, t1)

# Cetak hasil
print(f"📍 Prediksi Potensi Banjir Rob untuk Lokasi: {lokasi_nama} (Lat: {latitude}, Lon: {longitude})")
print("📅 Potensi Banjir Rob Berdasarkan Fase Bulan:")
for waktu, fase, lokasi in hasil_prediksi:
    print(f"{waktu} UTC - {fase} - di {lokasi}")
