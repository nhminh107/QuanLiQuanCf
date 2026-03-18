from Database.db_manager import DatabaseManager
from datetime import datetime


class NguyenLieu:
    def __init__(self, dbm: DatabaseManager, MaNL, TenNL, NhaCungCap, SoLuong, DonVi, DonGia, Date):
        self.DBM = dbm
        self.__MaNL = MaNL
        self.__TenNL = TenNL
        self.__NhaCungCap = NhaCungCap
        self.__SoLuong = SoLuong
        self.__DonVi = DonVi
        self.__DonGia = DonGia

        # Xử lý Date từ string sang object datetime để dễ quản lý
        if isinstance(Date, str):
            try:
                # Giả định định dạng truyền vào là 'YYYY-MM-DD'
                self.__Date = datetime.strptime(Date, '%Y-%m-%d')
            except ValueError:
                self.__Date = Date  # Nếu sai định dạng thì giữ nguyên để debug
        else:
            self.__Date = Date

    """ Getter """

    def getMaNL(self):
        return self.__MaNL

    def getTenNL(self):
        return self.__TenNL

    def getNhaCungCap(self):
        return self.__NhaCungCap

    def getSoLuong(self):
        return self.__SoLuong

    def getDonVi(self):
        return self.__DonVi

    def getDonGia(self):
        return self.__DonGia

    def getDate(self):
        # Trả về string để hiển thị lên UI cho dễ
        if isinstance(self.__Date, datetime):
            return self.__Date.strftime('%Y-%m-%d')
        return self.__Date

    """ Setter cập nhật SQL """

    def setTenNL(self, name: str):
        query = "UPDATE NguyenLieu SET TenNL = ? WHERE RTRIM(MaNL) = ?"
        if self.DBM.execute_non_query(query, (name, self.__MaNL)):
            self.__TenNL = name
            return 1
        return 0

    def setSoLuong(self, qty):
        if qty < 0: return -1
        query = "UPDATE NguyenLieu SET SoLuong = ? WHERE RTRIM(MaNL) = ?"
        if self.DBM.execute_non_query(query, (qty, self.__MaNL)):
            self.__SoLuong = qty
            return 1
        return 0

    def setDonGia(self, price):
        if price < 0: return -1
        query = "UPDATE NguyenLieu SET DonGia = ? WHERE RTRIM(MaNL) = ?"
        if self.DBM.execute_non_query(query, (price, self.__MaNL)):
            self.__DonGia = price
            return 1
        return 0

    def setDate(self, date_str: str):
        """Cập nhật ngày nhập hàng mới (truyền vào string YYYY-MM-DD)"""
        query = "UPDATE NguyenLieu SET Date = ? WHERE RTRIM(MaNL) = ?"
        if self.DBM.execute_non_query(query, (date_str, self.__MaNL)):
            try:
                self.__Date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
            return 1
        return 0

    def deleteNL(self):
        """Xóa nguyên liệu khỏi kho"""
        query = "DELETE FROM NguyenLieu WHERE RTRIM(MaNL) = ?"
        return 1 if self.DBM.execute_non_query(query, (self.__MaNL,)) else 0