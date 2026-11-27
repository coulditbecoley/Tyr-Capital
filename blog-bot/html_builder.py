"""
html_builder.py
Generates the individual HTML post file and adds a row to the Market notes list in blog.html.
"""

import os
import re
from datetime import datetime

REPO_PATH = os.environ.get("TYR_REPO_PATH", "/home/ubuntu/Tyr-Capital")
POSTS_DIR = os.path.join(REPO_PATH, "posts")
BLOG_HTML = os.path.join(REPO_PATH, "blog.html")

# Category → thumbnail image mapping
CATEGORY_THUMBS = {
    "Bitcoin":        "images/thumb-bitcoin.jpg",
    "Market Update":  "images/thumb-bitcoin.jpg",
    "Weekly Outlook": "images/thumb-outlook.jpg",
    "Lending":        "images/thumb-lending.jpg",
    "Passive Income": "images/thumb-passive.jpg",
    "Risk":           "images/thumb-risk.jpg",
    "Trading Basics": "images/thumb-trading.jpg",
    "Market Cycles":  "images/thumb-cycles.jpg",
    "Altcoins":       "images/thumb-outlook.jpg",
    "Crypto Education": "images/thumb-trading.jpg",
}

# Category → data-category slug mapping for the filter bar
CATEGORY_FILTER = {
    "Bitcoin":          "bitcoin",
    "Market Update":    "bitcoin",
    "Weekly Outlook":   "weekly-outlook",
    "Lending":          "lending",
    "Passive Income":   "passive-income",
    "Risk":             "risk",
    "Trading Basics":   "trading-basics",
    "Market Cycles":    "market-cycles",
    "Altcoins":         "market-cycles",
    "Crypto Education": "trading-basics",
}


def build_post_html(post):
    """
    Generate a full standalone HTML post page from the post data dict.
    Returns the HTML string.
    """
    title = post["title"]
    category = post["category"]
    excerpt = post["excerpt"]
    read_time = post["read_time"]
    date_full = post["date_full"]
    html_body = post["html_body"]
    slug = post["slug"]
    thumb = CATEGORY_THUMBS.get(category, "images/thumb-bitcoin.jpg")
    thumb_abs = f"https://tyrcapital.io/{thumb}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-6HGF1EDX4Y"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-6HGF1EDX4Y');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Tyr Capital</title>
  <meta name="description" content="{excerpt}">
  <meta name="keywords" content="{post.get('keywords', category + ', crypto, Bitcoin, digital assets, Tyr Capital')}">
  <meta name="author" content="Coley Grantham">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://tyrcapital.io/posts/{slug}.html">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://tyrcapital.io/posts/{slug}.html">
  <meta property="og:title" content="{title} | Tyr Capital">
  <meta property="og:description" content="{excerpt}">
  <meta property="og:image" content="{thumb_abs}">
  <meta property="og:site_name" content="Tyr Capital">
  <meta property="article:author" content="Coley Grantham">
  <meta property="article:published_time" content="{date_full}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | Tyr Capital">
  <meta name="twitter:description" content="{excerpt}">
  <meta name="twitter:image" content="{thumb_abs}">

  <!-- JSON-LD Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{excerpt}",
    "image": "{thumb_abs}",
    "author": {{"@type": "Person", "name": "Coley Grantham", "url": "https://www.linkedin.com/in/coley-grantham-1b10a4bb/"}},
    "publisher": {{"@type": "Organization", "name": "Tyr Capital", "url": "https://tyrcapital.io", "logo": {{"@type": "ImageObject", "url": "https://tyrcapital.io/favicon.png"}}}},
    "datePublished": "{date_full}",
    "dateModified": "{date_full}",
    "keywords": "{post.get('keywords', category)}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://tyrcapital.io/posts/{slug}.html"}}
  }}
  </script>

  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600&amp;family=Public+Sans:wght@400..700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>

  <a class="skip-link" href="#main">Skip to content</a>

  <div class="topbar">
    <div class="container nav">
      <a href="../index.html" class="brand">
        <span class="brand-mark"></span>
        <span>Tyr Capital</span>
      </a>
      <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation" aria-expanded="false" aria-controls="navLinks">
        <span></span><span></span><span></span>
      </button>
      <div class="nav-links" id="navLinks">
        <a href="../index.html#how">How it works</a>
        <a href="../index.html#about">About</a>
        <a href="../index.html#ceo">Leadership</a>
        <a href="../blog.html">Insights</a>
        <a class="btn btn-primary" href="../index.html#lender">Become a lender</a>
      </div>
    </div>
  </div>

  <main id="main">
  <article class="post-article">
    <div class="container post-container">

      <div class="post-header">
        <a href="../blog.html" class="back-link">Back to insights</a>
        <p class="post-meta"><span>{category}</span> &middot; {date_full} &middot; {read_time} read &middot; Coley Grantham</p>
        <h1 class="post-article-title">{title}</h1>
      </div>

      <div class="post-body">
        {html_body}
      </div>

      <div class="post-footer-cta">
        <h2>Lending to Tyr Capital</h2>
        <p>Tyr Capital borrows from a small group of private lenders on fixed terms of 6 to 24 months. Read how it works, and what the risks are, before you inquire.</p>
        <a class="btn btn-primary" href="../index.html#how">How lending works</a>
      </div>

    </div>
  </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="../index.html" class="brand">
            <span class="brand-mark"></span>
            <span>Tyr Capital</span>
          </a>
          <p class="footer-tagline">Disciplined execution.<br>Structured risk. Long-term thinking.</p>
        </div>
        <div class="footer-nav">
          <h2 class="footer-heading">Site</h2>
          <ul>
            <li><a href="../index.html#how">How lending works</a></li>
            <li><a href="../index.html#about">About</a></li>
            <li><a href="../index.html#ceo">Leadership</a></li>
            <li><a href="../blog.html">Insights</a></li>
            <li><a href="../index.html#lender">Become a lender</a></li>
          </ul>
        </div>
        <div class="footer-nav">
          <h2 class="footer-heading">Contact</h2>
          <ul>
            <li><a href="../index.html#contact">Book a call</a></li>
            <li><a href="mailto:tyrcapitalllc@gmail.com">tyrcapitalllc@gmail.com</a></li>
            <li><a href="https://www.linkedin.com/in/coley-grantham-1b10a4bb/" target="_blank" rel="noopener noreferrer">LinkedIn: Coley Grantham</a></li>
            <li><a href="https://t.me/tyrcapitaltrades" target="_blank" rel="noopener noreferrer">Telegram: Tyr Capital Trades</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <ul class="footer-legal">
          <li><a href="../risk-disclosures.html">Risk disclosures</a></li>
          <li><a href="../privacy.html">Privacy</a></li>
          <li><a href="../terms.html">Terms</a></li>
        </ul>
        <p class="footer-disclaimer">Tyr Capital LLC is a Wyoming limited liability company. Research and commentary on this site are for information only and are not financial, investment, legal or tax advice, or an offer to manage funds. Private loans to Tyr Capital are unsecured, are not bank deposits and are not insured by the FDIC or any other agency. You could lose some or all of the money you lend. Any loan is governed only by a signed loan agreement.</p>
        <p class="footer-copy">&copy; <span id="footerYear"></span> Tyr Capital LLC. All rights reserved. Site by <a href="https://skaldstudio.io/">Skald Studio</a>.</p>
      </div>
    </div>
  </footer>

  <script>
    document.getElementById('footerYear').textContent = new Date().getFullYear();
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navLinks = document.getElementById('navLinks');
    if (hamburgerBtn && navLinks) {{
      hamburgerBtn.addEventListener('click', function () {{
        const isOpen = navLinks.classList.toggle('open');
        hamburgerBtn.classList.toggle('open', isOpen);
        hamburgerBtn.setAttribute('aria-expanded', isOpen);
      }});
      navLinks.querySelectorAll('a').forEach(function (link) {{
        link.addEventListener('click', function () {{
          navLinks.classList.remove('open');
          hamburgerBtn.classList.remove('open');
          hamburgerBtn.setAttribute('aria-expanded', 'false');
        }});
      }});
    }}

    // GA read time tracking
    const readMilestones = {{30: false, 60: false, 120: false}};
    setInterval(function() {{
      Object.keys(readMilestones).forEach(function(sec) {{
        if (!readMilestones[sec]) {{
          readMilestones[sec] = true;
          if (typeof gtag === 'function') {{
            gtag('event', 'read_time', {{event_category: 'Engagement', event_label: sec + 's', page_title: document.title}});
          }}
        }}
      }});
    }}, 1000);
  </script>

</body>
</html>
"""


def write_post_file(post):
    """Write the generated post HTML to the posts/ directory."""
    filepath = os.path.join(POSTS_DIR, post["filename"])
    html = build_post_html(post)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[html_builder] Post file written: {filepath}")
    return filepath


def inject_blog_card(post):
    """Prepend a new row to the Market notes list in blog.html."""
    with open(BLOG_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    when = datetime.strptime(post["date_full"], "%B %d, %Y")
    category = post["category"]
    cat_slug = re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")
    new_row = f"""
          <li class="note" data-category="{cat_slug}">
            <time datetime="{when:%Y-%m-%d}">{when:%b} {when.day}, {when.year}</time>
            <a href="posts/{post['filename']}">{post['title']}</a>
            <span class="note-cat">{category}</span>
          </li>"""

    marker = '<ul class="notes" id="notesList">'
    if marker not in content:
        print("[html_builder] WARNING: Could not find notes list marker in blog.html")
        return
    content = content.replace(marker, marker + new_row, 1)

    with open(BLOG_HTML, "w", encoding="utf-8") as f:
        f.write(content)

    print("[html_builder] blog.html updated. New market note prepended.")


if __name__ == "__main__":
    # Quick test with dummy data
    test_post = {
        "title": "Test Post: Bitcoin Holds Key Support at $78K",
        "slug": "test-post-bitcoin-holds-key-support",
        "filename": "test-post-bitcoin-holds-key-support.html",
        "category": "Bitcoin",
        "excerpt": "Bitcoin is holding a critical support level as the market digests macro headwinds.",
        "read_time": "5 min",
        "date": "Apr 2026",
        "date_full": "April 23, 2026",
        "html_body": "<p>This is a test post body.</p>",
        "topic": "BTC support level test",
    }
    filepath = write_post_file(test_post)
    inject_blog_card(test_post)
    print("Test complete.")
