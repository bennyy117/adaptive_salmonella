# External validation — real prevalence + MLST group-aware (Direction AC)

Sinh từ `25_external_mlst.ipynb`. Sửa hai lỗ hổng validity lớn nhất của external validation cũ (Direction T/U/V):
1. **Real prevalence** thay vì balanced 50/50 ép tay.
2. **MLST group-aware split THẬT** (tự fetch MLST từ BV-BRC genome API) — đúng cái Direction U bị *skip thầm lặng* do metadata rỗng.

Dữ liệu: tự fetch từ BV-BRC — nhãn S/R từ `AMRMetadataReview_2021/tabular/AMR.tbl.v4`, feature = pgfam presence/absence từ genome_feature API, MLST từ genome API. ~370–382 genome/thuốc, ~13k–15k pgfam feature.

## Kết quả chính

| Thuốc | Prevalence thật | random F1 | random AUPRC | **MLST-group F1** | **F1 drop** | neg control (bal acc) |
|---|---:|---:|---:|---:|---:|---:|
| **TET** | 0.533 | 0.947 | 0.971 | **0.911** | **−0.036** 🟢 | 0.50 |
| CIP | 0.195 | 0.839 | 0.881 | **0.504** | **−0.335** 🔴 | 0.47 |
| GEN | 0.105 | 0.756 | 0.877 | **0.530** | **−0.226** 🔴 | 0.51 |
| NAL | 0.092 | 0.589 | 0.682 | **0.371** | **−0.217** 🔴 | 0.55 |

## Hai kết luận quan trọng

### 1. Balanced 50/50 ép tay thổi phồng kết quả
Với **prevalence thật**, điểm thấp hơn nhiều so với Direction U (balanced): CIP F1 0.96 → **0.84**; NAL 0.75 → **0.59**. AUPRC (metric đúng cho lớp hiếm) cho thấy NAL chỉ 0.68. → phải báo cáo real-prevalence + AUPRC, không dùng balanced accuracy trên subset cân bằng ép tay.

### 2. Điểm external cao phần lớn là LINEAGE (MLST) confounding
Khi chặn cùng MLST nằm cả train/test:
- **CIP/NAL/GEN sập về gần baseline** (F1 0.37–0.53, xấp xỉ mức negative control) → mô hình annotation học **cấu trúc dòng (MLST/serovar)**, KHÔNG phải cơ chế kháng. Khớp với Direction Z (top feature CIP/NAL không có gyrA/parC).
- **TET bền vững** (0.947 → 0.911) → dự đoán mang tính **cơ chế** (tet efflux là gene mobile, rõ cơ chế).

Đây chính là lá chắn mà Direction U/V thiếu (cluster-aware của họ thoái hóa thành random). Kết quả nhất quán với Direction AB trên bộ gốc: **chỉ một số thuốc (TET external; AXO/FOX gốc) cho bằng chứng cơ chế bền qua lineage; phần lớn còn lại bị population-structure confounding.**

## Cách viết vào khóa luận

- ✅ *"Với real prevalence + MLST group-aware split, external validation cho thấy **TET generalize qua dòng (mechanism-driven, F1 0.91)** trong khi **CIP/NAL/GEN sập về gần baseline (F1 0.37–0.53) → điểm cao trên random split chủ yếu là lineage confounding**. Điều này đính chính kết quả balanced-subset lạc quan của external validation trước."*
- ❌ Không claim "mô hình dự đoán kháng CIP/NAL từ genome" — annotation-based không bắt cơ chế quinolone; cần mutation-level gyrA/parC.

Nguồn: `direction_AC_external_realprev.csv`, `direction_AC_prevalence.csv`. Notebook: `25_external_mlst.ipynb`.
