import time
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. CẤU HÌNH THƯ MỤC LƯU TRỮ
save_path = r"D:\Ảnh Test App"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 2. CẤU HÌNH APPIUM
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app_package = 'com.tuananh15352.appqly'
options.app_activity = '.MainActivity'
options.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 10)

# 3. DANH SÁCH 20 TRƯỜNG HỢP KIỂM THỬ TIẾNG VIỆT
test_scenarios = [
    {"id": "01", "name": "Dang_nhap_thanh_cong", "email": "admin@gmail.com", "pass": "123456"},
    {"id": "02", "name": "De_trong_Email", "email": "", "pass": "123456"},
    {"id": "03", "name": "De_trong_Mat_khau", "email": "admin@gmail.com", "pass": ""},
    {"id": "04", "name": "De_trong_tat_ca", "email": "", "pass": ""},
    {"id": "05", "name": "Email_sai_dinh_dang", "email": "admin.gmail.com", "pass": "123456"},
    {"id": "06", "name": "Sai_mat_khau", "email": "admin@gmail.com", "pass": "999999"},
    {"id": "07", "name": "Tai_khoan_khong_ton_tai", "email": "chua_dk@gmail.com", "pass": "123456"},
    {"id": "08", "name": "Mat_khau_qua_ngan", "email": "admin@gmail.com", "pass": "123"},
    {"id": "09", "name": "Email_chua_ky_tu_la", "email": "admin!#%@gmail.com", "pass": "123456"},
    {"id": "10", "name": "Email_co_khoang_trang_dau", "email": " admin@gmail.com", "pass": "123456"},
    {"id": "11", "name": "Email_qua_dai", "email": "a" * 50 + "@gmail.com", "pass": "123456"},
    {"id": "12", "name": "Tan_cong_SQL_Injection", "email": "' OR '1'='1", "pass": "123456"},
    {"id": "13", "name": "Email_viet_Hoa", "email": "ADMIN@GMAIL.COM", "pass": "123456"},
    {"id": "14", "name": "Mat_khau_chua_dau_cach", "email": "admin@gmail.com", "pass": "123 456"},
    {"id": "15", "name": "Mat_khau_cuc_dai", "email": "admin@gmail.com", "pass": "p" * 31},
    {"id": "16", "name": "Mat_khau_ky_tu_dac_biet", "email": "admin@gmail.com", "pass": "123@#$ABC"},
    {"id": "17", "name": "Nhan_nut_lien_tuc", "email": "admin@gmail.com", "pass": "123456"},
    {"id": "18", "name": "Email_chi_toan_so", "email": "123456789", "pass": "123456"},
    {"id": "19", "name": "Mat_khau_chua_Emoji", "email": "admin@gmail.com", "pass": "123456😊"},
    {"id": "20", "name": "Ten_mien_khong_ton_tai", "email": "admin@test.xyz123", "pass": "123456"}
]

def execute_test(case):
    print(f"\n>>> [Case {case['id']}] {case['name']}")
    try:
        # Nhập liệu bằng index để tránh lỗi text
        email_el = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')))
        email_el.clear()
        if case['email']: email_el.send_keys(case['email'])

        pass_el = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="7"]')))
        pass_el.clear()
        if case['pass']: pass_el.send_keys(case['pass'])

        # Ẩn bàn phím
        if driver.is_keyboard_shown():
            driver.hide_keyboard()
            time.sleep(1)

        # Nhấn nút (Tọa độ chuẩn 1618)
        driver.tap([(540, 1618)])
        
        # Nếu là kịch bản nhấn liên tục (Case 17)
        if case['id'] == "17":
            driver.tap([(540, 1618)])

        time.sleep(4)
        
        # Lưu ảnh vào ổ D
        file_name = os.path.join(save_path, f"KetQua_{case['id']}_{case['name']}.png")
        driver.save_screenshot(file_name)
        print(f"    -> Đã lưu: {file_name}")

        # Quay lại màn hình Login nếu đã vào Home
        if len(driver.find_elements(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Đăng nhập"]')) == 0:
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')
            time.sleep(3)

    except Exception as e:
        print(f"    -> Lỗi: {e}")

# 4. CHẠY VÒNG LẶP
try:
    for scenario in test_scenarios:
        execute_test(scenario)
finally:
    driver.quit()
    print(f"\n--- XONG! Ae xem 20 ảnh tại: {save_path} ---")