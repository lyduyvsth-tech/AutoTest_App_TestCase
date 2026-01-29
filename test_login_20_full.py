import time
import os
import csv
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. THIẾT LẬP HỆ THỐNG
save_path = r"D:\Ảnh Test App"
if not os.path.exists(save_path): os.makedirs(save_path)

options = UiAutomator2Options()
options.platform_name = 'Android'
options.app_package = 'com.tuananh15352.appqly'
options.app_activity = '.MainActivity'
options.no_reset = True
# Tối ưu khởi động
options.set_capability("skipDeviceInitialization", True)
options.set_capability("skipServerInstallation", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 10)
final_results = []

# 2. DANH SÁCH 20 KỊCH BẢN KIỂM THỬ
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
    {"id": "10", "name": "Email có khoảng trắng đầu", "email": " admin@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "11", "name": "Email quá dài", "email": ("a"*50)+"@gmail.com", "pass": "123456", "exp": "login"},
    {"id": "12", "name": "Tấn công SQL Injection", "email": "' OR '1'='1", "pass": "123456", "exp": "login"},
    {"id": "13", "name": "Email viết Hoa", "email": "ADMIN@GMAIL.COM", "pass": "123456", "exp": "home"},
    {"id": "14", "name": "Mật khẩu chứa dấu cách", "email": "admin@gmail.com", "pass": "123 456", "exp": "login"},
    {"id": "15", "name": "Mật khẩu cực dài", "email": "admin@gmail.com", "pass": "p"*31, "exp": "login"},
    {"id": "16", "name": "Mật khẩu ký tự đặc biệt", "email": "admin@gmail.com", "pass": "123@#$ABC", "exp": "home"},
    {"id": "17", "name": "Nhấn nút liên tục", "email": "admin@gmail.com", "pass": "123456", "exp": "home"},
    {"id": "18", "name": "Email chỉ toàn số", "email": "123456789", "pass": "123456", "exp": "login"},
    {"id": "19", "name": "Mật khẩu chứa Emoji", "email": "admin@gmail.com", "pass": "123456😊", "exp": "login"},
    {"id": "20", "name": "Tên miền không tồn tại", "email": "admin@test.xyz123", "pass": "123456", "exp": "login"}
]

def run_test(case):
    print(f"\n>>> Thực thi Case {case['id']}: {case['name']}")
    status, note = "FAIL ❌", ""
    try:
        # Nhập liệu
        e = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')))
        p = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@index="7"]')
        e.clear(); e.send_keys(case['email'])
        p.clear(); p.send_keys(case['pass'])
        if driver.is_keyboard_shown(): driver.hide_keyboard()
        
        driver.tap([(540, 1618)]) # Tọa độ nút Đăng nhập
        time.sleep(3) 

        # --- LOGIC NHẬN DIỆN LỖI TRỰC QUAN ---
        # Tìm tất cả TextView để lấy thông báo lỗi thực tế
        all_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        error_msg = ""
        # Danh sách từ khóa báo lỗi thực tế từ app của bạn
        keywords = ["không được để trống", "không hợp lệ", "phải từ 6 ký tự"]
        
        for t in all_texts:
            for key in keywords:
                if key in t.text:
                    error_msg = t.text # Lấy đúng dòng thông báo đỏ
                    break

        # Kiểm tra đang ở đâu
        is_login = len(driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Đăng nhập')]")) > 0
        actual = "login" if is_login else "home"

        # SO SÁNH THÔNG MINH (ASSERTION)
        if actual == case['exp']:
            status = "PASS ✅"
            note = error_msg if error_msg else "Hệ thống xử lý chính xác"
        else:
            status = "FAIL ❌"
            note = f"BUG: Vẫn có thể {case['exp']} vào app"

        # Chụp ảnh và Reset
        driver.save_screenshot(os.path.join(save_path, f"{case['id']}_{case['name']}.png"))
        if actual == "home":
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')))

    except Exception as err:
        note = f"Lỗi kỹ thuật: {str(err)[:40]}"
    
    final_results.append({"STT": case['id'], "Kịch bản": case['name'], "Kết quả": status, "Ghi chú": note})

# 3. THỰC THI & TỔNG KẾT
try:
    for s in test_scenarios: run_test(s)
    
    # Xuất file Excel (.csv) chuẩn tiếng Việt
    report_file = os.path.join(save_path, "BaoCao_Test_Login.csv")
    with open(report_file, mode='w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=["STT", "Kịch bản", "Kết quả", "Ghi chú"])
        w.writeheader()
        w.writerows(final_results)
        # Ghi thống kê
        total = len(final_results)
        passes = sum(1 for x in final_results if "PASS" in x["Kết quả"])
        csv.writer(f).writerow([])
        csv.writer(f).writerow(["TỔNG CỘNG", f"PASS: {passes}", f"FAIL: {total-passes}", f"TỶ LỆ: {(passes/total)*100:.1f}%"])

    print(f"\n✅ Đã hoàn thành! Báo cáo tại: {report_file}")
finally:
    driver.quit()