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