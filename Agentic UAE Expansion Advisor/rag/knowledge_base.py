

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
SUPPORTED = {".md", ".txt"}
MAX_CHUNK_CHARS = 1200

STOPWORDS = set(
    "a an and are as at be by for from has have how in is it its of on or our "
    "should that the their there this to was we what when where which who why "
    "will with you your can do does into than then them they about".split()
)


@dataclass
class Chunk:
    source: str
    heading: str
    text: str


def stem(token: str) -> str:
    
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    return [stem(t) for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS and len(t) > 1]


def split_document(path: Path) -> list[Chunk]:
   
    raw = path.read_text(encoding="utf-8", errors="ignore")
    chunks, heading, buf = [], path.stem.replace("_", " ").title(), []

    def flush():
        body = "\n".join(buf).strip()
        if not body:
            return
        paragraphs, current = body.split("\n\n"), ""
        for para in paragraphs:
            if current and len(current) + len(para) > MAX_CHUNK_CHARS:
                chunks.append(Chunk(path.name, heading, current.strip()))
                current = ""
            current += para + "\n\n"
        if current.strip():
            chunks.append(Chunk(path.name, heading, current.strip()))

    for line in raw.splitlines():
        match = re.match(r"^#{1,3}\s+(.*)", line)
        if match:
            flush()
            heading, buf = match.group(1).strip(), []
        else:
            buf.append(line)
    flush()
    return chunks


class KnowledgeBase:
    def __init__(self, directory: Path = KNOWLEDGE_DIR, k1: float = 1.5, b: float = 0.75):
        self.directory = directory
        self.k1, self.b = k1, b
        self.reload()

    def reload(self):
        self.directory.mkdir(exist_ok=True)
        self.chunks: list[Chunk] = []
        for path in sorted(self.directory.iterdir()):
            if path.suffix.lower() in SUPPORTED:
                self.chunks.extend(split_document(path))

       
        self.docs = [tokenize(f"{c.heading} {c.heading} {c.text}") for c in self.chunks]
        self.tfs = [Counter(d) for d in self.docs]
        self.avg_len = sum(map(len, self.docs)) / max(len(self.docs), 1)
        df = Counter(term for d in self.docs for term in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    @property
    def sources(self) -> list[str]:
        return sorted({c.source for c in self.chunks})

    def search(self, query: str, k: int = 4) -> list[tuple[float, Chunk]]:
        terms = tokenize(query)
        scored = []
        for chunk, tf, doc in zip(self.chunks, self.tfs, self.docs):
            score = 0.0
            for t in terms:
                if t not in tf:
                    continue
                f = tf[t]
                norm = f + self.k1 * (1 - self.b + self.b * len(doc) / self.avg_len)
                score += self.idf[t] * f * (self.k1 + 1) / norm
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]


knowledge_base = KnowledgeBase()
