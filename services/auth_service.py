from models.NhanVien import NhanVien
from Database.db_manager import DatabaseManager
import config
from datetime import date
import hashlib

class AuthService:
    def __init__(self, dbm: DatabaseManager):
        self.__DBM : DatabaseManager = dbm
        self.__client : NhanVien = None

    def is_logged_in(self):
        return self.__client is not None

    def getUser(self):
        return self.__client
    def setPassword(self,oldPass, newPass):
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
            #Tài khoản đã bị xóa
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
            #Ko có quyền xóa tài khoản khác

        query = "UPDATE NHANVIEN SET isActive = ? WHERE RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query, ('0', MaNV))

        if success:
            return 1
        return 0
        #Lỗi ko xác định, có thể ko tồn tại mã NV

    def set_salary_by_id(self, salary, MaNV: str):

        if self.__client.getRole() != "Quản Lí":
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
        query3 = "UPDATE NhanVien SET ChamCong = ChamCong + 1 WHERE RTRIM(MaNV) = ?"
        success = self.__DBM.execute_non_query(query2, (self.__client.getMaNV(), today))
        sc2 = self.__DBM.execute_non_query(query3, (self.__client.getMaNV(),))

        if success and sc2:
            return 1

        return 0
        #Lỗi hệ thông

    def create_account(self, MaNV, pw, role, luong, sdt):
        """Tạo nhân viên mới, chỉ có Manager mới làm được"""

        today = date.today()

        if self.__client.getRole() != "Quản Lí":
            return -1

        hashed_pass = hashlib.sha256(pw.encode()).hexdigest()
        query = "INSERT INTO NhanVien (MaNV, MatKhau, VaiTro, Luong, SDT,ChamCong, isActive) VALUES (?, ?, ?, ?, ?, ?, ?)"
        success = self.__DBM.execute_non_query(query, (MaNV, hashed_pass, role, luong, sdt,1,'1'))

        query2 = "INSERT INTO CHAMCONG(MaNV, Date) VALUES (?, ?)"
        success2 = self.__DBM.execute_non_query(query2, (MaNV, today))
        if success and success2:
            return NhanVien(self.__DBM, MaNV, hashed_pass, role, luong, sdt, 1)

        return 0 #Không thành công



if __name__ == '__main__':
    dbm = DatabaseManager()
    dbm.connect()

    """Đoạn code test tính năng đăng nhập"""
    auth_service = AuthService(dbm)
    res = auth_service.login('QL0002', 'Hoangminh123@') #OK
    print(res)

    """res2 = auth_service.setPassword('123456', '')
    print(res2)""" #OK

    """res3 = auth_service.create_account('NV0001', '123456', 'Nhân Viên', 25000, '0903543123')
    print(res3)""" #OK

    res4 = auth_service.set_salary_by_id(salary=27000, MaNV='NV0001')
    print(res4) #OK


