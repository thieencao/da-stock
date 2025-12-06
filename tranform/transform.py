import pandas as pd
import numpy as np
import os
import re

# ==========================================
# 1. CẤU HÌNH ĐƯỜNG DẪN (PATH CONFIG) - ĐÃ SỬA
# ==========================================

# Lấy đường dẫn thư mục hiện tại (chính là folder 'transform')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data input: Vẫn lấy từ thư mục cha/data (đi ngược ra 1 cấp -> vào data)
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), 'data')

# Data output: Lưu ngay bên trong folder transform
# Nó sẽ tạo ra: .../DA_STOCK/transform/cleaned_data/
OUTPUT_DIR = os.path.join(CURRENT_DIR, 'cleaned_data')

# Tạo thư mục nếu chưa có
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"--- BẮT ĐẦU XỬ LÝ DỮ LIỆU ---")
print(f"File code đang chạy tại: {CURRENT_DIR}")
print(f"Đọc dữ liệu gốc từ:      {DATA_DIR}")
print(f"Lưu dữ liệu sạch vào:    {OUTPUT_DIR}")
print("-" * 30)

# ==========================================
# 2. HÀM TIỆN ÍCH (HELPER FUNCTIONS)
# ==========================================

def clean_column_name(col_name):
    """
    Chuẩn hóa tên cột: lowercase, không dấu, snake_case
    """
    if not isinstance(col_name, str):
        return str(col_name)
    
    col_name = col_name.lower()
    
    # Map tiếng Việt (giữ nguyên logic cũ)
    replacements = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }
    
    for k, v in replacements.items():
        col_name = col_name.replace(k, v)
    
    col_name = re.sub(r'[^\w\s]', '', col_name)
    col_name = re.sub(r'\s+', '_', col_name).strip('_')
    return col_name

def process_financial_report(filename):
    """
    Logic xử lý riêng cho Báo cáo tài chính
    UPDATE: Đã thêm xử lý trùng lặp tên cột
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        print(f"[SKIP] Không tìm thấy file: {filename}")
        return

    print(f"[PROCESSING] {filename}...")
    df = pd.read_csv(file_path)
    
    # 1. Chuẩn hóa tên cột
    df.columns = [clean_column_name(c) for c in df.columns]

    # --- FIX LỖI: XỬ LÝ TRÙNG TÊN CỘT (QUAN TRỌNG) ---
    # Nếu có 2 cột giống tên nhau sau khi clean, Pandas sẽ bị lỗi khi gán dữ liệu
    # Đoạn này sẽ đổi tên cột trùng thành: col, col_2, col_3...
    new_columns = []
    col_counts = {}
    
    for col in df.columns:
        if col in col_counts:
            col_counts[col] += 1
            new_col_name = f"{col}_{col_counts[col]}"
        else:
            col_counts[col] = 1
            new_col_name = col
        new_columns.append(new_col_name)
    
    df.columns = new_columns
    # -------------------------------------------------
    
    # 2. Xử lý Null (Domain Logic: Tài chính null là bằng 0)
    cols_identifier = ['ticker', 'cp', 'symbol', 'year', 'nam', 'quarter', 'quy']
    
    # Lấy danh sách các cột số (loại trừ các cột định danh)
    cols_numeric = [c for c in df.columns if c not in cols_identifier]
    
    # Fill 0
    # Dùng dictionary để fill an toàn hơn cho từng cột
    fill_values = {col: 0 for col in cols_numeric}
    df.fillna(value=fill_values, inplace=True)
    
    # 3. Loại bỏ dòng rác
    if 'cp' in df.columns:
        df.dropna(subset=['cp'], inplace=True)
    if 'year' in df.columns:
        df.dropna(subset=['year'], inplace=True)

    # 4. Deduplication
    if 'cp' in df.columns and 'year' in df.columns:
        subset_dedup = ['cp', 'year']
        if 'quarter' in df.columns: subset_dedup.append('quarter')
        df.drop_duplicates(subset=subset_dedup, keep='last', inplace=True)
    else:
        df.drop_duplicates(inplace=True)

    # Save
    save_path = os.path.join(OUTPUT_DIR, f"clean_{filename}")
    df.to_csv(save_path, index=False)
    print(f"   -> Đã lưu: clean_{filename} | Shape: {df.shape}")

def process_market_data(filename):
    """ Xử lý Giá/Macro: Sort date, Dropna """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path): return

    print(f"[PROCESSING] {filename}...")
    df = pd.read_csv(file_path)
    df.columns = [clean_column_name(c) for c in df.columns]
    
    # Date handling
    date_col = next((c for c in df.columns if 'date' in c or 'time' in c or 'ngay' in c), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df.dropna(subset=[date_col], inplace=True)
        df.sort_values(by=date_col, inplace=True)
    
    # Dropna cho cột giá
    cols_price = ['open', 'high', 'low', 'close', 'volume', 'gia_dong_cua']
    existing_price_cols = [c for c in cols_price if c in df.columns]
    if existing_price_cols:
        df.dropna(subset=existing_price_cols, inplace=True)
    
    # Deduplication
    if date_col:
        subset = ['ticker', date_col] if 'ticker' in df.columns else [date_col]
        df.drop_duplicates(subset=subset, keep='last', inplace=True)

    save_path = os.path.join(OUTPUT_DIR, f"clean_{filename}")
    df.to_csv(save_path, index=False)
    print(f"   -> Saved: {save_path}")

# ==========================================
# 3. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    
    # List các file cần xử lý (như cũ)
    finance_files = [
        'finance_yearly_balance_sheet.csv',
        'finance_yearly_cash_flow.csv',
        'finance_yearly_income_statement.csv'
    ]
    market_files = ['ohlcv_vn30_2020_2025.csv', 'VNINDEX_2020_2025.csv']
    
    for f in finance_files: process_financial_report(f)
    for f in market_files: process_market_data(f)
    process_market_data('vietnam_macro_2020_2025.csv')

    print("-" * 30)
    print(f"HOÀN THÀNH! File sạch nằm tại: {OUTPUT_DIR}")
    process_market_data('vn30_profile.csv')