import time
import os
import csv
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. KHỞI TẠO HỆ THỐNG 
save_path = r"D:\Ảnh Test App"
if not os.path.exists(save_path): os.makedirs(save_path)

options = UiAutomator2Options()
options.platform_name = 'Android'
options.app_package = 'com.tuananh15352.appqly'
options.app_activity = '.MainActivity'
options.no_reset = True
# Tối ưu khởi động: Bỏ qua các bước kiểm tra thừa của Appium
options.set_capability("skipDeviceInitialization", True)
options.set_capability("skipServerInstallation", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 8) # Đợi tối ưu để xử lý nhanh 
final_results = []

# 2. DỮ LIỆU KIỂM THỬ (20 Cases + Kết quả mong đợi) 
test_scenarios = [
    {"id": "01", "name": "Đăng nhập thành công", "email": "admin@gmail.com", "pass": "123456", "exp": "home"},
    {"id": "02", "name": "Để trống Email", "email": "", "pass": "123456", "exp": "login"},
    {"id": "03", "name": "Để trống Mật khẩu", "email": "admin@gmail.com", "pass": "", "exp": "login"},
    {"id": "04", "name": "Để trống tất cả", "email": "", "pass": "", "exp": "login"},
    {"id": "05", "name": "Email sai định dạng", "email": "admin.gmail.com", "pass": "123456", "exp": "login"},
    {"id": "06", "name": "Sai mật khẩu", "email": "admin@gmail.com", "pass": "999999", "exp": "login"},
    {"id": "07", "name": "Tài khoản không tồn tại", "email": "chua_dk@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "08", "name": "Mật khẩu quá ngắn", "email": "admin@gmail.com", "pass": "123", "exp": "login"},
    {"id": "09", "name": "Email chứa ký tự lạ", "email": "admin!#%@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "10", "name": "Email có khoảng trắng", "email": " admin@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "11", "name": "Email quá dài", "email": ("a"*50)+"@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "12", "name": "SQL Injection", "email": "' OR '1'='1", "pass": "123456", "exp": "login"},
    {"id": "13", "name": "Email viết Hoa", "email": "ADMIN@GMAIL.COM", "pass": "123456", "exp": "home"},
    {"id": "14", "name": "Pass chứa dấu cách", "email": "admin@gmail.com", "pass": "123 456", "exp": "login"},
    {"id": "15", "name": "Mật khẩu cực dài", "email": "admin@gmail.com", "pass": "p"*31, "exp": "login"},
    {"id": "16", "name": "Pass ký tự đặc biệt", "email": "admin@gmail.com", "pass": "123@#$", "exp": "home"},
    {"id": "17", "name": "Nhấn nút liên tục", "email": "admin@gmail.com", "pass": "123456", "exp": "home"},
    {"id": "18", "name": "Email chỉ toàn số", "email": "12345678", "pass": "123456", "exp": "login"},
    {"id": "19", "name": "Pass chứa Emoji", "email": "admin@gmail.com", "pass": "123456😊", "exp": "login"},
    {"id": "20", "name": "Tên miền không tồn tại", "email": "admin@test.xyz", "pass": "123456", "exp": "login"}
]

def run_test(case):
    print(f"\n>>> Case {case['id']}: {case['name']}")
    status, note = "FAIL ❌", ""
    try:
        # Tương tác nhanh bằng XPATH Index 
        e = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')))
        p = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@index="7"]')
        e.clear(); e.send_keys(case['email'])
        p.clear(); p.send_keys(case['pass'])

        if driver.is_keyboard_shown(): driver.hide_keyboard()
        
        driver.tap([(540, 1618)]) # Tọa độ nút chuẩn 
        if case['id'] == "17": driver.tap([(540, 1618)])
        time.sleep(2.5) # Đợi xử lý tối ưu

        # Kiểm tra thực tế vs Mong đợi (Assertion)
        is_login = len(driver.find_elements(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Đăng nhập"]')) > 0
        actual = "login" if is_login else "home"

        if actual == case['exp']:
            status = "PASS ✅"
            note = f"Đúng: App ở lại {actual}" if actual == "login" else "Đăng nhập thành công"
        else:
            status = "FAIL ❌"
            note = f"BUG: Mong không {case['exp']} được nhưng app lại vào {actual}"

        # Chụp ảnh và Reset app thông minh 
        driver.save_screenshot(os.path.join(save_path, f"{case['id']}_{case['name']}.png"))
        if actual == "home":
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')))

    except Exception as err:
        note = f"Lỗi: {str(err)[:40]}"
    
    final_results.append({"STT": case['id'], "Kịch bản": case['name'], "Kết quả": status, "Ghi chú": note})

# 3. THỰC THI, THỐNG KÊ & XUẤT BÁO CÁO 
try:
    for s in test_scenarios: run_test(s)

    # Tính toán số liệu cho báo cáo cuối khóa
    total = len(final_results)
    passes = sum(1 for x in final_results if "PASS" in x["Kết quả"])
    fails = total - passes
    rate = (passes / total) * 100

    # Xuất file Excel (.csv) chuẩn 
    report_file = os.path.join(save_path, "BaoCao_HoanHao_Hunonic.csv")
    with open(report_file, mode='w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=["STT", "Kịch bản", "Kết quả", "Ghi chú"])
        w.writeheader(); w.writerows(final_results)
        csv.writer(f).writerow([])
        csv.writer(f).writerow(["TỔNG KẾT", f"PASS: {passes}", f"FAIL: {fails}", f"TỶ LỆ: {rate:.1f}%"])

    print("\n" + "="*55)
    print(f"📊 KẾT QUẢ: {passes}/{total} PASS | Tỷ lệ: {rate:.1f}%")
    print(f"📁 Minh chứng và Báo cáo tại: {save_path}")
    print("="*55)

finally:
    driver.quit()