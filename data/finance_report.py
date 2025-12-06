from vnstock import Finance
import pandas as pd
import time
import random
import os

# ==========================================
# CẤU HÌNH AN TOÀN
# ==========================================
VN30_SYMBOLS = [
    "ACB","BID","BVH","CTG","FPT","GAS","GVR","HDB","HPG","MBB",
    "MSN","MWG","NVL","PDR","PLX","POW","SAB","SHB","SSI","STB",
    "TCB","TPB","VCB","VHM","VIB","VIC","VJC","VNM","VPB","VRE"
]

START_YEAR = 2020
END_YEAR   = 2025

# --- Danh sách chứa dữ liệu ---
list_balance_sheet = []
list_income_stmt   = []
list_cash_flow     = []

def filter_time_range(df, start_year, end_year):
    """Hàm lọc dữ liệu và chuẩn hóa tên cột năm"""
    if df.empty: return df
    
    if 'Năm' in df.columns:
        df.rename(columns={'Năm': 'year'}, inplace=True)
    elif 'yearReport' in df.columns:
        df.rename(columns={'yearReport': 'year'}, inplace=True)
        
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        return df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    return df

def random_sleep(min_s, max_s):
    """Hàm ngủ ngẫu nhiên để giả lập người dùng thật"""
    sleep_time = random.uniform(min_s, max_s)
    # print(f"   💤 Nghỉ {sleep_time:.1f}s...") # Bỏ comment nếu muốn xem chi tiết
    time.sleep(sleep_time)

# ==========================================
# CRAWL DỮ LIỆU (CHẾ ĐỘ AN TOÀN)
# ==========================================
print(f"🚀 Bắt đầu lấy báo cáo ({START_YEAR}-{END_YEAR})...")
print("⚠️ Chế độ 'AN TOÀN': Tốc độ sẽ chậm để tránh bị chặn IP.\n")

for i, sym in enumerate(VN30_SYMBOLS):
    success = False
    retry_count = 0
    max_retries = 3

    print(f"[{i+1}/{len(VN30_SYMBOLS)}] 🔍 Đang xử lý: {sym}")

    while not success and retry_count < max_retries:
        try:
            finance = Finance(symbol=sym, source='VCI')

            # --- 1. Lấy Balance Sheet ---
            df_bs = finance.balance_sheet(period='year', lang='vi')
            df_bs = filter_time_range(df_bs, START_YEAR, END_YEAR)
            df_bs['symbol'] = sym
            if not df_bs.empty: list_balance_sheet.append(df_bs)
            
            # 🛑 Nghỉ nhẹ 3-5s giữa các request trong cùng 1 mã
            random_sleep(3, 5) 

            # --- 2. Lấy Income Statement ---
            df_is = finance.income_statement(period='year', lang='vi')
            df_is = filter_time_range(df_is, START_YEAR, END_YEAR)
            df_is['symbol'] = sym
            if not df_is.empty: list_income_stmt.append(df_is)

            # 🛑 Nghỉ nhẹ 3-5s
            random_sleep(3, 5)

            # --- 3. Lấy Cash Flow ---
            df_cf = finance.cash_flow(period='year', lang='vi')
            df_cf = filter_time_range(df_cf, START_YEAR, END_YEAR)
            df_cf['symbol'] = sym
            if not df_cf.empty: list_cash_flow.append(df_cf)

            print(f"   ✅ {sym}: Hoàn thành.")
            success = True
            
            # 🛑 QUAN TRỌNG: Nghỉ dài 10-15s sau khi xong 1 mã
            # Đây là bước quan trọng nhất để reset bộ đếm của server
            print("   ⏳ Đang chuyển mã tiếp theo...")
            random_sleep(10, 15)

        except Exception as e:
            retry_count += 1
            wait_time = 30 * retry_count # Chờ 30s, 60s, 90s nếu lỗi
            print(f"   ⚠️ Lỗi {sym} (Lần {retry_count}): {e}")
            print(f"   🛑 Tạm dừng {wait_time}s để server mở lại...")
            time.sleep(wait_time)

    if not success:
        print(f"   ❌ Bỏ qua {sym} do lỗi quá nhiều lần.")

# ==========================================
# LƯU FILE
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))

save_map = {
    "finance_yearly_balance_sheet.csv": list_balance_sheet,
    "finance_yearly_income_statement.csv": list_income_stmt,
    "finance_yearly_cash_flow.csv": list_cash_flow
}

print("\n" + "="*40)
for filename, data_list in save_map.items():
    if data_list:
        final_df = pd.concat(data_list, ignore_index=True)
        output_path = os.path.join(current_dir, filename)
        final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"📂 Đã lưu: {filename} ({len(final_df)} dòng)")
    else:
        print(f"⚠️ Không có dữ liệu cho {filename}")
print("="*40)