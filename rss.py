import datetime
import re
import os
import sys
from email.utils import format_datetime

# --- CONFIG
BASE_URL = "https://semilin.dev/blog/"
POSTS = [
    ("2023-12-11", "layout_quality.org", "What makes a keyboard layout good?"),
    ("2022-07-17", "final_reflection_on_semimak.org", "200 WPM - Final Reflection on Semimak"),
    ("2021-10-14", "reflection_on_semimak.org", "Reflecting on Semimak, 3 months later"),
    ("2021-07-01", "semimak.org", "Introducing Semimak"),
]

def get_body(org_file):
    html_file = org_file.replace(".org", ".html")
    path = f"./docs/blog/{html_file}"
    if not os.path.exists(path): return ""
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'<div id="content" class="content">(.*)</div>\s<div id="postamble"', content, re.DOTALL)
        return match.group(1) if match else print('regex problem!!')

if sys.argv[1] == "index":
    org_lines = ["#+TITLE: (blog semi)", "#+options: toc:nil", ""]
    org_lines.extend([f"- ({d}) [[file:{f}][{t}]]" for d, f, t in POSTS])
    with open("./src/blog/index.org", "w") as f:
        f.write("\n".join(org_lines))
    sys.exit(0)

rss_items = []
for date_str, filename, title in POSTS:
    url = BASE_URL + filename.replace(".org", ".html")
    pub_date = format_datetime(datetime.datetime.strptime(date_str, "%Y-%m-%d"))
    body = get_body(filename)
    
    rss_items.append(f""" <item>
  <title>{title}</title>
  <link>{url}</link>
  <guid>{url}</guid>
  <pubDate>{pub_date}</pubDate>
  <description><![CDATA[{body}]]></description>
 </item>""")

rss_template = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
 <title>(blog semi)</title>
 <link>{BASE_URL}</link>
 <description>Blog Feed</description>
{"\n".join(rss_items)}
</channel>
</rss>"""

with open("./docs/blog/feed.xml", "w") as f:
    f.write(rss_template)
