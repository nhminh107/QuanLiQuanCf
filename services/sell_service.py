from Database.db_manager import DatabaseManager
from models.NhanVien import NhanVien
from datetime import datetime
from services.auth_service import AuthService


class SellService:
    def __init__(self, dbm: DatabaseManager, user: NhanVien):
        self.__DBM = dbm
        self.__user = user

    def checkGG(self, MaGG):
        query = """
            SELECT MaGG, GiaTri, DateStart, DateEnd
            FROM GiamGia
            WHERE MaGG = ?
        """
        row = self.__DBM.fetch_one(query, (MaGG,))
        if row is None:
            return -1

        now = datetime.now()
        if row.DateStart and now < row.DateStart:
            return -1
        if row.DateEnd and now > row.DateEnd:
            return -1

        return row.GiaTri

    def previewInvoice(self, items, MaGG=None):
        if not items or len(items) == 0:
            return -2

        tongtien = 0
        for item in items:
            mahh = item["MaHH"]
            soluong = item["SoLuong"]
            row = self.__DBM.fetch_one("SELECT Gia FROM HangHoa WHERE MaHH = ?", (mahh,))

            if row is None:
                return -1

            gia = row[0]
            tongtien += gia * soluong

        giamgia = 0
        if MaGG:
            gg = self.checkGG(MaGG)
            if gg == -1:
                return -1
            giamgia = gg

        thanhtien = tongtien - giamgia
        if thanhtien < 0:
            thanhtien = 0

        return (tongtien, giamgia, thanhtien)

    def generateMaHD(self):
        query = """
            UPDATE COUNTER
            SET value = value + 1
            OUTPUT INSERTED.value
            WHERE name = 'MaHD'
        """
        row = self.__DBM.fetch_one(query)
        if row is None:
            return None

        return f"HD{str(row[0]).zfill(4)}"

    def sellGoods(self, items, MaGG=None):
        if not items or len(items) == 0:
            return -2

        try:
            preview = self.previewInvoice(items, MaGG)
            if isinstance(preview, int):
                return preview

            tongtien, giamgia, thanhtien = preview

            mahd = self.generateMaHD()
            if mahd is None:
                return 0

            ok = self.__DBM.execute_non_query("""
                INSERT INTO HoaDon (MaHD, [Date], MaNV, TongTien, GiamGia, ThanhTien)
                VALUES (?, GETDATE(), ?, ?, ?, ?)
            """, (mahd, self.__user.getMaNV(), tongtien, MaGG, thanhtien))

            if not ok:
                return 0

            for item in items:
                mahh = item["MaHH"]
                soluong = item["SoLuong"]

                row = self.__DBM.fetch_one("SELECT Gia FROM HangHoa WHERE MaHH = ?", (mahh,))
                if row is None:
                    return 0

                gia = row[0]

                ok = self.__DBM.execute_non_query("""
                    INSERT INTO CT_HoaDon (MaHD, MaHangHoa, SoLuong, GiaBan, Note)
                    VALUES (?, ?, ?, ?, '')
                """, (mahd, mahh, soluong, gia))

                if not ok:
                    return 0

            return 1

        except Exception as e:
            print(f"Lỗi Exception tại sellGoods: {e}")
            return 0


if __name__ == '__main__':
    dbm = DatabaseManager()
    if not dbm.connect():
        print("Lỗi kết nối CSDL")
        exit()

    auth_service = AuthService(dbm)
    res = auth_service.login('QL0002', 'Hoangminh123@')
    print("--- TEST ĐĂNG NHẬP ---")
    print("Login:", res)

    if res != 1:
        print("Không đăng nhập được → dừng test")
    else:
        user = auth_service.getUser()
        sell_service = SellService(dbm, user)

        print("\n--- TEST 1: checkGG ---")
        try:
            gg_val = sell_service.checkGG("GG01")
            print("checkGG('GG01'):", gg_val)
        except Exception as e:
            print("Lỗi checkGG:", e)

        print("\n--- TEST 2: previewInvoice ---")
        items = [
            {"MaHH": "A0001", "SoLuong": 2},
            {"MaHH": "A0002", "SoLuong": 1}
        ]
        try:
            preview = sell_service.previewInvoice(items, MaGG=None)
            print("previewInvoice (Không GG):", preview)
        except Exception as e:
            print("Lỗi previewInvoice:", e)

        print("\n--- TEST 3: generateMaHD ---")
        try:
            mahd = sell_service.generateMaHD()
            print("generateMaHD():", mahd)
        except Exception as e:
            print("Lỗi generateMaHD:", e)

        print("\n--- TEST 4: sellGoods ---")
        try:
            res_sell = sell_service.sellGoods(items, MaGG=None)
            print("sellGoods (Không GG):", res_sell)
        except Exception as e:
            print("Lỗi sellGoods:", e)