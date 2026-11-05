

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
    initial_sidebar_state="expanded",
)


TOOL_LABELS = {
    "search_knowledge_base": "Searching knowledge base",
    "find_competitors": "Researching competitors",
    "analyze_competitor_menu": "Analyzing competitor menu",
    "search_exa": "Searching the web",
    "get_contents": "Reading sources",
    "exa_answer": "Looking up market data",
    "find_similar": "Finding similar businesses",
}

QUICK_ACTIONS = [
    ("📍", "Best locations", "Which Dubai and Abu Dhabi areas should we open our first branches in, and what are the tradeoffs?"),
    ("🏆", "Competitor landscape", "Who are our main pizza and kebab competitors in Dubai and Abu Dhabi, and how do we differentiate?"),
    ("🍕", "Menu adaptation", "How should we adapt our meaty pizza and kebab sandwich menu for UAE customers?"),
    ("💰", "Pricing strategy", "What pricing strategy should we use for dine-in and delivery in the UAE?"),
    ("📣", "Marketing plan", "Build a launch marketing plan, including Ramadan, Eid and UAE National Day campaigns."),
    ("⚠️", "Risks & operations", "What are the key licensing, supply chain, staffing and operational risks of expanding?"),
]


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --brand: #0f3d3e;
    --brand-2: #14595b;
    --accent: #c8a24a;
    --ink: #1c2526;
    --muted: #64748b;
    --line: #e5e7eb;
    --surface: #ffffff;
    --canvas: #f6f7f5;
}

html, body, [class*="css"], .stMarkdown, .stChatMessage { font-family: 'Inter', sans-serif; }
.stApp { background: var(--canvas); }
#MainMenu, footer, header [data-testid="stToolbar"] { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1100px; }

/* Sidebar */
section[data-testid="stSidebar"] { background: var(--brand); }
section[data-testid="stSidebar"] * { color: #e8efef !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18);
    color: #fff !important; border-radius: 8px; width: 100%;
}
section[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.16); border-color: var(--accent); }
section[data-testid="stSidebar"] .stDownloadButton > button {
    background: var(--accent); border: none; color: var(--brand) !important; font-weight: 600; border-radius: 8px; width: 100%;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary,
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover { background: transparent; }
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.06); border: 1px dashed rgba(255,255,255,0.3);
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    background: var(--accent); color: var(--brand) !important; border: none;
}
.sb-brand { font-size: 1.15rem; font-weight: 700; letter-spacing: -0.01em; margin-bottom: 0.1rem; }
.sb-sub { font-size: 0.8rem; opacity: 0.7; margin-bottom: 1.2rem; }
.sb-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.6; margin: 1.2rem 0 0.4rem; }
.sb-row { display: flex; justify-content: space-between; font-size: 0.85rem; padding: 0.35rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); }
.sb-row span:last-child { font-weight: 600; text-align: right; }

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%);
    border-radius: 16px; padding: 2rem 2.2rem; color: #fff; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero::after {
    content: ""; position: absolute; right: -60px; top: -60px; width: 220px; height: 220px;
    border-radius: 50%; background: radial-gradient(circle, rgba(200,162,74,0.35), transparent 70%);
}
.hero-eyebrow { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent); font-weight: 600; }
.hero h1 { font-size: 1.9rem; font-weight: 700; margin: 0.3rem 0 0.4rem; color: #fff; letter-spacing: -0.02em; }
.hero p { font-size: 0.98rem; opacity: 0.85; margin: 0; max-width: 640px; }
.chips { margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.chip { font-size: 0.75rem; padding: 0.25rem 0.7rem; border-radius: 999px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); }

/* Section titles */
.section-title { font-size: 0.8rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin: 0.5rem 0 0.75rem; }

/* Quick action buttons */
div[data-testid="stMainBlockContainer"] .stButton > button {
    background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
    padding: 0.9rem 1rem; text-align: left; justify-content: flex-start; color: var(--ink);
    font-weight: 500; width: 100%; min-height: 3.4rem; transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
div[data-testid="stMainBlockContainer"] .stButton > button:hover {
    border-color: var(--brand-2); color: var(--brand); box-shadow: 0 4px 12px rgba(15,61,62,0.08); transform: translateY(-1px);
}

/* Chat */
.stChatMessage { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.75rem; }
.stChatMessage h1 { font-size: 1.3rem; color: var(--brand); }
.stChatMessage h2 { font-size: 1.1rem; color: var(--brand); margin-top: 1rem; }
.stChatMessage h3 { font-size: 1rem; }
.msg-meta { font-size: 0.72rem; color: var(--muted); margin-top: 0.5rem; }
[data-testid="stChatInput"] { border-radius: 12px; }
/* Streamlit's autosize can stick at max height after a rerun; size to content instead. */
[data-testid="stChatInput"] textarea { field-sizing: content; height: auto !important; min-height: 40px; max-height: 160px; }
</style>
"""


def init_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.started = datetime.now()


def reset_session():
    for key in ("session_id", "messages", "started"):
        st.session_state.pop(key, None)


def build_report() -> str:
    lines = [
        "# UAE Market Expansion Report",
        f"_Generated {datetime.now():%d %B %Y, %H:%M}_",
        "",
    ]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lines += ["---", f"## Question: {msg['content']}", ""]
        else:
            lines += [msg["content"], ""]
    return "\n".join(lines)


def render_knowledge_panel():
    st.markdown('<div class="sb-label">Knowledge base</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sb-row"><span>Documents</span><span>{len(knowledge_base.sources)}</span></div>'
        f'<div class="sb-row"><span>Indexed chunks</span><span>{len(knowledge_base.chunks)}</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Manage documents"):
        for name in knowledge_base.sources:
            st.caption(f"📄 {name}")
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
            # Bump the key to clear the uploader after indexing.
            st.session_state.kb_uploads = st.session_state.get("kb_uploads", 0) + 1
            st.toast(f"Indexed {len(uploads)} document(s)")
            st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sb-brand">🧭 Expansion Advisor</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-sub">AI market-entry strategist</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-label">Business profile</div>', unsafe_allow_html=True)
        for label, value in [
            ("Origin", "Jordan"),
            ("Concept", "Meaty pizza & kebab"),
            ("Markets", "Dubai · Abu Dhabi"),
            ("Delivery", "Talabat first"),
        ]:
            st.markdown(f'<div class="sb-row"><span>{label}</span><span>{value}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-label">Capabilities</div>', unsafe_allow_html=True)
        st.markdown(
            "- Knowledge base retrieval (RAG)\n- Live competitor research\n- Competitor menu scraping\n- Location & pricing strategy\n- Seasonal marketing plans"
        )

        render_knowledge_panel()

        st.markdown('<div class="sb-label">Session</div>', unsafe_allow_html=True)
        questions = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(
            f'<div class="sb-row"><span>Questions asked</span><span>{questions}</span></div>'
            f'<div class="sb-row"><span>Started</span><span>{st.session_state.started:%H:%M}</span></div>',
            unsafe_allow_html=True,
        )
        st.write("")

        if st.session_state.messages:
            st.download_button(
                "⬇  Export report (.md)",
                data=build_report(),
                file_name=f"uae_expansion_report_{datetime.now():%Y%m%d_%H%M}.md",
                mime="text/markdown",
                width="stretch",
            )
        if st.button("＋  New consultation", width="stretch"):
            reset_session()
            st.rerun()


def render_hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Market Entry Intelligence</div>
            <h1>UAE Restaurant Expansion Advisor</h1>
            <p>Data-backed recommendations on locations, competitors, menu, pricing and marketing
            for taking a Jordanian pizza &amp; kebab brand into Dubai and Abu Dhabi.</p>
            <div class="chips">
                <span class="chip">Dubai Marina</span><span class="chip">Downtown</span>
                <span class="chip">Business Bay</span><span class="chip">Yas Island</span>
                <span class="chip">Al Reem</span><span class="chip">Saadiyat</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_actions():
    st.markdown('<div class="section-title">Start with a topic</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (icon, title, prompt) in enumerate(QUICK_ACTIONS):
        if cols[i % 3].button(f"{icon}  {title}", key=f"qa_{i}", width="stretch"):
            st.session_state.pending_prompt = prompt
            st.rerun()


def stream_answer(prompt: str) -> str:
    
    status = st.status("Analyzing your question…", expanded=False)
    placeholder = st.empty()
    content = ""
    tools_used = []

    try:
        for event in agent.run(
            prompt,
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


def main():
    st.markdown(CSS, unsafe_allow_html=True)
    init_state()
    render_sidebar()
    render_hero()

    if not st.session_state.messages and "pending_prompt" not in st.session_state:
        render_quick_actions()

    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "user" else "🧭"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about locations, competitors, pricing, marketing…")
    prompt = prompt or st.session_state.pop("pending_prompt", None)
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧭"):
        answer = stream_answer(prompt)

    if answer:
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


if __name__ == "__main__":
    main()
