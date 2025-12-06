from vnstock import Quote
import pandas as pd
import time
import random
import os

# ==========================================
# CẤU HÌNH
# ==========================================
vn30_symbols = [
    "ACB","BID","BVH","CTG","FPT","GAS","GVR","HDB","HPG","MBB",
    "MSN","MWG","NVL","PDR","PLX","POW","SAB","SHB","SSI","STB",
    "TCB","TPB","VCB","VHM","VIB","VIC","VJC","VNM","VPB","VRE"
]

START_DATE = "2020-09-30"
END_DATE   = "2025-09-30"
FILE_NAME  = "ohlcv_vn30_2020_2025.csv"

all_data = []

print(f"🚀 Bắt đầu lấy dữ liệu giá (OHLCV) từ {START_DATE} đến {END_DATE}...\n")

for i, symbol in enumerate(vn30_symbols):
    try:
        # --- SỬ DỤNG CLASS QUOTE NHƯ YÊU CẦU ---
        quote = Quote(symbol=symbol, source='VCI')
        
        # Lấy dữ liệu lịch sử
        df = quote.history(start=START_DATE, end=END_DATE, interval='1D')
        
        if df is not None and not df.empty:
            # Thêm cột symbol để biết dòng này của mã nào
            df["symbol"] = symbol
            
            # Reset index để cột ngày tháng (time) không bị biến thành index
            if 'time' not in df.columns and 'Date' not in df.columns:
                df.reset_index(inplace=True)
                
            all_data.append(df)
            print(f"[{i+1}/{len(vn30_symbols)}] ✅ {symbol}: Lấy xong {len(df)} dòng.")
        else:
            print(f"[{i+1}/{len(vn30_symbols)}] ⚠️ {symbol}: Không có dữ liệu.")

        # 🛑 Nghỉ ngẫu nhiên 1-3 giây
        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"[{i+1}/{len(vn30_symbols)}] ❌ Lỗi {symbol}: {e}")
        time.sleep(3)

# ==========================================
# LƯU FILE
# ==========================================
if all_data:
    # Gộp dữ liệu
    ohlcv_vn30 = pd.concat(all_data, ignore_index=True)
    
    # Xử lý đường dẫn lưu vào thư mục hiện tại (folder 'data')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, FILE_NAME)
    
    ohlcv_vn30.to_csv(output_path, index=False)
    
    print("\n" + "="*40)
    print(f"🎉 HOÀN THÀNH! Tổng cộng {len(ohlcv_vn30)} dòng dữ liệu.")
    print(f"📂 File đã lưu tại: {output_path}")
    print("="*40)
    
    # Xem trước 5 dòng
    print(ohlcv_vn30.head())
else:
    print("\n❌ Không lấy được dữ liệu nào.")