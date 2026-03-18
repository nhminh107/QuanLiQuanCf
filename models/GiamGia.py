from Database.db_manager import DatabaseManager
from datetime import datetime


class GiamGia:
    def __init__(self, dbm: DatabaseManager, MaGG, ChuongTrinh, DateStart, DateEnd, GiaTri):
        self.DBM = dbm
        self.__MaGG = MaGG
        self.__ChuongTrinh = ChuongTrinh
        self.__DateStart = DateStart
        self.__DateEnd = DateEnd
        self.__GiaTri = GiaTri

    """ Getter """

    def getMaGG(self):
        return self.__MaGG

    def getChuongTrinh(self):
        return self.__ChuongTrinh

    def getDateStart(self):
        return self.__DateStart

    def getDateEnd(self):
        return self.__DateEnd

    def getGiaTri(self):
        return self.__GiaTri

    """ Setter cập nhật SQL """

    def setChuongTrinh(self, text: str):
        query = "UPDATE GiamGia SET ChuongTrinh = ? WHERE RTRIM(MaGG) = ?"
        success = self.DBM.execute_non_query(query, (text, self.__MaGG))
        if success:
            self.__ChuongTrinh = text
            return 1
        return 0

    def setDateStart(self, new_date):
        # Kiểm tra: Ngày bắt đầu không được sau ngày kết thúc
        if new_date > self.__DateEnd:
            return -1

        query = "UPDATE GiamGia SET DateStart = ? WHERE RTRIM(MaGG) = ?"
        success = self.DBM.execute_non_query(query, (new_date, self.__MaGG))
        if success:
            self.__DateStart = new_date
            return 1
        return 0

    def setDateEnd(self, new_date):
        # Kiểm tra: Ngày kết thúc không được trước ngày bắt đầu
        if new_date < self.__DateStart:
            return -1

        query = "UPDATE GiamGia SET DateEnd = ? WHERE RTRIM(MaGG) = ?"
        success = self.DBM.execute_non_query(query, (new_date, self.__MaGG))
        if success:
            self.__DateEnd = new_date
            return 1
        return 0

    def setGiaTri(self, val):
        if val < 0:
            return -1

        query = "UPDATE GiamGia SET GiaTri = ? WHERE RTRIM(MaGG) = ?"
        success = self.DBM.execute_non_query(query, (val, self.__MaGG))
        if success:
            self.__GiaTri = val
            return 1
        return 0

    def is_active(self):
        """Hàm kiểm tra xem mã giảm giá hiện tại có đang trong thời hạn dùng được không"""
        now = datetime.now()
        return self.__DateStart <= now <= self.__DateEnd

    def deleteGG(self):
        query = "DELETE FROM GiamGia WHERE RTRIM(MaGG) = ?"
        return 1 if self.DBM.execute_non_query(query, (self.__MaGG,)) else 0