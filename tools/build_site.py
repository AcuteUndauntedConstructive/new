#!/usr/bin/env python3
"""Turn the Hop to Heal 2.0 design boards into the real website in docs/.

Usage (from the repo root):  python3 tools/build_site.py

WARNING: this overwrites docs/*.html. Run it only when the designs in
hoptoheal/website-designs-2.0/project/ changed and you want to re-import them.
For day-to-day work, edit the pages in docs/ directly.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'hoptoheal', 'website-designs-2.0', 'project')
ASSETS = os.path.join(ROOT, 'hoptoheal', 'assets')
OUT = os.path.join(ROOT, 'docs')

PAGES = {  # design board -> (page file, title, description)
    'Main': ('index.html', 'Hop to Heal · Child development and counselling centre, Mayur Vihar, Delhi', 'Occupational therapy, speech therapy, special education and counselling for children, parents and adults in Mayur Vihar Phase 1, Delhi.'),
    'Services': ('services.html', 'Services · Hop to Heal', 'All therapies and services at Hop to Heal, for children, families, adults and elders.'),
    'Counselling': ('counselling.html', 'Counselling · Hop to Heal', '30-minute counselling sessions, online on Google Meet or at the centre.'),
    'HopCheck': ('hopcheck.html', 'HopCheck · Hop to Heal', 'A free check for parents and children that shows which support could help.'),
    'ParentCheck': ('hopcheck-parent.html', 'HopCheck for grown-ups · Hop to Heal', 'The grown-up part of HopCheck.'),
    'KidCheck': ('hopcheck-child.html', 'HopCheck: My turn! · Hop to Heal', 'The child part of HopCheck, for ages 7 to 16.'),
    'Result': ('hopcheck-result.html', 'HopCheck result · Hop to Heal', 'A HopCheck result reviewed and signed by a therapist.'),
    'QuestionBank': ('question-bank.html', 'HopCheck question bank · Hop to Heal', 'Team page: HopCheck questions and scoring rules.'),
    'SignIn': ('sign-in.html', 'Sign in · Hop to Heal', 'Sign in to your Hop to Heal portal.'),
    'Book': ('book.html', 'Book a session · Hop to Heal', 'Book a therapy or counselling session.'),
    'Pay': ('pay.html', 'Pay · Hop to Heal', 'Pay for your booking.'),
    'Parent': ('portal.html', 'My portal · Hop to Heal', 'Parent portal: sessions, plans, care tips and payments.'),
    'Child': ('child.html', 'Child progress · Hop to Heal', 'Goals, progress, notes and reports for your child.'),
    'Therapist': ('therapist.html', 'Therapist portal · Hop to Heal', 'Team page: therapist portal.'),
    'Update': ('therapist-update.html', 'Session update · Hop to Heal', 'Team page: update a child after a session.'),
    'TestPlan': ('test-plan.html', 'Tester checklist · Hop to Heal', 'Team page: what to test before launch.'),
}
IMAGES = {  # design asset id -> (source file in hoptoheal/assets, file name on the site)
    'b35ebc36e430a1ea4cd8d1dc63b7911d': ('logo_full_transparent.png', 'logo.png'),
    '74d34aee036d0a0bc9d06f3ed62064cb': ('logo_wordmark_no_sun.png', 'logo-wordmark.png'),
    'f14847ef8e56cc58049ec7094badbf01': ('team-heena-gupta.jpg', 'team-heena-gupta.jpg'),
    '828e482bd62f885b7a113dfe7dab9fac': ('team-jiya-gupta.jpg', 'team-jiya-gupta.jpg'),
    '741d715af7d217bb9708dbfa85b9b338': ('team-vishal-gupta.jpg', 'team-vishal-gupta.jpg'),
    '7c0cf822c9768687f9c54c21aaf0d3a3': ('team-subodh-gupta.jpg', 'team-subodh-gupta.jpg'),
    '0f3429ec7928a645fbc6c3a7139e61c8': ('photo-founder-at-centre.jpg', 'photo-founder-at-centre.jpg'),
    '60fe6366ce2a5dacd4361ab7eb852f69': ('photo-fine-motor-activity.jpg', 'photo-fine-motor-activity.jpg'),
    'b88b6c156d46cd420bc2afdb492d6fd0': ('photo-festive-centre.jpg', 'photo-festive-centre.jpg'),
}
ROOT_STYLE = {  # boards that were fixed-size artboards need a web-page root instead
    'KidCheck': ("width: 390px; height: 844px;", "width: 100%; max-width: 480px; min-height: 100dvh; margin: 0 auto;"),
    'QuestionBank': ("width: 1600px; height: 4000px;", "max-width: 1600px; margin: 0 auto;"),
}
PAGE_BG = {'KidCheck': '#123D2E', 'ParentCheck': '#FFEDC9', 'Therapist': '#EEF3EA', 'Update': '#EEF3EA'}

def convert(name):
    t = open(os.path.join(SRC, name + '.dc.html'), encoding='utf8').read()
    file, title, desc = PAGES[name]
    helmet = re.search(r'<helmet>(.*?)</helmet>', t, re.S).group(1).strip()
    body = re.search(r'</helmet>(.*)</x-dc>', t, re.S).group(1).strip()
    m = re.search(r"<script type=\"text/x-dc\" data-dc-script data-props='(.*?)'>(.*?)</script>", t, re.S)
    props = {k: v.get('default') for k, v in json.loads(m.group(1)).items() if not k.startswith('$')}
    code = m.group(2).strip('\n')

    def links(s):
        for board, (page, _, _) in PAGES.items():
            s = s.replace(board + '.dc.html', page)
        assert '.dc.html' not in s, (name, re.findall(r'\w+\.dc\.html', s)[:3])
        for blob, (_, img) in IMAGES.items():
            s = s.replace('/_blob/' + blob, 'assets/img/' + img)
        assert '/_blob/' not in s, (name, 'unmapped image')
        return s
    body, code, helmet = links(body), links(code), links(helmet)

    # artboard leftovers
    first = body.index('>') + 1
    head_tag = re.sub(r';?\s*min-height: \d{3,4}px', '', body[:first])
    if name in ROOT_STYLE:
        old, new = ROOT_STYLE[name]
        assert old in head_tag, name
        head_tag = head_tag.replace(old, new).replace('overflow: hidden', 'overflow: visible') if name == 'QuestionBank' else head_tag.replace(old, new)
    body = head_tag + body[first:]
    body = re.sub(r' hint-placeholder-[a-z]+="[^"]*"', '', body)
    body = re.sub(r'minmax\((\d+)px, 1fr\)', r'minmax(min(\1px, 100%), 1fr)', body)
    for bad in ('<table', '<select'):  # the browser moves unknown tags out of tables/selects
        for chunk in re.findall(re.escape(bad) + r'.*?</' + bad[1:] + '>', body, re.S):
            assert '<sc-' not in chunk, (name, 'sc-if/sc-for inside ' + bad)
    assert '</script' not in code and '</template' not in body, name

    bg = PAGE_BG.get(name, '#F6FAF3')
    return file, f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#FBA826">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
{helmet}
<link rel="stylesheet" href="assets/site.css">
<script src="assets/app.js"></script>
</head>
<body style="background: {bg}">
<div class="preview-bar" role="note">Preview site: example data only. Sign-in, saved accounts and payments are not live yet.</div>
<div id="app"></div>
<noscript><p style="padding: 24px; font-family: sans-serif">Please turn on JavaScript to use this site, or call Hop to Heal on +91 95994 33591.</p></noscript>

<!-- What the page shows. {{{{name}}}} values come from renderVals() in the script below. -->
<template id="view">
{body}
</template>

<!-- What the page does. -->
<script>
{code}
HopApp.mount(Component, {json.dumps(props, ensure_ascii=False)});
</script>
</body>
</html>
'''

def main():
    os.makedirs(os.path.join(OUT, 'assets', 'img'), exist_ok=True)
    for blob, (src, dst) in IMAGES.items():
        shutil.copyfile(os.path.join(ASSETS, src), os.path.join(OUT, 'assets', 'img', dst))
    shutil.copyfile(os.path.join(ASSETS, 'hoppy.svg'), os.path.join(OUT, 'assets', 'img', 'favicon.svg'))
    for name in PAGES:
        file, html = convert(name)
        open(os.path.join(OUT, file), 'w', encoding='utf8').write(html)
        print('built', file, len(html))

if __name__ == '__main__':
    main()
