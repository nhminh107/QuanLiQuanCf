from models.NhanVien import  NhanVien
from models.HangHoa import HangHoa
from models.NguyenLieu import NguyenLieu
from Database.db_manager import DatabaseManager
from config import IMAGE_PATH
class ProductManager:
    def __init__(self, user: NhanVien):
        self.__user = user

    def create_goods(self, MaHH: str, price, cost, TenHH: str):
        """Thêm hàng hóa mới vào Database"""
        query_check = "SELECT COUNT(*) FROM HangHoa WHERE RTRIM(MaHH) = ?"
        result = self.__user.DBM.fetch_one(query_check, (MaHH,))

        if result and result[0] > 0:
            return -1  # Mã hàng hóa đã tồn tại


        query_insert = "INSERT INTO HangHoa (MaHH, Gia, Cost, TenHH) VALUES (?, ?, ?, ?)"
        # Lưu ý: Nếu có trường IMG, hãy thêm vào sau
        success = self.__user.DBM.execute_non_query(query_insert, (MaHH, price, cost, TenHH))

        if success:
            # Trả về Object để UI cập nhật danh sách ngay lập tức
            return HangHoa(self.__user.DBM, MaHH, price, cost, TenHH, IMAGE_PATH + MaHH)

        return 0  # Lỗi DB

    def delete_goods(self, MaHH):
        """Xóa hàng hóa dựa trên mã"""
        # Lưu ý: Trong thực tế, nếu MaHH đã có trong bảng ChiTietHoaDon,
        # lệnh DELETE này sẽ lỗi do ràng buộc khóa ngoại (Foreign Key).

        query = "DELETE FROM HangHoa WHERE RTRIM(MaHH) = ?"
        success = self.__user.DBM.execute_non_query(query, (MaHH,))

        if success:
            return 1  # Xóa thành công
        return 0  # Xóa thất bại (có thể do ràng buộc dữ liệu hoặc sai mã)