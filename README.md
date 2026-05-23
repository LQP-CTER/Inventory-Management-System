# He Thong Quan Ly Kho Hang (Inventory Management System - IMS)

Day la mot ung dung Desktop chuyen nghiep duoc phat trien tren ngon ngu Python, su dung thu vien CustomTkinter de xay dung giao dien nguoi dung hien dai, SQLAlchemy ORM lam trinh ket noi co so du lieu va SQLite cho muc dich luu tru noi bo. He thong duoc thiet ke toi uu de quan ly thong tin hang hoa, nha cung cap, hoat dong xuat/nhap/chuyen kho, cung nhu dong bo hoa du lieu theo quy trinh duyet phieu nghiem ngat.

## Phien Ban Nang Cap Enterprise (Phase 6 & Phase 7)

Phien ban hien tai cua he thong da duoc nang cap toan dien duoi goc nhin cua Chuyen vien Phan tich Nghiep vu (Business Analyst - BA) va Chuyen gia Thiet ke Trai nghiem Nguoi dung (UI/UX Designer).

### 1. Duoi Goc Nhin Business Analyst (BA) - Logic Nghiep Vu

- Quy trinh duyet phieu hai buoc (Transaction Approval Workflow):
  - Cac giao dich Nhap kho (Inbound) va Xuat kho (Outbound) ban dau khi duoc khoi tao boi nhan vien se o trang thai Draft (Nhap). Cac giao dich nay chua tac dong den so luong ton kho thuc te.
  - Quan tri vien (Admin) co quyen truy cap vao tab Transactions de kiem tra va phe duyet (Approve).
  - Khi duoc phe duyet, trang thai chuyen thanh Completed, luc nay so luong hang hoa va gia tri tai san moi duoc chinh thuc cap nhat vao so ton kho.

- Dinh gia ton kho (Inventory Valuation):
  - Ap dung phuong phap Binh quan gia quyen (Weighted Average Cost) de tinh toan chinh xac gia tri hang ton kho thoi gian thuc tren Dashboard tong.
  - Cac phieu Xuat kho (Outbound) tu dong trich xuat gia von trung binh hien tai de ghi nhan gia tri xuat kho chinh xac, giup de dang doi soat tai chinh va ngan ngua sai sot.

- Nhat ky kiem toan he thong (System Audit Logs):
  - Tich hop tab Audit Logs chuyen dung danh rieng cho tai khoan Admin.
  - Ghi lai chi tiet moi hanh dong trong he thong bao gom: dang nhap, tao tai khoan, them/sua san pham, thay doi trang thai va phe duyet giao dich. Moi thong tin duoc luu lai kem dinh danh nguoi dung, phan he bi anh huong va thoi gian thuc hien chinh xac den tung giay.

### 2. Duoi Goc Nhin UI/UX Designer - Trai Nghiem Nguoi Dung

- Thanh dieu huong Sidebar linh hoat (Responsive Sidebar):
  - Tich hop nut Hamburger Menu o goc trai tren cung cho phep thu gon hoac mo rong Sidebar linh hoat.
  - Khi Sidebar duoc thu gon, chu thich bang chu se bien mat va chi hien thi phan ky tu viet tat/icon dai dien, giup mo rong toi da khong gian hien thi cac bang du lieu lon va dashboard phuc tap.

- Cong cu tim kiem va bo loc thoi gian thuc (Real-time Search):
  - Cac phan he quan ly san pham (Products) va xem ton kho (Inventory View) da duoc trang bi thanh tim kiem thoi gian thuc. Duyen sach duoc tu dong loc va hien thi ngay khi nguoi dung nhap tung ky tu ma khong can nhan Enter hay click tim kiem.
  - Phai transactions ho tro bo loc chuyen nghiep theo loai phieu va theo trang thai (Draft / Completed).

- He thong thong bao Toast (Toast Notifications):
  - Thay the toan bo cac popup messagebox canh bao gay gian doan phien lam viec bang he thong thong bao Toast trượt muot ma tu phia duoi ben phai man hinh.
  - Cac Toast message co mau xanh bieu thi thanh cong va mau do bieu thi loi, tu dong bien mat sau 3 giay de giu luong cong viec luon lien mach.

- Hieu ung Mica/Acrylic:
  - Tan dung thu vien pywinstyles tren Windows de tao ra lop nen trong suot khuech tan (glassmorphism) cho cua so dang nhap, nang tam tham my cho ung dung desktop.

## Co So Du Lieu va Mo Hinh Entity (Database Schema)

He thong hoat dong tren 9 bang co so du lieu chinh thong qua engine SQLite va SQLAlchemy:

1. users: Luu tru tai khoan, mat khau va phan quyen truy cap (Admin hoac Employee).
2. employees: Thong tin nhan su trong to chuc.
3. inventory: Danh muc san pham chi tiet.
4. inventory_category: Cac nhom phan loai san pham.
5. suppliers: Thong tin nha cung cap hang hoa.
6. warehouses: Danh sach cac kho hang ma he thong quan ly.
7. inventory_transaction: Nhat ky chung ve cac giao dich kho.
8. inventory_transaction_detail: Chi tiet cac dong mat hang thuoc ve mot giao dich.
9. inventory_balance: So ton va gia tri kho (luu tru luong ton dau ky, luong nhap, luong xuat va cac moc don gia/gia tri tai san).
10. audit_logs: Nhat ky ghi vet kiem toan thao tac nguoi dung.

## Cau Truc Thu Muc Du An

- main.py: Diem khoi chay chinh cua ung dung, thuc hien phan luong login va load dashboard tuong ung.
- inventory_management.py: Khai bao cac lop ORM bang SQLAlchemy, thiet lap quan he gia cac bang va khoi tao co so du lieu ban dau.
- db_adapter.py: Adapter quan ly ket noi va thao tac co so du lieu thuan tuy SQL/SQLAlchemy.
- widget_adapters.py: Cac ham ho tro tuong thich giua cac widget trong giao dien CustomTkinter.
- ui_login.py: Giao dien man hinh dang nhap hien dai voi hieu ung Glassmorphism.
- ui_admin_dashboard.py: Khung dashboard chinh cua phan he quan tri, chiu trach nhiem tich hop Sidebar va quan ly dieu huong tab.
- ui_components.py: Cac component dung chung nhu ToastNotification, Sidebar, cac o nhap lieu dac thu.
- ui_dashboard_tab.py: Tab bao cao tong quan, bieu do, gia tri ton kho va thong ke.
- ui_products_tab.py: Tab danh muc san pham va cong cu tim kiem thoi gian thuc.
- ui_inventory_tab.py: Tab theo doi so ton kho thoi gian thuc o cac kho.
- ui_inbound_tab.py: Giao dien tao phieu nhap kho o trang thai Draft.
- ui_outbound_tab.py: Giao dien tao phieu xuat kho o trang thai Draft.
- ui_transactions_tab.py: Giao dien quan ly, loc va phe duyet phieu cua Admin.
- ui_transfer_tab.py: Giao dien thuc hien dieu chuyen noi bo giua cac kho.
- ui_users_tab.py: Quan ly tai khoan va cap quyen cho he thong.
- ui_audit_tab.py: Xem toan bo nhat ky thao tac kiem toan (Audit Logs) danh rieng cho Admin.
- Addtional_features.py: Cac tien ich autocompletion bo sung cho o chon/nhap lieu.
- requirements.txt: Danh sach dependencies can thiet de chay ung dung.

## Huong Dan Cai Dat

De khoi chay ung dung tren may tinh ca nhan, vui long thuc hien cac buoc sau:

1. Tai ma nguon tu kho luu tru:
   git clone https://github.com/LQP-CTER/Inventory-Management-System.git
   cd Inventory-Management-System

2. Cai dat moi truong va dependencies:
   Doi voi he dieu hanh Windows, chay lenh sau trong terminal de cai dat tat ca cac thu vien lien quan:
   pip install -r requirements.txt

3. Khoi tao co so du lieu:
   Co so du lieu SQLite (inventory_management_system.db) va cac bang se tu dong duoc khoi tao trong lan dau tien ban chay chuong trinh. Ban khong can phai setup db bang tay.

## Huong Dan Chay Ung Dung

Sau khi hoan tat cac buoc cai dat, hay chay lenh sau tai thu muc goc cua du an:
python main.py

Cua so Login hien dai se hien thi. Ban co the dang nhap bang cac tai khoan san co trong co so du lieu de bat dau trai nghiem cac phan he nghiep vu nang cao va giao dien mượt ma.
