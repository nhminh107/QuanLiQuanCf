from models.NhanVien import NhanVien
from Database.db_manager import DatabaseManager
import config
from datetime import date
import hashlib


class AuthService:
    def __init__(self, dbm: DatabaseManager):
        self.__DBM: DatabaseManager = dbm
        self.__client: NhanVien = None

    def is_logged_in(self):
        return self.__client is not None

    def getUser(self):
        return self.__client

    def setPassword(self, oldPass, newPass):
        return self.__client.setPassword(oldPass, newPass)

    def is_admin(self):
        if self.is_logged_in():
            return self.__client.getRole() == u"Quản Lí"
        return False

    def login(self, username, pw):
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
        query = "SELECT * FROM NHANVIEN WHERE RTRIM(MaNV) = ? AND MatKhau = ?"
        res = self.__DBM.fetch_one(query, (username, hashed_pw))

        if res is None:
            return -2
        if res.isActive == '0':
            return -1
            # Tài khoản đã bị xóa
        if res:
            self.__client = NhanVien(self.__DBM, res.MaNV, res.MatKhau, res.VaiTro, res.Luong, res.SDT, res.ChamCong)
            self.ChamCong()
            return 1

        self.__client = None
        return 0

    def delete_account_by_id(self, MaNV: str):
        """Tính năng dành cho Quản Lí"""
        if self.__client.getRole() != "Quản Lí":
            return -1

        query = "UPDATE NHANVIEN SET isActive = ? WHERE RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query, ('0', MaNV))

        if success:
            return 1
        return 0

    def set_salary_by_id(self, salary, MaNV: str):
        if self.__client.getRole() != "Quản Lí":
            return -1

        query = "UPDATE NHANVIEN SET Luong = ? WHERE RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query, (salary, MaNV))

        if success:
            return 1
        return 0

    def ChamCong(self):
        today = date.today()
        query = "SELECT COUNT(*) FROM ChamCong WHERE RTRIM(MaNV) = ? AND [Date] = ?"
        result = self.__DBM.fetch_one(query, (self.__client.getMaNV(), today))

        if result[0] > 0:
            return -1

        query2 = "INSERT INTO CHAMCONG(MaNV, [Date]) VALUES (?, ?)"
        query3 = "UPDATE NhanVien SET ChamCong = ChamCong + 1 WHERE RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query2, (self.__client.getMaNV(), today))
        sc2 = self.__DBM.execute_non_query(query3, (self.__client.getMaNV(),))

        if success and sc2:
            return 1
        return 0

    # ================== SINH MaNV ==================
    def generateMaNV(self):
        # Note: Truy vấn MaNV từ bảng COUNTER tương tự SellService
        query = """
            UPDATE COUNTER
            SET value = value + 1
            OUTPUT INSERTED.value
            WHERE name = 'MaNV'
        """
        row = self.__DBM.fetch_one(query)
        if row is None:
            return None
        return f"NV{str(row[0]).zfill(4)}"

    def create_account(self, pw, role, luong, sdt):
        """Tạo nhân viên mới, MaNV tự động từ COUNTER"""
        today = date.today()

        if self.__client.getRole() != "Quản Lí":
            return -1

        # Note: Tự động lấy mã nhân viên mới
        MaNV = self.generateMaNV()
        if MaNV is None:
            return 0

        hashed_pass = hashlib.sha256(pw.encode()).hexdigest()
        query = "INSERT INTO NhanVien (MaNV, MatKhau, VaiTro, Luong, SDT, ChamCong, isActive) VALUES (?, ?, ?, ?, ?, ?, ?)"
        success = self.__DBM.execute_non_query(query, (MaNV, hashed_pass, role, luong, sdt, 1, '1'))

        query2 = "INSERT INTO CHAMCONG(MaNV, [Date]) VALUES (?, ?)"
        success2 = self.__DBM.execute_non_query(query2, (MaNV, today))

        if success and success2:
            return NhanVien(self.__DBM, MaNV, hashed_pass, role, luong, sdt, 1)

        return 0


if __name__ == '__main__':
    dbm = DatabaseManager()
    dbm.connect()

    auth_service = AuthService(dbm)
    # Login tài khoản quản lý để có quyền tạo account
    res = auth_service.login('QL0002', 'Hoangminh123@')
    print(f"Login: {res}")

    if res == 1:
        # Note: Không cần truyền MaNV thủ công nữa
        new_nv = auth_service.create_account('123456', 'Nhân Viên', 25000, '0903543123')
        if new_nv:
            print(f"Tạo thành công: {new_nv.getMaNV()}")
        else:
            print("Tạo thất bại")