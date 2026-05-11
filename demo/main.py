#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI Web Demo for CS229 - Word Sense Disambiguation Project

Features:
1. WSD Demo (MFS & BERT+SVM)
2. Knowledge Base Viewer
3. Query Execution
4. WordNet Augmentation Viewer
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import subprocess
from pathlib import Path

# Optional: NLTK for WordNet
try:
    from nltk.corpus import wordnet as wn
    import nltk
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    HAS_WORDNET = True
except ImportError:
    HAS_WORDNET = False
    wn = None

# Paths
ROOT = Path(__file__).parent.parent
WSD_DIR = ROOT / "wsd"
KB_DIR = ROOT / "kb"
RESULTS_DIR = ROOT / "results"
DATA_DIR = ROOT / "data"

app = FastAPI(
    title="CS229 - WSD Demo",
    description="Word Sense Disambiguation & Knowledge Representation Demo",
    version="1.0.0"
)

# Static files and templates
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# ==================== DATA LOADING ====================

def load_json_file(path: Path) -> dict:
    """Load JSON file safely."""
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def load_text_file(path: Path) -> str:
    """Load text file safely."""
    if path.exists():
        return path.read_text(encoding='utf-8')
    return ""


def load_prolog_file(path: Path) -> List[str]:
    """Load Prolog file as list of facts."""
    if path.exists():
        content = path.read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('%')]
        return lines
    return []


# ==================== API MODELS ====================

class WSDRequest(BaseModel):
    word: str
    pos: str = "n"
    context: Optional[str] = None


class QueryRequest(BaseModel):
    query: str


# ==================== API ENDPOINTS ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/paragraph")
async def get_paragraph():
    """Get the Privacy Policy paragraph."""
    paragraph = load_text_file(DATA_DIR / "paragraph.txt")
    return {"paragraph": paragraph}


@app.get("/api/questions")
async def get_questions():
    """Get the list of questions."""
    questions = load_text_file(DATA_DIR / "question.txt")
    return {"questions": questions}


@app.get("/api/annotations")
async def get_annotations():
    """Get reference annotations."""
    path = WSD_DIR / "data" / "reference_annotations.csv"
    if path.exists():
        import csv
        annotations = []
        with path.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                annotations.append(row)
        return {"annotations": annotations, "total": len(annotations)}
    return {"annotations": [], "total": 0}


@app.get("/api/wsd/results")
async def get_wsd_results():
    """Get WSD evaluation results."""
    # Load evaluation files (both have same format now)
    mfs_eval = load_json_file(WSD_DIR / "results" / "mfs_eval.json")
    bert_eval = load_json_file(WSD_DIR / "results" / "bert_eval.json")
    
    # Load predictions for details
    mfs_preds = load_json_file(WSD_DIR / "results" / "predictions_mfs.json")
    bert_preds = load_json_file(WSD_DIR / "results" / "predictions_bert_semcor.json")
    
    return {
        "mfs": {
            "evaluation": mfs_eval,
            "predictions": mfs_preds.get("predictions", [])[:20]
        },
        "bert": {
            "evaluation": bert_eval,
            "predictions": bert_preds.get("predictions", [])[:20]
        }
    }


@app.post("/api/wsd/predict")
async def wsd_predict(req: WSDRequest):
    """Predict word sense using MFS."""
    if not HAS_WORDNET:
        raise HTTPException(status_code=500, detail="WordNet not available")
    
    word = req.word.lower()
    pos = req.pos.lower()
    
    # Map POS
    pos_map = {'n': wn.NOUN, 'v': wn.VERB, 'a': wn.ADJ, 'r': wn.ADV}
    wn_pos = pos_map.get(pos)
    
    # Get synsets
    synsets = wn.synsets(word, pos=wn_pos) if wn_pos else wn.synsets(word)
    
    if not synsets:
        return {"word": word, "pos": pos, "senses": [], "mfs": None}
    
    senses = []
    for syn in synsets[:5]:  # Top 5 senses
        senses.append({
            "name": syn.name(),
            "definition": syn.definition(),
            "examples": syn.examples()[:2],
            "lemmas": syn.lemma_names()[:5]
        })
    
    mfs = synsets[0].name() if synsets else None
    
    return {
        "word": word,
        "pos": pos,
        "senses": senses,
        "mfs": mfs,
        "total_senses": len(synsets)
    }


@app.get("/api/kb")
async def get_knowledge_base():
    """Get knowledge base facts."""
    kb_facts = load_prolog_file(KB_DIR / "kb.pl")
    kb_aug_facts = load_prolog_file(KB_DIR / "kb_aug.pl")
    kb_fol = load_text_file(KB_DIR / "kb_fol.md")
    
    return {
        "kb": kb_facts,
        "kb_augmented": kb_aug_facts,  # Show all
        "kb_augmented_total": len(kb_aug_facts),
        "fol": kb_fol
    }


def compute_query_answers():
    """Compute answers for all 8 predefined queries from kb.pl."""
    kb_facts = load_prolog_file(KB_DIR / "kb.pl")
    
    # Parse facts into a structured format
    facts_dict = {}
    for fact in kb_facts:
        if '(' in fact and fact.endswith('.'):
            # Extract predicate name and arguments
            pred_name = fact.split('(')[0]
            args_str = fact[len(pred_name)+1:-2]  # Remove predicate name, '(', and ').'
            args = [arg.strip() for arg in args_str.split(',')]
            
            if pred_name not in facts_dict:
                facts_dict[pred_name] = []
            facts_dict[pred_name].append(args)
    
    # Compute answers for each query
    answers = {
        "Q1": [],  # collects(google, X)
        "Q2": [],  # uses_for(google, Purpose)
        "Q3": None,  # varies_by(data_collection, privacy_controls)
        "Q4": [],  # stores_under_identifier(google, unique_identifier, not_signed_in, Purpose)
        "Q5": None,  # purpose(google, personal_information, create_or_use_account)
        "Q6": [],  # collects_content(google, X)
        "Q7": [],  # uses_technology(google, Tech)
        "Q8": []   # retains + allows_setting
    }
    
    # Q1: collects(google, X)
    if 'collects' in facts_dict:
        for args in facts_dict['collects']:
            if len(args) >= 2 and args[0] == 'google':
                answers["Q1"].append(args[1])
    
    # Q2: uses_for(google, Purpose)
    if 'uses_for' in facts_dict:
        for args in facts_dict['uses_for']:
            if len(args) >= 2 and args[0] == 'google':
                answers["Q2"].append(args[1])
    
    # Q3: varies_by(data_collection, privacy_controls)
    if 'varies_by' in facts_dict:
        for args in facts_dict['varies_by']:
            if len(args) >= 2 and args[0] == 'data_collection' and args[1] == 'privacy_controls':
                answers["Q3"] = True
                break
    if answers["Q3"] is None:
        answers["Q3"] = False
    
    # Q4: stores_under_identifier(google, unique_identifier, not_signed_in, Purpose)
    if 'stores_under_identifier' in facts_dict:
        for args in facts_dict['stores_under_identifier']:
            if len(args) >= 4 and args[0] == 'google' and args[1] == 'unique_identifier' and args[2] == 'not_signed_in':
                answers["Q4"].append(args[3])
    
    # Q5: purpose(google, personal_information, create_or_use_account)
    if 'purpose' in facts_dict:
        for args in facts_dict['purpose']:
            if len(args) >= 3 and args[0] == 'google' and args[1] == 'personal_information' and args[2] == 'create_or_use_account':
                answers["Q5"] = True
                break
    if answers["Q5"] is None:
        answers["Q5"] = False
    
    # Q6: collects_content(google, X)
    if 'collects_content' in facts_dict:
        for args in facts_dict['collects_content']:
            if len(args) >= 2 and args[0] == 'google':
                answers["Q6"].append(args[1])
    
    # Q7: uses_technology(google, Tech)
    if 'uses_technology' in facts_dict:
        for args in facts_dict['uses_technology']:
            if len(args) >= 2 and args[0] == 'google':
                answers["Q7"].append(args[1])
    
    # Q8: retains(google, data, Policy) + allows_setting
    policies = []
    if 'retains' in facts_dict:
        for args in facts_dict['retains']:
            if len(args) >= 3 and args[0] == 'google' and args[1] == 'data':
                policies.append(args[2])
    
    settings = []
    if 'allows_setting' in facts_dict:
        for args in facts_dict['allows_setting']:
            if len(args) >= 2 and args[0] == 'google':
                settings.append(args[1])
    
    if policies or settings:
        answers["Q8"] = policies + settings
    
    return answers


@app.get("/api/queries")
async def get_queries():
    """Get predefined queries with answers."""
    queries_md = load_text_file(RESULTS_DIR / "queries.md")
    queries_pl = load_text_file(RESULTS_DIR / "queries.pl")
    
    # Compute answers
    answers = compute_query_answers()
    
    # Parse queries from markdown
    queries = []
    lines = queries_md.split('\n')
    for line in lines:
        if line.startswith('| Q'):
            parts = line.split('|')
            if len(parts) >= 5:
                qid = parts[1].strip()
                query_data = {
                    "id": qid,
                    "question": parts[2].strip(),
                    "prolog": parts[3].strip(),
                    "answer_shape": parts[4].strip(),
                    "answer": answers.get(qid, []),
                    "answer_count": len(answers.get(qid, [])) if isinstance(answers.get(qid), list) else (1 if answers.get(qid) else 0)
                }
                queries.append(query_data)
    
    return {
        "queries": queries,
        "prolog_code": queries_pl
    }


@app.post("/api/query/execute")
async def execute_query(req: QueryRequest):
    """
    Execute a Prolog-style query on the Knowledge Base.
    
    Query format: predicate_name or predicate_name(args)
    Examples:
      - collects → returns all collects/2 facts
      - uses_for → returns all uses_for/2 facts
      - purpose → returns all purpose/3 facts
      - collects(google, X) → returns matching facts
    """
    query = req.query.strip()
    query_lower = query.lower()
    
    kb_facts = load_prolog_file(KB_DIR / "kb.pl")
    kb_aug = load_prolog_file(KB_DIR / "kb_aug.pl")
    
    results = []
    
    # Extract predicate name from query
    # e.g., "collects(google, X)" -> "collects"
    # e.g., "collects" -> "collects"
    if "(" in query_lower:
        predicate = query_lower.split("(")[0].strip()
    else:
        predicate = query_lower.strip()
    
    # Search in main KB - exact predicate matching
    for fact in kb_facts:
        fact_lower = fact.lower()
        # Check if fact starts with the predicate name followed by (
        if fact_lower.startswith(f"{predicate}("):
            results.append(fact)
    
    # If searching for synonym or is_a, also search in augmented KB
    if predicate in ["synonym", "is_a"]:
        for fact in kb_aug:
            fact_lower = fact.lower()
            if fact_lower.startswith(f"{predicate}("):
                results.append(fact)
                if len(results) >= 20:  # Limit for display
                    break
    
    # If no results with exact match, try fuzzy search on arguments
    if not results and "(" in query_lower:
        # Extract arguments and search
        args_part = query_lower.split("(")[1].rstrip(")")
        args = [a.strip() for a in args_part.split(",")]
        
        for fact in kb_facts:
            fact_lower = fact.lower()
            if all(arg in fact_lower for arg in args if arg and arg != "x"):
                results.append(fact)
    
    return {
        "query": req.query,
        "predicate": predicate,
        "results": results,
        "count": len(results),
        "note": f"Matched predicate: {predicate}/N" if results else "No exact match found"
    }


@app.get("/api/augmentation")
async def get_augmentation():
    """Get WordNet augmentation data."""
    kb_aug_facts = load_prolog_file(KB_DIR / "kb_aug.pl")
    
    # Parse into categories
    synonyms = [f for f in kb_aug_facts if f.startswith("synonym(")]
    is_a = [f for f in kb_aug_facts if f.startswith("is_a(")]
    
    return {
        "synonyms": synonyms,  # Show all
        "is_a": is_a,  # Show all
        "total_synonyms": len(synonyms),
        "total_is_a": len(is_a),
        "total": len(kb_aug_facts)
    }


@app.get("/api/summary")
async def get_summary():
    """Get project summary statistics."""
    # Count facts
    kb_facts = load_prolog_file(KB_DIR / "kb.pl")
    kb_aug_facts = load_prolog_file(KB_DIR / "kb_aug.pl")
    
    # Get WSD accuracy
    mfs_eval = load_json_file(WSD_DIR / "results" / "mfs_eval.json")
    
    return {
        "paragraph_length": len(load_text_file(DATA_DIR / "paragraph.txt")),
        "kb_facts": len(kb_facts),
        "kb_augmented_facts": len(kb_aug_facts),
        "total_queries": 8,
        "mfs_accuracy": mfs_eval.get("accuracy", 0),
        "annotations_count": 82
    }


# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

