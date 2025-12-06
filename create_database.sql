USE da_stock_db;

-- 1. Bảng DIM: Danh sách công ty
-- Khóa chính: ticker
DROP TABLE IF EXISTS dim_company_info;
CREATE TABLE dim_company_info (
    ticker VARCHAR(10) NOT NULL,
    ten_cong_ty VARCHAR(255),
    nganh VARCHAR(100),
    PRIMARY KEY (ticker)
);DROP TABLE IF EXISTS fact_market_index;
CREATE TABLE fact_market_index (
    -- 1. CÁC CỘT DỮ LIỆU
    symbol VARCHAR(20) NOT NULL,      
    time DATETIME NOT NULL,           
    open DOUBLE,                      
    high DOUBLE,                    
    low DOUBLE,                       
    close DOUBLE,                    
    volume BIGINT,                   

    -- 2. KHÓA CHÍNH VÀ INDEX
    -- Mỗi chỉ số tại một thời điểm là duy nhất
    PRIMARY KEY (symbol, time),
    INDEX idx_time (time)
);
-- 2. Bảng FACT: Chỉ số tài chính (ROE, ROA, P/E...)
-- Khóa chính: (ticker, year) -> Một mã trong 1 năm chỉ có 1 dòng
DROP TABLE IF EXISTS fact_financial_ratio;
CREATE TABLE fact_financial_ratio (
    cp VARCHAR(10) NOT NULL,
    year INT NOT NULL,
    shares_outstanding DOUBLE,
    close DOUBLE,
    eps DOUBLE,
    roa DOUBLE,
    roe DOUBLE,
    bvps DOUBLE,
    pe DOUBLE,
    pb DOUBLE,
    loi_nhuan_sau_thue_cua_co_dong_cong_ty_me_dong DOUBLE,
    tong_cong_tai_san_dong DOUBLE,
    von_chu_so_huu_dong DOUBLE,
    PRIMARY KEY (cp, year),
    INDEX idx_year (year)
);

-- 3. Bảng FACT: Giá cổ phiếu (OHLCV)
-- Khóa chính: (ticker, time) -> Một mã tại 1 thời điểm chỉ có 1 dòng
DROP TABLE IF EXISTS fact_stock_price;
CREATE TABLE fact_stock_price (
    time DATETIME NOT NULL,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume BIGINT,
    symbol VARCHAR(10) NOT NULL,
    year INT,
    PRIMARY KEY (symbol, time),
    INDEX idx_time (time)
);

-- 4. Bảng FACT: Báo cáo tài chính (Cân đối kế toán, KQKD...)
-- Ví dụ đại diện, các bảng khác cấu trúc tương tự
-- Xóa bảng cũ nếu tồn tại để tạo lại cấu trúc mới chuẩn chỉnh
DROP TABLE IF EXISTS fact_balance_sheet;

CREATE TABLE fact_balance_sheet (
    -- 1. CÁC CỘT ĐỊNH DANH (DIMENSIONS)
    cp VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    symbol VARCHAR(20),

    -- 2. CÁC CỘT SỐ LIỆU TÀI CHÍNH (METRICS - DOUBLE)
    tong_cong_tai_san_dong DOUBLE,
    tien_va_tuong_duong_tien_dong DOUBLE,
    tien_gui_tai_ngan_hang_nha_nuoc_viet_nam DOUBLE,
    tien_gui_tai_cac_tctd_khac_va_cho_vay_cac_tctd_khac DOUBLE,
    chung_khoan_kinh_doanh DOUBLE,
    chung_khoan_kinh_doanh_2 DOUBLE,
    du_phong_giam_gia_chung_khoan_kinh_doanh DOUBLE,
    cac_cong_cu_tai_chinh_phai_sinh_va_khoan_no_tai_chinh_khac DOUBLE,
    cho_vay_khach_hang DOUBLE,
    cho_vay_khach_hang_2 DOUBLE,
    du_phong_rui_ro_cho_vay_khach_hang DOUBLE,
    chung_khoan_dau_tu DOUBLE,
    chung_khoan_dau_tu_san_sang_de_ban DOUBLE,
    chung_khoan_dau_tu_giu_den_ngay_dao_han DOUBLE,
    du_phong_giam_gia_chung_khoan_dau_tu DOUBLE,
    dau_tu_dai_han_dong DOUBLE,
    dau_tu_vao_cong_ty_lien_doanh DOUBLE,
    tai_san_dai_han_khac_dong DOUBLE,
    du_phong_giam_gia_dau_tu_dai_han DOUBLE,
    tai_san_co_dinh_dong DOUBLE,
    tai_san_co_dinh_huu_hinh DOUBLE,
    tai_san_co_dinh_vo_hinh DOUBLE,
    gia_tri_rong_tai_san_dau_tu DOUBLE,
    tai_san_co_khac DOUBLE,
    tong_cong_nguon_von_dong DOUBLE,
    no_phai_tra_dong DOUBLE,
    cac_khoan_no_chinh_phu_va_nhnn_viet_nam DOUBLE,
    tien_gui_va_vay_cac_to_chuc_tin_dung_khac DOUBLE,
    tien_gui_cua_khach_hang DOUBLE,
    cac_cong_cu_tai_chinh_phai_sinh_va_khoan_no_tai_chinh_khac_2 DOUBLE,
    von_tai_tro_uy_thac_dau_tu_cua_cp_va_cac_to_chuc_td_khac DOUBLE,
    phat_hanh_giay_to_co_gia DOUBLE,
    cac_khoan_no_khac DOUBLE,
    von_chu_so_huu_dong DOUBLE,
    von_cua_to_chuc_tin_dung DOUBLE,
    quy_cua_to_chuc_tin_dung DOUBLE,
    lai_chua_phan_phoi_dong DOUBLE,
    von_gop_cua_chu_so_huu_dong DOUBLE,
    dau_tu_vao_cong_ty_con DOUBLE,
    tai_san_co_dinh_thue_tai_chinh DOUBLE,
    chenh_lech_ty_gia_hoi_doai DOUBLE,
    cac_quy_khac DOUBLE,
    loi_ich_cua_co_dong_thieu_so DOUBLE,
    tai_san_ngan_han_dong DOUBLE,
    gia_tri_thuan_dau_tu_ngan_han_dong DOUBLE,
    cac_khoan_phai_thu_ngan_han_dong DOUBLE,
    hang_ton_kho_rong DOUBLE,
    tai_san_luu_dong_khac DOUBLE,
    tai_san_dai_han_dong DOUBLE,
    phai_thu_dai_han_dong DOUBLE,
    tai_san_dai_han_khac DOUBLE,
    no_ngan_han_dong DOUBLE,
    no_dai_han_dong DOUBLE,
    von_va_cac_quy_dong DOUBLE,
    co_dong_thieu_so DOUBLE,
    tra_truoc_cho_nguoi_ban_ngan_han_dong DOUBLE,
    phai_thu_ve_cho_vay_ngan_han_dong DOUBLE,
    hang_ton_kho_rong_dong DOUBLE,
    tai_san_luu_dong_khac_dong DOUBLE,
    quy_dau_tu_va_phat_trien_dong DOUBLE,
    co_phieu_pho_thong_dong DOUBLE,
    vay_va_no_thue_tai_chinh_dai_han_dong DOUBLE,
    nguoi_mua_tra_tien_truoc_ngan_han_dong DOUBLE,
    vay_va_no_thue_tai_chinh_ngan_han_dong DOUBLE,
    tra_truoc_dai_han_dong DOUBLE,
    phai_thu_dai_han_khac_dong DOUBLE,
    phai_thu_ve_cho_vay_dai_han_dong DOUBLE,
    loi_the_thuong_mai DOUBLE,
    von_ngan_sach_nha_nuoc_va_quy_khac DOUBLE,
    loi_the_thuong_mai_dong DOUBLE,
    trai_phieu_chuyen_doi_dong DOUBLE,
    chenh_lech_danh_gia_lai_tai_san DOUBLE,

    -- 3. KHÓA CHÍNH VÀ INDEX
    PRIMARY KEY (cp, year),
    INDEX idx_year (year)
);
-- Tương tự cho fact_income_statement, fact_cash_flow...
-- Xóa bảng cũ nếu tồn tại
DROP TABLE IF EXISTS fact_cash_flow;
CREATE TABLE fact_cash_flow (
    -- 1. CÁC CỘT ĐỊNH DANH
    cp VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    symbol VARCHAR(20),

    -- 2. CÁC CỘT SỐ LIỆU DÒNG TIỀN (DOUBLE)
    lailo_cac_hoat_dong_khac DOUBLE,
    luu_chuyen_tien_thuan_tu_hdkd_truoc_thay_doi_vld DOUBLE,
    luu_chuyen_tien_thuan_tu_hdkd_truoc_thue DOUBLE,
    chi_tu_cac_quy_cua_tctd DOUBLE,
    mua_sam_tscd DOUBLE,
    tien_thu_co_tuc_va_loi_nhuan_duoc_chia DOUBLE,
    luu_chuyen_tu_hoat_dong_dau_tu DOUBLE,
    tang_von_co_phan_tu_gop_von_vahoac_phat_hanh_co_phieu DOUBLE,
    luu_chuyen_tien_tu_hoat_dong_tai_chinh DOUBLE,
    luu_chuyen_tien_thuan_trong_ky DOUBLE,
    tien_va_tuong_duong_tien DOUBLE,
    anh_huong_cua_chenh_lech_ty_gia DOUBLE,
    tien_va_tuong_duong_tien_cuoi_ky DOUBLE,
    luu_chuyen_tien_te_rong_tu_cac_hoat_dong_sxkd DOUBLE,
    tien_thu_duoc_tu_thanh_ly_tai_san_co_dinh DOUBLE,
    dau_tu_vao_cac_doanh_nghiep_khac DOUBLE,
    tien_thu_tu_viec_ban_cac_khoan_dau_tu_vao_doanh_nghiep_khac DOUBLE,
    co_tuc_da_tra DOUBLE,
    
    lailo_rong_truoc_thue DOUBLE,
    khau_hao_tscd DOUBLE,
    du_phong_rr_tin_dung DOUBLE,
    lailo_chenh_lech_ty_gia_chua_thuc_hien DOUBLE,
    lailo_tu_hoat_dong_dau_tu DOUBLE,
    thu_nhap_lai DOUBLE,
    tanggiam_cac_khoan_phai_thu DOUBLE,
    tanggiam_hang_ton_kho DOUBLE,
    tanggiam_cac_khoan_phai_tra DOUBLE,
    tanggiam_chi_phi_tra_truoc DOUBLE,
    chi_phi_lai_vay_da_tra DOUBLE,
    tien_thu_nhap_doanh_nghiep_da_tra DOUBLE,
    tien_chi_khac_tu_cac_hoat_dong_kinh_doanh DOUBLE,
    tien_chi_cho_vay_mua_cong_cu_no_cua_don_vi_khac_dong DOUBLE,
    tien_thu_hoi_cho_vay_ban_lai_cac_cong_cu_no_cua_don_vi_khac_dong DOUBLE,
    chi_tra_cho_viec_mua_lai_tra_co_phieu DOUBLE,
    tien_thu_duoc_cac_khoan_di_vay DOUBLE,
    tien_tra_cac_khoan_di_vay DOUBLE,
    tien_thu_khac_tu_cac_hoat_dong_kinh_doanh DOUBLE,
    tien_thanh_toan_von_goc_di_thue_tai_chinh DOUBLE,
    co_tuc_da_nhan DOUBLE,
    lailo_tu_thanh_ly_tai_san_co_dinh DOUBLE,
    thu_lai_va_co_tuc DOUBLE,
    tanggiam_cac_khoan_phai_thu_2 DOUBLE,
    tanggiam_cac_khoan_phai_tra_2 DOUBLE,

    -- 3. KHÓA CHÍNH VÀ INDEX
    PRIMARY KEY (cp, year),
    INDEX idx_year (year)
);
-- Xóa bảng cũ nếu tồn tại
DROP TABLE IF EXISTS fact_income_statement;

CREATE TABLE fact_income_statement (
    -- 1. CÁC CỘT ĐỊNH DANH
    cp VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    symbol VARCHAR(20),

    -- 2. CÁC CỘT SỐ LIỆU KINH DOANH (DOUBLE)
    doanh_thu_dong DOUBLE,
    tang_truong_doanh_thu DOUBLE,
    loi_nhuan_sau_thue_cua_co_dong_cong_ty_me_dong DOUBLE,
    tang_truong_loi_nhuan DOUBLE,
    
    -- Nhóm Ngân hàng / Tài chính
    thu_nhap_lai_va_cac_khoan_tuong_tu DOUBLE,
    chi_phi_lai_va_cac_khoan_tuong_tu DOUBLE,
    thu_nhap_lai_thuan DOUBLE,
    thu_nhap_tu_hoat_dong_dich_vu DOUBLE,
    chi_phi_hoat_dong_dich_vu DOUBLE,
    lai_thuan_tu_hoat_dong_dich_vu DOUBLE,
    kinh_doanh_ngoai_hoi_va_vang DOUBLE,
    chung_khoan_kinh_doanh DOUBLE,
    chung_khoan_dau_tu DOUBLE,
    hoat_dong_khac DOUBLE,
    chi_phi_hoat_dong_khac DOUBLE,
    lailo_thuan_tu_hoat_dong_khac DOUBLE,
    co_tuc_da_nhan DOUBLE,
    tong_thu_nhap_hoat_dong DOUBLE,
    ln_tu_hdkd_truoc_cf_du_phong DOUBLE,
    chi_phi_du_phong_rui_ro_tin_dung DOUBLE,

    -- Nhóm Doanh nghiệp sản xuất / Chung
    doanh_thu_ban_hang_va_cung_cap_dich_vu DOUBLE,
    cac_khoan_giam_tru_doanh_thu DOUBLE,
    doanh_thu_thuan DOUBLE,
    gia_von_hang_ban DOUBLE,
    lai_gop DOUBLE,
    thu_nhap_tai_chinh DOUBLE,
    chi_phi_tai_chinh DOUBLE,
    chi_phi_tien_lai_vay DOUBLE,
    lailo_tu_hoat_dong_kinh_doanh DOUBLE,
    chi_phi_ban_hang DOUBLE,
    chi_phi_quan_ly_dn DOUBLE,
    thu_nhap_khac DOUBLE,
    thu_nhapchi_phi_khac DOUBLE, -- Lưu ý tên cột này hơi lạ trong csv gốc, giữ nguyên
    loi_nhuan_khac DOUBLE,
    lai_lo_trong_cong_ty_lien_doanh_lien_ket DOUBLE,
    lailo_tu_cong_ty_lien_doanh DOUBLE,

    -- Nhóm Kết quả & Thuế
    ln_truoc_thue DOUBLE,
    thue_tndn DOUBLE,
    chi_phi_thue_tndn_hien_hanh DOUBLE,
    chi_phi_thue_tndn_hoan_lai DOUBLE,
    loi_nhuan_thuan DOUBLE,
    co_dong_cua_cong_ty_me DOUBLE,
    co_dong_thieu_so DOUBLE,
    lai_co_ban_tren_co_phieu DOUBLE,

    -- 3. KHÓA CHÍNH VÀ INDEX
    PRIMARY KEY (cp, year),
    INDEX idx_year (year)
);
DROP TABLE IF EXISTS fact_vn_macro_economic;

CREATE TABLE fact_vn_macro_economic (
    year INT NOT NULL,
    gdp DOUBLE,
    cpi DOUBLE,
    unemployment DOUBLE,
    interestrate DOUBLE,
    exchangerate DOUBLE,
    retailsales DOUBLE,
    PRIMARY KEY (year)
);
