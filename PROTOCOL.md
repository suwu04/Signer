# PROTOCOL: Systematic Review on Real‑Time Indian Sign Language (ISL) Translation for Mobile Applications (PRISMA 2020)

**Version:** 1.0  
**Protocol type:** Retrospective archival of pre-specified methodology (PRISMA 2020 aligned)  
**Date of archival:** 2025-08-13  
**Planned/actual search window:** 2019-01-01 to 2025-02-10  
**Corresponding work:** “A Systematic Literature Review on Real-Time Indian Sign Language Translation Systems Using NLP and Gesture Recognition for Mobile Applications” (IEEEtran manuscript)

---

## 1. Administrative Information

### 1.1 Authors and Affiliations (CRediT Roles)
- **Deeraj A K** — BMS College of Engineering, Department of Information Science  
  Roles: Conceptualization; Methodology; Screening; Data Curation; Writing – Original Draft
- **G Chandrasekhar** — BMS College of Engineering, Department of Information Science  
  Roles: Methodology; Validation; Formal Analysis; Writing – Review & Editing; Supervision
- **Suraj Sajeevan** — BMS College of Engineering, Department of Information Science  
  Roles: Investigation; Screening; Data Extraction; Visualization; Writing – Review & Editing

> **Contact (corresponding author):** _Replace with email(s)_

### 1.2 Registration and Archiving
- **Public registration:** Not registered (e.g., PROSPERO/OSF not used).  
- **Archiving:** This protocol is **retrospectively archived** in this GitHub repository to document the methodology used prior to synthesis and to support reproducibility.
- **Amendments policy:** Any deviations or updates will be committed as new versions with clear changelog notes (see §13).

### 1.3 Funding and Conflicts of Interest
- **Funding:** No external funding.  
- **Conflicts of interest:** None declared by the authors.

---

## 2. Background and Objectives

### 2.1 Rationale
Automatic sign language recognition and translation systems have advanced through deep learning, but **ISL** remains under-resourced. This review synthesizes methods and deployment considerations for **real-time, mobile-first** ISL translation, focusing on bidirectional pipelines (speech/text→sign; sign→text) and avatar rendering via HamNoSys/SiGML.

### 2.2 Objectives and Research Questions
- **Primary Objective:** Identify architectures and techniques enabling **real-time ISL translation** suitable for mobile or edge deployment.
- **Research Questions (RQs):**
  - **RQ1:** What model architectures (CNNs, RNNs/LSTM/GRU, Transformers, 3D CNNs, hybrids) are used for sign recognition and translation?
  - **RQ2:** What **temporal modelling** strategies are most effective for continuous/co-articulated signing?
  - **RQ3:** How do systems implement **linguistic processing** (glossing, grammar reordering, HamNoSys→SiGML) to preserve **semantic fidelity**?
  - **RQ4:** What datasets and evaluation protocols exist for **ISL** and how do they compare to ASL/BSL corpora?
  - **RQ5:** What are the **latency**, **FPS**, and **resource** profiles of systems claiming real-time operation on mobile/edge hardware?
  - **RQ6:** What gaps exist (data scarcity, signer variability, non-manual features, deployment constraints), and what are future directions?

---

## 3. Eligibility Criteria

- **Study types:** Peer‑reviewed journal articles, conference papers, and reputable preprints (e.g., arXiv) **with empirical evaluation**.  
- **Publication window:** 2019‑01‑01 to 2025‑02‑10.  
- **Languages:** English.  
- **Domains:** Computer Vision, NLP, Human–Computer Interaction, Assistive Tech.  
- **Population/Context:** Sign language users (focus on ISL; comparative insights from ASL/BSL etc. included if methods generalizable to ISL).  
- **Interventions/Systems:** Automatic sign recognition/translation; avatar-based sign generation; real-time or near-real-time pipelines; mobile/edge deployment.  
- **Comparators:** Prior baselines or cross-model comparisons where available.  
- **Outcomes (must report ≥1):**
  - Recognition/translation metrics (e.g., accuracy, BLEU, WER, mAP)
  - **Latency/FPS** or time-to-response metrics for real-time claim
  - Dataset characteristics and reproducibility artefacts (code/data availability)
- **Exclusions:** Patents; purely opinion pieces; static‑gesture‑only without translation; non-empirical descriptions; works lacking sufficient methodological detail.

---

## 4. Information Sources

- **Databases:** IEEE Xplore, ACM Digital Library, SpringerLink, Elsevier ScienceDirect, Scopus.  
- **Supplementary:** Google Scholar (first ~200 hits per query), arXiv (cs.CV, cs.CL).  
- **Manual methods:** Backward/forward citation chasing from included studies; author webpages and project repositories when linked.

**Search completed:** 2025‑02‑10.

---

## 5. Search Strategy

Representative boolean strings (adapted per database syntax):

- **Core string:**  
  `("Indian Sign Language" OR ISL OR "sign language translation" OR "sign language recognition") AND ("real-time" OR realtime OR "low latency" OR "edge" OR mobile) AND ("CNN" OR "LSTM" OR GRU OR "Transformer" OR "3D CNN" OR "deep learning" OR "attention")`

- **Avatar/grammar add-on:**  
  `AND (HamNoSys OR SiGML OR gloss OR "grammar reordering" OR "sign synthesis" OR avatar)`

- **Sign-to-text focus:**  
  `("sign to text" OR SLR OR "continuous sign" OR "co-articulation") AND (temporal OR "sequence modelling" OR "self-attention")`

- **Database-specific notes:**
  - **IEEE Xplore:** Use field filters (Abstract/Title/Author Keywords); apply year range.
  - **ACM DL:** Use ACM CCS Keywords + full text; apply year range.
  - **Scopus:** TITLE-ABS-KEY; limit to English; subject areas: COMP, ENG.
  - **Google Scholar:** Enclose phrases in quotes; screen by title relevance; stop when marginal utility drops.
  - **arXiv:** Use categories cs.CV and cs.CL; filter 2019–2025.

**Deduplication:** Export RIS/BibTeX from each source → import to Mendeley → automatic and manual deduplication.

---

## 6. Selection Process (Screening)

Two independent reviewers screen **titles/abstracts**, then **full text**, against §3. Disagreements resolved by discussion; a third reviewer adjudicates if needed.

- **Tooling:** Mendeley for library; spreadsheet (CSV/Sheets) for screening log.  
- **Inter-rater reliability:** Cohen’s κ calculated on a 10–20% pilot set; threshold target κ ≥ 0.70 before proceeding.
- **Logging:** Exclusions at full-text stage recorded with reasons (e.g., no real-time evaluation; non-translation).

**Planned reporting:** PRISMA 2020 flow diagram with counts at each stage.

---

## 7. Data Collection and Items

### 7.1 Extraction Process
- Two reviewers independently extract using a structured template; conflicts reconciled against the source PDF.
- Pilot 5–10 papers to refine the template and ensure consistency.

### 7.2 Extraction Template (fields)
- Bibliographic: authors, year, venue
- Target language(s): ISL/ASL/BSL/other
- **Task(s):** SLR; SLT; text→sign; sign→text; speech→sign
- **Datasets:** name, size, public/private, signer diversity, capture conditions
- **Model/Architecture:** CNN, RNN/LSTM/GRU, Transformer, 3D CNN, hybrid; **temporal modelling** details
- **Preprocessing & Linguistics:** tokenization, POS, lemmatization, glossing, grammar reordering, HamNoSys/SiGML
- **Training details:** splits, augmentation, hyperparameters (if reported)
- **Evaluation metrics:** accuracy, BLEU, WER, mAP; **latency/FPS**
- **Hardware/Deployment:** device, framework, edge/mobile optimizations (quantization, pruning, ONNX/CoreML/TFLite)
- **Reproducibility:** code link, dataset availability, license
- **Key findings/limitations**
- **Risk of bias indicators** (see §8)

Data stored in a versioned CSV/Sheet (`/data/extraction.csv`).

---

## 8. Risk of Bias / Study Quality Assessment

A bespoke, domain-appropriate checklist (score 0–2 per item; higher = better):  
1) **Dataset transparency** (public + documented)  
2) **Annotation quality** (guidelines, inter-annotator agreement)  
3) **Diversity** (signers, lighting, backgrounds)  
4) **Method transparency** (architecture, hyperparameters)  
5) **Evaluation rigor** (standard splits, cross‑dataset testing)  
6) **Real-time evidence** (measured latency/FPS, hardware specified)  
7) **Reproducibility** (code/models available)  
8) **Linguistic validity** (gloss/grammar handling; non‑manuals considered)

- Two reviewers score independently; disagreements resolved by consensus.
- Sensitivity analysis: exclude high‑risk studies and re‑summarize trends.

---

## 9. Outcomes and Effect Measures

- **Primary outcomes:** recognition/translation accuracy, BLEU/WER, **latency/FPS**.  
- **Secondary outcomes:** model size, parameter count, inference cost; semantic fidelity proxies; user study results where available.

Where appropriate, summarize with medians/IQR; forest/meta-analysis **not planned** due to heterogeneity.

---

## 10. Synthesis Plan

- **Qualitative synthesis:** Group by architecture (CNN/RNN/Transformer/hybrid), modality, and deployment context (mobile/edge/cloud).  
- **Subgroup analyses:** ISL vs non‑ISL datasets; sign-to-text vs text-to-sign; avatar vs non-avatar pipelines.  
- **Narrative comparisons:** Accuracy–latency trade-offs; effects of temporal modelling; impact of grammar pipelines (HamNoSys/SiGML).  
- **Visual summaries:** Tables of methods; concept figures (e.g., NLP pipeline; system architecture).

---

## 11. Data Management

- Reference manager: **Mendeley** (deduplication, citation export).  
- Data files: `data/` directory in this repo (CSV for screening log, extraction table).  
- Code (optional): `analysis/` for any summarization scripts (Python/R).  
- Version control: Git commits with semantic messages; tags for protocol versions.

---

## 12. Ethics and Dissemination

- No human/animal subjects or identifiable data collected.  
- Results disseminated via IEEE‑style manuscript and this public repository.  
- **License:** CC BY 4.0 for this protocol document; ensure third‑party figures respect their licenses.

---

## 13. Versioning and Amendments

- **v1.0 (2025‑08‑13):** Initial retrospective archival of protocol reflecting the methodology used in the manuscript.  
- Future amendments will document: reason for change, sections affected, and impact on results (if any).

---

## 14. PRISMA 2020 Compliance Notes (Abstract & Methods)

- **Abstract items covered:** background, objectives, eligibility criteria, information sources, risk of bias, synthesis, registration/funding statements.  
- **Methods items covered:** eligibility, information sources, search strategy, selection process, data items, risk of bias, effect measures, synthesis methods, reporting bias considerations.

---

## 15. Appendices

### Appendix A: Full Search Strings (Copy‑Paste Ready)

**IEEE Xplore (Abstract or Metadata):**  
```
("Indian Sign Language" OR ISL OR "sign language translation" OR "sign language recognition")
AND ("real-time" OR realtime OR "low latency" OR edge OR mobile)
AND ("CNN" OR "LSTM" OR GRU OR Transformer OR "3D CNN" OR "deep learning" OR attention)
AND (HamNoSys OR SiGML OR gloss OR "grammar reordering" OR avatar)
Year Range: 2019–2025; Language: English
```

**ACM Digital Library:**  
```
query: "Indian Sign Language" OR ISL OR "sign language translation" OR "sign language recognition"
AND ("real-time" OR realtime OR "low latency" OR edge OR mobile)
AND (CNN OR LSTM OR GRU OR Transformer OR "3D CNN" OR "deep learning" OR attention)
AND (HamNoSys OR SiGML OR gloss OR "grammar reordering" OR avatar)
Filter: 2019–2025; English; HCI/AI/ML subject areas
```

**Scopus (TITLE-ABS-KEY):**  
```
TITLE-ABS-KEY(("Indian Sign Language" OR ISL OR "sign language translation" OR "sign language recognition")
AND ("real-time" OR realtime OR "low latency" OR edge OR mobile)
AND (CNN OR LSTM OR GRU OR Transformer OR "3D CNN" OR "deep learning" OR attention)
AND (HamNoSys OR SiGML OR gloss OR "grammar reordering" OR avatar))
AND (PUBYEAR > 2018 AND PUBYEAR < 2026) AND (LANGUAGE(English))
```

**Google Scholar:**  
```
"Indian Sign Language" "real-time" translation OR recognition mobile Transformer OR LSTM HamNoSys SiGML gloss
```
Screen by title; review first ~200 results per major query; stop when marginal utility declines.

**arXiv:**  
```
("Indian Sign Language" OR ISL OR "sign language translation" OR "sign language recognition")
AND (realtime OR "real-time" OR mobile OR edge)
cat: cs.CV OR cs.CL  date: 2019–2025
```

### Appendix B: Screening Log Columns
- record_id, source, year, title, authors, venue, include_title_abs (Y/N), include_fulltext (Y/N), exclusion_reason, notes

### Appendix C: Risk of Bias Scoring Sheet
- study_id, item1_dataset_transparency, item2_annotation_quality, item3_diversity, item4_method_transparency, item5_eval_rigor, item6_realtime_evidence, item7_reproducibility, item8_linguistic_validity, total, risk_category (low/moderate/high)

---

**Retrospective Archiving Statement:**  
This protocol summarizes the **pre-specified methodology** that guided study identification, selection, extraction, and synthesis in the associated manuscript. It is archived here to enhance transparency and reproducibility in line with **PRISMA 2020**.
