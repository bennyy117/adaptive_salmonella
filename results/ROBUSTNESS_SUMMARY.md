# Robustness & statistical validation summary (Direction Y + Y2)

Bản này tổng hợp các kết quả khoa học MỚI dùng để củng cố khóa luận, sinh từ hai notebook mới `20_stat_test.ipynb` (module đơn giản) và `21_stat_test_fusion.ipynb` (toàn bộ module nâng cao của Direction O). Các số dưới đây chạy trên bộ 5 thuốc gốc (repo `347251369`, accessory matrix 1167×18125), repeated stratified CV, feature selection + threshold chỉ fit trên train (không rò rỉ).

Phương pháp kiểm định: **corrected resampled *t*-test (Nadeau–Bengio)** cho repeated k-fold, **Wilcoxon signed-rank**, **bootstrap 95% CI** cho Δ F1, **hiệu chỉnh Holm–Bonferroni** trên 5 thuốc.

## 1. Câu hỏi trung tâm: adaptive feature fusion có thắng paper-ready 50 có ý nghĩa không?

### 1a. Module đơn giản (chi2 / hybrid) — Direction Y (5×5 CV)

| Thuốc | Δ F1 (adaptive − baseline) | 95% CI | p (Holm) | Có ý nghĩa? |
|---|---:|---|---:|:--:|
| AMP | −0.005 | [−0.016, +0.004] | 1.00 | Không |
| AUG | +0.009 | [−0.003, +0.021] | 1.00 | Không |
| AXO | +0.009 | [−0.015, +0.040] | 1.00 | Không |
| CHL | −0.007 | [−0.024, +0.009] | 1.00 | Không |
| FOX | −0.001 | [−0.010, +0.008] | 1.00 | Không |

### 1b. Toàn bộ module nâng cao của Direction O — Direction Y2 (3×5 CV local; notebook đặt 5×5)

| Thuốc | Module nâng cao tốt nhất | Δ F1 | 95% CI | p (Holm) | Có ý nghĩa? |
|---|---|---:|---|---:|:--:|
| AMP | paper_ready50 + chi2_500 | −0.007 | [−0.021, +0.006] | 1.00 | Không |
| AUG | ensemble_top_50 | +0.008 | [−0.005, +0.024] | 1.00 | Không |
| AXO | ensemble_top_50 | +0.012 | [−0.008, +0.033] | 1.00 | Không |
| CHL | paper_ready50 + chi2_200 | −0.015 | [−0.031, −0.001] | 1.00 | Không (kém hơn) |
| FOX | paper_ready50 + chi2_200 | +0.003 | [−0.009, +0.016] | 1.00 | Không |

**Kết luận nhất quán giữa Y và Y2: 0/5 thuốc có cải thiện có ý nghĩa thống kê.** Paper-ready 50 markers là baseline rất mạnh; adaptive feature fusion đạt **parity** (ngang bằng), không vượt trội có ý nghĩa — kể cả với ensemble selector, sample-graph và gene-graph embedding.

## 2. Quan sát mô tả vẫn giữ: mỗi thuốc một module tốt nhất

| Thuốc | Module tốt nhất (mean F1, Y2) | F1 |
|---|---|---:|
| AMP | paper_ready50 | 0.918 |
| AUG | ensemble_top_50 | 0.939 |
| AXO | ensemble_top_50 | 0.967 |
| CHL | paper_ready50 | 0.891 |
| FOX | paper_ready50 + chi2_200 | 0.954 |

Module thắng khác nhau theo thuốc (khớp tinh thần Direction O), nhưng khác biệt không đủ lớn để có ý nghĩa thống kê.

## 3. Lineage-aware evaluation (leave-cluster-out, agglomerative 30 cụm theo Jaccard)

Chẩn đoán: Jaccard tối đa giữa 2 mẫu bất kỳ chỉ ~0.069 → accessory genome rất đa dạng, không có near-duplicate. Ép về 30 cụm rồi GroupKFold:

| Thuốc | F1 drop (Y module đơn giản) | F1 drop (Y2 O adaptive-best) |
|---|---:|---:|
| AMP | +0.039 | +0.023 |
| AUG | −0.026 | +0.021 |
| AXO | +0.021 | −0.004 |
| CHL | −0.016 | +0.024 |
| FOX | −0.001 | +0.019 |

Mức tụt nhỏ (≤ ~0.04 F1) → model bền vừa phải với phân hoạch cụm accessory. **Cảnh báo trung thực:** đây là proxy dựa trên accessory content, KHÔNG phải lineage thật (serovar/cgMLST). Muốn claim lineage-independence mạnh cần metadata serovar/cgMLST/SNP-distance.

## 4. Negative control (shuffled labels) — balanced accuracy

| Thuốc | Y (đơn giản) | Y2 (O adaptive-best) |
|---|---:|---:|
| AMP | 0.51 | 0.50 |
| AUG | 0.48 | 0.48 |
| AXO | 0.50 | 0.45 |
| CHL | 0.51 | 0.50 |
| FOX | 0.47 | 0.53 |

Tất cả ≈ 0.5 → **pipeline không rò rỉ**; kết quả cao ở các phần khác không do leakage.

## 5. Cách viết vào khóa luận (an toàn, không overclaim)

- ✅ *"Accessory-based adaptive feature fusion đạt hiệu năng **ngang bằng thống kê** với 50 marker do chuyên gia chọn (Δ F1 ~0.01, không có ý nghĩa sau hiệu chỉnh Holm trên 5 thuốc). Đóng góp: (i) chọn feature tự động đạt parity mà không cần marker chọn tay; (ii) module thắng khác nhau theo thuốc; (iii) negative control sạch và mức tụt nhỏ khi lineage-aware."*
- ❌ Tránh: *"Direction O cải thiện F1 có ý nghĩa ở 4/5 thuốc"* — kiểm định cho thấy đó là nhiễu.
- Nguồn số: `direction_Y_*.csv`, `direction_Y2_*.csv` trong thư mục này. Notebook tái tạo: `20_stat_test.ipynb`, `21_stat_test_fusion.ipynb`.
