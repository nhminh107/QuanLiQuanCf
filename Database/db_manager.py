import pyodbc
from config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.conn_str = (
            f"Driver={DB_CONFIG['driver']};"
            f"Server={DB_CONFIG['server']};"
            f"Database={DB_CONFIG['database']};"
            f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
        )

        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False

    def fetch_all(self, query, params=()):
        """Dùng cho lệnh SELECT khi muốn lấy nhiều dòng"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        """Dùng cho lệnh SELECT khi muốn lấy nhiều dòng"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def execute_non_query(self, query, params=()):
        """Dùng cho INSERT, UPDATE, DELETE"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True

        except Exception as e:
            print(f"Lỗi thực thi: {e}")
            self.conn.rollback()
            return False

    def close_db(self):
        """#Khi kết thúc chương trình, nhớ gọi hàm nayf """
        if self.conn:
            self.conn.close()
