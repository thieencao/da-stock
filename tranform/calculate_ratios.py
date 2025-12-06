import pandas as pd
import os
import numpy as np

# ==========================================
# 1. CẤU HÌNH ĐƯỜNG DẪN
# ==========================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DATA_DIR = os.path.join(CURRENT_DIR, 'cleaned_data')
OUTPUT_FILE = os.path.join(CLEAN_DATA_DIR, 'financial_ratios.csv')

def load_clean_data(filename):
    path = os.path.join(CLEAN_DATA_DIR, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"⚠️ Không tìm thấy file: {filename}")
        return None

# ==========================================
# 2. XỬ LÝ & TÍNH TOÁN
# ==========================================
def calculate():
    print("--- BẮT ĐẦU TÍNH TOÁN CHỈ SỐ TÀI CHÍNH ---")
    
    # 1. Load dữ liệu tài chính
    df_bs = load_clean_data('clean_finance_yearly_balance_sheet.csv') # Cân đối kế toán
    df_is = load_clean_data('clean_finance_yearly_income_statement.csv') # KQKD
    # df_cf = load_clean_data('clean_finance_yearly_cash_flow.csv') # Dòng tiền (Nếu cần dùng sau này)
    df_price = load_clean_data('clean_ohlcv_vn30_2020_2025.csv') # Giá chứng khoán

    if df_bs is None or df_is is None or df_price is None:
        return

    # 2. Merge Bảng Cân đối kế toán & KQKD
    # Key merge là Ticker và Year
    print("Dang gop bang can doi ke toan va KQKD...")
    df_finance = pd.merge(df_bs, df_is, on=['cp', 'year'], how='inner', suffixes=('_bs', '_is'))
    
    # Lưu ý: Sau khi merge, nếu có cột trùng tên thì nó sẽ thêm đuôi _bs, _is. 
    # Bạn cần check đúng tên cột trong file CSV thực tế của bạn.
    # Dưới đây là mapping các cột quan trọng (Bạn cần SỬA LẠI TÊN CỘT cho khớp với file clean của bạn)
    
    # Giả định tên cột sau khi clean (snake_case)
    col_lnst = 'loi_nhuan_sau_thue_cua_co_dong_cong_ty_me' # Hoặc 'loi_nhuan_sau_thue'
    col_tong_tai_san = 'tong_cong_tai_san_dong'
    col_von_chu_so_huu = 'von_chu_so_huu_dong'
    col_von_gop = 'von_gop_cua_chu_so_huu_dong' # Dùng để tính số lượng CP
    
    # Kiểm tra xem cột có tồn tại không, nếu không tìm cột gần đúng
    def find_col(df, keyword):
        for col in df.columns:
            if keyword in col: return col
        return None

    # Tự động tìm tên cột chính xác (Phòng hờ tên cột của bạn khác chút)
    real_col_lnst = find_col(df_finance, 'loi_nhuan_sau_thue')
    real_col_tts = find_col(df_finance, 'tong_cong_tai_san')
    real_col_vcsh = find_col(df_finance, 'von_chu_so_huu')
    real_col_vongop = find_col(df_finance, 'von_gop') 

    print(f"Mapping cột: LNST={real_col_lnst}, TTS={real_col_tts}, VCSH={real_col_vcsh}, VonGop={real_col_vongop}")

    if not all([real_col_lnst, real_col_tts, real_col_vcsh, real_col_vongop]):
        print("❌ Lỗi: Không tìm thấy đủ các cột cần thiết để tính toán. Hãy kiểm tra lại tên cột trong file CSV.")
        return

    # 3. Tính Số lượng cổ phiếu lưu hành (Shares Outstanding)
    # Công thức ước tính: Vốn góp / 10,000đ
    df_finance['shares_outstanding'] = df_finance[real_col_vongop] / 10000

    # 4. Tính EPS, ROA, ROE, BVPS cơ bản
    # Tránh chia cho 0 bằng cách replace 0 -> NaN hoặc dùng numpy
    df_finance['eps'] = df_finance[real_col_lnst] / df_finance['shares_outstanding']
    df_finance['roa'] = df_finance[real_col_lnst] / df_finance[real_col_tts]
    df_finance['roe'] = df_finance[real_col_lnst] / df_finance[real_col_vcsh]
    df_finance['bvps'] = df_finance[real_col_vcsh] / df_finance['shares_outstanding']

# 5. Xử lý dữ liệu Giá để tính P/E, P/B
    print("Dang xu ly du lieu gia (OHLCV)...")
    
    # --- BƯỚC QUAN TRỌNG: CHUẨN HÓA TÊN CỘT ---
    # Trong file CSV của bạn cột tên là 'symbol', nhưng bảng Finance đang dùng 'ticker'.
    # Cần đổi tên để 2 bảng khớp nhau khi Merge.
    if 'symbol' in df_price.columns:
        df_price.rename(columns={'symbol': 'cp'}, inplace=True)
    
    # Kiểm tra cột 'time' (Dựa trên ảnh bạn gửi)
    if 'time' in df_price.columns:
        # Convert sang kiểu datetime
        df_price['time'] = pd.to_datetime(df_price['time'])
        # Tách lấy năm
        df_price['year'] = df_price['time'].dt.year
        
        # --- LẤY GIÁ ĐÓNG CỬA CUỐI NĂM ---
        # 1. Sắp xếp: Mã CK (tăng dần) -> Thời gian (GIẢM DẦN - để ngày mới nhất lên đầu)
        df_price = df_price.sort_values(by=['cp', 'time'], ascending=[True, False])
        
        # 2. Group theo Mã và Năm, lấy dòng đầu tiên (chính là dòng có ngày lớn nhất trong năm)
        df_price_yearly = df_price.groupby(['cp', 'year']).first().reset_index()
        
        # 3. Chỉ lấy cột cần thiết: ticker, year, close
        df_price_yearly = df_price_yearly[['cp', 'year', 'close']]
        
        print(f"   -> Đã lấy được giá cuối năm của {len(df_price_yearly)} bản ghi.")

        # --- MERGE VÀO BẢNG TÀI CHÍNH ---
        # Lúc này cả 2 bảng đều có cột 'ticker' và 'year' nên merge sẽ khớp 100%
        df_final = pd.merge(df_finance, df_price_yearly, on=['cp', 'year'], how='left')
        
        # 6. Tính toán P/E và P/B
        # P/E = Giá thị trường / EPS
        # P/E = (Giá * 1000) / EPS
        df_final['pe'] = (df_final['close'] * 1000) / df_final['eps']
        
        # P/B = (Giá * 1000) / BVPS
        df_final['pb'] = (df_final['close'] * 1000) / df_final['bvps']
        
    else:
        print("⚠️ Lỗi: Không tìm thấy cột 'time' trong file giá. Bỏ qua tính P/E, P/B.")
        # Nếu lỗi thì vẫn giữ nguyên bảng tài chính cũ để không bị crash
        df_final = df_finance

    # 7. Chọn lọc các cột kết quả để lưu (cho gọn nhẹ)
    output_cols = ['cp', 'year', 'shares_outstanding', 'close', 
                   'eps', 'roa', 'roe', 'bvps', 'pe', 'pb']
    
    # Thêm các cột gốc quan trọng để đối chiếu nếu cần
    output_cols.extend([real_col_lnst, real_col_tts, real_col_vcsh])
    
    # Lưu file
    df_final = df_final[output_cols].round(3) # Làm tròn 2 số lẻ
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    print("-" * 30)
    print(f"✅ TÍNH TOÁN HOÀN TẤT!")
    print(f"File kết quả: {OUTPUT_FILE}")
    print(df_final[['cp', 'year', 'eps', 'pe', 'roe']].head())

if __name__ == "__main__":
    calculate()