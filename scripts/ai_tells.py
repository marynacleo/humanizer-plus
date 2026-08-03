#!/usr/bin/env python3
"""Detect AI-writing tells in EN/FR/RU prose. Read-only, no dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".html", ".htm", ".rst", ".mdx"}

# These rules depend on capitalisation, everything else is matched case-insensitively.
CASE_SENSITIVE = {"title_case", "ru_title_case", "tool_trace", "fake_candid"}

# (id, label, regex, severity) - severity: hard = always fix, soft = check in context
PHRASE_RULES = {
    "common": [
        ("dash", "em or en dash", r"[—–]|&[mn]dash;|&#821[12];", "hard"),
        ("dash_double", "double hyphen used as a dash", r"\s--\s", "hard"),
        ("emoji_bullet", "emoji on a heading or bullet",
         r"(?m)^\s*(?:#{1,6}|[-*])\s*[\U0001F300-\U0001FAFF✅✨⚡⭐]", "hard"),
        ("bold_header_list", "inline-header list item",
         r"(?m)^\s*[-*]\s*\*\*[^*]{2,40}\*\*\s*:", "hard"),
        ("heading_period", "full stop at the end of a heading",
         r"(?m)^\s*#{1,6}\s+.*[^.?!:]\.\s*$", "hard"),
        ("title_case", "Title Case heading",
         r"(?m)^[ \t]*#{1,6}[ \t]+(?=(?:.*?\s(?:The|Of|And|In|On|For|To|With|Or|An?|De[s]?|Du|La|Le|Les|Et|En|Pour|Avec|Sur)\b){2}).*$", "hard"),
        ("tool_trace", "AI tool name",
         r"\b(?:Claude|Codex|ChatGPT|OpenAI|Anthropic|Gemini|GPT-4|LLM-generated)\b", "soft"),
    ],
    "en": [
        ("ai_vocab", "AI vocabulary",
         r"\b(?:delve|delves|crucial|pivotal|tapestry|testament|underscore[sd]?|showcas(?:e|es|ing)|"
         r"foster(?:s|ing)?|garner(?:s|ed)?|intricate|intricacies|interplay|vibrant|"
         r"enhanc(?:e|es|ing|ed)|align with|multifaceted|realm of|myriad)\b", "soft"),
        ("promo", "advertising register",
         r"\b(?:nestled|in the heart of|breathtaking|must-visit|stunning|renowned|boasts?|"
         r"rich (?:cultural|history|heritage)|natural beauty|hidden gem)\b", "soft"),
        ("significance", "inflated significance",
         r"\b(?:stands as|serves as|is a testament|plays a (?:vital|crucial|key|pivotal) role|"
         r"marking a|reflects broader|evolving landscape|setting the stage|key turning point)\b", "soft"),
        ("neg_parallel", "negative parallelism",
         r"\b(?:not only\b[^.]{0,80}\bbut also|it'?s not just\b|it'?s not merely\b|isn'?t just about)\b", "hard"),
        ("signpost", "announcing instead of doing",
         r"\b(?:let'?s (?:dive|explore|break this down|take a look)|here'?s what you need to know|"
         r"without further ado|in this article,? we)\b", "hard"),
        ("chat_artifact", "chat residue",
         r"\b(?:I hope this helps|Of course!|Certainly!|You'?re absolutely right|"
         r"Would you like me to|Let me know if|Great question)(?!\w)", "hard"),
        ("hedge", "excessive hedging",
         r"\b(?:could potentially|might possibly|it could be argued that|it is important to note that|"
         r"it is worth noting that)\b", "soft"),
        ("filler", "filler phrase",
         r"\b(?:in order to|due to the fact that|at this point in time|in the event that|"
         r"has the ability to|a wide (?:range|variety) of)\b", "soft"),
        ("authority", "false authority",
         r"\b(?:the real question is|at its core|what really matters|the heart of the matter|"
         r"fundamentally,|the deeper issue)\b", "soft"),
        ("vague_source", "vague attribution",
         r"\b(?:experts (?:say|argue|believe)|observers have|industry reports|some critics argue|"
         r"studies (?:show|suggest) that)\b", "soft"),
        ("copula", "copula avoidance",
         r"\b(?:serves as a|stands as a|represents a|features a|offers a)\b", "soft"),
        ("cutoff", "cutoff disclaimer or gap-filling",
         r"\b(?:as of my last|up to my last training|while specific details are|"
         r"not publicly available|maintains a low profile|it is believed that)\b", "hard"),
        ("curly_quote", "curly quotes", r"[“”]", "soft"),
        ("fake_candid", "fake-candid opener",
         r"(?m)(?:^|\.\s+)(?:Honestly\?|Look,|Here'?s the thing|The thing is,|Let'?s be honest)", "soft"),
    ],
    "fr": [
        ("fr_opener", "formulaic opener",
         r"(?i)\b(?:dans un monde où|à l'ère du numérique|force est de constater|"
         r"il est important de noter|plongeons dans|décryptons|sans plus attendre)\b", "hard"),
        ("fr_empty_adj", "empty adjective",
         r"(?i)\b(?:véritable|incontournable|unique en son genre|au cœur de|riche(?:sse)? (?:culturelle|patrimoine)|"
         r"un atout majeur|une expérience inoubliable)\b", "soft"),
        ("fr_neg_parallel", "non seulement / mais aussi",
         r"(?i)\bnon seulement\b[^.]{0,80}\bmais (?:aussi|également)\b", "hard"),
        ("fr_conclusion", "boilerplate ending",
         r"(?i)\b(?:en conclusion|pour conclure|en somme|n'hésitez pas à nous contacter)\b", "soft"),
        ("fr_nominal", "heavy nominalisation",
         r"(?i)\bla (?:mise en place|réalisation|mise en œuvre) de la\b", "soft"),
        ("fr_chat", "chat residue",
         r"(?i)\b(?:bien sûr\s*!|excellente question|j'espère que cela vous aide|"
         r"souhaitez-vous que je)(?!\w)", "hard"),
    ],
    "ru": [
        ("ru_title_case", "Title Case heading (Cyrillic)",
         r"(?m)^[ \t]*#{1,6}[ \t]+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)+\s*$", "hard"),
        ("ru_opener", "formulaic opener",
         r"(?i)\b(?:в современном мире|в наше время|давайте разберём|стоит отметить, что|"
         r"важно отметить, что|как известно,)\b", "hard"),
        ("ru_empty", "empty vocabulary",
         r"(?i)\b(?:динамично развивающ\w+|играет ключевую роль|широкий спектр|уникальное сочетание|"
         r"неотъемлемой частью|позволяет значительно|богат\w+ культурн\w+ наследи\w+)\b", "soft"),
        ("ru_neg_parallel", "ne tolko / no i",
         r"(?i)\bне только\b[^.]{0,80}\bно и\b", "hard"),
        ("ru_conclusion", "boilerplate ending",
         r"(?i)\b(?:в заключение|подводя итог|таким образом,? можно сделать вывод)\b", "soft"),
        ("ru_chat", "chat residue",
         r"(?i)\b(?:отличный вопрос|надеюсь, это поможет|хотите, я|вы абсолютно правы)\b", "hard"),
        ("ru_kancelyarit", "bureaucratese",
         r"(?i)\b(?:осуществл\w+|в целях обеспечения|данный (?:вопрос|аспект)|в рамках реализации)\b", "soft"),
    ],
}

RULE_OF_THREE = re.compile(
    r"\b\w[\w'-]*,\s+\w[\w'-]*(?:\s+\w[\w'-]*)?,\s+(?:and|et|и)\s+\w[\w'-]*\b", re.IGNORECASE)

CODE_BLOCK = re.compile(r"(?ms)^```.*?^```")
INLINE_CODE = re.compile(r"`[^`\n]*`")
FRONTMATTER = re.compile(r"(?s)\A---\n.*?\n---\n")
HTML_COMMENT = re.compile(r"(?s)<!--.*?-->")
URL = re.compile(r"https?://\S+")
# Text inside guillemets is quoted or cited, and the skill says not to rewrite quotations.
QUOTED = re.compile(r"«[^»\n]{0,300}»")


def detect_lang(text: str) -> str:
    if re.search(r"[а-яА-ЯёЁ]", text):
        return "ru"
    if re.search(r"(?i)\b(?:le|la|les|des|une|vous|nous|pour|avec|est)\b", text) and \
       len(re.findall(r"[éèêàçùô]", text)) > 3:
        return "fr"
    return "en"


def blank(match: re.Match[str]) -> str:
    """Replace a match with spaces so line and column positions stay intact."""
    return re.sub(r"\S", " ", match.group(0))


SCRIPT_STYLE = re.compile(r"(?is)<(script|style)\b.*?</\1>")
HTML_TAG = re.compile(r"(?s)<[^>]+>")
ALT_TITLE = re.compile(r"""(?i)\b(?:alt|title|content)\s*=\s*(["'])(.*?)\1""")


def strip_html(text: str) -> str:
    """Keep visible text plus alt/title/meta values; blank the markup around them."""
    text = SCRIPT_STYLE.sub(blank, text)

    def clean_tag(match: re.Match[str]) -> str:
        tag = match.group(0)
        kept = [" "] * len(tag)
        for attribute in ALT_TITLE.finditer(tag):
            start, end = attribute.span(2)
            kept[start:end] = list(attribute.group(2))
        return "".join(kept)

    return HTML_TAG.sub(clean_tag, text)


def strip_noise(text: str, is_html: bool = False) -> str:
    """Blank out code, frontmatter, comments and URLs so prose rules do not fire on them."""
    for pattern in (FRONTMATTER, CODE_BLOCK, HTML_COMMENT, INLINE_CODE, URL, QUOTED):
        text = pattern.sub(blank, text)
    if is_html:
        text = strip_html(text)
    return text


# Typography rules that only bind public-facing text; internal notes may keep dashes.
PUBLIC_ONLY = {"dash", "dash_double", "heading_period", "title_case", "ru_title_case", "curly_quote"}


def scan(text: str, lang: str, is_html: bool = False, internal: bool = False) -> dict:
    clean = strip_noise(text, is_html)
    lines = clean.splitlines()
    words = len(re.findall(r"[\w'’-]+", clean))
    rules = PHRASE_RULES["common"] + PHRASE_RULES.get(lang, [])
    hits: list[dict] = []

    for rule_id, label, pattern, severity in rules:
        if internal and rule_id in PUBLIC_ONLY:
            severity = "soft"
        flags = 0 if rule_id in CASE_SENSITIVE else re.IGNORECASE
        for match in re.finditer(pattern, clean, flags):
            line_no = clean.count("\n", 0, match.start()) + 1
            source = lines[line_no - 1].strip() if line_no <= len(lines) else ""
            hits.append({
                "rule": rule_id,
                "label": label,
                "severity": severity,
                "line": line_no,
                "match": match.group(0).strip()[:60],
                "context": source[:110],
            })

    triples = len(RULE_OF_THREE.findall(clean))
    hard = sum(1 for hit in hits if hit["severity"] == "hard")
    soft = sum(1 for hit in hits if hit["severity"] == "soft")
    density = round((hard * 2 + soft + triples) / max(words, 1) * 1000, 1)

    return {
        "words": words,
        "lang": lang,
        "hard": hard,
        "soft": soft,
        "rule_of_three": triples,
        "density_per_1000_words": density,
        "hits": sorted(hits, key=lambda hit: hit["line"]),
    }


def collect(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(
        path for path in target.rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part.startswith((".", "_")) for part in path.parts)
    )


def report(path: Path, result: dict, show_all: bool) -> None:
    verdict = "clean" if result["hard"] == 0 and result["density_per_1000_words"] < 4 else "review"
    print(f"\n== {path} [{result['lang']}] {result['words']} words — {verdict}")
    print(f"   hard: {result['hard']}  soft: {result['soft']}  triplets: {result['rule_of_three']}"
          f"  density: {result['density_per_1000_words']} per 1000 words")
    shown = result["hits"] if show_all else [h for h in result["hits"] if h["severity"] == "hard"][:40]
    for hit in shown:
        mark = "!" if hit["severity"] == "hard" else "·"
        print(f"   {mark} {path.name}:{hit['line']} {hit['label']}: {hit['match']!r}")
    remaining = len(result["hits"]) - len(shown)
    if remaining > 0:
        print(f"   ... {remaining} more soft hits, run with --all")


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect AI-writing tells in EN/FR/RU prose")
    parser.add_argument("target", help="file or folder")
    parser.add_argument("--lang", default="auto", choices=["auto", "en", "fr", "ru"])
    parser.add_argument("--all", action="store_true", help="show soft hits as well")
    parser.add_argument("--internal", action="store_true",
                        help="internal note, not public text: typography counts as soft")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    target = Path(args.target)
    if not target.exists():
        print(f"no such path: {target}", file=sys.stderr)
        return 2

    paths = collect(target)
    if not paths:
        print("no text files found (.md .txt .html .rst .mdx)", file=sys.stderr)
        return 2

    results = {}
    worst = 0
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        lang = detect_lang(text) if args.lang == "auto" else args.lang
        result = scan(text, lang, path.suffix.lower() in {".html", ".htm"}, args.internal)
        results[str(path)] = result
        worst = max(worst, result["hard"])
        if not args.json:
            report(path, result, args.all)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if worst else 0


if __name__ == "__main__":
    raise SystemExit(main())
