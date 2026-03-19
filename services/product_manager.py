from models.NhanVien import  NhanVien
from models.HangHoa import HangHoa
from models.NguyenLieu import NguyenLieu
from Database.db_manager import DatabaseManager
from services.auth_service import AuthService
from config import IMAGE_PATH
from datetime import date


class ProductManager:
    def __init__(self, user: NhanVien):
        self.__user = user

    def create_goods(self, MaHH: str, price, cost, TenHH: str):
        """Thêm hàng hóa mới vào Database"""
        query_check = "SELECT COUNT(*) FROM HangHoa WHERE RTRIM(MaHH) = ?"
        result = self.__user.DBM.fetch_one(query_check, (MaHH,))

        if result and result[0] > 0:
            return -1  # Mã hàng hóa đã tồn tại


        query_insert = "INSERT INTO HangHoa (MaHH, Gia, Cost, IMG, TenHH, isActive) VALUES (?, ?, ? , ?, ?, ?)"
        # Lưu ý: Nếu có trường IMG, hãy thêm vào sau
        success = self.__user.DBM.execute_non_query(query_insert, (MaHH, price, cost, IMAGE_PATH+MaHH, TenHH, '1'))

        if success:
            # Trả về Object để UI cập nhật danh sách ngay lập tức
            return HangHoa(self.__user.DBM, MaHH, price, cost, TenHH, IMAGE_PATH + MaHH)

        return 0  # Lỗi DB

    def delete_goods(self, MaHH):
        """Xóa hàng hóa dựa trên mã"""
        # Lưu ý: Trong thực tế, nếu MaHH đã có trong bảng ChiTietHoaDon,
        # lệnh DELETE này sẽ lỗi do ràng buộc khóa ngoại (Foreign Key).

        query = "UPDATE HangHoa SET isActive = ? WHERE RTRIM(MaHH) = ?"
        success = self.__user.DBM.execute_non_query(query, ('0', MaHH))

        if success:
            return 1  # Xóa thành công
        return 0  # Xóa thất bại (có thể do ràng buộc dữ liệu hoặc sai mã)

    def nhap_nguyen_lieu(self, MaNL: str, TenNL: str, NhaCungCap: str, SoLuong: float, DonVi: str, DonGia: float,
                         Date_input=None):
        """
        Thêm một bản ghi nhập nguyên liệu.
        Nếu Date_input không có, mặc định lấy ngày hôm nay.
        """
        # 1. Xử lý ngày tháng tự động
        current_date = Date_input if Date_input else date.today()

        # 2. Kiểm tra trùng mã (Nếu bảng NguyenLieu dùng MaNL làm Primary Key)
        query_check = "SELECT COUNT(*) FROM NguyenLieu WHERE RTRIM(MaNL) = ?"
        result = self.__user.DBM.fetch_one(query_check, (MaNL,))

        if result and result[0] > 0:
            return -1  # Mã nguyên liệu đã tồn tại

        # 3. Thực hiện INSERT
        # Lưu ý: Dùng [Date] để tránh trùng từ khóa hệ thống của SQL Server
        query_insert = """
            INSERT INTO NguyenLieu (MaNL, TenNL, NhaCungCap, SoLuong, DonVi, DonGia, [Date]) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        params = (MaNL, TenNL, NhaCungCap, SoLuong, DonVi, DonGia, current_date)

        success = self.__user.DBM.execute_non_query(query_insert, params)

        if success:
            # Trả về Object NguyenLieu mới
            return NguyenLieu(
                self.__user.DBM,
                MaNL, TenNL, NhaCungCap,
                SoLuong, DonVi, DonGia, current_date
            )

        return 0  # Lỗi DB
if __name__ == "__main__":
    dbm = DatabaseManager()
    dbm.connect()

    """Đoạn code test tính năng đăng nhập"""
    auth_service = AuthService(dbm)
    res = auth_service.login('QL0002', 'Hoangminh123@')  # OK
    print(res)
    pd = ProductManager(auth_service.getUser())

    """res2 = pd.create_goods('TEST1000', 100000, 8000, 'TEST001')
    print(res2) ----OK"""


    res3 = pd.delete_goods('TEST1000')
    print(res3)