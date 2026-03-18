from Database.db_manager import DatabaseManager
import hashlib


class NhanVien:
    def __init__(self, dbm: DatabaseManager, idnv, password, role, salary, sdt, chamcong):
        self.DBM = dbm
        self.__MaNV = idnv
        self.__password = password
        self.__role = role
        self.__luong = salary
        self.__sdt = sdt
        self.__chamcong = chamcong

    """Getter/Setter"""

    def getMaNV(self):
        return self.__MaNV

    def getRole(self):
        return self.__role

    def getSalary(self):
        return self.__luong

    def getPhoneNum(self):
        return self.__sdt

    def getCC(self):
        return self.__chamcong

    def setPassword(self, old_input, newPass: str):

        if self.__password != old_input:
            return -1
            # Sai mật khẩu cũ

        hashPass = hashlib.sha256(newPass.encode()).hexdigest()

        query = ' UPDATE NhanVien SET MatKhau = ? WHERE RTRIM(MaNV) = ? '
        success = self.DBM.execute_non_query(query, (hashPass, self.__MaNV))

        if success:
            return 1

        # Có lỗi gì đó làm ko đổi được thì trả về 0
        return 0

    def setPhoneNum(self, sdt):
        self.__sdt = sdt

        query = ' UPDATE NhanVien SET SDT = ? WHERE RTRIM(MaNV) = ? '
        success = self.DBM.execute_non_query(query, (sdt, self.__MaNV))

        if success:
            return 1
        return 0

    def setLuong(self, salary):
        if salary <= 20000:
            return -1
            # Lương không được nhỏ hơn 20000

        query = ' UPDATE NhanVien SET Luong = ? WHERE RTRIM(MaNV) = ? '
        success = self.DBM.execute_non_query(query, (salary, self.__MaNV))

        if success:
            return 1

        return 0

    def deleteAccount(self):
        """Xóa chính tài khoản này. Sau này UI nhớ thêm sự kiện đăng xuất"""
        query = 'DELETE FROM NhanVien WHERE RTRIM(MANV) = ?'
        success = self.DBM.execute_non_query(query, (self.__MaNV))

        if success:
            return 1

        return 0

    def deleteAnotherAccount(self, MaNhanVien):
        """Xóa tài khoản khác, chỉ role Quản Lí mới được xóa"""

        if self.__role != "Quản lí":
            return -1
            # IN ra: Bạn phải là quản lí mới được xóa
        query = 'DELETE FROM NhanVien WHERE RTRIM(MANV) = ?'
        success = self.DBM.execute_non_query(query, (MaNhanVien))

        if success:
            return 1
        return 0



