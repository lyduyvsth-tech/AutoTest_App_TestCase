HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH AUTO TEST 

Tài liệu này hướng dẫn chi tiết các bước thiết lập môi trường và thực thi kiểm thử tự động cho ứng dụng.

I. Yêu cầu cài đặt nền tảng 

Vui lòng cài đặt các công cụ theo đúng thứ tự dưới đây để tránh xung đột hệ thống:


Node.js (Bản LTS): Dùng để khởi chạy Appium Server.


Python 3.x: Ngôn ngữ lập trình chính.


Lưu ý: Khi cài đặt, bắt buộc tích chọn "Add Python to PATH".


JDK 11+: Cần cấu hình biến môi trường JAVA_HOME để hỗ trợ Android SDK.


Android Studio: 

Cài đặt để lấy bộ công cụ Android SDK.

Sử dụng Device Manager để tạo máy ảo (Emulator) phiên bản Android 11 trở lên.

Cài đặt file APK vào máy ảo bằng cách kéo thả file trực tiếp vào màn hình máy ảo.

II. 
Cấu hình biến môi trường 
Cấu hình các đường dẫn trong System Variables để Appium có thể điều khiển thiết bị:


ANDROID_HOME: Đường dẫn đến thư mục SDK (Ví dụ: C:\Users\Admin\AppData\Local\Android\Sdk).


PATH: Thêm 2 đường dẫn sau để chạy lệnh từ CMD:


%ANDROID_HOME%\platform-tools (Để thực thi lệnh adb).


%ANDROID_HOME%\tools.

III. 
Thực thi cài đặt tự động 
Mở CMD/PowerShell tại thư mục dự án và chạy các lệnh sau:

Bash
# 1. Cài đặt Appium Server toàn cục [cite: 20]
npm install -g appium [cite: 21]

# 2. Cài đặt Driver điều khiển Android [cite: 22]
appium driver install uiautomator2 [cite: 23]

# 3. Cài đặt thư viện Python và báo cáo [cite: 24]
pip install appium-python-client pytest pytest-html [cite: 25]
IV. 
Quy trình chạy Test chuẩn 
Thực hiện theo trình tự 3 bước sau để đảm bảo kết nối ổn định:

Bước 1: Khởi động Máy ảo 

Mở Android Studio và bật máy ảo đã tạo.

Kiểm tra kết nối bằng lệnh: adb devices.

Bước 2: Khởi động Appium Server 

Mở một cửa sổ CMD mới và chạy lệnh: 

Bash
appium [cite: 34]
Giữ cửa sổ này chạy ngầm tại port 4723 suốt quá trình test.

Bước 3: Thực thi Script và Xuất báo cáo 

Mở thêm một cửa sổ CMD tại thư mục chứa file script.

Chạy lệnh để thực thi và xuất báo cáo HTML: 

Bash
py test_login_20_full.py [cite: 39]