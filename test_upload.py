from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
import logging
import re
from datetime import datetime
import os

# Konfigurasi logging
logging.getLogger('selenium').setLevel(logging.FATAL)

# Data fakultas dan prodi yang tersedia
FAKULTAS_PRODI = {
    "Fakultas Agama Islam": ["Ilmu Hadis", "Bahasa dan Sastra Arab", "Perbankan Syariah", "Pendidikan Agama Islam"],
    "Fakultas Ekonomi dan Bisnis": ["Ekonomi Pembangunan", "Manajemen", "Akuntansi", "Bisnis Jasa Makanan"],
    "Fakultas Farmasi": ["Farmasi", "Profesi Apoteker"],
    "Fakultas Hukum": ["Ilmu Hukum"],
    "Fakultas Keguruan dan Ilmu Pendidikan": [
        "Bimbingan dan Konseling",
        "Pendidikan Bahasa dan Sastra Indonesia",
        "Pendidikan Bahasa Inggris",
        "Pendidikan Matematika",
        "Pendidikan Fisika",
        "Pendidikan Biologi",
        "Pendidikan Pancasila dan Kewarganegaraan",
        "Pendidikan Guru Sekolah Dasar",
        "Pendidikan Guru PAUD",
        "Pendidikan Profesi Guru",
        "Pendidikan Vokasional Teknologi Otomotif"
    ],
    "Fakultas Kedokteran": ["Kedokteran", "Program Profesi Dokter"],
    "Fakultas Kesehatan Masyarakat": ["Kesehatan Masyarakat"],
    "Fakultas Sains dan Teknologi Terapan": ["Matematika", "Fisika", "Sistem Informasi", "Biologi"],
    "Fakultas Psikologi": ["Psikologi"],
    "Fakultas Sastra, Budaya, dan Komunikasi": ["Sastra Inggris", "Sastra Indonesia", "Ilmu Komunikasi"],
    "Fakultas Teknologi Industri": ["Teknik Industri", "Informatika", "Teknik Kimia", "Teknik Elektro", "Teknologi Pangan"]
}

# Data test cases
test_data = [
    {
        "nim": "23456789",
        "nama": "Alice Johnson",
        "tempat_lahir": "Bandung",
        "tanggal_lahir": "2001-03-10",
        "fakultas": "Fakultas Sains dan Teknologi Terapan",
        "prodi": "Sistem Informasi",
        "email": "alice.j@example.com",
        "no_hp": "087812345678",
        "foto": "test.jpg"
    },
    # Test case data kosong
    {
        "nim": "",
        "nama": "",
        "tempat_lahir": "",
        "tanggal_lahir": "",
        "fakultas": "",
        "prodi": "",
        "email": "",
        "no_hp": "",
        "foto": ""
    },
    # Test case format invalid
    {
        "nim": "2100091834",
        "nama": "John Carmen",
        "tempat_lahir": "Bojong",
        "tanggal_lahir": "2004-05-21",
        "fakultas": "Fakultas Hukum",
        "prodi": "Ilmu Hukum",
        "email": "test@gmail.com",
        "no_hp": "082391746213",
        "foto": "test1.jpeg"
    },
    {
        "nim": "2100091833",
        "nama": "Clayman",
        "tempat_lahir": "cirebon",
        "tanggal_lahir": "2001-03-11",
        "fakultas": "Fakultas Hukum",
        "prodi": "Ilmu Hukum",
        "email": "test2@gmail.com",
        "no_hp": "087192716212",
        "foto": "test1.jpeg"
    },
    {
        "nim": "2100091839",
        "nama": "Rimuru",
        "tempat_lahir": "Jakal",
        "tanggal_lahir": "2001-05-19",
        "fakultas": "Fakultas Hukum",
        "prodi": "Ilmu Hukum",
        "email": "test3@gmail.com",
        "no_hp": "089381720451",
        "foto": "test1.jpeg"
    }
]

def validate_data(data):
    """
    Validasi data mahasiswa sebelum upload
    """
    errors = []
    
    # Validasi NIM
    if not data["nim"]:
        errors.append("NIM tidak boleh kosong")
    elif not data["nim"].isdigit():
        errors.append("NIM harus berupa angka")
    elif len(data["nim"]) != 10:
        errors.append("NIM harus 10 digit")
        
    # Validasi nama
    if not data["nama"]:
        errors.append("Nama tidak boleh kosong")
    elif not all(x.isalpha() or x.isspace() for x in data["nama"]):
        errors.append("Nama hanya boleh mengandung huruf dan spasi")
        
    # Validasi tempat lahir
    if not data["tempat_lahir"]:
        errors.append("Tempat lahir tidak boleh kosong")
    elif not all(x.isalpha() or x.isspace() for x in data["tempat_lahir"]):
        errors.append("Tempat lahir hanya boleh mengandung huruf dan spasi")
        
    # Validasi tanggal lahir
    if not data["tanggal_lahir"]:
        errors.append("Tanggal lahir tidak boleh kosong")
    else:
        try:
            datetime.strptime(data["tanggal_lahir"], '%Y-%m-%d')
        except ValueError:
            errors.append("Format tanggal lahir tidak valid (YYYY-MM-DD)")
            
    # Validasi fakultas dan prodi
    if not data["fakultas"]:
        errors.append("Fakultas tidak boleh kosong")
    elif data["fakultas"] not in FAKULTAS_PRODI:
        errors.append("Fakultas tidak valid")
    
    if not data["prodi"]:
        errors.append("Program studi tidak boleh kosong")
    elif data["fakultas"] in FAKULTAS_PRODI and data["prodi"] not in FAKULTAS_PRODI[data["fakultas"]]:
        errors.append("Program studi tidak sesuai dengan fakultas")
        
    # Validasi email
    if not data["email"]:
        errors.append("Email tidak boleh kosong")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        errors.append("Format email tidak valid")
        
    # Validasi no hp
    if not data["no_hp"]:
        errors.append("Nomor HP tidak boleh kosong")
    elif not data["no_hp"].isdigit():
        errors.append("Nomor HP harus berupa angka")
    elif len(data["no_hp"]) < 10 or len(data["no_hp"]) > 13:
        errors.append("Nomor HP harus 10-13 digit")
        
    # Validasi foto
    if not data["foto"]:
        errors.append("Foto tidak boleh kosong")
    elif not data["foto"].lower().endswith(('.png', '.jpg', '.jpeg')):
        errors.append("Format foto harus PNG atau JPG/JPEG")
        
    return errors

def test_upload(data):
    # Validasi data terlebih dahulu
    validation_errors = validate_data(data)
    if validation_errors:
        print(f"\nTest case dengan data:")
        print_test_data(data)
        print("Gagal validasi dengan error:")
        for error in validation_errors:
            print(f"- {error}")
        return False

    # Konfigurasi Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Inisialisasi driver dengan options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Buka halaman upload
        driver.get("http://pkpl.fwh.is/add.php")  # Ganti dengan URL yang sesuai
        
        # Input NIM
        nim_input = wait.until(EC.presence_of_element_located((By.ID, "nim")))
        nim_input.send_keys(data["nim"])
        
        # Input nama
        nama_input = wait.until(EC.presence_of_element_located((By.ID, "nama")))
        nama_input.send_keys(data["nama"])
        
        # Input tempat lahir
        tempat_lahir_input = wait.until(EC.presence_of_element_located((By.ID, "tempatlahir")))
        tempat_lahir_input.send_keys(data["tempat_lahir"])
        
        # Input tanggal lahir
        tanggal_lahir_input = wait.until(EC.presence_of_element_located((By.ID, "tanggallahir")))
        tanggal_lahir_input.send_keys(data["tanggal_lahir"])
        
        # Select fakultas
        fakultas_select = Select(wait.until(EC.presence_of_element_located((By.ID, "fakultas"))))
        fakultas_select.select_by_visible_text(data["fakultas"])
        
        # Select prodi
        prodi_select = Select(wait.until(EC.presence_of_element_located((By.ID, "prodi"))))
        prodi_select.select_by_visible_text(data["prodi"])
        
        # Input email
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(data["email"])
        
        # Input no hp
        no_hp_input = wait.until(EC.presence_of_element_located((By.ID, "hp")))
        no_hp_input.send_keys(data["no_hp"])
        
        # Upload foto
        if data["foto"]:
            foto_input = wait.until(EC.presence_of_element_located((By.ID, "foto")))
            foto_path = os.path.abspath(data["foto"])
            foto_input.send_keys(foto_path)
        
        # Klik tombol submit
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()
        
        print(f"\nTest case dengan data:")
        print_test_data(data)
        
        # Tangani alert jika muncul
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            
            # Cek apakah pesan alert mengindikasikan keberhasilan
            if "berhasil" in alert_text.lower():
                print(f"Status: Berhasil - {alert_text}")
                return True
            else:
                print(f"Status: Gagal - {alert_text}")
                return False
                
        except TimeoutException:
            # Tidak ada alert, cek apakah ada pesan error di halaman
            try:
                error_element = driver.find_element(By.CLASS_NAME, "error-message")
                print(f"Status: Gagal - {error_element.text}")
                return False
            except:
                print("Status: Berhasil - Data berhasil diupload")
                return True
                
    except Exception as e:
        print(f"Status: Error - {str(e)}")
        return False
    finally:
        driver.quit()

def print_test_data(data):
    """
    Mencetak data test case dengan format yang rapi
    """
    print(f"NIM: {data['nim']}")
    print(f"Nama: {data['nama']}")
    print(f"Tempat Lahir: {data['tempat_lahir']}")
    print(f"Tanggal Lahir: {data['tanggal_lahir']}")
    print(f"Fakultas: {data['fakultas']}")
    print(f"Program Studi: {data['prodi']}")
    print(f"Email: {data['email']}")
    print(f"No HP: {data['no_hp']}")
    print(f"Foto: {data['foto']}")

def run_tests():
    print("=== Memulai pengujian upload data mahasiswa ===\n")
    total_tests = len(test_data)
    successful_tests = 0
    
    # Buat direktori untuk file test jika belum ada
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
    
    for i, data in enumerate(test_data, 1):
        print(f"Test case {i} dari {total_tests}")
        if test_upload(data):
            successful_tests += 1
        print("-" * 50)
    
    print("\n=== Hasil pengujian ===")
    print(f"Total test case: {total_tests}")
    print(f"Berhasil: {successful_tests}")
    print(f"Gagal: {total_tests - successful_tests}")

if __name__ == "__main__":
    run_tests()