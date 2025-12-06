from vnstock import Quote
import pandas as pd
import os

# ==========================================
# 1. CẤU HÌNH
# ==========================================
SYMBOL = 'VNINDEX'
START_DATE = "2020-01-01"  # Lấy rộng ra từ đầu năm 2020
END_DATE   = "2025-09-30"
FILE_NAME  = "VNINDEX_2020_2025.csv"

# ==========================================
# 2. XỬ LÝ DỮ LIỆU
# ==========================================
def get_vnindex_data():
    print(f"🚀 Bắt đầu lấy dữ liệu {SYMBOL} ({START_DATE} - {END_DATE})...")
    
    try:
        # Khởi tạo đối tượng Quote
        # source='VCI' hoặc 'TCBS' đều được, VCI thường trả về nhanh hơn cho lịch sử giá
        quote = Quote(symbol=SYMBOL, source='VCI')
        
        # Lấy dữ liệu lịch sử (interval='1D' là khung ngày)
        df = quote.history(start=START_DATE, end=END_DATE, interval='1D')
        
        if df is not None and not df.empty:
            # Thêm cột symbol để định danh
            df.insert(0, 'symbol', SYMBOL)
            
            # Reset index để cột ngày tháng (time/Date) hiển thị rõ ràng
            if 'time' not in df.columns and 'Date' not in df.columns:
                df.reset_index(inplace=True)
                
            return df
        else:
            return None

    except Exception as e:
        print(f"❌ Lỗi khi lấy {SYMBOL}: {e}")
        return None

# ==========================================
# 3. CHẠY VÀ LƯU FILE
# ==========================================
if __name__ == "__main__":
    df = get_vnindex_data()
    
    if df is not None:
        # Lấy đường dẫn thư mục hiện tại (thư mục chứa code này)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, FILE_NAME)
        
        # Lưu file CSV
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print("\n" + "="*40)
        print(f"🎉 HOÀN THÀNH!")
        print(f"📂 File đã lưu tại: {output_path}")
        print(f"📊 Tổng số dòng: {len(df)}")
        print("="*40)
        
        # Xem trước 5 dòng đầu
        print(df.head())
    else:
        print(f"❌ Không lấy được dữ liệu của {SYMBOL}.")