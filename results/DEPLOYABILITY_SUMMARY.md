# Deployability summary — calibration & screening utility (Direction AA)

Sinh từ `23_calibration.ipynb`: out-of-fold probabilities (5×5 stratified CV) trên paper-ready 50, so sánh xác suất chưa/đã hiệu chỉnh (Platt sigmoid, isotonic), và phân tích tính hữu dụng khi sàng lọc. Trả lời: *model có dùng thực tế được không?*

## 1. Calibration — isotonic cải thiện rõ chất lượng xác suất

Brier & ECE (thấp = tốt); LR làm ví dụ:

| Thuốc | Brier uncal | Brier isotonic | ECE uncal | ECE isotonic |
|---|---:|---:|---:|---:|
| AMP | 0.028 | **0.022** | 0.057 | **0.007** |
| AUG | 0.017 | **0.015** | 0.033 | **0.009** |
| AXO | 0.0035 | **0.0034** | 0.013 | **0.004** |
| CHL | 0.031 | **0.019** | 0.076 | **0.005** |
| FOX | 0.006 | **0.005** | 0.024 | **0.005** |

→ Model chưa hiệu chỉnh hơi lệch (ECE tới 0.076 ở CHL); **isotonic calibration giảm ECE xuống ~0.005–0.01** ở mọi thuốc. Khuyến nghị: khi triển khai, bọc model bằng `CalibratedClassifierCV(method="isotonic")` để xác suất đáng tin.

## 2. Operating points — phù hợp sàng lọc (isotonic, ngưỡng 0.5)

| Thuốc | Sensitivity | Specificity | PPV | NPV | Alert rate |
|---|---:|---:|---:|---:|---:|
| AMP | 0.89 | 0.99 | 0.97 | 0.98 | 16% |
| AUG | 0.94 | 0.99 | 0.92 | 0.99 | 12% |
| AXO | 0.97 | 0.997 | 0.96 | 0.998 | 6% |
| CHL | 0.83 | 0.999 | 0.99 | 0.98 | 9% |
| FOX | 0.92 | 0.999 | 0.99 | 0.995 | 6% |

→ **NPV rất cao (0.98–0.998)** = rule-out tốt (âm tính đáng tin); specificity ~0.99 = ít báo động giả; alert rate thấp (6–16%) = gánh nặng xác nhận thấp. CHL sensitivity 0.83 thấp nhất (bỏ sót nhiều nhất) — có thể hạ ngưỡng nếu ưu tiên bắt hết ca kháng.

## 3. Decision curve — net benefit dương so với "điều trị tất cả/không ai"

Ở mọi threshold probability `pt` (0.05–0.5) và mọi thuốc, `net_benefit_model` **luôn > nb_treat_all và > 0** (treat-none). Ví dụ AMP: NB model ~0.15 ổn định trong khi treat-all âm dần (< 0 khi pt>0.1). → model mang lại lợi ích ra quyết định thực sự, không phải chỉ chính xác trên giấy.

## 4. Cách viết vào khóa luận

- ✅ *"Sau hiệu chỉnh isotonic, xác suất dự đoán được calibrate tốt (ECE ~0.005–0.01). Ở ngưỡng vận hành, model đạt NPV 0.98–0.998 và specificity ~0.99, alert rate 6–16% → phù hợp làm công cụ **sàng lọc/rule-out**. Decision-curve cho net benefit dương so với treat-all/treat-none."*
- ⚠️ Giới hạn: đánh giá trên bộ 5 thuốc gốc, cross-validation nội bộ; triển khai thật cần validation theo lineage/serovar/nguồn/năm và trên dữ liệu external nhiều thuốc hơn. AMR prediction là bài toán high-stakes — công cụ là hỗ trợ, không thay thế kiểm nghiệm.
- **Bảng dùng:** `direction_AA_calibration.csv`, `direction_AA_operating_points.csv`, `direction_AA_decision_curve.csv`, `direction_AA_reliability.csv`. Notebook: `23_calibration.ipynb`.
