# Folium's iframes really annoy me so like this file just splits them out into separate html files

import re
import glob
from pathlib import Path

src_pattern = re.compile('srcdoc="(.*?)"', re.S)
error_check = re.compile('&.*?;')
dirname = "./reports"

replacements = {
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#x27;": "'"
}

for file_name in glob.glob(f"{dirname}/ProjectReport*.html"):
    name = file_name[14 + len(dirname):-5]
    print(name)
    with open(file_name) as f:
        content = f.read()

    print(file_name, len(content))
    i = 1
    while (src := src_pattern.search(content)):
        html = src.group(1)
        for _from, _to in replacements.items():
            html = html.replace(_from, _to)
        unresolved = error_check.findall(html)
        if len(unresolved):
            print("Unresolved: ", set(unresolved))

        out_dir = f"srcs/{name.lower()}"
        Path(f"{dirname}/{out_dir}").mkdir(parents=True, exist_ok=True)
        out_html = f"{out_dir}/{name.lower()}{i}.html"
        with open(f"{dirname}/{out_html}", "w") as html_f:
            html_f.write(html)

        content = content[:src.start()] + f'src="{out_html}"' + content[src.end():]
        i += 1

    print("Stripped to ", len(content))
    with open(file_name, 'w') as f:
        f.write(content)
