# streamlit_app.py
from __future__ import annotations
import math
import json
from typing import Dict, List
import streamlit as st


# -----------------------------
# UI language
# -----------------------------
LANGS = ["fr", "en"]
if "lang" not in st.session_state:
    st.session_state.lang = "fr"

col_lang_1, col_lang_2 = st.columns([1, 3])
with col_lang_1:
    st.session_state.lang = st.selectbox("Langue • Language", LANGS, index=0, format_func=lambda x: "Français" if x=="fr" else "English")

L = st.session_state.lang

# -----------------------------
# Labels and category options
# -----------------------------
labels = {
    "fr": {
        "app_title": "Finanthrope — Calculateur d'Épargne",
        "app_sub": "Calculez votre capacité d'épargne mensuelle",
        "revenus": "Revenus mensuels",
        "revenus_desc": "Ajoutez vos différentes sources de revenus",
        "dep_q": "Dépenses quotidiennes",
        "dep_q_desc": "Abonnements, nourriture, téléphone, loisirs, voyages",
        "dep_a": "Dépenses administratives",
        "dep_a_desc": "Assurances habitation, auto, décès, mutuelle, frais bancaires",
        "dep_f": "Dépenses familiales",
        "dep_f_desc": "Frais scolaires, cantine, sport, loisirs enfants",
        "credits": "Crédits et prêts",
        "credits_desc": "Crédit auto, immobilier, travaux, consommation, prêt étudiant",
        "impots": "Impôts",
        "impots_desc": "Sur le salaire, fonciers, PFU",
        "type": "Type",
        "amount": "Montant",
        "add": "Ajouter une ligne",
        "remove": "Supprimer",
        "no_rows": "Aucune entrée. Ajoutez une ligne pour commencer.",
        "totals": "Résumé",
        "total_rev": "Total revenus",
        "total_dep": "Total dépenses",
        "capacity": "Capacité d'épargne",
        "breakdown": "Répartition des dépenses",
        "download": "Télécharger les données",
        "file_saved": "Fichier prêt",
        "euros": "€",
        "positive": "Capacité positive",
        "negative": "Capacité négative",
    },
    "en": {
        "app_title": "Finanthrope — Savings Capacity Calculator",
        "app_sub": "Estimate your monthly savings capacity",
        "revenus": "Monthly income",
        "revenus_desc": "Add your different income sources",
        "dep_q": "Everyday expenses",
        "dep_q_desc": "Subscriptions, food, phone, leisure, travel",
        "dep_a": "Administrative expenses",
        "dep_a_desc": "Home, car, life insurance, health cover, bank fees",
        "dep_f": "Family expenses",
        "dep_f_desc": "School, canteen, sports, kids leisure",
        "credits": "Loans and credit",
        "credits_desc": "Car, mortgage, renovation, consumer, student",
        "impots": "Taxes",
        "impots_desc": "On salary, property, flat tax",
        "type": "Type",
        "amount": "Amount",
        "add": "Add a row",
        "remove": "Remove",
        "no_rows": "No entries yet. Add a row to get started.",
        "totals": "Summary",
        "total_rev": "Total income",
        "total_dep": "Total expenses",
        "capacity": "Savings capacity",
        "breakdown": "Expense breakdown",
        "download": "Download data",
        "file_saved": "File ready",
        "euros": "€",
        "positive": "Positive capacity",
        "negative": "Negative capacity",
    },
}

budgetLabels = {
  "fr": {
    "revenus": {
      "salaire": "Salaire",
      "prime_salaire": "Prime du salaire",
      "prime_activite": "Prime d'activité",
      "allocation_logement": "Allocation logement",
      "revenu_immobilier": "Revenu immobilier",
      "activite_secondaire": "Activité secondaire net",
    },
    "depensesQuotidiennes": {
      "abonnement": "Abonnements",
      "nourriture": "Nourriture",
      "telephone": "Téléphone",
      "loisirs": "Loisirs",
      "voyage": "Voyages",
    },
    "depensesAdministratives": {
      "assurance_habitation": "Assurance habitation",
      "assurance_auto": "Assurance auto",
      "assurance_deces": "Assurance décès",
      "mutuelle": "Mutuelle",
      "frais_bancaires": "Frais bancaires",
    },
    "depensesFamiliales": {
      "scolaire": "Frais scolaires",
      "cantine": "Cantine",
      "sport": "Sport",
      "loisirs_enfants": "Loisirs enfants",
    },
    "credits": {
      "credit_auto": "Crédit auto",
      "credit_immobilier": "Crédit immobilier",
      "credit_travaux": "Crédit travaux",
      "credit_consommation": "Crédit consommation",
      "pret_etudiant": "Prêt étudiant",
    },
    "impots": {
      "impot_salaire": "Impôts sur le salaire",
      "impot_foncier": "Impôts fonciers",
      "impot_pfu": "Impôts PFU",
    },
  },
  "en": {
    "revenus": {
      "salaire": "Salary",
      "prime_salaire": "Salary bonus",
      "prime_activite": "Activity bonus",
      "allocation_logement": "Housing allowance",
      "revenu_immobilier": "Property income",
      "activite_secondaire": "Side activity net",
    },
    "depensesQuotidiennes": {
      "abonnement": "Subscriptions",
      "nourriture": "Food",
      "telephone": "Phone",
      "loisirs": "Leisure",
      "voyage": "Travel",
    },
    "depensesAdministratives": {
      "assurance_habitation": "Home insurance",
      "assurance_auto": "Car insurance",
      "assurance_deces": "Life insurance",
      "mutuelle": "Health cover",
      "frais_bancaires": "Bank fees",
    },
    "depensesFamiliales": {
      "scolaire": "School fees",
      "cantine": "Canteen",
      "sport": "Sports",
      "loisirs_enfants": "Kids leisure",
    },
    "credits": {
      "credit_auto": "Car loan",
      "credit_immobilier": "Mortgage",
      "credit_travaux": "Renovation loan",
      "credit_consommation": "Consumer loan",
      "pret_etudiant": "Student loan",
    },
    "impots": {
      "impot_salaire": "Salary tax",
      "impot_foncier": "Property tax",
      "impot_pfu": "Flat tax",
    },
  },
}

# Helper to build select options for a section
def options_for(section_key: str) -> List[str]:
    mapping = budgetLabels[L][section_key]
    return [mapping[k] for k in mapping.keys()]

# Reverse lookup to keep stable keys even when the language changes
def key_from_label(section_key: str, human_label: str) -> str:
    mapping = budgetLabels[L][section_key]
    for k, v in mapping.items():
        if v == human_label:
            return k
    # fallback to first
    return list(mapping.keys())[0]

def label_from_key(section_key: str, k: str) -> str:
    return budgetLabels[L][section_key].get(k, k)

# -----------------------------
# App header
# -----------------------------
st.title(labels[L]["app_title"])
st.caption(labels[L]["app_sub"])

# -----------------------------
# State model
# -----------------------------
SECTION_KEYS = {
    "revenus": "revenus",
    "depensesQuotidiennes": "dep_q",
    "depensesAdministratives": "dep_a",
    "depensesFamiliales": "dep_f",
    "credits": "credits",
    "impots": "impots",
}

default_state = {
    "revenus": [],
    "dep_q": [],
    "dep_a": [],
    "dep_f": [],
    "credits": [],
    "impots": [],
}

for k, v in default_state.items():
    if k not in st.session_state:
        st.session_state[k] = []

# -----------------------------
# Section renderer
# -----------------------------
def render_section(title: str, desc: str, state_key: str, section_key_for_labels: str):
    st.subheader(title)
    if desc:
        st.caption(desc)

    rows: List[Dict] = st.session_state[state_key]

    if len(rows) == 0:
        st.info(labels[L]["no_rows"])

    # Build grid of rows
    to_delete = None
    for i, row in enumerate(rows):
        c1, c2, c3 = st.columns([3, 3, 1])
        # Current label for select respecting language
        current_label = label_from_key(section_key_for_labels, row.get("type", ""))
        with c1:
            sel = st.selectbox(
                f'{labels[L]["type"]} {state_key}-{i}',
                options_for(section_key_for_labels),
                index=options_for(section_key_for_labels).index(current_label) if current_label in options_for(section_key_for_labels) else 0,
                key=f"sel-{state_key}-{i}",
            )
            # Store underlying key
            row["type"] = key_from_label(section_key_for_labels, sel)
        with c2:
            amt = st.number_input(
                f'{labels[L]["amount"]} {state_key}-{i}',
                min_value=0.0, step=0.01, format="%.2f",
                value=float(row.get("montant", 0.0)),
                key=f"amt-{state_key}-{i}",
            )
            row["montant"] = amt
        with c3:
            if st.button(labels[L]["remove"], key=f"rm-{state_key}-{i}"):
                to_delete = i

    if to_delete is not None:
        del rows[to_delete]
        st.session_state[state_key] = rows
        st.rerun()

    if st.button(labels[L]["add"], key=f"add-{state_key}"):
        rows.append({"type": list(budgetLabels[L][section_key_for_labels].keys())[0], "montant": 0.0})
        st.session_state[state_key] = rows
        st.rerun()

    # Section total
    section_total = sum(float(r.get("montant", 0.0)) for r in rows)
    st.markdown(f"**Total**: {section_total:,.2f} {labels[L]['euros']}")

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([2, 1])

with left:
    render_section(
        labels[L]["revenus"],
        labels[L]["revenus_desc"],
        SECTION_KEYS["revenus"],
        "revenus",
    )

    render_section(
        labels[L]["dep_q"],
        labels[L]["dep_q_desc"],
        SECTION_KEYS["depensesQuotidiennes"],
        "depensesQuotidiennes",
    )

    render_section(
        labels[L]["dep_a"],
        labels[L]["dep_a_desc"],
        SECTION_KEYS["depensesAdministratives"],
        "depensesAdministratives",
    )

    render_section(
        labels[L]["dep_f"],
        labels[L]["dep_f_desc"],
        SECTION_KEYS["depensesFamiliales"],
        "depensesFamiliales",
    )

    render_section(
        labels[L]["credits"],
        labels[L]["credits_desc"],
        SECTION_KEYS["credits"],
        "credits",
    )

    render_section(
        labels[L]["impots"],
        labels[L]["impots_desc"],
        SECTION_KEYS["impots"],
        "impots",
    )

# -----------------------------
# Summary card
# -----------------------------
def total_for(state_key: str) -> float:
    return sum(float(r.get("montant", 0.0)) for r in st.session_state[state_key])

total_revenus = total_for("revenus")
total_quotidiennes = total_for("dep_q")
total_admin = total_for("dep_a")
total_familiales = total_for("dep_f")
total_credits = total_for("credits")
total_impots = total_for("impots")
total_depenses = total_quotidiennes + total_admin + total_familiales + total_credits + total_impots
capacite_epargne = total_revenus - total_depenses

with right:
    st.subheader(labels[L]["totals"])
    c1, c2 = st.columns(2)
    with c1:
        st.metric(labels[L]["total_rev"], f"{total_revenus:,.2f} {labels[L]['euros']}")
    with c2:
        st.metric(labels[L]["total_dep"], f"{total_depenses:,.2f} {labels[L]['euros']}")

    # Capacity indicator
    color = "✅" if capacite_epargne >= 0 else "⚠️"
    tag = labels[L]["positive"] if capacite_epargne >= 0 else labels[L]["negative"]
    st.markdown(f"### {labels[L]['capacity']}: {capacite_epargne:,.2f} {labels[L]['euros']} {color}")
    st.caption(tag)

    # Breakdown with progress bars
    st.markdown(f"#### {labels[L]['breakdown']}")
    dep_map = [
        (labels[L]["dep_q"], total_quotidiennes),
        (labels[L]["dep_a"], total_admin),
        (labels[L]["dep_f"], total_familiales),
        (labels[L]["credits"], total_credits),
        (labels[L]["impots"], total_impots),
    ]
    denom = total_depenses if total_depenses > 0 else 1.0
    for name, val in dep_map:
        pct = min(1.0, float(val) / denom)
        st.write(f"{name} — {val:,.2f} {labels[L]['euros']} ({int(round(pct*100))}%)")
        st.progress(pct)

    # Download JSON snapshot
    payload = {
        "lang": L,
        "sections": {
            "revenus": st.session_state["revenus"],
            "depensesQuotidiennes": st.session_state["dep_q"],
            "depensesAdministratives": st.session_state["dep_a"],
            "depensesFamiliales": st.session_state["dep_f"],
            "credits": st.session_state["credits"],
            "impots": st.session_state["impots"],
        },
        "totals": {
            "revenus": total_revenus,
            "depenses": total_depenses,
            "capacite_epargne": capacite_epargne,
            "quotidiennes": total_quotidiennes,
            "administratives": total_admin,
            "familiales": total_familiales,
            "credits": total_credits,
            "impots": total_impots,
        },
    }
    st.download_button(
        labels[L]["download"],
        data=json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="finanthrope_budget.json",
        mime="application/json",
    )

# Footer
st.markdown(
    "<br><small>© Finanthrope · Streamlit</small>",
    unsafe_allow_html=True
)
