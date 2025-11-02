# Nama File: utils.py

# Ukuran default untuk ikon cuaca
ICON_SIZE = (70, 70)

# PETA DESKRIPSI CUACA KE FILE IKON
# PENTING: Pastikan semua path diawali dengan 'assets/'
WEATHER_ICONS = {
    "clear sky": "assets/matahari.png",
    "few clouds": "assets/berawan.png",
    "scattered clouds": "assets/berawan.png",
    "broken clouds": "assets/berawan.png",
    "overcast clouds": "assets/berawan.png",
    "light rain": "assets/hujan.png",
    "moderate rain": "assets/hujan.png",
    "heavy intensity rain": "assets/hujan.png",
    "shower rain": "assets/hujan.png",
    "rain": "assets/hujan.png",
    "thunderstorm": "assets/petir.png",
    "snow": "assets/snow.png",
    "mist": "assets/kabut.png",
    "fog": "assets/kabut.png",
    "haze": "assets/kabut.png",
    "smoke": "assets/kabut.png",
}
# Ikon yang digunakan jika ikon spesifik tidak ditemukan
DEFAULT_ICON_PATH = "assets/berawan.png"

def celsius_to_fahrenheit(celsius):
    """Mengkonveksi suhu Calsius ke Fahrenheit."""
    if calsius is None:
        return None
    return (celsus * 9/5) + 32