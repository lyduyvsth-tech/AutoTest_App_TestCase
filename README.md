# [cite_start]HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH AUTO TEST [cite: 1]

[cite_start]Tài liệu này hướng dẫn chi tiết các bước thiết lập môi trường và thực thi kiểm thử tự động cho ứng dụng[cite: 3].

## [cite_start]I. YÊU CẦU CÀI ĐẶT NỀN TẢNG [cite: 2]
[cite_start]Cài đặt các công cụ sau theo đúng thứ tự để đảm bảo hệ thống không bị lỗi xung đột[cite: 3]:

* [cite_start]**Node.js (Bản LTS):** Cần thiết để khởi chạy Appium Server[cite: 4].
* **Python 3.x:** Ngôn ngữ lập trình chính. [cite_start]Lưu ý: Khi cài đặt phải tích vào ô **"Add Python to PATH"**[cite: 5].
* [cite_start]**Android Studio:** [cite: 6]
    * [cite_start]Cài đặt để lấy bộ công cụ **Android SDK**[cite: 7].
    * [cite_start]Sử dụng **Device Manager** để tạo máy ảo Android (Emulator) với phiên bản Android 11 trở lên[cite: 8].
    * [cite_start]Cài đặt file APK vào máy ảo bằng cách kéo thả file vào màn hình máy ảo[cite: 9].
* [cite_start]**JDK 11+:** Cấu hình biến môi trường `JAVA_HOME` để hỗ trợ Android SDK[cite: 10].

## II. [cite_start]CẤU HÌNH BIẾN MÔI TRƯỜNG [cite: 11]
[cite_start]Cấu hình đường dẫn SDK trong **System Variables** để Appium có thể điều khiển thiết bị[cite: 12]:

1. [cite_start]**ANDROID_HOME:** Đường dẫn đến thư mục SDK (Ví dụ: `C:\Users\Admin\AppData\Local\Android\Sdk`)[cite: 13].
2. [cite_start]**PATH:** Thêm 2 đường dẫn con sau để chạy lệnh từ CMD[cite: 14]:
    * [cite_start]`%ANDROID_HOME%\platform-tools` (Dùng để chạy lệnh `adb`)[cite: 15].
    * [cite_start]`%ANDROID_HOME%\tools`[cite: 16].

## III. [cite_start]THỰC THI CÀI ĐẶT TỰ ĐỘNG [cite: 17]
[cite_start]Tại thư mục dự án, mở CMD/PowerShell và chạy các lệnh sau để cài đặt Driver và thư viện cần thiết[cite: 18]:

```bash
# 1. Cài đặt Appium Server toàn cục
npm install -g appium

# 2. Cài đặt Driver điều khiển Android
appium driver install uiautomator2

# 3. Cài đặt thư viện Python kết nối Appium và thư viện báo cáo
pip install appium-python-client pytest pytest-html
[cite_start]``` [cite: 21, 23, 25]

---

## IV. [cite_start]QUY TRÌNH CHẠY TEST CHUẨN [cite: 26]
[cite_start]Thực hiện theo đúng trình tự sau để tránh lỗi kết nối[cite: 27]:

### [cite_start]Bước 1: Khởi động Máy ảo [cite: 28]
* [cite_start]Mở **Android Studio**, bật máy ảo Android đã tạo và đảm bảo nó đã lên màn hình chính[cite: 29].
* Kiểm tra bằng lệnh `adb devices` trong CMD (nếu hiện danh sách thiết bị là thành công)[cite: 30].

### Bước 2: Khởi động Appium Server [cite: 31]
Mở một cửa sổ CMD mới và chạy lệnh:
```bash
appium
``` [cite: 34]
* [cite_start]**Lưu ý:** Để cửa sổ này chạy ngầm suốt quá trình test tại port **4723**[cite: 35].

### [cite_start]Bước 3: Thực thi Script và Xuất báo cáo [cite: 36]
[cite_start]Mở thêm một cửa sổ CMD nữa tại thư mục chứa file `test_login_20_full.py` và chạy lệnh sau để vừa chạy test vừa xuất báo cáo HTML[cite: 37]:
```bash
py test_login_20_full.py
[cite_start]``` [cite: 39]