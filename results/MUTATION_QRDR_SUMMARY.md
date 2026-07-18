# Mutation-level validation cho quinolone (Direction AD)

Sinh từ `26_mutation.ipynb`. Đây là **mutation calling THẬT** cho QRDR (Quinolone Resistance-Determining Region), thay cho keyword-proxy của Direction X (chưa chạy). Tự fetch protein sequence gyrA/parC từ BV-BRC (feature_sequence API), trích residue ở vị trí đột biến kháng thuốc đã biết:

- **gyrA**: Ser83, Asp87 (đánh số E. coli/Salmonella)
- **parC**: Ser80, Glu84

Đột biến = residue khác wild-type. Genome CIP/NAL từ AMR.tbl.v4, real prevalence.

## 1. QRDR mutation liên hệ mạnh với kháng thuốc (association)

| Thuốc | Site | Wild-type | % wild-type | n đột biến | R-rate nếu ĐỘT BIẾN | R-rate nếu wild-type |
|---|---|---|---:|---:|---:|---:|
| CIP | gyrA83 | S | 78.8% | 79 | **0.76** | 0.04 |
| CIP | gyrA87 | D | 92.0% | 30 | 0.87 | 0.13 |
| CIP | parC80 | S | 92.8% | 24 | 0.88 | 0.15 |
| NAL | gyrA83 | S | 95.5% | 17 | **0.77** | 0.06 |
| NAL | gyrA87 | D | 93.4% | 25 | 0.84 | 0.04 |
| NAL | parC80 | S | 97.1% | 8 | 0.75 | 0.08 |

→ Đột biến QRDR (nhất là gyrA83) là marker kháng quinolone rất rõ: có đột biến → 75–88% kháng; wild-type → chỉ 4–15%. Đây là cơ chế kháng đã được y văn xác nhận, khớp hoàn toàn.

## 2. Mutation-only prediction (chỉ 4 feature) — random vs MLST group-aware

| Thuốc | n | prevalence | tỷ lệ có đột biến QRDR | mutation random F1 | mutation MLST-group F1 |
|---|---:|---:|---:|---:|---:|
| CIP | 373 | 0.193 | 23.3% | 0.813 | 0.563 |
| **NAL** | 381 | 0.092 | 8.9% | 0.840 | **0.854** |

**So với annotation-based (Direction AC):**

| Thuốc | Annotation random→MLST | Mutation random→MLST |
|---|---|---|
| CIP | 0.839 → **0.504** (sập) | 0.813 → 0.563 |
| NAL | 0.589 → **0.371** (sập) | 0.840 → **0.854 (giữ nguyên)** |

## 3. Kết luận (capstone của khóa luận)

- **Đột biến QRDR thật giải thích cơ chế kháng quinolone** với association rất sạch — điều mà annotation presence/absence KHÔNG bắt được (Direction Z: top feature CIP/NAL không có gyrA/parC).
- **Mechanism-level features cứu được dự đoán bền-lineage:** với NAL, mutation-only (4 feature) giữ F1 0.85 dưới MLST group-aware split, trong khi annotation sập từ 0.59 xuống 0.37. → khẳng định điểm annotation cao là **lineage confounding**, còn mutation là **tín hiệu nhân quả generalize được**.
- **CIP** phức tạp hơn: mutation-only vẫn tụt một phần dưới MLST-split (0.81→0.56) vì CIP còn cơ chế khác (qnr plasmid-mediated, efflux) ngoài QRDR — hợp với y văn.

## 4. Cách viết vào khóa luận

- ✅ *"Mutation calling QRDR thật (gyrA S83/D87, parC S80) cho thấy đột biến liên hệ mạnh với kháng quinolone (R-rate 0.75–0.88 khi đột biến vs 0.04–0.15 khi wild-type). Với NAL, mutation-only features generalize qua dòng (F1 0.85 dưới MLST group-aware) trong khi annotation-based sập về 0.37 — chứng minh mechanism features vượt trội annotation về tính nhân quả và generalization."*
- Đây là bằng chứng trực tiếp cho luận điểm: cần **mutation-level features** cho quinolone, không dùng annotation presence/absence.

Nguồn: `direction_AD_qrdr_association.csv`, `direction_AD_mutation_prediction.csv`. Notebook: `26_mutation.ipynb`.
