from models.NhanVien import NhanVien
from Database.db_manager import DatabaseManager
import config
from datetime import date
import hashlib

class AuthService:
    def __init__(self, dbm: DatabaseManager, ):
        self.__DBM : DatabaseManager = dbm
        self.__client : NhanVien = None

    def is_logged_in(self):
        return self.__client is not None

    def is_admin(self):
        if self.is_logged_in():
            return self.__client.getRole() == u"Quản lí"
        return False

    def login(self, username, pw):

        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()

        query = "SELECT * FROM NHANVIEN WHERE RTRIM(MaNV) = ? "

        res = self.__DBM.fetch_one(query, (username, hashed_pw))

        if res:
            self.__client = NhanVien(self.__DBM, res.MaNV, res.MatKhau, res.VaiTro, res.Luong, res.SDT, res.ChamCong)
            self.ChamCong()

            return True

        self.__client = None
        return False

    def delete_account_by_id(self, MaNV: str):
        """Tính năng dành cho Quản Lí"""
        if self.__client.getRole() != "Quản lí":
            return -1
            #Ko có quyền xóa tài khoản khác

        query = "DELETE FROM NHANVIEN RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query, (MaNV))

        if success:
            return 1
        return 0
        #Lỗi ko xác định, có thể ko tồn tại mã NV

    def set_salary_by_id(self, salary, MaNV: str):

        if self.__client.getRole() != "Quản lí":
            return -1
            #Ko có quyền xóa tài khoản khác

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
            #Đã chấm công rồi

        query2 = "INSERT INTO CHAMCONG(MaNV, Date) VALUES (?, ?)"
        success = self.__DBM.execute_non_query(query2, (self.__client.getMaNV(), today))

        if success:
            return 1

        return 0
        #Lỗi hệ thông

    def create_account(self, MaNV, pw, role, luong, sdt):
        """Tạo nhân viên mới, chỉ có Manager mới làm được"""
        if self.__client.getRole() != "Quản lí":
            return -1

        hashed_pass = hashlib.sha256(pw.encode()).hexdigest()
        query = "INSERT INTO NhanVien (MaNV, MatKhau, VaiTro, Luong, SDT) VALUES (?, ?, ?, ?, ?)"
        success = self.__DBM.execute_non_query(query, (MaNV, hashed_pass, role, luong, sdt, 1))

        if success:
            return NhanVien(self.__DBM, MaNV, hashed_pass, role, luong, sdt, 1)

        return 0 #Không thành công






