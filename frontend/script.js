const API_BASE = '';

const weatherIcons = {
    'clear sky': 'assets/matahari.png',
    'few clouds': 'assets/berawan.png',
    'scattered clouds': 'assets/berawan.png',
    'broken clouds': 'assets/berawan.png',
    'overcast clouds': 'assets/berawan.png',
    'light rain': 'assets/hujan.png',
    'moderate rain': 'assets/hujan.png',
    'heavy intensity rain': 'assets/hujan.png',
    'shower rain': 'assets/hujan.png',
    'rain': 'assets/hujan.png',
    'thunderstorm': 'assets/petir.png',
    'snow': 'assets/snow.png',
    'mist': 'assets/kabut.png',
    'fog': 'assets/kabut.png',
    'haze': 'assets/kabut.png'
};

const defaultIconPath = 'assets/berawan.png';

let currentFavorites = [];

// --- Weather Functions ---

async function searchWeather() {
    const city = document.getElementById('cityInput').value.trim();
    if (!city) {
        alert('Masukkan nama kota!');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/weather/current?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        displayWeather(data);
        loadForecast(city);
    } catch (error) {
        showError('Gagal mengambil data cuaca');
        console.error(error);
    }
}

// FITUR BARU: Cek cuaca dari dropdown wilayah
async function cekCuacaDariWilayah() {
    const kabSelect = document.getElementById('kabupatenSelect');
    
    if (!kabSelect.value) {
        alert('Silakan pilih Kabupaten/Kota terlebih dahulu!');
        return;
    }

    const selectedOption = kabSelect.options[kabSelect.selectedIndex];
    let cityName = selectedOption.textContent;

    cityName = cityName
        .replace(/^Kabupaten\s+/i, '')
        .replace(/^Kota\s+/i, '')
        .trim();

    document.getElementById('cityInput').value = cityName;

    const provSelect = document.getElementById('provinsiSelect');
    const provName = provSelect.options[provSelect.selectedIndex].textContent;
    document.getElementById('wilayahInfo').innerHTML = `
        🔍 Mencari cuaca untuk: <strong>${cityName}, ${provName}</strong>
    `;

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/weather/current?city=${encodeURIComponent(cityName)}`);
        const data = await response.json();

        if (data.error) {
            showError(data.error);
            document.getElementById('wilayahInfo').innerHTML = `
                ❌ Cuaca untuk ${cityName} tidak ditemukan. Coba pilih wilayah lain.
            `;
            return;
        }

        displayWeather(data);
        loadForecast(cityName);
        
        document.getElementById('wilayahInfo').innerHTML = `
            ✅ Menampilkan cuaca: <strong>${data.city}</strong>
        `;
    } catch (error) {
        showError('Gagal mengambil data cuaca');
        console.error(error);
    }
}

function displayWeather(data) {
    const iconPath = weatherIcons[data.raw_description] || defaultIconPath;

    document.getElementById('weatherDisplay').innerHTML = `
        <div class="weather-icon">
            <img src="${iconPath}" alt="${data.description}" onerror="this.src='${defaultIconPath}'" />
        </div>
        
        <div class="city-header">
            <div class="city-name">${data.city}</div>
            <button id="favoriteButton" class="btn-favorite" onclick="toggleFavorite()" title="Tambah ke favorit">
                <span class="material-symbols-outlined">star</span>
            </button>
        </div>
        <div class="temperature">${Math.round(data.temperature)}°C</div>
        `;

    // Panggil fungsi baru untuk mengecek & update tombol
    updateFavoriteButton(data.city);
}

async function loadForecast(city) {
    try {
        const response = await fetch(`${API_BASE}/api/weather/forecast?city=${encodeURIComponent(city)}`);
        const data = await response.json(); 

        if (!data.error && data.length > 0) {
            document.getElementById('forecastSection').style.display = 'block';
            
            const forecastHTML = data.map(day => {
                const iconPath = weatherIcons[day.raw_description] || defaultIconPath;

                return `
                <div class="forecast-item">
                    <div style="font-size: 0.75rem; color: #718096; font-weight: 600; margin-bottom: 12px;">${new Date(day.day).toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric', month: 'short' })}</div>
                    
                    <div class="weather-icon" style="animation: none; margin-bottom: 12px;">
                        <img src="${iconPath}" alt="${day.description}" onerror="this.src='${defaultIconPath}'" style="width: 50px; height: 50px;" />
                    </div>
                    
                    <div style="font-size: 1.25rem; font-weight: 700; color: #1a202c;">${Math.round(day.temp)}°C</div>
                    <div style="font-size: 0.75rem; color: #718096; margin-top: 8px;">${day.description}</div>
                </div>
                `;
            }).join('');
            
            document.getElementById('forecastDisplay').innerHTML = forecastHTML;
        } else if (data.error) {
            document.getElementById('forecastSection').style.display = 'none';
        }
    } catch (error) {
        document.getElementById('forecastSection').style.display = 'none';
        console.error('Error loading forecast:', error);
    }
}

// --- Chatbot Functions ---

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, timestamp: new Date().toISOString() })
        });

        const data = await response.json();
        addMessage(data.response, 'bot');
    } catch (error) {
        addMessage('Maaf, terjadi kesalahan. Coba lagi nanti.', 'bot');
        console.error(error);
    }
}

function addMessage(text, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// --- Wilayah Functions ---

async function loadProvinsi() {
    try {
        const response = await fetch(`${API_BASE}/api/wilayah/provinces`);
        const data = await response.json();

        const select = document.getElementById('provinsiSelect');
        select.innerHTML = '<option value="">Pilih Provinsi...</option>';

        data.data.forEach(prov => {
            const option = document.createElement('option');
            option.value = prov.code;
            option.textContent = prov.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading provinsi:', error);
    }
}

async function loadKabupaten() {
    const provCode = document.getElementById('provinsiSelect').value;
    const kabSelect = document.getElementById('kabupatenSelect');
    const kecSelect = document.getElementById('kecamatanSelect');
    const desaSelect = document.getElementById('desaSelect');
    const btnCekCuaca = document.getElementById('btnCekCuacaWilayah');

    kabSelect.innerHTML = '<option value="">Pilih Kabupaten/Kota...</option>';
    kecSelect.innerHTML = '<option value="">Pilih Kecamatan...</option>';
    desaSelect.innerHTML = '<option value="">Pilih Desa/Kelurahan...</option>';

    kabSelect.disabled = true;
    kecSelect.disabled = true;
    desaSelect.disabled = true;
    btnCekCuaca.disabled = true;

    if (!provCode) return;

    try {
        const response = await fetch(`${API_BASE}/api/wilayah/regencies/${provCode}`);
        const data = await response.json();

        data.data.forEach(kab => {
            const option = document.createElement('option');
            option.value = kab.code;
            option.textContent = kab.name;
            kabSelect.appendChild(option);
        });

        kabSelect.disabled = false;
    } catch (error) {
        console.error('Error loading kabupaten:', error);
    }
}

async function loadKecamatan() {
    const kabCode = document.getElementById('kabupatenSelect').value;
    const kecSelect = document.getElementById('kecamatanSelect');
    const desaSelect = document.getElementById('desaSelect');
    const btnCekCuaca = document.getElementById('btnCekCuacaWilayah');

    kecSelect.innerHTML = '<option value="">Pilih Kecamatan...</option>';
    desaSelect.innerHTML = '<option value="">Pilih Desa/Kelurahan...</option>';

    kecSelect.disabled = true;
    desaSelect.disabled = true;

    if (!kabCode) {
        btnCekCuaca.disabled = true;
        return;
    }

    btnCekCuaca.disabled = false;

    try {
        const response = await fetch(`${API_BASE}/api/wilayah/districts/${kabCode}`);
        const data = await response.json();

        data.data.forEach(kec => {
            const option = document.createElement('option');
            option.value = kec.code;
            option.textContent = kec.name;
            kecSelect.appendChild(option);
        });

        kecSelect.disabled = false;
    } catch (error) {
        console.error('Error loading kecamatan:', error);
    }
}

async function loadDesa() {
    const kecCode = document.getElementById('kecamatanSelect').value;
    const desaSelect = document.getElementById('desaSelect');

    desaSelect.innerHTML = '<option value="">Pilih Desa/Kelurahan...</option>';
    desaSelect.disabled = true;

    if (!kecCode) return;

    try {
        const response = await fetch(`${API_BASE}/api/wilayah/villages/${kecCode}`);
        const data = await response.json();

        data.data.forEach(desa => {
            const option = document.createElement('option');
            option.value = desa.code;
            option.textContent = desa.name;
            desaSelect.appendChild(option);
        });

        desaSelect.disabled = false;
    } catch (error) {
        console.error('Error loading desa:', error);
    }
}

// --- UI Utility Functions ---

// --- Favorites Functions ---

/**
 * 1. Mengambil daftar favorit dari backend
 * 2. Menyimpan ke variabel global currentFavorites
 * 3. Memanggil fungsi renderFavoritesList
 */
async function loadFavorites() {
    try {
        const response = await fetch(`${API_BASE}/api/favorites`);
        currentFavorites = await response.json();
        renderFavoritesList();
    } catch (error) {
        console.error('Gagal memuat favorit:', error);
    }
}

/**
 * 2. Menampilkan daftar favorit ke dalam <ul> di HTML
 */
function renderFavoritesList() {
    const listElement = document.getElementById('favoritesList');
    listElement.innerHTML = ''; // Kosongkan list

    if (currentFavorites.length === 0) {
        listElement.innerHTML = '<li class="empty-fav">Belum ada kota favorit.</li>';
        return;
    }

    currentFavorites.forEach(city => {
        const li = document.createElement('li');
        li.className = 'favorite-item';
        
        // Klik pada nama kota akan langsung mencari cuaca
        const span = document.createElement('span');
        span.textContent = city;
        span.onclick = () => searchFromFavorite(city);
        
        // Tombol hapus
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Hapus';
        deleteBtn.className = 'btn-delete-fav';
        deleteBtn.onclick = () => removeFavorite(city);
        
        li.appendChild(span);
        li.appendChild(deleteBtn);
        listElement.appendChild(li);
    });
}

/**
 * 3. Helper untuk mencari cuaca dari list favorit
 */
function searchFromFavorite(city) {
    document.getElementById('cityInput').value = city;
    searchWeather();
    window.scrollTo(0, 0); // Scroll ke atas halaman
}

/**
 * 4. Fungsi yang dipanggil saat tombol favorit (⭐/★) di-klik
 * Akan menambah atau menghapus berdasarkan status saat ini.
 */
async function toggleFavorite() {
    // Ambil nama kota dari tampilan cuaca
    const cityNameElement = document.querySelector('#weatherDisplay .city-name');
    if (!cityNameElement) return; // Belum ada kota yang dicari
    
    const city = cityNameElement.textContent;

    if (currentFavorites.includes(city)) {
        // Jika SUDAH ada, hapus
        await removeFavorite(city);
    } else {
        // Jika BELUM ada, tambah
        await addFavorite(city);
    }
}

/**
 * 5. Mengirim request POST untuk MENAMBAH favorit baru
 */
async function addFavorite(city) {
    try {
        await fetch(`${API_BASE}/api/favorites`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city: city })
        });
        await loadFavorites(); // Muat ulang daftar favorit
        updateFavoriteButton(city); // Perbarui tampilan tombol
    } catch (error) {
        console.error('Gagal menambah favorit:', error);
    }
}

/**
 * 6. Mengirim request DELETE untuk MENGHAPUS favorit
 */
async function removeFavorite(city) {
    try {
        await fetch(`${API_BASE}/api/favorites/${city}`, {
            method: 'DELETE'
        });
        await loadFavorites(); // Muat ulang daftar favorit
        updateFavoriteButton(city); // Perbarui tampilan tombol
    } catch (error) {
        console.error('Gagal menghapus favorit:', error);
    }
}

/**
 * 7. Memperbarui tampilan tombol favorit (⭐/★)
 */
function updateFavoriteButton(city) {
    const btn = document.getElementById('favoriteButton');
    if (!btn) return;

    if (currentFavorites.includes(city)) {
        btn.classList.add('active'); // CSS akan menangani perubahannya
        btn.title = 'Hapus dari favorit';
    } else {
        btn.classList.remove('active'); // CSS akan menangani perubahannya
        btn.title = 'Tambah ke favorit';
    }
}

function showLoading() {
    document.getElementById('weatherDisplay').innerHTML = '<div class="loading">⏳ Memuat data cuaca...</div>';
}

function showError(message) {
    document.getElementById('weatherDisplay').innerHTML = `
        <div class="error">❌ ${message}</div>
    `;
}

// --- Initialize ---

// Menggunakan 'defer' di tag script, namun 'DOMContentLoaded' tetap 
// merupakan cara yang aman untuk memastikan semua elemen HTML ada.
window.addEventListener('DOMContentLoaded', () => {
    loadProvinsi();
    loadFavorites(); // <-- TAMBAHKAN BARIS INI
    
    // Kita juga bisa memindahkan listener event dari HTML ke sini
    // agar lebih rapi (tapi ini opsional):
    
    // document.querySelector('.btn[onclick="searchWeather()"]').addEventListener('click', searchWeather);
    // document.getElementById('cityInput').addEventListener('keypress', (e) => {
    //     if (e.key === 'Enter') searchWeather();
    // });
    // ... dst ...
});