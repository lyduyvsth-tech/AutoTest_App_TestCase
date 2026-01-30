# HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH AUTO TEST

## I. YÊU CẦU CÀI ĐẶT NỀN TẢNG
Cài đặt các công cụ sau theo đúng thứ tự để đảm bảo hệ thống không bị lỗi xung đột:
* **Node.js (Bản LTS):** Cần thiết để khởi chạy Appium Server.
* **Python 3.x:** Khi cài đặt phải tích vào ô "Add Python to PATH".
* **Android Studio:** Để lấy bộ Android SDK và tạo máy ảo Android 11+.
* **JDK 11+:** Cấu hình biến môi trường JAVA_HOME.

## II. CẤU HÌNH BIẾN MÔI TRƯỜNG
Cấu hình đường dẫn SDK trong System Variables:
* **ANDROID_HOME:** Đường dẫn đến thư mục SDK.
* **PATH:** Thêm `%ANDROID_HOME%\platform-tools` và `%ANDROID_HOME%\tools`.

## III. THỰC THI CÀI ĐẶT TỰ ĐỘNG
Mở CMD/PowerShell tại thư mục dự án và chạy các lệnh sau:

```bash
# 1. Cài đặt Appium Server toàn cục
npm install -g appium

# 2. Cài đặt Driver điều khiển Android
appium driver install uiautomator2

# 3. Cài đặt thư viện Python và báo cáo
pip install appium-python-client pytest pytest-html

IV. QUY TRÌNH CHẠY TEST CHUẨN
Thực hiện theo đúng trình tự sau để tránh lỗi kết nối:

Bước 1: Khởi động Máy ảo
Mở Android Studio, bật máy ảo và kiểm tra bằng lệnh adb devices.

Bước 2: Khởi động Appium Server
Mở một cửa sổ CMD mới, gõ lệnh:

Bash
appium
Giữ cửa sổ này chạy ngầm tại port 4723 suốt quá trình test.

Bước 3: Thực thi Script và Xuất báo cáo
Mở CMD tại thư mục chứa file script và chạy lệnh:

Bash
py test_login_20_full.py