# streamlit_app.py
from __future__ import annotations
import io
import json
from typing import Dict, List
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Finanthrope — Budget",
    page_icon="💶",
    layout="wide"
)

# ---------- Desktop styling ----------
st.markdown(
    """
    <style>
      .summary-card { position: sticky; top: 1rem; }
      .block-container { padding-top: 1rem; padding-bottom: 2rem; }
      .stSelectbox, .stNumberInput { margin-bottom: 0.25rem; }

      /* Gold PDF button: wrap the button in <div class="gold-pdf"> ... </div> */
      .gold-pdf button {
        background: linear-gradient(135deg, #D4AF37, #B8860B);
        color: #ffffff !important;
        border: 0;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.45);
      }
      .gold-pdf button:hover { filter: brightness(1.06); }
      .gold-pdf button:focus {
        outline: 2px solid rgba(212, 175, 55, 0.55);
        outline-offset: 2px;
      }

      /* Calmer JSON button so the gold option stands out */
      .calm-json button {
        background: #f4f5f7;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb;
      }
      .calm-json button:hover { background: #eef0f3; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# UI language
# -----------------------------
LANGS = ["fr", "en"]
if "lang" not in st.session_state:
    st.session_state.lang = "fr"

with st.container():
    col_lang_1, col_lang_2 = st.columns([1, 6], gap="small")
    with col_lang_1:
        st.session_state.lang = st.selectbox(
            "Langue • Language",
            LANGS,
            index=0,
            format_func=lambda x: "Français" if x == "fr" else "English"
        )

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
        "download_pdf": "Télécharger le PDF",
        "file_saved": "Fichier prêt",
        "euros": "€",
        "positive": "Capacité positive",
        "negative": "Capacité négative",
        "per_month": "par mois",
        "section_total": "Total",
        "reset": "Tout réinitialiser",
        "pdf_title": "Résumé budgétaire",
        "pdf_rev": "Revenus",
        "pdf_dep": "Dépenses",
        "pdf_chart": "Répartition des dépenses",
        "pdf_capacity": "Capacité d’épargne",
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
        "download_pdf": "Download PDF",
        "file_saved": "File ready",
        "euros": "€",
        "positive": "Positive capacity",
        "negative": "Negative capacity",
        "per_month": "per month",
        "section_total": "Total",
        "reset": "Reset all",
        "pdf_title": "Budget summary",
        "pdf_rev": "Income",
        "pdf_dep": "Expenses",
        "pdf_chart": "Expense breakdown",
        "pdf_capacity": "Savings capacity",
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

# -----------------------------
# Helpers
# -----------------------------
def options_for(section_key: str) -> List[str]:
    mapping = budgetLabels[L][section_key]
    return [mapping[k] for k in mapping.keys()]

def key_from_label(section_key: str, human_label: str) -> str:
    mapping = budgetLabels[L][section_key]
    for k, v in mapping.items():
        if v == human_label:
            return k
    return list(mapping.keys())[0]

def label_from_key(section_key: str, k: str) -> str:
    return budgetLabels[L][section_key].get(k, k)

# -----------------------------
# PDF generator (Coolors palette + donut)
# -----------------------------
def create_pdf(payload: Dict, labels: Dict, lang: str) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    import matplotlib.pyplot as plt
    import io as _io

    # Coolors palette https://coolors.co/palette/eae4e9-fff1e6-fde2e4-fad2e1-e2ece9-bee1e6-f0efeb-dfe7fd-cddafd
    COL_EAE4E9 = colors.HexColor("#EAE4E9")
    COL_FFF1E6 = colors.HexColor("#FFF1E6")
    COL_FDE2E4 = colors.HexColor("#FDE2E4")
    COL_FAD2E1 = colors.HexColor("#FAD2E1")
    COL_E2ECE9 = colors.HexColor("#E2ECE9")
    COL_BEE1E6 = colors.HexColor("#BEE1E6")
    COL_F0EFEB = colors.HexColor("#F0EFEB")
    COL_DFE7FD = colors.HexColor("#DFE7FD")
    COL_CDDAFD = colors.HexColor("#CDDAFD")

    # Text and lines
    COL_TEXT = colors.HexColor("#1F2937")
    COL_BORDER = COL_CDDAFD
    COL_HEADER_BG = COL_DFE7FD
    COL_HEADER_TEXT = COL_TEXT
    COL_SECTION_SPACER = 8

    # Donut palette (slices)
    CHART_PALETTE = ["#FDE2E4", "#FAD2E1", "#E2ECE9", "#BEE1E6", "#CDDAFD"]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    h_style = styles["Heading2"]
    p_style = styles["BodyText"]

    title_style.textColor = COL_TEXT
    h_style.textColor = COL_TEXT
    p_style.textColor = COL_TEXT

    story = []

    # Title
    story.append(Paragraph(f"Finanthrope — {labels[lang]['pdf_title']}", title_style))
    story.append(Spacer(1, COL_SECTION_SPACER))

    # Top metrics
    totals = payload["totals"]
    cap = totals["capacite_epargne"]
    badge = "✅" if cap >= 0 else "⚠️"
    for line in [
        f"{labels[lang]['total_rev']}: {totals['revenus']:,.2f} {labels[lang]['euros']}",
        f"{labels[lang]['total_dep']}: {totals['depenses']:,.2f} {labels[lang]['euros']}",
        f"{labels[lang]['pdf_capacity']}: {cap:,.2f} {labels[lang]['euros']} {badge}",
    ]:
        story.append(Paragraph(line, p_style))
    story.append(Spacer(1, COL_SECTION_SPACER))

    # Section table helper
    def add_section(title: str, section_key: str, dict_key: str):
        rows = payload["sections"][section_key]
        data = [[labels[lang]["type"], labels[lang]["amount"] + f" ({labels[lang]['euros']})"]]
        for r in rows:
            human = budgetLabels[lang][dict_key].get(r.get("type", ""), r.get("type", ""))
            amt = float(r.get("montant", 0.0))
            data.append([human, f"{amt:,.2f}"])

        table = Table(data, hAlign="LEFT", colWidths=[None, 60*mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), COL_HEADER_BG),
            ("TEXTCOLOR", (0,0), (-1,0), COL_HEADER_TEXT),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("ALIGN", (1,1), (-1,-1), "RIGHT"),
            ("INNERGRID", (0,0), (-1,-1), 0.25, COL_BORDER),
            ("BOX", (0,0), (-1,-1), 0.5, COL_BORDER),
            ("BOTTOMPADDING", (0,0), (-1,0), 6),
            ("TOPPADDING", (0,0), (-1,0), 6),
        ]))

        story.append(Paragraph(title, h_style))
        story.append(table)
        story.append(Spacer(1, COL_SECTION_SPACER))

    # Income and expense sections
    add_section(labels[lang]["pdf_rev"], "revenus", "revenus")
    add_section(labels[lang]["pdf_dep"] + " — " + labels[lang]["dep_q"], "depensesQuotidiennes", "depensesQuotidiennes")
    add_section(labels[lang]["pdf_dep"] + " — " + labels[lang]["dep_a"], "depensesAdministratives", "depensesAdministratives")
    add_section(labels[lang]["pdf_dep"] + " — " + labels[lang]["dep_f"], "depensesFamiliales", "depensesFamiliales")
    add_section(labels[lang]["pdf_dep"] + " — " + labels[lang]["credits"], "credits", "credits")
    add_section(labels[lang]["pdf_dep"] + " — " + labels[lang]["impots"], "impots", "impots")

    # Donut chart with legend (no overlapping labels)
    dep_vals = [
        totals["quotidiennes"],
        totals["administratives"],
        totals["familiales"],
        totals["credits"],
        totals["impots"],
    ]
    dep_names = [
        labels[lang]["dep_q"],
        labels[lang]["dep_a"],
        labels[lang]["dep_f"],
        labels[lang]["credits"],
        labels[lang]["impots"],
    ]

    if sum(dep_vals) > 0:
        fig, ax = plt.subplots(figsize=(5.4, 4.2), dpi=220)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        wedges, _ = ax.pie(
            dep_vals,
            radius=1.0,
            startangle=90,
            labels=None,                # avoid label overlap
            autopct=None,
            colors=CHART_PALETTE,
            wedgeprops=dict(width=0.36, edgecolor="white")
        )

        # Inner hole
        centre_circle = plt.Circle((0, 0), 0.64, color="white")
        ax.add_artist(centre_circle)

        # Soft outer ring from the palette
        ring = plt.Circle((0, 0), 1.0, fill=False, linewidth=1.4, color="#CDDAFD")
        ax.add_artist(ring)

        ax.set_title(labels[lang]["pdf_chart"], color="#1F2937")

        total = float(sum(dep_vals))
        legend_labels = [f"{n} — {int(round(v/total*100))}%"
                         for n, v in zip(dep_names, dep_vals)]
        leg = ax.legend(
            wedges,
            legend_labels,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False
        )
        for text in leg.get_texts():
            text.set_color("#1F2937")

        plt.tight_layout()
        img_buf = _io.BytesIO()
        fig.savefig(img_buf, format="png", bbox_inches="tight")
        plt.close(fig)
        img_buf.seek(0)

        story.append(Image(img_buf, width=150*mm, height=110*mm))
        story.append(Spacer(1, COL_SECTION_SPACER))

    doc.build(story)
    buf.seek(0)
    return buf.read()

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

for k in default_state.keys():
    if k not in st.session_state:
        st.session_state[k] = []

# Reset
with st.expander("⚙️ " + (labels[L]["reset"]), expanded=False):
    if st.button(labels[L]["reset"]):
        for k in default_state.keys():
            st.session_state[k] = []
        st.rerun()

# -----------------------------
# Section renderer
# -----------------------------
def render_section(title: str, desc: str, state_key: str, section_key_for_labels: str):
    st.markdown(f"### {title}")
    if desc:
        st.caption(desc)

    rows: List[Dict] = st.session_state[state_key]

    if len(rows) == 0:
        st.info(labels[L]["no_rows"])

    to_delete = None
    for i, row in enumerate(rows):
        c1, c2, c3 = st.columns([4, 3, 1])
        current_label = label_from_key(section_key_for_labels, row.get("type", ""))
        with c1:
            sel = st.selectbox(
                f'{labels[L]["type"]} {state_key}-{i}',
                options_for(section_key_for_labels),
                index=options_for(section_key_for_labels).index(current_label)
                      if current_label in options_for(section_key_for_labels) else 0,
                key=f"sel-{state_key}-{i}",
            )
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

    cols = st.columns([1, 3])
    with cols[0]:
        if st.button(labels[L]["add"], key=f"add-{state_key}"):
            rows.append({"type": list(budgetLabels[L][section_key_for_labels].keys())[0], "montant": 0.0})
            st.session_state[state_key] = rows
            st.rerun()
    with cols[1]:
        section_total = sum(float(r.get("montant", 0.0)) for r in rows)
        st.markdown(f"**{labels[L]['section_total']}**: {section_total:,.2f} {labels[L]['euros']}")

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([7, 5], gap="large")

with left:
    with st.container():
        render_section(labels[L]["revenus"], labels[L]["revenus_desc"], SECTION_KEYS["revenus"], "revenus")
        st.divider()
        render_section(labels[L]["dep_q"], labels[L]["dep_q_desc"], SECTION_KEYS["depensesQuotidiennes"], "depensesQuotidiennes")
        st.divider()
        render_section(labels[L]["dep_a"], labels[L]["dep_a_desc"], SECTION_KEYS["depensesAdministratives"], "depensesAdministratives")
        st.divider()
        render_section(labels[L]["dep_f"], labels[L]["dep_f_desc"], SECTION_KEYS["depensesFamiliales"], "depensesFamiliales")
        st.divider()
        render_section(labels[L]["credits"], labels[L]["credits_desc"], SECTION_KEYS["credits"], "credits")
        st.divider()
        render_section(labels[L]["impots"], labels[L]["impots_desc"], SECTION_KEYS["impots"], "impots")

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
delta_pct = (capacite_epargne / total_revenus * 100) if total_revenus > 0 else 0.0

with right:
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.subheader(labels[L]["totals"])
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.metric(labels[L]["total_rev"], f"{total_revenus:,.2f} {labels[L]['euros']}")
    with c2:
        st.metric(labels[L]["total_dep"], f"{total_depenses:,.2f} {labels[L]['euros']}")
    with c3:
        st.metric(
            labels[L]["capacity"],
            f"{capacite_epargne:,.2f} {labels[L]['euros']}",
            delta=f"{delta_pct:.1f}%" if total_revenus > 0 else None
        )

    color = "✅" if capacite_epargne >= 0 else "⚠️"
    tag = labels[L]["positive"] if capacite_epargne >= 0 else labels[L]["negative"]
    st.caption(f"{tag} {color}")

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

    # ------- Downloads -------
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

    col_dl1, col_dl2 = st.columns([1, 1])
    with col_dl1:
        st.markdown('<div class="calm-json">', unsafe_allow_html=True)
        st.download_button(
            labels[L]["download"],
            data=json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="finanthrope_budget.json",
            mime="application/json",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_dl2:
        st.markdown('<div class="gold-pdf">', unsafe_allow_html=True)
        st.download_button(
            label=labels[L]["download_pdf"],
            data=create_pdf(payload, labels, L),
            file_name="finanthrope_resume.pdf" if L == "fr" else "finanthrope_summary.pdf",
            mime="application/pdf"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><small>© Finanthrope · Streamlit</small>", unsafe_allow_html=True)
