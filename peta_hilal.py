from pytz import timezone
from datetime import timedelta # mencari selisih hari
from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, sunrise_sunset, moon_phases
import numpy as np #memotong data nya dari ribuan menjadi beberapa
import matplotlib.pyplot as plt # untuk memvisualisasikan data
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
from cartopy import crs as ccrs
from cartopy.feature import NaturalEarthFeature # petanya 
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from timezonefinder import TimezoneFinder
from pytz import timezone

#IMPORT LIBRARY
ts = load.timescale()
e = load('de440s.bsp') # Menggunakan ephemeris DE440s
sun, moon, earth = e['sun'], e['moon'], e['earth']

#TENTUKAN AWAL WAKTU DAN LOKASI 
dates = ts.utc(2025, 2, 28, 0) # Tanggal 28 Maret 2025 dalam UTC
t0 = dates
t1 = dates + 1 # Perhitungan dalam rentang satu hari
latitudes = np.linspace(-12, 7, 10) # Rentang lintang Indonesia (10 titik)
longitudes = np.linspace(94, 142, 10) # Rentang bujur Indonesia (10 titik)

#Inisialisasi Array untuk Menyimpan Hasil
altitudes = np.zeros((len(latitudes), len(longitudes))) # Ketinggian Bulan
elongations = np.zeros((len(latitudes), len(longitudes))) # Elongasi Bulan
print (altitudes)

#Tentukan Zona Waktu Berdasarkan Bujur
from datetime import timedelta, tzinfo

def determine_time_zone(lon):
    offset_hours = int(lon // 15)
    class FixedOffset(tzinfo):
        def __init__(self, offset):
            self.__offset = timedelta(hours=offset)
        def utcoffset(self, dt):
            return self.__offset
        def tzname(self, dt):
            return f'UTC{offset:+d}'
        def dst(self, dt):
            return timedelta(0)
    return FixedOffset(offset_hours)
for i, lat in enumerate(latitudes):
    for j, lon in enumerate(longitudes):
        # Buat posisi pengamat berdasarkan latitude & longitude
        longlat = Topos(latitude=lat, longitude=lon)
        observer = earth + longlat

        # Cari waktu matahari terbit & terbenam
        f = sunrise_sunset(e, longlat)
        sunset_times, is_sunsets = find_discrete(t0, t1, f)

        # Pilih hanya waktu sunset (is_sunsets == False berarti sunset)
        sunset_times = sunset_times[is_sunsets == False]

        # Konversi waktu sunset ke zona waktu lokal
        local_tz = determine_time_zone(lon)
        local_sunset_times = [
            t.utc_datetime().replace(tzinfo=timezone('UTC')).astimezone(local_tz)
            for t in sunset_times
        ]

        for local_sunset_time in local_sunset_times:
            # Konversi kembali ke UTC
            local_sunset_time_utc = local_sunset_time.astimezone(timezone('UTC'))

            # Konversi ke format Skyfield Time
            skyfield_time = ts.from_datetime(local_sunset_time_utc)

            # Hitung posisi Bulan sebenarnya (geosentrik)
            true = earth.at(skyfield_time).observe(moon)

            # Hitung posisi Bulan tampak dari pengamat
            apparent = observer.at(skyfield_time).observe(moon).apparent()
            alt, az, _ = apparent.altaz()

            # Hitung elongasi geosentrik Bulan dari Matahari
            astrometric_sun = earth.at(skyfield_time).observe(sun)
            elongation = true.separation_from(astrometric_sun).degrees

            # Simpan hasil ke array
            altitudes[i, j] = alt.degrees
            elongations[i, j] = elongation

#VISUALISASI PETA 
fig = plt.figure(figsize=(10, 6)) # Ukuran peta
ax = plt.axes(projection=ccrs.PlateCarree()) # Proyeksi peta
ax.set_extent([94, 142, -12, 7], crs=ccrs.PlateCarree()) # Batas koordinat Indonesia