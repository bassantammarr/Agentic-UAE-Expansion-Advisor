import uuid
from pathlib import Path
from datetime import datetime

import streamlit as st
from agno.run.agent import RunEvent

from agent import agent
from rag import knowledge_base
from rag.knowledge_base import KNOWLEDGE_DIR, SUPPORTED


st.set_page_config(
    page_title="UAE Expansion Advisor",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


TOOL_LABELS = {
    "search_knowledge_base": "Searching your documents",
    "find_competitors": "Researching competitors",
    "analyze_competitor_menu": "Reading a competitor menu",
    "search_exa": "Searching the web",
    "get_contents": "Reading sources",
    "exa_answer": "Looking up market data",
    "find_similar": "Finding similar businesses",
}

DISTRICTS = [
    ("Dubai Marina", "Dubai", (226, 88), (218, 100, "end")),
    ("Downtown", "Dubai", (272, 76), (280, 74, "start")),
    ("Business Bay", "Dubai", (284, 92), (284, 108, "middle")),
    ("Yas Island", "Abu Dhabi", (140, 126), (148, 123, "start")),
    ("Al Reem", "Abu Dhabi", (112, 150), (112, 166, "middle")),
    ("Saadiyat", "Abu Dhabi", (92, 136), (84, 133, "end")),
]

ICONS = {
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "store": '<path d="M4 10v10h16V10"/><path d="M3 4h18l-1.5 6h-15z"/><path d="M9 20v-5h6v5"/>',
    "slice": '<path d="M12 21 3 5c5.5-3 12.5-3 18 0z"/><circle cx="10" cy="9" r="1"/><circle cx="14" cy="13" r="1"/>',
    "tag": '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "megaphone": '<path d="M3 10v4h4l8 5V5L7 10z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
    "alert": '<path d="M12 3 2 20h20z"/><path d="M12 10v4"/><path d="M12 17h.01"/>',
}

TOPICS = [
    ("pin", "Locations", "Which of the six districts should we open in first, and why?"),
    ("store", "Competitors", "Who already sells pizza or kebab on Talabat around Dubai Marina, and at what prices?"),
    ("slice", "Menu", "Which dishes should change for UAE tastes, and which should stay exactly as they are in Jordan?"),
    ("tag", "Pricing", "How should we price a mixed-grill pizza against Downtown competitors?"),
    ("megaphone", "Marketing", "What should the launch plan look like around Ramadan, Eid and UAE National Day?"),
    ("alert", "Risks and operations", "Which licences, rents and delivery fees could hurt the first branch?"),
]

DEFAULT_BRIEF = {"origin": "Jordan", "concept": "Meaty pizza and kebab sandwiches", "delivery": "Talabat"}
NUMBER_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;500;600&display=swap');

:root {
    --plum: #2a1d2e;
    --plum-card: #36273b;
    --plum-field: #3d2d42;
    --plum-line: rgba(255,255,255,0.13);
    --on-plum: #f6f1f7;
    --on-plum-muted: #c9bccc;
    --amber: #f2b33d;
    --gold: #8c6a3c;
    --ink: #1f1823;
    --muted: #6d6572;
    --paper: #ffffff;
    --tile: #f5f3f6;
    --tile-line: #e7e3e9;
}

html, body, [class*="css"], .stMarkdown, .stChatMessage, button, input, textarea { font-family: 'Inter', sans-serif; }
.stApp { background: var(--paper); }
header[data-testid="stHeader"], #MainMenu, footer,
[data-testid="stSidebar"], [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }
.block-container { padding-top: 0 !important; padding-bottom: 6rem; max-width: 1100px; }

/* ---------- Dark hero band (full-bleed background) ---------- */
.st-key-hero {
    background: var(--plum);
    box-shadow: 0 0 0 100vmax var(--plum);
    clip-path: inset(0 -100vmax);
    padding: 0.9rem 0 3.2rem;
    margin-bottom: 2.2rem;
    color: var(--on-plum);
}
.st-key-hero p, .st-key-hero span, .st-key-hero label { color: var(--on-plum); }

/* Top bar */
.st-key-topbar { border-bottom: 1px solid var(--plum-line); padding-bottom: 0.9rem; margin-bottom: 2.6rem; }
.brand { display: flex; align-items: center; gap: 0.6rem; font-weight: 600; font-size: 0.95rem; color: var(--on-plum); }
.brand svg { flex: none; }
.brief { font-size: 0.8rem; color: var(--on-plum-muted) !important; text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.st-key-topbar [data-testid="stPopover"] button,
.st-key-topbar .stButton > button {
    background: transparent; border: none; color: var(--on-plum); font-size: 0.8rem; font-weight: 500;
    padding: 0.35rem 0.6rem; min-height: 0; white-space: nowrap;
}
.st-key-topbar [data-testid="stPopover"] button:hover { color: var(--amber); }
.st-key-topbar [data-testid="stPopover"] button svg,
.st-key-topbar [data-testid="stPopover"] button [data-testid="stIconMaterial"] { display: none; }
.st-key-topbar button p { font-size: 0.8rem; white-space: nowrap; }
.st-key-newconv button {
    border: 1px solid var(--plum-line) !important; border-radius: 999px !important; padding: 0.45rem 0.9rem !important;
}
.st-key-newconv button:hover { border-color: var(--amber) !important; color: var(--amber) !important; }

@media (max-width: 640px) {
    .st-key-topbar { margin-bottom: 1.6rem; }
    .st-key-topbar [data-testid="stHorizontalBlock"] { flex-direction: row; flex-wrap: wrap; gap: 0.3rem; }
    .st-key-topbar [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; flex: 0 0 auto !important; }
    .st-key-topbar [data-testid="stColumn"]:first-child { flex: 1 0 100% !important; margin-bottom: 0.3rem; }
    .st-key-topbar [data-testid="stColumn"]:nth-child(2) { display: none; }
}

/* Headline */
.hero-title {
    font-family: 'Bricolage Grotesque', 'Inter', sans-serif; font-weight: 800; letter-spacing: -0.03em;
    font-size: clamp(2.4rem, 4.6vw, 3.4rem); line-height: 1.02; color: var(--on-plum); margin: 0 0 1.1rem; max-width: 10.5ch;
}
.hero-title.compact { font-size: 1.9rem; max-width: none; margin-bottom: 0.8rem; }
.hero-copy { font-size: 0.95rem; line-height: 1.6; color: var(--on-plum) !important; max-width: 31rem; margin: 0 0 1.6rem; }

/* Question box */
.st-key-hero [data-testid="stForm"] {
    background: var(--plum-card); border: 1px solid var(--plum-line); border-radius: 14px; padding: 0.45rem 0.45rem 0.45rem 0.4rem;
}
.st-key-hero [data-testid="stForm"] [data-baseweb="input"] { background: transparent; border: none; }
.st-key-hero [data-testid="stForm"] [data-baseweb="base-input"] { background: transparent; }
.st-key-hero [data-testid="stForm"] input { color: var(--on-plum); font-size: 0.9rem; text-overflow: ellipsis; caret-color: var(--amber); }
.st-key-hero [data-testid="stForm"] input::placeholder { color: var(--on-plum-muted); opacity: 1; }
.scope { font-size: 0.75rem; color: var(--on-plum-muted) !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: right; }
.st-key-hero [data-testid="stFormSubmitButton"] button {
    background: var(--gold); color: var(--on-plum); border: none; border-radius: 10px; font-weight: 600; padding: 0.55rem 0.8rem; width: 100%;
    white-space: nowrap;
}
.st-key-hero [data-testid="stFormSubmitButton"] button p { white-space: nowrap; }
.st-key-hero [data-testid="stFormSubmitButton"] button:hover { background: var(--amber); color: var(--plum); }

/* District card */
.st-key-mapcard { background: var(--plum-card); border: 1px solid var(--plum-line); border-radius: 16px; padding: 1rem 1rem 0.6rem; }
.map-head { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; margin-bottom: 0.7rem; }
.map-head b { font-size: 0.85rem; font-weight: 600; }
.map-head span { font-size: 0.7rem; color: var(--on-plum-muted) !important; }
.map { width: 100%; height: auto; display: block; border-radius: 12px; }
.city-label { font-size: 0.75rem; color: var(--on-plum-muted) !important; }
.st-key-mapcard [data-testid="stBaseButton-pills"],
.st-key-mapcard [data-testid="stBaseButton-pillsActive"] {
    border-radius: 999px; font-size: 0.78rem; padding: 0.3rem 0.8rem; min-height: 0;
}
.st-key-mapcard [data-testid="stBaseButton-pills"] { background: transparent !important; border: 1px solid rgba(255,255,255,0.28) !important; color: var(--on-plum) !important; }
.st-key-mapcard [data-testid="stBaseButton-pills"] p, .st-key-mapcard [data-testid="stBaseButton-pills"] span { color: var(--on-plum) !important; }
.st-key-mapcard [data-testid="stBaseButton-pills"]:hover { border-color: var(--amber) !important; }
.st-key-mapcard [data-testid="stBaseButton-pills"]:hover p, .st-key-mapcard [data-testid="stBaseButton-pills"]:hover span { color: var(--amber) !important; }
.st-key-mapcard [data-testid="stBaseButton-pillsActive"] { background: var(--amber) !important; border: 1px solid var(--amber) !important; color: var(--plum) !important; }
.st-key-mapcard [data-testid="stBaseButton-pillsActive"] p, .st-key-mapcard [data-testid="stBaseButton-pillsActive"] span { color: var(--plum) !important; }

/* ---------- Topic cards ---------- */
.section-row { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; margin-bottom: 1rem; }
.section-row h2 { font-family: 'Bricolage Grotesque', 'Inter', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--ink); margin: 0; padding: 0; }
.section-row span { font-size: 0.75rem; color: var(--muted); }
[class*="st-key-topiccard"] { position: relative; }
[class*="st-key-topicpick"] { position: absolute !important; inset: 0; width: 100% !important; height: 100%; z-index: 2; }
[class*="st-key-topicpick"] .stButton, [class*="st-key-topicpick"] button {
    width: 100% !important; height: 100%; max-width: none; opacity: 0; cursor: pointer;
}
.topic {
    background: var(--tile); border: 1px solid var(--tile-line); border-radius: 14px; padding: 1rem 1.1rem 1.2rem;
    min-height: 9.6rem; margin-bottom: 0.4rem; transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}
[class*="st-key-topiccard"]:hover .topic { border-color: var(--gold); box-shadow: 0 6px 18px rgba(42,29,46,0.08); transform: translateY(-1px); }
.topic-head { display: flex; align-items: center; gap: 0.6rem; font-size: 0.8rem; font-weight: 600; color: var(--ink); margin-bottom: 1.2rem; }
.topic-icon { width: 30px; height: 30px; border-radius: 50%; background: var(--amber); display: grid; place-items: center; flex: none; }
.topic p { font-size: 0.92rem; line-height: 1.45; color: var(--ink); margin: 0; }

/* ---------- Conversation ---------- */
.stChatMessage { background: var(--paper); border: 1px solid var(--tile-line); border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.75rem; }
.stChatMessage h1 { font-size: 1.3rem; color: var(--plum); }
.stChatMessage h2 { font-size: 1.1rem; color: var(--plum); margin-top: 1rem; }
.stChatMessage h3 { font-size: 1rem; }
.st-key-convhead .stDownloadButton button { border-radius: 999px; font-size: 0.8rem; border: 1px solid var(--tile-line); }
[data-testid="stChatInput"] { border-radius: 12px; }
[data-testid="stChatInput"] textarea { field-sizing: content; height: auto !important; min-height: 40px; max-height: 160px; }
</style>
"""


def init_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.started = datetime.now()
    for key, value in DEFAULT_BRIEF.items():
        st.session_state.setdefault(f"brief_{key}", value)


def reset_session():
    for key in ("session_id", "messages", "started", "pending_prompt", "question"):
        st.session_state.pop(key, None)


def selected_districts() -> list[str]:
    return list(st.session_state.get("pills_dubai") or []) + list(st.session_state.get("pills_abudhabi") or [])


def scope_label() -> str:
    chosen = selected_districts()
    if not chosen:
        return "All six districts"
    if len(chosen) <= 2:
        return " and ".join(chosen)
    return f"{len(chosen)} districts"


def build_agent_prompt(question: str) -> str:
    """Add the district scope and any edited brief to what the agent sees."""
    notes = []
    chosen = selected_districts()
    if chosen:
        notes.append(f"Focus only on these districts: {', '.join(chosen)}.")
    brief = {k: st.session_state[f"brief_{k}"] for k in DEFAULT_BRIEF}
    if brief != DEFAULT_BRIEF:
        notes.append(
            f"Business brief: a {brief['origin']} brand selling {brief['concept'].lower()}, "
            f"expanding to Dubai and Abu Dhabi with {brief['delivery']} as the main delivery platform."
        )
    return f"{question}\n\n({' '.join(notes)})" if notes else question


def build_report() -> str:
    lines = ["# UAE Market Expansion Report", f"_Generated {datetime.now():%d %B %Y, %H:%M}_", ""]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lines += ["---", f"## Question: {msg['content']}", ""]
        else:
            lines += [msg["content"], ""]
    return "\n".join(lines)


def pick_topic(question: str):
    st.session_state.question = question


def submit_question():
    question = (st.session_state.get("question") or "").strip()
    if question:
        st.session_state.pending_prompt = question
        st.session_state.question = ""


# ---------- Hero ----------

def map_svg() -> str:
    chosen = set(selected_districts())
    marks = []
    for name, _city, (x, y), (lx, ly, anchor) in DISTRICTS:
        active = name in chosen
        fill = "#f2b33d" if active else "none"
        halo = f'<circle cx="{x}" cy="{y}" r="9" fill="#f2b33d" opacity="0.22"/>' if active else ""
        marks.append(
            f'{halo}<circle cx="{x}" cy="{y}" r="4.2" fill="{fill}" stroke="#f2b33d" stroke-width="1.6"/>'
            f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="8.5" font-weight="600" fill="#f6f1f7">{name}</text>'
        )
    return f"""
<svg class="map" viewBox="0 0 340 210" role="img" aria-label="Map of the six districts in Dubai and Abu Dhabi">
  <rect width="340" height="210" fill="#2a1d2e"/>
  <path d="M0,180 C80,170 130,145 180,118 S285,58 340,30 L340,210 L0,210 Z" fill="#3d2d42"/>
  <path d="M0,180 C80,170 130,145 180,118 S285,58 340,30" fill="none" stroke="#7d6a82" stroke-width="1"/>
  <ellipse cx="92" cy="134" rx="11" ry="5" fill="#3d2d42" transform="rotate(-20 92 134)"/>
  <ellipse cx="140" cy="125" rx="9" ry="5" fill="#3d2d42" transform="rotate(-25 140 125)"/>
  <ellipse cx="228" cy="80" rx="6" ry="3" fill="#3d2d42" transform="rotate(-30 228 80)"/>
  <text x="44" y="42" font-size="8" font-style="italic" fill="#8f7f94">Arabian Gulf</text>
  <text x="300" y="138" text-anchor="middle" font-size="9" fill="#a898ad">Dubai</text>
  <text x="96" y="196" text-anchor="middle" font-size="9" fill="#a898ad">Abu Dhabi</text>
  {''.join(marks)}
</svg>"""


def render_sources_popover(n_docs: int):
    with st.popover(f"{n_docs} sources"):
        st.caption("Documents the advisor searches before going to the web.")
        for name in knowledge_base.sources:
            st.markdown(f"📄 {name}")
        uploads = st.file_uploader(
            "Add notes (.md / .txt)",
            type=[ext.lstrip(".") for ext in SUPPORTED],
            accept_multiple_files=True,
            key=f"kb_upload_{st.session_state.get('kb_uploads', 0)}",
        )
        if uploads:
            for f in uploads:
                (KNOWLEDGE_DIR / Path(f.name).name).write_bytes(f.getvalue())
            knowledge_base.reload()
            st.session_state.kb_uploads = st.session_state.get("kb_uploads", 0) + 1
            st.toast(f"Indexed {len(uploads)} document(s)")
            st.rerun()


def render_brief_popover():
    with st.popover("Edit brief"):
        st.text_input("Home country", key="brief_origin")
        st.text_input("Concept", key="brief_concept")
        st.selectbox("Main delivery platform", ["Talabat", "Deliveroo", "Careem"], key="brief_delivery")
        st.caption("Changes apply to your next question.")


def render_topbar(n_docs: int):
    with st.container(key="topbar"):
        left, brief, sources, edit, new = st.columns([3, 4.2, 1, 1, 1.7], vertical_alignment="center", gap="small")
        left.markdown(
            '<div class="brand"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f2b33d" stroke-width="1.6">'
            '<circle cx="12" cy="12" r="10"/><path d="m15.5 8.5-2 5-5 2 2-5z" fill="#f2b33d"/></svg>Expansion Advisor</div>',
            unsafe_allow_html=True,
        )
        brief.markdown(
            f'<div class="brief">{st.session_state.brief_origin} to Dubai and Abu Dhabi, '
            f'{st.session_state.brief_delivery} first</div>',
            unsafe_allow_html=True,
        )
        with sources:
            render_sources_popover(n_docs)
        with edit:
            render_brief_popover()
        with new:
            with st.container(key="newconv"):
                if st.button("New conversation", width="stretch"):
                    reset_session()
                    st.rerun()


def render_hero(compact: bool):
    n_docs = len(knowledge_base.sources)
    docs_word = NUMBER_WORDS[n_docs] if n_docs < len(NUMBER_WORDS) else str(n_docs)

    with st.container(key="hero"):
        render_topbar(n_docs)
        left, right = st.columns([1.05, 1], gap="large", vertical_alignment="center")

        with left:
            title_cls = "hero-title compact" if compact else "hero-title"
            st.markdown(f'<div class="{title_cls}">Where should the first oven go?</div>', unsafe_allow_html=True)
            if not compact:
                st.markdown(
                    f'<p class="hero-copy">Plan the move of a {st.session_state.brief_origin}ian pizza and kebab brand '
                    f'into Dubai and Abu Dhabi. Answers draw on your {docs_word} documents and on competitors’ '
                    f'current {st.session_state.brief_delivery} menus.</p>'
                    if st.session_state.brief_origin == "Jordan"
                    else f'<p class="hero-copy">Plan the move of a {st.session_state.brief_origin} brand into Dubai '
                    f'and Abu Dhabi. Answers draw on your {docs_word} documents and on competitors’ current '
                    f'{st.session_state.brief_delivery} menus.</p>',
                    unsafe_allow_html=True,
                )
            with st.form("ask", border=False):
                q, scope, ask = st.columns([6, 1.7, 1.3], vertical_alignment="center", gap="small")
                q.text_input(
                    "Your question",
                    key="question",
                    placeholder="Ask anything about opening in the UAE",
                    label_visibility="collapsed",
                )
                scope.markdown(f'<div class="scope">{scope_label()}</div>', unsafe_allow_html=True)
                ask.form_submit_button("Ask", on_click=submit_question, width="stretch")

        with right:
            with st.container(key="mapcard"):
                st.markdown(
                    '<div class="map-head"><b>Districts in scope</b><span>Abu Dhabi to Dubai is about 140 km</span></div>'
                    + map_svg(),
                    unsafe_allow_html=True,
                )
                for city, key in (("Dubai", "pills_dubai"), ("Abu Dhabi", "pills_abudhabi")):
                    label, pills = st.columns([1, 4.2], vertical_alignment="center", gap="small")
                    label.markdown(f'<div class="city-label">{city}</div>', unsafe_allow_html=True)
                    pills.pills(
                        city,
                        [d[0] for d in DISTRICTS if d[1] == city],
                        selection_mode="multi",
                        key=key,
                        label_visibility="collapsed",
                    )


# ---------- Topics ----------

def render_topics():
    st.markdown(
        '<div class="section-row"><h2>Or start from a topic</h2><span>Pick one to put its question in the box above</span></div>',
        unsafe_allow_html=True,
    )
    for i, (icon, title, question) in enumerate(TOPICS):
        if i % 3 == 0:
            cols = st.columns(3, gap="medium")
        with cols[i % 3]:
            with st.container(key=f"topiccard{i}"):
                st.markdown(
                    f'<div class="topic"><div class="topic-head"><span class="topic-icon">'
                    f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2a1d2e" stroke-width="1.8" '
                    f'stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg></span>{title}</div>'
                    f'<p>{question}</p></div>',
                    unsafe_allow_html=True,
                )
                st.button(title, key=f"topicpick{i}", on_click=pick_topic, args=(question,))


# ---------- Conversation ----------

def stream_answer(agent_prompt: str) -> str:
    status = st.status("Analyzing your question…", expanded=False)
    placeholder = st.empty()
    content = ""
    tools_used = []

    try:
        for event in agent.run(
            agent_prompt,
            stream=True,
            stream_events=True,
            session_id=st.session_state.session_id,
        ):
            if event.event == RunEvent.tool_call_started.value:
                name = getattr(event.tool, "tool_name", "tool")
                label = TOOL_LABELS.get(name, f"Running {name}")
                tools_used.append(label)
                status.update(label=f"{label}…", state="running")
                status.write(f"🔎 {label}")
            elif event.event == RunEvent.tool_call_completed.value:
                status.update(label="Reviewing findings and drafting answer…", state="running")
            elif event.event == RunEvent.run_content.value and event.content:
                content += event.content
                placeholder.markdown(content + " ▌")
            elif event.event == RunEvent.run_error.value:
                raise RuntimeError(getattr(event, "content", "Agent run failed"))
    except Exception as exc:
        status.update(label="Something went wrong", state="error", expanded=True)
        status.write(str(exc))
        return ""

    placeholder.markdown(content)
    summary = f"Done · used {len(tools_used)} research step(s)" if tools_used else "Done"
    status.update(label=summary, state="complete", expanded=False)
    return content


def render_conversation(prompt: str | None):
    with st.container(key="convhead"):
        head, export = st.columns([4, 1.3], vertical_alignment="center")
        head.markdown('<div class="section-row"><h2>Conversation</h2></div>', unsafe_allow_html=True)
        if st.session_state.messages:
            export.download_button(
                "Export report (.md)",
                data=build_report(),
                file_name=f"uae_expansion_report_{datetime.now():%Y%m%d_%H%M}.md",
                mime="text/markdown",
                width="stretch",
            )

    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🧭"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🧭"):
        answer = stream_answer(build_agent_prompt(prompt))
    if answer:
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


def main():
    st.markdown(CSS, unsafe_allow_html=True)
    init_state()

    prompt = st.session_state.pop("pending_prompt", None)
    in_conversation = bool(st.session_state.messages) or bool(prompt)

    render_hero(compact=in_conversation)

    follow_up = st.chat_input("Ask a follow-up…") if in_conversation else None
    prompt = prompt or follow_up

    if in_conversation or prompt:
        render_conversation(prompt)
    else:
        render_topics()


if __name__ == "__main__":
    main()
