HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH AUTO TEST 
I. YÊU CẦU CÀI ĐẶT NỀN TẢNG
Bạn cần cài đặt các công cụ sau theo đúng thứ tự để đảm bảo hệ thống không bị lỗi xung đột:
1.	Node.js (Bản LTS): Cần thiết để khởi chạy Appium Server.
2.	Python 3.x: Ngôn ngữ lập trình chính. Lưu ý: Khi cài đặt phải tích hợp vào biến môi trường bằng cách tích vào ô "Add Python to PATH".
3.	Android Studio:
o	Cài đặt để lấy bộ công cụ Android SDK.
o	Sử dụng Device Manager để tạo máy ảo Android (Emulator) với phiên bản Android 11 trở lên.
o	Cài đặt file APK của Hunonic vào máy ảo bằng cách kéo thả file vào màn hình máy ảo.
4.	JDK 11+: Cấu hình biến môi trường JAVA_HOME để hỗ trợ Android SDK.
________________________________________
II. CẤU HÌNH BIẾN MÔI TRƯỜNG 
Để Appium có thể điều khiển được điện thoại, bạn phải cấu hình đường dẫn SDK trong System Variables:
•	ANDROID_HOME: Đường dẫn đến thư mục SDK (Ví dụ: C:\Users\Admin\AppData\Local\Android\Sdk).
•	PATH: Thêm 2 đường dẫn con sau vào biến Path để có thể chạy lệnh từ CMD:
o	%ANDROID_HOME%\platform-tools (Dùng để chạy lệnh adb).
o	%ANDROID_HOME%\tools.
________________________________________
III. THỰC THI CÀI ĐẶT TỰ ĐỘNG 
Tại thư mục dự án, mở CMD/PowerShell và chạy các lệnh sau để cài đặt Driver và thư viện cần thiết:
Bash
# 1. Cài đặt Appium Server toàn cục
npm install -g appium

# 2. Cài đặt Driver điều khiển Android
appium driver install uiautomator2

# 3. Cài đặt thư viện Python kết nối Appium và thư viện báo cáo
pip install appium-python-client pytest pytest-html
________________________________________
IV. QUY TRÌNH CHẠY TEST CHUẨN 
Sau khi môi trường đã sẵn sàng, thực hiện theo đúng trình tự sau để tránh lỗi kết nối:
Bước 1: Khởi động Máy ảo
Mở Android Studio, bật máy ảo Android đã tạo và đảm bảo nó đã lên màn hình chính. Kiểm tra bằng lệnh adb devices trong CMD (nếu hiện danh sách thiết bị là thành công).
Bước 2: Khởi động Appium Server
Mở một cửa sổ CMD mới, gõ lệnh:
Bash
appium
Để cửa sổ này chạy ngầm suốt quá trình test tại port 4723.
Bước 3: Thực thi Script và Xuất báo cáo
Mở thêm một cửa sổ CMD nữa tại thư mục chứa file test_login_20_full.py và chạy lệnh sau để vừa chạy test vừa xuất báo cáo HTML:
Bash
py test_login_20_full.py 

