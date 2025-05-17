#mengimport modul dan data yang diperlukan
from skyfield.api import load, wgs84
from skyfield import almanac
from datetime import datetime, timezone 

#memmuat data astronomi dan waktu
eph = load('de421.bsp') #posisi planet yang di pakai di skyfield
ts =load.timescale()# waktu kalkulasi yang di pakai di astronomi 


#menentukan lokasi dan rentang wakttu 
lokasi_nama = "lhokseumawe, aceh"
latitude = 5.1881
longitude = 97.1467
lokasi = wgs84.latlon(latitude, longitude) #mendefinisikan sebuah titik lokasi di permukaan bumi

#prediksi waktu 
start_date = datetime(2025, 5, 1, tzinfo=timezone.utc) #tanggal awal
start_date = datetime(2025, 5, 31, tzinfo=timezone.utc) #tanggal akhir

t0 = ts.utc(start_date) #waktu awal
t1 = ts.utc(end_date) #waktu akhir 


