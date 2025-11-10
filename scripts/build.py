import os, pathlib, yaml, markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "content.yaml"
TPL_DIR = ROOT / "templates"
OUT_DIR = ROOT / "dist"
ASSETS_DIR = ROOT / "assets"

def md_filter(text: str) -> str:
    if not text:
        return ""
    return markdown.markdown(
        text,
        extensions=["extra","sane_lists","smarty","toc","tables","attr_list"]
    )

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Copy assets alongside output for simple static hosting
    # (Keep relative link ../assets/styles.css working)
    (OUT_DIR / "assets").mkdir(exist_ok=True)
    # crude copy: only styles.css for now
    with open(ASSETS_DIR / "styles.css","rb") as src, open(OUT_DIR / "assets" / "styles.css","wb") as dst:
        dst.write(src.read())

    with open(DATA, "r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)

    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(["html","xml"])
    )
    env.filters["markdown"] = md_filter

    template = env.get_template("page.html.j2")
    html = template.render(**payload)

    out_file = OUT_DIR / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote {out_file}")

if __name__ == "__main__":
    main()