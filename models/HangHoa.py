from Database.db_manager import DatabaseManager
from PIL import Image
import os

class HangHoa:
    def __init__(self, dbm: DatabaseManager, MaHH, price, cost, TenHH, img_path):
        self.DBM = dbm
        self.__MaHH = MaHH
        self.__price = price
        self.__cost = cost
        self.__TenHH = TenHH
        self.__isActive = True
        self.__img_path = img_path
        try:
            self.image_obj = Image.open(img_path)
        except Exception:
            self.image_obj = None  # Phòng trường hợp file ảnh bị lỗi/thiếu

    """ Getter """
    def getActive(self):
        return self.__isActive
    def getMaHH(self):
        return self.__MaHH

    def getTenHH(self):
        return self.__TenHH

    def getPrice(self):
        return self.__price

    def getCost(self):
        return self.__cost

    def getProfit(self):
        """Tính lợi nhuận trực tiếp trên đối tượng"""
        return self.__price - self.__cost

    """ Setter kết nối SQL """

    def setTenHH(self, new_name: str):
        if not new_name.strip():
            return -1  # Tên không được để trống

        query = "UPDATE HangHoa SET TenHH = ? WHERE RTRIM(MaHH) = ?"
        success = self.DBM.execute_non_query(query, (new_name, self.__MaHH))
        if success:
            self.__TenHH = new_name
            return 1
        return 0

    def setPrice(self, new_price):
        if new_price <= self.__cost:
            return -1  # Giá bán không nên nhỏ hơn hoặc bằng giá vốn

        query = "UPDATE HangHoa SET Gia = ? WHERE RTRIM(MaHH) = ?"
        success = self.DBM.execute_non_query(query, (new_price, self.__MaHH))
        if success:
            self.__price = new_price
            return 1
        return 0

    def setCost(self, new_cost):
        if new_cost < 0:
            return -1

        query = "UPDATE HangHoa SET Cost = ? WHERE RTRIM(MaHH) = ?"
        success = self.DBM.execute_non_query(query, (new_cost, self.__MaHH))
        if success:
            self.__cost = new_cost
            return 1
        return 0

    def setIMG(self, new_img_path):
        """Cập nhật đường dẫn ảnh mới"""
        if not os.path.exists(new_img_path):
            return -1  # File ảnh không tồn tại

        query = "UPDATE HangHoa SET IMG = ? WHERE RTRIM(MaHH) = ?"
        success = self.DBM.execute_non_query(query, (new_img_path, self.__MaHH))
        if success:
            self.__img_path = new_img_path
            self.image_obj = Image.open(new_img_path)
            return 1
        return 0

    def deleteProduct(self):
        """Xóa món hàng này khỏi thực đơn"""
        query = "DELETE FROM HangHoa WHERE RTRIM(MaHH) = ?"
        success = self.DBM.execute_non_query(query, (self.__MaHH,))
        return 1 if success else 0