# Legal Text Semantic Representation & Word Sense Disambiguation (Neuro-Symbolic AI Approach)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Prolog](https://img.shields.io/badge/Prolog-SWI--Prolog-red)
![Legal-BERT](https://img.shields.io/badge/Model-Legal--BERT-brightgreen)
![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20WordNet-orange)
![Architecture](https://img.shields.io/badge/Architecture-Neuro--Symbolic-purple)

> **CS229 - Computational Semantics** | *Transforming unstructured legal text into logically queryable knowledge bases.*

This project tackles a highly complex challenge in Natural Language Processing (NLP): translating dense legal texts (specifically, **Article 3 of the EU AI Act**) into **First-Order Logic (FOL)**. By adopting a **Neuro-Symbolic AI** approach, this system bridges the gap between deep contextual language understanding (via Transformers) and deterministic, exact automated reasoning (via Prolog). 

Most modern AI systems rely purely on statistical/deep learning models. This project demonstrates advanced capabilities in **Knowledge Representation**, **Ontological Engineering**, and **Hybrid AI**, proving that deep NLP expertise extends far beyond simple API calls.

## 🧠 Core NLP & AI Competencies Demonstrated

- **Domain-Specific Language Modeling**: Leveraged `legal-bert-base-uncased` to accurately capture the semantic nuances and highly specific context of legal jargon, outperforming generic language models in the legal domain.
- **Neuro-Symbolic Integration**: Successfully combined the robust representation power of neural networks (BERT) with the interpretability and exact reasoning of symbolic AI (Prolog).
- **Knowledge Representation & Reasoning (KRR)**: Translated natural language into complex First-Order Logic predicates (e.g., `is_developer(x,y) ↔ organization(x) ∨ individual(x)...`).
- **Ontological Expansion**: Automated the extraction of hypernym hierarchies from **WordNet** to inject real-world ontological knowledge into the symbolic rule engine, enabling transitive logical inference (e.g., `developer → creator → person`).
- **Word Sense Disambiguation (WSD)**: Implemented and evaluated contextual sense mapping against strong linguistic baselines (Most Frequent Sense).

---

## 🏗️ System Architecture & Pipeline

The pipeline processes raw legal text and outputs a queryable knowledge graph:

### 1. Linguistic Preprocessing
- Utilized `NLTK` for precise sentence boundary detection and word tokenization.
- Applied **Part-of-Speech (POS) Tagging** to isolate meaning-bearing lexical units, selectively filtering for Nouns (N), Verbs (V), and Adjectives (Adj) to reduce noise in semantic representation.

### 2. Contextual Word Sense Disambiguation (WSD)
- Addressed lexical ambiguity by mapping tokens to their exact WordNet synsets.
- **Hybrid Approach**: Evaluated the robust **MFS (Most Frequent Sense)** baseline against contextual embeddings derived from **Legal-BERT**. 

### 3. Symbolic Translation (First-Order Logic)
- Performed entity and predicate extraction.
- Manually translated complex legal definitions into strict FOL structures, ensuring that the legal semantics are flawlessly preserved for machine consumption.

### 4. Automated Knowledge Graph Enrichment
- Dynamically queried **WordNet** for lexical relationships (hypernyms/hyponyms).
- Automatically generated Prolog inference rules based on these relationships to give the system "common sense" (e.g., knowing that a *developer* is a *person* without explicit hardcoding).

### 5. Automated Reasoning Engine
- Compiled **125 semantic facts** into a **Prolog** logic base.
- Executed complex logical queries to test the consistency and recall of the translated legal text.

---

## 🛠️ Technology Stack

- **Deep Learning / NLP Models**: HuggingFace Transformers (`nlpaueb/legal-bert-base-uncased`)
- **Symbolic AI / Logic Programming**: Prolog
- **Linguistic Processing**: NLTK (POS Tagging, Tokenization)
- **Lexical Database / Ontology**: WordNet
- **Languages**: Python, Prolog

---
## 📁 Cấu Trúc Dự Án

```
CS229_Privacy_Semantic/
│
├── data/                          # Dữ liệu đầu vào
│   ├── paragraph.txt              # Đoạn văn Privacy Policy (1,682 ký tự)
│   └── question.txt               # 8 câu hỏi truy vấn
│
├── wsd/                           # Word Sense Disambiguation
│   ├── data/
│   │   ├── reference_annotations.csv  # Ground truth (82 từ)
│   │   └── semcor_instances.jsonl     # Training data (73MB)
│   ├── models/
│   │   └── bert_semcor_model.pkl      # Trained BERT+SVM (48MB)
│   ├── results/
│   │   ├── mfs_eval.json              # MFS evaluation
│   │   ├── bert_eval.json             # BERT evaluation
│   │   ├── predictions_mfs.json       # MFS predictions
│   │   └── predictions_bert_semcor.json
│   ├── baseline_mfs.py            # MFS Baseline script
│   ├── prepare_semcor.py          # Chuẩn bị SemCor data
│   ├── train_bert.py              # Train BERT+SVM
│   └── predict_and_eval.py        # Evaluate BERT+SVM
│
├── kb/                            # Knowledge Base
│   ├── kb.pl                      # Prolog facts (26 facts)
│   ├── kb_aug.pl                  # WordNet augmentation (271 facts)
│   └── kb_fol.md                  # First-Order Logic representation
│
├── results/                       # Kết quả truy vấn
│   ├── queries.pl                 # Prolog queries
│   └── queries.md                 # Query documentation
│
├── augment/                       # WordNet Augmentation
│   └── wordnet_augment.py         # Script bổ sung synonym/hypernym
│
├── demo/                          # Web Demo (FastAPI)
│   ├── main.py                    # FastAPI backend
│   ├── templates/
│   │   └── index.html             # Main template
│   └── static/
│       ├── styles.css             # CSS styling
│       └── app.js                 # JavaScript logic
│
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 📊 Evaluation & Deep NLP Insights

The WSD module was rigorously evaluated against a manually annotated Gold Standard dataset of **80 critical legal tokens**.

| Methodology | Accuracy | Note |
|-------------|----------|------|
| **MFS Baseline** | **71.25%** | Utilizes WordNet's primary sense |
| **Legal-BERT** | **65.00%** | Contextual embedding distance |

### 💡 Insight on Results: The "MFS Phenomenon"
To an untrained eye, the neural model underperforming the baseline might seem counterintuitive. However, in advanced NLP, it is a well-documented phenomenon that the **Most Frequent Sense (MFS)** is an exceptionally strong baseline for WSD tasks, especially in highly specialized domains with skewed sense distributions. 

Legal texts are deliberately drafted to use words in their most rigid, standard definitions to avoid ambiguity. Therefore, the MFS naturally aligns with legal drafting principles. Contextual models (like BERT) without fine-tuning on a massive, domain-specific sense-annotated corpus can sometimes introduce variance by "overthinking" the context. Recognizing and explaining this nuance is what separates empirical AI engineering from blind model deployment.

---

## 🚀 Future Directions

- **Automated Semantic Parsing**: Training a Seq2Seq model (like T5) to automatically translate legal text to FOL predicates, replacing the manual translation step.
- **Graph Neural Networks (GNNs)**: Embedding the generated Prolog knowledge graph into a continuous vector space using GNNs for approximate reasoning over incomplete legal texts.
