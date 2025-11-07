🌤️ PlanPlan - Weather App Indonesia

Aplikasi Cuaca Indonesia dengan AI Assistant - Project UAS Pemrograman Python

📋 Deskripsi Project

Aplikasi web modern yang menyediakan informasi cuaca real-time untuk wilayah Indonesia. Aplikasi ini dilengkapi dengan AI Chatbot berbasis Gemini AI yang dapat menjawab pertanyaan seputar cuaca dan fenomena alam, serta integrasi dengan API Wilayah Indonesia untuk memudahkan pencarian cuaca berdasarkan lokasi administratif.

✨ Fitur Utama

🌡️ Informasi Cuaca Real-time: Data cuaca terkini dari OpenWeatherMap API

📅 Ramalan 5 Hari: Prediksi cuaca untuk 5 hari ke depan

🗺️ Pencarian Wilayah: Dropdown cascade Provinsi → Kabupaten → Kecamatan → Desa

🤖 AI Chatbot: Asisten cuaca powered by Google Gemini AI

⭐ Favorites: Simpan kota favorit untuk akses cepat

📱 Responsive Design: Tampilan modern dengan glassmorphism effect

🎨 Animated UI: Animasi smooth dan interactive elements

🎓 Informasi Tim

Mata Kuliah: Pemrograman Python

Semester: 5

Kelas: TI23A1

Dosen Pengampu: Triyono, S.Kom

👥 Anggota Kelompok

| No | Nama | NIM | Role |
| 1 | Fawwaz Gibran S. A. F | 230103021 | Project Manager & Backend |
| 2 | Alyesa Putri Aprilia | 230103007 | Backend & Dokumentasi |
| 3 | Elisabeth Puteri S. A | 230103019 | Frontend & Backend |
| 4 | Grestiana Ismi Rohkayu | 230103024 | Frontend & Backend |
| 5 | Rio Mahesa | 230103036 | Frontend |

🛠️ Teknologi yang Digunakan

Backend

Flask 3.0.0 - Web framework Python

Python 3.8+ - Bahasa pemrograman

Google Generative AI - Gemini AI untuk chatbot

Requests - HTTP library untuk API calls

Frontend

HTML5 - Struktur halaman

CSS3 - Styling dengan glassmorphism & animasi

Vanilla JavaScript - Interaktivitas dan AJAX

API External

OpenWeatherMap API - Data cuaca real-time

Wilayah.id API - Data wilayah Indonesia (Provinsi, Kabupaten, Kecamatan, Desa)

Google Gemini AI - Natural Language Processing untuk chatbot

📁 Struktur Project

project_cuaca_uas/
├── app.py                  # Main Flask application
├── api_service.py          # Service layer untuk API calls
├── data_manager.py         # Manager untuk data favorites
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── README.md               # Dokumentasi project
├── frontend/
│   └── index.html          # Main HTML page
│   └── style.css           # Style untuk HTML
│   └── script.js           # Logic
├── assets/
│   ├── matahari.png        # Weather icons
│   ├── berawan.png
│   ├── hujan.png
│   ├── petir.png
│   ├── kabut.png
│   └── snow.png
└── favorites.json          # User favorites data (auto-generated)


🚀 Cara Instalasi & Menjalankan

Prerequisites

Pastikan sudah terinstall:

Python 3.8 atau lebih tinggi

pip (Python package manager)

Langkah Instalasi

Install Dependencies

pip install -r requirements.txt


Setup API Keys
Buat file .env di root folder dan isi dengan:

OPENWEATHER_API_KEY=375e722d3184ce7b16ae59068ef9480
GEMINI_API_KEY=your_gemini_api_key_here


Untuk mendapatkan Gemini API Key:

Kunjungi: https://aistudio.google.com/app/apikey

Login dengan Google Account

Create API key dan copy

Buat Folder Frontend

mkdir frontend


Lalu copy file index.html ke dalam folder frontend/

Jalankan Aplikasi

python app.py


Aplikasi akan berjalan di: http://localhost:5000

📖 Cara Penggunaan

Mencari Cuaca Manual

Ketik nama kota di search box.

Klik tombol "Cari".

Lihat informasi cuaca dan ramalan 5 hari.

Mencari Cuaca via Dropdown Wilayah

Pilih Provinsi dari dropdown pertama.

Pilih Kabupaten/Kota dari dropdown kedua.

(Opsional) Pilih Kecamatan dan Desa.

Klik tombol "🌤️ Cek Cuaca Wilayah Ini".

Menggunakan AI Chatbot

Ketik pertanyaan di chatbox sidebar kanan.

Contoh: "Apa itu hujan tropis?" atau "Tips menghadapi musim hujan".

AI akan menjawab pertanyaan seputar cuaca.

Catatan: Chatbot hanya menjawab topik tentang cuaca dan iklim.

🔌 API Endpoints

Weather API

Get Current Weather: GET /api/weather/current?city=Jakarta

Get 5-Day Forecast: GET /api/weather/forecast?city=Jakarta

Wilayah API

Get Provinces: GET /api/wilayah/provinces

Get Regencies: GET /api/wilayah/regencies/{province_code}

Get Districts: GET /api/wilayah/districts/{regency_code}

Get Villages: GET /api/wilayah/villages/{district_code}

Chatbot API

Send Message: POST /api/chat

{
  "message": "Apa itu hujan tropis?"
}


Favorites API

Get Favorites: GET /api/favorites

Add Favorite: POST /api/favorites

{
  "city": "Jakarta"
}


Delete Favorite: DELETE /api/favorites/{city_name}

🐛 Troubleshooting

Error: Module Not Found

pip install -r requirements.txt --upgrade


Error: API Key Invalid
Pastikan file .env ada dan format benar:

GEMINI_API_KEY=AIzaSy...
OPENWEATHER_API_KEY=375e7...


Error: Port 5000 Already in Use
Edit app.py baris terakhir, ganti port:

app.run(debug=True, port=5001, host='0.0.0.0')


Chatbot Tidak Berfungsi

Cek apakah google-generativeai terinstall.

Verifikasi Gemini API key valid dan sudah diset di .env.

Cek terminal untuk log error.

Dropdown Wilayah Tidak Muncul

Pastikan koneksi internet stabil.

Cek apakah API Wilayah.id sedang down.

Buka browser console (F12) untuk lihat error.