# Lineage-aware validation & single-marker reliance (Direction AB)

Sinh từ `24_lineage.ipynb`. Đây là kiểm tra validity quan trọng nhất mà các notebook cũ còn thiếu: kiểm soát **cấu trúc quần thể (population structure)** bằng khoảng cách phát sinh loài THẬT từ core SNP matrix (126,087 SNP × 1167 genome), thay vì Jaccard annotation (vốn thoái hóa thành random ở V/U).

## 1. Phát hiện nền tảng: dữ liệu gần như ĐƠN DÒNG (clonal)

Cluster core-SNP (average linkage) theo ngưỡng khoảng cách:

| Ngưỡng SNP-distance | Số dòng (lineage) | Dòng lớn nhất | % dữ liệu |
|---:|---:|---:|---:|
| 0.05 | 14 | 1137 | 97.4% |
| 0.10 | 13 | 1138 | 97.5% |
| 0.20 | 13 | 1138 | 97.5% |
| 0.30 | 8 | 1156 | 99.1% |

→ **~97–99% genome thuộc MỘT dòng clonal duy nhất.** Đa dạng phát sinh loài của bộ dữ liệu rất thấp. Hệ quả: random cross-validation thực chất là đánh giá **trong cùng một dòng**; không thể kiểm chứng cross-lineage generalization thật sự. Đây là giới hạn cốt lõi cần nêu rõ.

## 2. Sub-lineage blocked CV: random vs leave-sub-lineage-out (ward K=20, cân bằng)

F1 khi KHÔNG cho cùng sub-lineage nằm cả train lẫn test (config accessory_chi2_200):

| Thuốc | random F1 | sub-lineage F1 | F1 drop | Diễn giải |
|---|---:|---:|---:|---|
| **AXO** | 0.943 | 0.895 | **−0.048** | robust → dự đoán mang tính cơ chế |
| **FOX** | 0.898 | 0.865 | **−0.033** | robust → dự đoán mang tính cơ chế |
| AUG | 0.927 | 0.689 | −0.238 | một phần confound bởi dòng |
| CHL | 0.873 | 0.570 | −0.303 | phần lớn confound bởi dòng |
| AMP | 0.854 | 0.470 | −0.384 | phần lớn confound bởi dòng |

(paper_ready50 cùng xu hướng: AXO/FOX drop nhỏ; AMP/AUG/CHL drop lớn.)

**Kết luận quan trọng:** hiệu năng cao trên random split **KHÔNG đồng nghĩa với dự đoán cơ chế kháng**. Với **AXO/FOX (cephalosporin)** dự đoán bền qua sub-lineage → nhiều khả năng bắt cơ chế thật (ESBL/AmpC). Với **AMP/AUG/CHL** hiệu năng tụt mạnh (0.24–0.38 F1) khi chặn rò rỉ dòng → một phần lớn là **population-structure confounding**, không phải tín hiệu kháng nhân quả.

> Lưu ý: vì dữ liệu ~97% một dòng, "sub-lineage" ở đây là các cụm con trong dòng chính (ward chia ~40%/32%/...); đây là blocked-CV giữa sub-population, không phải nhiều dòng độc lập. Đã nêu rõ để tránh overclaim.

## 3. Single-marker reliance (feature-dropout, accessory_chi2_200/LR)

F1 khi bỏ top-k feature quan trọng nhất:

| Thuốc | full | bỏ top-1 | bỏ top-5 | bỏ top-10 | Nhận xét |
|---|---:|---:|---:|---:|---|
| AXO | 0.943 | 0.937 | **0.837** | 0.839 | phụ thuộc mạnh top 2–5 marker |
| FOX | 0.898 | 0.891 | 0.799 | **0.768** | phụ thuộc top 5–10 marker |
| AUG | 0.927 | 0.921 | 0.899 | 0.898 | phụ thuộc nhẹ |
| AMP | 0.854 | 0.850 | 0.842 | 0.849 | tín hiệu phân tán, bền |
| CHL | 0.873 | 0.873 | 0.879 | 0.877 | tín hiệu phân tán, bền |

→ AXO/FOX dựa vào một nhúm marker hàng đầu (nhất quán: đó là các marker cơ chế beta-lactam, nên vừa lineage-robust vừa nhạy khi bỏ). AMP/CHL phân tán, không phụ thuộc 1 marker đơn.

## 4. Cách viết vào khóa luận (kết quả CHÍNH đáng tin)

Câu chuyện chính mạnh và trung thực:

1. **Accessory genome là nguồn tín hiệu chính** (Direction C, vẫn đúng).
2. **Cảnh báo population structure:** bộ dữ liệu ~97% một dòng clonal → điểm random split lạc quan.
3. **Kiểm tra lineage-aware:** dưới sub-lineage blocked CV, **AXO/FOX bền (drop ≤0.05) → dự đoán mang tính cơ chế; AMP/AUG/CHL tụt 0.24–0.38 → phần lớn là lineage confounding.** Đây là kết quả chính nuanced, có giá trị khoa học cao.
4. Kết hợp với Y/Y2 (adaptive fusion = parity, không có ý nghĩa) và Z (top feature lẫn co-selection) → thông điệp nhất quán: **mô hình dự đoán tốt nhưng cần thận trọng về nhân quả và generalization; chỉ AXO/FOX cho bằng chứng cơ chế mạnh.**

**Không nên viết:** "mô hình generalize sang dòng/serovar mới" — dữ liệu không đủ đa dạng để khẳng định.

Nguồn: `direction_AB_population_structure.csv`, `direction_AB_sublineage_aware.csv`, `direction_AB_feature_dropout.csv`. Notebook: `24_lineage.ipynb`.
