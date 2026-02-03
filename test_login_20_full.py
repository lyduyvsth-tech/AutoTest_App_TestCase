import time
import os
import csv
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# ==============================================================================
# 1. CẤU HÌNH HỆ THỐNG (TỐI ƯU CAPS)
# ==============================================================================
save_path = r"D:\Ket Qua Test App"
if not os.path.exists(save_path): os.makedirs(save_path)

print(">>> Đang khởi tạo Appium Driver...")
options = UiAutomator2Options()
options.platform_name = 'Android'
options.app_package = 'com.tuananh15352.appqly'
options.app_activity = '.MainActivity'
options.no_reset = True
options.set_capability("skipDeviceInitialization", True)
options.set_capability("skipServerInstallation", True)
options.set_capability("newCommandTimeout", 300)
# [TỐI ƯU MỚI] Chặn bàn phím ảo hiện lên -> Tăng tốc độ nhập liệu cực nhanh
options.set_capability("unicodeKeyboard", True) 
options.set_capability("resetKeyboard", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 5)

# Locators (Định nghĩa sẵn để dùng lại)
LOC_EMAIL = (AppiumBy.XPATH, '//android.widget.EditText[@index="5"]')
LOC_PASS  = (AppiumBy.XPATH, '//android.widget.EditText[@index="7"]')
LOC_ANY_INPUT = (AppiumBy.XPATH, "//android.widget.EditText")

# XPath tìm lỗi
keywords = ["không được để trống", "không hợp lệ", "phải từ 6 ký tự", "tồn tại", "sai"]
xpath_query = " or ".join([f"contains(@text, '{k}')" for k in keywords])
ERROR_LOCATOR = (AppiumBy.XPATH, f"//android.widget.TextView[{xpath_query}]")

# ==============================================================================
# 2. DỮ LIỆU TEST CASE
# ==============================================================================
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

final_results = []

# ==============================================================================
# 3. HÀM HỖ TRỢ (Non-Blocking)
# ==============================================================================
def get_text_safe(locator, timeout=5):
    """Lấy text nhanh, bỏ qua lỗi Stale"""
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            # Poll every 0.3s instead of default 0.5s for speed
            el = WebDriverWait(driver, 0.3).until(EC.visibility_of_element_located(locator))
            txt = el.text
            if txt: return txt
        except: continue
    return ""

def quick_check_login_screen():
    """Check siêu tốc (0.1s) xem có ô nhập liệu không"""
    try:
        driver.find_element(*LOC_ANY_INPUT)
        return True
    except:
        return False

# ==============================================================================
# 4. LUỒNG CHẠY CHÍNH (SINGLE-PASS EXECUTION)
# ==============================================================================
def run_test_ultra_fast(case):
    print(f"[{case['id']}] {case['name']}...", end=" ", flush=True)
    status, note = "FAIL ❌", ""
    
    try:
        # --- BƯỚC 1: NHẬP LIỆU (SELF-HEALING TÍCH HỢP) ---
        inp_email = None
        try:
            # Tìm Email để nhập luôn. Nếu thấy -> Gán vào biến.
            inp_email = WebDriverWait(driver, 2).until(EC.presence_of_element_located(LOC_EMAIL))
        except:
            # Nếu không thấy (Wait 2s) -> Restart App -> Tìm lại
            # print("♻️", end="")
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')
            inp_email = wait.until(EC.presence_of_element_located(LOC_EMAIL))
        
        # Nhập Email (Dùng biến đã tìm thấy, không tìm lại)
        inp_email.clear()
        if case['email']: inp_email.send_keys(case['email'])
        
        # Nhập Pass (Tìm trực tiếp vì Email đã có thì Pass chắc chắn có)
        inp_pass = driver.find_element(*LOC_PASS)
        inp_pass.clear()
        if case['pass']: inp_pass.send_keys(case['pass'])
        
        # Không cần hide_keyboard() nữa vì đã dùng unicodeKeyboard
        
        # Click Đăng nhập
        driver.tap([(540, 1618)]) 

        # --- BƯỚC 2: KIỂM TRA KẾT QUẢ ---
        actual_result = "unknown"
        error_msg = ""

        if case['exp'] == 'login':
            # Ưu tiên bắt lỗi trước
            error_msg = get_text_safe(ERROR_LOCATOR, timeout=6) # Giảm timeout xuống 6s
            if error_msg:
                actual_result = "login"
            else:
                # Nếu không lỗi, check xem có còn ô nhập liệu không
                if quick_check_login_screen():
                    actual_result = "login" # Vẫn ở trang login nhưng ko bắt được text lỗi
                else:
                    actual_result = "home"
        else:
            # Mong đợi vào Home
            try:
                wait.until(EC.invisibility_of_element_located(LOC_ANY_INPUT))
                actual_result = "home"
            except TimeoutException:
                actual_result = "login"

        # --- BƯỚC 3: ĐÁNH GIÁ ---
        if actual_result == case['exp']:
            status = "PASS ✅"
            note = error_msg if error_msg else "OK"
        else:
            status = "FAIL ❌"
            if case['exp'] == 'login' and actual_result == 'home':
                note = "BUG: Login được dù sai data"
            else:
                note = f"Mong: {case['exp']} - Thực: {actual_result}"

        print(f"-> {status}")

        # --- BƯỚC 4: RESET ---
        if actual_result == "home":
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')

    except Exception as e:
        print(f"-> ERR: {str(e)[:30]}")
        status = "ERROR ⚠️"
        note = str(e)
        try:
            driver.terminate_app('com.tuananh15352.appqly')
            driver.activate_app('com.tuananh15352.appqly')
        except: pass

    final_results.append({"STT": case['id'], "Kịch bản": case['name'], "Kết quả": status, "Ghi chú": note})

# ==============================================================================
# 5. THỰC THI
# ==============================================================================
try:
    start_time = time.time()
    for s in test_scenarios: 
        run_test_ultra_fast(s)
    
    duration = time.time() - start_time
    
    report_file = os.path.join(save_path, "BaoCao_Ultra_Fast.csv")
    with open(report_file, mode='w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ["STT", "Kịch bản", "Kết quả", "Ghi chú"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(final_results)
        
        passes = sum(1 for x in final_results if "PASS" in x["Kết quả"])
        csv.writer(f).writerow([])
        csv.writer(f).writerow(["TỔNG", f"{duration:.1f}s", f"PASS: {passes}/{len(final_results)}"])

    print(f"\n✅ XONG! Time: {duration:.1f}s - File: {report_file}")

finally:
    driver.quit()