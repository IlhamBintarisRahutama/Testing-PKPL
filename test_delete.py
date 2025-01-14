from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Inisialisasi driver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Fungsi untuk membuka URL
def open_url():
    driver.get("http://pkpl.fwh.is/biodata.php?nim=2100091834")
    time.sleep(2)  # Tunggu hingga halaman dimuat

# Fungsi untuk menguji penghapusan data
def test_delete():
    try:
        # Buka halaman terlebih dahulu
        open_url()
        
        # Temukan elemen <a> dengan teks "HAPUS DATA"
        delete_link = driver.find_element(By.LINK_TEXT, "HAPUS DATA")
        
        # Klik tautan delete
        delete_link.click()
        time.sleep(2)  # Tunggu hingga proses selesai
        
        # Tangani alert (popup JavaScript)
        alert = driver.switch_to.alert
        alert_text = alert.text  # Ambil teks dari alert
        if alert_text == "Data berhasil dihapus!":
            print("Data berhasil dihapus!")
        alert.accept()  # Klik OK pada alert
        time.sleep(2)
        
        # Verifikasi apakah halaman mengarah ke list.php setelah penghapusan
        current_url = driver.current_url
        if current_url == "http://pkpl.fwh.is/list.php":
            print("Halaman berhasil diarahkan ke list.php!")
        else:
            print("Pengalihan halaman gagal!")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Menjalankan fungsi
test_delete()

# Tutup browser
driver.quit()
