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
        self.__isActive = True

    """Getter/Setter"""

    def getActive(self):
        return self.__isActive
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

        hash_old_pass = hashlib.sha256(old_input.encode()).hexdigest()
        if self.__password.strip() != hash_old_pass:
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




