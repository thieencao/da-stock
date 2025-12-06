import pandas as pd
import os
from sqlalchemy import create_engine, text
import pymysql

# ==========================================
# 1. CẤU HÌNH KẾT NỐI (DB CONFIG)
# ==========================================
# ⚠️ HÃY SỬA LẠI PASS MYSQL CỦA BẠN
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '123456789'     # <--- Điền mật khẩu của bạn vào đây
DB_NAME = 'da_stock_db'

# Đường dẫn folder chứa data sạch
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) 
CLEAN_DATA_DIR = os.path.join(PROJECT_ROOT, 'tranform', 'cleaned_data')

# ==========================================
# 2. LOGIC MAPPING (TÊN FILE -> TÊN BẢNG)
# ==========================================
def map_table_name(filename):
    """
    Ánh xạ tên file CSV sang tên bảng MySQL đã tạo.
    """
    # Chuẩn hóa tên file để so sánh (bỏ 'clean_', bỏ '.csv', chữ thường)
    base_name = filename.replace('clean_', '').replace('.csv', '').lower()
    
    mapping = {
        # Dim
        'vn30_profile': 'dim_company_info',
        
        # Fact
        'vnindex_2020_2025': 'fact_market_index',
        'financial_ratios': 'fact_financial_ratio',
        'ohlcv_vn30_2020_2025': 'fact_stock_price',
        'finance_yearly_balance_sheet': 'fact_balance_sheet',
        'finance_yearly_income_statement': 'fact_income_statement',
        'finance_yearly_cash_flow': 'fact_cash_flow',
        'macro_economic': 'fact_macro_economic'
    }
    
    # Trả về tên bảng nếu tìm thấy, nếu không thì báo None
    return mapping.get(base_name)

# ==========================================
# 3. HÀM TẠO KẾT NỐI
# ==========================================
def get_database_connection():
    connection_str = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    try:
        engine = create_engine(connection_str)
        # Test kết nối
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        print(f" Lỗi kết nối MySQL: {e}")
        return None

# ==========================================
# 4. HÀM LOAD DỮ LIỆU CHÍNH
# ==========================================
def load_data_to_mysql():
    print(f"--- BẮT ĐẦU LOAD DỮ LIỆU (MODE: TRUNCATE & APPEND) ---")
    
    engine = get_database_connection()
    if not engine: return

    if not os.path.exists(CLEAN_DATA_DIR):
        print(f" Không tìm thấy thư mục: {CLEAN_DATA_DIR}")
        return

    files = [f for f in os.listdir(CLEAN_DATA_DIR) if f.endswith('.csv')]
    print(f" Tìm thấy {len(files)} file CSV.")
    print("-" * 40)

    # Mở kết nối để thực thi lệnh
    with engine.connect() as conn:
        for file in files:
            # 1. Xác định tên bảng
            table_name = map_table_name(file)
            
            if not table_name:
                print(f" Skip file: {file} (Không nằm trong danh sách Mapping)")
                continue
                
            file_path = os.path.join(CLEAN_DATA_DIR, file)
            print(f"Processing: {file} -> Table: {table_name}")
            
            try:
                # 2. XÓA DỮ LIỆU CŨ (TRUNCATE)
                # Giữ lại vỏ bảng (index, key), chỉ xóa ruột
                try:
                    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
                    print(f"   -> [1/3] Truncate bảng cũ... OK")
                except Exception as ex:
                    print(f"   ->  Cảnh báo: Không thể Truncate (Có thể bảng chưa tồn tại).")

                # 3. ĐỌC CSV
                df = pd.read_csv(file_path)
                print(f"   -> [2/3] Đọc CSV: {df.shape[0]} dòng... OK")
                
                # 4. ĐỔ DỮ LIỆU MỚI (APPEND)
                # chunksize=2000: Cắt nhỏ để insert cho nhẹ máy
                df.to_sql(name=table_name, con=engine, if_exists='append', index=False, chunksize=2000)
                print(f"   -> [3/3] Load vào MySQL...  SUCCESS!")
                
            except Exception as e:
                print(f"   ->  FAILED: Lỗi khi xử lý file {file}")
                print(f"      Chi tiết: {e}")
            
            print("-" * 40)

if __name__ == "__main__":
    load_data_to_mysql()
    print("HOÀN TẤT QUÁ TRÌNH LOAD!")