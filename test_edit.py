from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, ElementNotInteractableException
import time
import os

# Data lama dan data baru
test_data = [
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
    },
    {
        "nim": "2200017123",
        "nama": "Maou Rimuru",
        "tempat_lahir": "Hutan Jura",
        "tanggal_lahir": "19-07-2002",
        "fakultas": "Fakultas Farmasi",
        "prodi": "Farmasi",
        "email": "test9@gmail.com",
        "no_hp": "088523716542",
        "foto": "test2.jpeg"
    }
]

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=chrome_options)

def update_data(driver, old_data, new_data):
    try:
        # Akses halaman edit
        driver.get(f"http://pkpl.fwh.is/change.php?nim={old_data['nim']}")
        
        # Tunggu form muncul dan pastikan halaman sudah siap
        wait = WebDriverWait(driver, 10)
        name_field = wait.until(EC.presence_of_element_located((By.NAME, "nama")))
        
        # Bersihkan dan isi form
        name_field.clear()
        name_field.send_keys(new_data["nama"])
        
        # Update tempat lahir
        tempat_lahir = driver.find_element(By.NAME, "tempatlahir")
        tempat_lahir.clear()
        tempat_lahir.send_keys(new_data["tempat_lahir"])
        
        # Update tanggal lahir
        tanggal_lahir = driver.find_element(By.NAME, "tanggallahir")
        tanggal_lahir.clear()
        tanggal_lahir.send_keys(new_data["tanggal_lahir"])
        
        # Update fakultas (menggunakan Select untuk dropdown)
        try:
            fakultas_select = Select(driver.find_element(By.NAME, "fakultas"))
            fakultas_select.select_by_visible_text(new_data["fakultas"])
        except:
            # Jika bukan dropdown, gunakan input biasa
            fakultas = driver.find_element(By.NAME, "fakultas")
            fakultas.clear()
            fakultas.send_keys(new_data["fakultas"])
        
        # Update prodi (menggunakan Select untuk dropdown)
        try:
            prodi_select = Select(driver.find_element(By.NAME, "prodi"))
            prodi_select.select_by_visible_text(new_data["prodi"])
        except:
            # Jika bukan dropdown, gunakan input biasa
            prodi = driver.find_element(By.NAME, "prodi")
            prodi.clear()
            prodi.send_keys(new_data["prodi"])
        
        # Update email
        email = driver.find_element(By.NAME, "email")
        email.clear()
        email.send_keys(new_data["email"])
        
        # Update no hp
        hp = driver.find_element(By.NAME, "hp")
        hp.clear()
        hp.send_keys(new_data["no_hp"])
        
        # Upload foto
        if "foto" in new_data:
            foto_path = os.path.abspath(new_data["foto"])
            if os.path.exists(foto_path):
                foto_input = driver.find_element(By.NAME, "foto")
                foto_input.send_keys(foto_path)
            else:
                print(f"File foto tidak ditemukan: {foto_path}")
        
        # Submit form
        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()
        
        # Handling alert jika muncul
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            print(f"Alert message: {alert.text}")
            alert.accept()
        except TimeoutException:
            print("Tidak ada alert yang muncul")
        
        # Tunggu konfirmasi update (bisa disesuaikan dengan kondisi website)
        time.sleep(2)  # Tunggu sebentar untuk memastikan form tersubmit
        
        # Cek apakah ada pesan sukses (sesuaikan dengan website)
        try:
            success_message = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
            )
            print("Update berhasil!")
        except TimeoutException:
            print("Tidak dapat menemukan pesan sukses, tapi form sudah tersubmit")
            
    except Exception as e:
        print(f"Error saat update data: {str(e)}")
        raise

def main():
    driver = None
    try:
        driver = setup_driver()
        update_data(driver, test_data[0], test_data[1])
    finally:
        if driver:
            time.sleep(2)  # Tunggu sebentar sebelum menutup browser
            driver.quit()

main()