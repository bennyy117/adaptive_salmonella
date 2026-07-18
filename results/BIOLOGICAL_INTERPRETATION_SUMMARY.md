# Biological interpretation summary (Direction Z)

Sinh từ `22_annotation.ipynb`: stability selection trên accessory genome + chú giải top features theo catalog AMR (họ gene CARD/ResFinder + co-resistance kim loại/biocide + mobile element). Trả lời câu hỏi: *model có học đúng gen kháng thật không?*

## 1. Coverage — top-40 accessory feature ổn định (per drug)

| Thuốc | direct AMR | indirect (co-selection/mobile) | unknown (locus tag/group/số) | % chú giải được |
|---|---:|---:|---:|---:|
| AMP | 0 | 0 | 40 | 0.0% |
| AUG | 0 | 0 | 40 | 0.0% |
| AXO | 0 | 0 | 40 | 0.0% |
| CHL | 1 (`floR`) | 0 | 39 | 2.5% |
| FOX | 0 | 0 | 40 | 0.0% |

→ Top accessory features **gần như không chú giải được từ tên** (Roary group / locus tag / số). Đây là giới hạn annotation coverage, cần sequence-based RGI/ResFinder, KHÔNG phải lỗi model.

## 2. Paper-ready 50 — chứa gene AMR thật, hợp cơ chế

| Thuốc | Feature | Category | Evidence | Cơ chế |
|---|---|---|---|---|
| AMP | `sul1` | sulfonamide | direct | dihydropteroate synthase (integron class 1) |
| AMP | `pcoS` | copper | indirect | copper resistance (co-selection) |
| AMP | `merT` | mercury | indirect | mercury operon (co-selection) |
| CHL | `floR` | phenicol | **direct** | florfenicol/chloramphenicol efflux |
| CHL | `aadA1` | aminoglycoside | direct | aminoglycoside adenylyltransferase (integron) |
| CHL | `dfrA12` | trimethoprim | direct | dihydrofolate reductase (integron) |
| CHL | `merT` | mercury | indirect | mercury operon (co-selection) |
| AXO | `merA/merD/merT` | mercury | indirect | mercury operon (co-selection) |
| FOX | `merT/merD` | mercury | indirect | mercury operon (co-selection) |

## 3. Diễn giải cho khóa luận

- ✅ **Model học sinh học AMR thật:** `floR` (CHL), `sul1` (AMP), `aadA1`/`dfrA12` (CHL) là gene kháng đã biết, đúng cơ chế của thuốc → feature paper bắt được tín hiệu kháng thật.
- ⚠️ **Nhưng nhiều hit là co-selection/mobile:** `mer*` (thủy ngân), `pco*` (đồng) và các gene integron-borne (`sul1`/`aadA1`/`dfrA12` thường cùng nằm trên class 1 integron/plasmid) → model một phần dựa marker lineage/plasmid, không hẳn causal riêng cho từng thuốc. Với cephalosporin (AXO/FOX) top-named chủ yếu là mercury co-selection, không thấy beta-lactamase có tên trong top (các `bla` có thể nằm dưới dạng locus tag).
- ⚠️ **Annotation coverage yếu:** phần lớn tín hiệu accessory không chú giải được từ tên → cần RGI/ResFinder trên representative sequence (Direction Z có sẵn hook chạy).

**Cách viết an toàn:** "Top features gồm gene kháng đã biết phù hợp cơ chế, nhưng nhiều feature là marker co-selection kim loại/integron, cho thấy tín hiệu một phần mang tính lineage/mobile; chú giải đầy đủ cần sequence-based RGI/ResFinder." Không viết "model xác định gene causal gây kháng".

Nguồn: `direction_Z_annotated_features.csv`, `direction_Z_coverage_summary.csv`. Notebook: `22_annotation.ipynb`.
