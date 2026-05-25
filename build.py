import json
import re
import html

HIGHLIGHT_NAME = "Hongo"

CONF_ICONS = {
    "CVPR": "📸", "ICCV": "📷", "ECCV": "🔭",
    "NeurIPS": "🧠", "ICML": "⚡", "ICLR": "🔬",
    "WACV": "🏔️", "SIGGRAPH": "🎨", "IROS": "🤖",
}


def make_author_html(author_str):
    # Split on " and " or ", "
    names = re.split(r"\s+and\s+|,\s*", author_str)
    parts = []
    for name in names:
        name = name.strip()
        if not name:
            continue
        escaped = html.escape(name)
        if HIGHLIGHT_NAME in name:
            parts.append(f"<strong>{escaped}</strong>")
        else:
            parts.append(escaped)
    return ", ".join(parts)


def conf_icon(conf_str):
    for key, icon in CONF_ICONS.items():
        if key in conf_str:
            return icon
    return "📄"


def make_venue_html(paper):
    conf = html.escape(paper.get("conf", ""))
    award = paper.get("award")
    if award:
        return f'{conf} &nbsp;·&nbsp; {html.escape(award)}'
    return conf


def make_links_html(paper):
    links = [
        ("paper_url", "Paper"),
        ("code_url", "Code"),
        ("project_url", "Project Page"),
        ("demo_url", "Demo"),
        ("talk_url", "Talk"),
    ]
    parts = []
    for key, label in links:
        url = paper.get(key)
        if url:
            parts.append(f'<a class="pub-link" href="{html.escape(url)}">{label}</a>')
    return "\n            ".join(parts)


def render_card(paper):
    icon = conf_icon(paper.get("conf", ""))
    venue = make_venue_html(paper)
    title = html.escape(paper.get("title", ""))
    authors = make_author_html(paper.get("author", ""))
    links = make_links_html(paper)
    return f"""      <div class="pub-card">
        <div class="pub-thumb">{icon}</div>
        <div>
          <div class="pub-venue">{venue}</div>
          <div class="pub-title">{title}</div>
          <div class="pub-authors">{authors}</div>
          <div class="pub-links">
            {links}
          </div>
        </div>
      </div>"""


def build():
    with open("template.html", encoding="utf-8") as f:
        template = f.read()
    with open("papers.json", encoding="utf-8") as f:
        papers = json.load(f)

    cards = "\n\n".join(render_card(p) for p in papers)
    output = template.replace("{{PAPERS}}", cards)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Built index.html from {len(papers)} paper(s).")


if __name__ == "__main__":
    build()
