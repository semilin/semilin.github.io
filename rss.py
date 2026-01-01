import datetime
from email.utils import format_datetime

BASE_URL = "https://semilin.dev/blog/"
BLOG_TITLE = "(blog semi)"
RSS_TITLE = "(blog semi)"
RSS_DESCRIPTION = "'(languages philosophy code keyboards)"

posts = [
    ("2023-12-11", "layout_quality.org", "What makes a keyboard layout good?"),
    ("2022-07-17", "final_reflection_on_semimak.org", "200 WPM - Final Reflection on Semimak"),
    ("2021-10-14", "reflection_on_semimak.org", "Reflecting on Semimak, 3 months later"),
    ("2021-07-01", "semimak.org", "Introducing Semimak"),
]

def generate_files():
    org_content = f"#+TITLE: {BLOG_TITLE}\n#+options: toc:nil\n\n"
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
 <title>{RSS_TITLE}</title>
 <description>{RSS_DESCRIPTION}</description>
 <link>{BASE_URL}</link>
 <lastBuildDate>{format_datetime(datetime.datetime.now())}</lastBuildDate>
 <pubDate>{format_datetime(datetime.datetime.now())}</pubDate>
"""

    for date_str, filename, title in posts:
        org_content += f"- ({date_str}) [[file:{filename}][{title}]]\n"
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        web_link = BASE_URL + filename.replace(".org", ".html")
        
        rss_content += f""" <item>
  <title>{title}</title>
  <link>{web_link}</link>
  <guid>{web_link}</guid>
  <pubDate>{format_datetime(dt)}</pubDate>
 </item>
"""

    rss_content += "</channel>\n</rss>"

    # Write index.org
    with open("./src/blog/index.org", "w") as f:
        f.write(org_content)
    print("Generated index.org")

    # Write rss.xml
    with open("./docs/blog/rss.xml", "w") as f:
        f.write(rss_content)
    print("Generated rss.xml")

if __name__ == "__main__":
    generate_files()
