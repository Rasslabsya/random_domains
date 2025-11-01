import streamlit as st
import random
import json
import re
from typing import Dict, List, Tuple

@st.cache_data
def load_countries(path: str = "countries.json") -> Dict[str, Dict[str, List[str]]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

COUNTRIES = load_countries()

_WEIGHT_RE = re.compile(r"\((\d+)\)")

def extract_weight(label: str) -> int:
    m = _WEIGHT_RE.search(label)
    return int(m.group(1)) if m else 1

def list_weights_for_blocks(blocks: List[str]) -> List[int]:
    return [extract_weight(b) for b in blocks]

def choose_blocks(blocks: Dict[str, List[str]], *, rng: random.Random) -> List[str]:
    labels = list(blocks.keys())
    weights = list_weights_for_blocks(labels)
    k = rng.randint(3, 4)
    return random.sample(labels, k=k)

def pick_domains(pool: List[str], *, rng: random.Random) -> List[str]:
    count = rng.randint(3, 10)
    k = min(count, len(pool))
    return rng.sample(pool, k)

def generate_for_country(country: str) -> List[Tuple[str, List[str]]]:
    rng = random.Random()
    blocks = COUNTRIES[country]
    chosen_blocks = choose_blocks(blocks, rng=rng)
    result = []
    for b in chosen_blocks:
        result.append((b, pick_domains(blocks[b], rng=rng)))
    return result


st.set_page_config(page_title="🎲 Генератор доменов", layout="centered")

st.title("🎲 Генератор доменов по странам")
st.markdown("Выберите страну и получите случайные домены из разных тематических блоков.")

country = st.selectbox("🌍 Выберите страну:", list(COUNTRIES.keys()))

if st.button("Сгенерировать"):
    items = generate_for_country(country)
    for block, domains in items:
        st.subheader(block)
        st.code("\n".join(domains))
else:
    st.info("👆 Выберите страну и нажмите **Сгенерировать**.")

