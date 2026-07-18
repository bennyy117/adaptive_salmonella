# Results snapshot

Thư mục này lưu các bảng kết quả chốt đã được trích từ notebook/PDF hiện có để dễ viết báo cáo, slide và kiểm tra claim. Đây là snapshot thủ công từ các kết quả đã chạy, không phải output tự động mới từ model.

Các file:

- `direction_O_summary.csv`: kết quả Direction O trên 5 thuốc gốc.
- `direction_R_setting_mean.csv`: mean F1 theo setting trong mô phỏng leave-one-drug-out.
- `external_validation_summary.csv`: kết quả external validation từ Direction T/U/V.
- `claim_evidence_limitations.csv`: bảng claim, bằng chứng và giới hạn cần viết kèm.
- `next_steps.csv`: thứ tự việc nên làm tiếp.
- `notebook_inventory.csv`: inventory notebook tạo từ `scripts/build_project_inventory.py`.

### Kết quả robustness/thống kê mới (từ notebook Y và Y2)

- `ROBUSTNESS_SUMMARY.md`: bản tổng hợp để viết chương Results/Robustness. Kết luận chính: adaptive feature fusion **ngang bằng** paper-ready 50 về mặt thống kê (0/5 thuốc có ý nghĩa sau Holm), cả với module đơn giản (Y) lẫn module nâng cao của Direction O (Y2).
- `direction_Y_statistical_comparison.csv`, `direction_Y_lineage_aware.csv`, `direction_Y_negative_control.csv`: kết quả module đơn giản (chi2/hybrid), sinh từ `20_stat_test.ipynb`.
- `direction_Y2_statistical_comparison.csv`, `direction_Y2_mean_scores.csv`, `direction_Y2_lineage_aware.csv`, `direction_Y2_negative_control.csv`: kết quả toàn bộ module Direction O qua harness thống kê, sinh từ `21_stat_test_fusion.ipynb`.

### Chú giải sinh học (Direction Z)

- `BIOLOGICAL_INTERPRETATION_SUMMARY.md`: bản tổng hợp cho chương Biological interpretation/Limitations. Kết luận: paper-ready 50 chứa gene AMR thật hợp cơ chế (floR/sul1/aadA1/dfrA12), nhưng nhiều hit là co-selection kim loại/integron; top accessory gần như không chú giải được từ tên (cần sequence-based RGI/ResFinder).
- `direction_Z_annotated_features.csv`, `direction_Z_coverage_summary.csv`: sinh từ `22_annotation.ipynb`.

### Deployability — calibration & screening (Direction AA)

- `DEPLOYABILITY_SUMMARY.md`: chương "dùng thực tế được không". Kết luận: isotonic calibration đưa ECE về ~0.005–0.01; NPV 0.98–0.998 + specificity ~0.99 → phù hợp rule-out/sàng lọc; decision-curve net benefit dương so với treat-all/none.
- `direction_AA_calibration.csv`, `direction_AA_operating_points.csv`, `direction_AA_decision_curve.csv`, `direction_AA_reliability.csv`: sinh từ `23_calibration.ipynb`.

### Lineage-aware validation & single-marker reliance (Direction AB)

- `LINEAGE_AWARE_SUMMARY.md`: kiểm tra validity quan trọng nhất. Kết luận: dữ liệu ~97-99% một dòng clonal (core SNP); dưới sub-lineage blocked CV, AXO/FOX bền (drop ≤0.05, mang tính cơ chế) còn AMP/AUG/CHL tụt 0.24-0.38 (phần lớn là population-structure confounding); feature-dropout cho thấy AXO/FOX dựa vào vài marker hàng đầu.
- `direction_AB_population_structure.csv`, `direction_AB_sublineage_aware.csv`, `direction_AB_feature_dropout.csv`: sinh từ `24_lineage.ipynb`.

### External real-prevalence + MLST group-aware (Direction AC)

- `EXTERNAL_VALIDITY_SUMMARY.md`: tự fetch BV-BRC, real prevalence + MLST group-split (sửa lỗi balanced-subset & group-split-skip của U). Kết luận: TET generalize thật (F1 0.91 dưới MLST-split); CIP/NAL/GEN sập về ~0.5 → lineage confounding.
- `direction_AC_external_realprev.csv`, `direction_AC_prevalence.csv`: sinh từ `25_external_mlst.ipynb`.

### Mutation-level QRDR cho quinolone (Direction AD)

- `MUTATION_QRDR_SUMMARY.md`: mutation calling thật gyrA/parC. Đột biến QRDR liên hệ mạnh với kháng (R 0.75-0.88 vs 0.04-0.15); mutation-only cho NAL giữ F1 0.85 dưới MLST-split (annotation sập còn 0.37).
- `direction_AD_qrdr_association.csv`, `direction_AD_mutation_prediction.csv`: sinh từ `26_mutation.ipynb`.

Lưu ý: output đầy đủ từ Colab vẫn nằm trong các notebook hoặc `/content/...` khi chạy lại. Nếu cần tái lập hoàn toàn, nên chạy lại Direction W và copy toàn bộ `direction_W_final_outputs/` vào đây.
