import json

FAVORITES_FILE = "favorites.json"

def load_favorites():
    """Membaca daftar kota favorit dari file JSON."""
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f) # Mengembalikan list, misal: ["Jakarta", "Solo"]
    except (FileNotFoundError, json.JSONDecodeError):
            # Jika file belum ada atau isinya rusak, kembalikan list kosong
        return []
def save_favorites(city_list):
    """Menyimpan list kota favorit (yang baru) ke file JSON."""
    try:
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(city_list, f, indent=4)
    except Exception as e:
        print(f"Gagal menyimpan favorit: {e}")