#!/usr/bin/env python3
"""Pacific Dance — full-site mock generator.
Builds 8 pages into deck/site/ from locked brand decisions (meeting + Lori's feedback)
and the real content archive. Rerun after edits: python3 build.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CTA = "Book a Free Class"

NAV_ITEMS = [
    ("index.html", "Home"),
    ("classes.html", "Classes & Schedules"),
    ("about.html", "About"),
    ("performing-groups.html", "Performing Groups"),
    ("recital.html", "Recital & Events"),
    ("policies.html", "Policies & Info"),
    ("contact.html", "Contact"),
]

def head(title, desc=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Podkova:wght@400;500;600;700;800&family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css?v=10">
</head>
<body>
"""

def nav(active):
    on = ' style="color:var(--royal)"'
    items = "".join(
        f'<li><a href="{href}"{on if href == active else ""}>{label}</a></li>'
        for href, label in NAV_ITEMS[1:]
    )
    return f"""<div class="annbar">Enrollment is open — the first class is free. <a href="enroll.html">Book now →</a></div>
<header>
  <div class="wrap nav">
    <a class="logo" href="index.html"><img src="../assets/img/pd-logo.jpg" alt="Pacific Dance"></a>
    <ul>{items}</ul>
    <a class="btn btn-primary" href="enroll.html">{CTA}</a>
  </div>
</header>
"""

FOOTER = f"""<footer id="footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <img class="logo-f" src="../assets/img/pd-logo.jpg" alt="Pacific Dance">
        <p style="margin-top:16px; max-width:32ch">Pure joy in dance, confidence for life — training dancers since 1994.</p>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li>4880 Irvine Boulevard, Suite 101</li>
          <li>Irvine, CA 92620</li>
          <li><a href="tel:+17147311108">714.731.1108</a></li>
          <li><a href="mailto:info@pacificdance.net">info@pacificdance.net</a></li>
        </ul>
      </div>
      <div>
        <h4>Hours</h4>
        <ul>
          <li>Mon–Thu · 12:30 – 9:00 pm</li>
          <li>Fri · 12:30 – 8:00 pm</li>
          <li>Sat · 9:00 am – 2:00 pm</li>
          <li>Sun · 9:00 am – 1:00 pm</li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="classes.html">Classes &amp; Schedules</a></li>
          <li><a href="enroll.html">{CTA}</a></li>
          <li><a href="how-to-enroll.html">How to Enroll</a></li>
          <li><a href="performing-groups.html">Performing Groups</a></li>
          <li><a href="recital.html">Recital &amp; Events</a></li>
          <li><a href="policies.html">Policies &amp; Info</a></li>
        </ul>
      </div>
    </div>
    <div class="fine">
      <span>© 2026 Pacific Dance · Irvine, CA</span>
      <span>Website mock — for review, not live</span>
    </div>
  </div>
</footer>
</body>
</html>"""

def page_hero(eyebrow, h1, sub="", bg=None, bg_alt=""):
    p = f"<p>{sub}</p>" if sub else ""
    if bg:
        return f"""<section class="page-hero lp-hero">
  <div class="hero-bg"><img src="{bg}" alt="{bg_alt}"></div>
  <div class="wrap" style="position:relative">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    {p}
  </div>
</section>
"""
    return f"""<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    {p}
  </div>
</section>
"""

def cta_band(h="The first class is free.", p="Tell us a little about your dancer and Lori will help you find the perfect class — no commitment, no card.", href="enroll.html"):
    return f"""<section class="block dark finale">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{p}</p>
    <a class="btn" style="background:var(--sky); color:var(--navy)" href="{href}">{CTA}</a>
    <small>Takes about a minute · Lori, our Owner / Director, replies within a day or two</small>
  </div>
</section>
"""

def personal_help():
    return """<div class="help-line">
      <b>We'd love to help you personally.</b> The best fit for a dancer usually starts with a quick conversation — so we can match yours to the right class for their age, level, and needs. New students can try <b>one free class</b>, and we welcome students <b>year-round</b> (start after the first week of the month and we'll pro-rate your tuition). Call <a href="tel:+17147311108">714-731-1108</a> or email <a href="mailto:info@pacificdance.net">info@pacificdance.net</a> for class availability — we look forward to working with you!
    </div>"""

# ============================================================ CLASSES
SCHEDULE = [
    # (class, level_note, ages, styles, [(day, time), ...])
    ("Mommy & Me", "", "18 mo – 3 yrs", "combo", [("Sun","9:00 AM")]),
    ("Ballet/Tap Combo", "", "3–5", "combo ballet tap", [("Tue","4:30"),("Fri","3:30"),("Sat","9:00"),("Sat","10:00"),("Sun","9:00")]),
    ("Ballet/Lyrical Combo", "", "4–6", "combo ballet lyrical", [("Tue","4:30"),("Wed","3:30"),("Sat","10:00")]),
    ("Pre-Jazz Hop Tumble", "", "4–6", "combo jazz hiphop", [("Mon","4:30"),("Fri","4:30")]),
    ("Pre-Hip Hop", "", "5–7", "hiphop", [("Wed","3:45"),("Thu","4:00")]),
    ("Pre-Ballet", "", "5–7", "ballet", [("Mon","3:45")]),
    ("Ballet I", "", "6 & up", "ballet", [("Mon","5:00"),("Wed","4:30"),("Fri","4:30"),("Sat","10:00")]),
    ("Ballet II", "", "by level", "ballet", [("Mon","5:30"),("Tue","5:30"),("Wed","6:30"),("Sat","10:00")]),
    ("Ballet III", "", "by level", "ballet", [("Tue","4:30"),("Thu","6:30")]),
    ("Pre-Pointe", "", "by level", "ballet", [("Wed","5:30"),("Fri","5:30")]),
    ("Ballet — Beginning", "", "Adult", "ballet adult", [("Thu","8:30 PM")]),
    ("Jazz I", "", "6 & up", "jazz", [("Tue","5:30"),("Sat","9:00"),("Sun","10:00")]),
    ("Jazz/Lyrical I", "", "8 & up", "jazz lyrical", [("Tue","3:30"),("Thu","3:30")]),
    ("Jazz/Musical Theatre II", "", "by level", "jazz", [("Mon","5:00")]),
    ("Lyrical I", "", "8 & up", "lyrical", [("Mon","5:30"),("Wed","4:00")]),
    ("Lyrical — Advanced", "", "by level", "lyrical", [("Tue","7:30")]),
    ("Contemporary II", "", "10 & up", "lyrical", [("Tue","6:30"),("Sat","12:00")]),
    ("Tap I", "", "6 & up", "tap", [("Thu","5:30")]),
    ("Tap I", "", "Teen/Adult", "tap adult", [("Mon","7:30"),("Wed","1:00")]),
    ("Turns & Technique I-B/II", "", "by level", "technique", [("Wed","5:00"),("Thu","4:30"),("Sat","11:00"),("Sun","12:00")]),
    ("Hip Hop — Beginning", "", "6 & up", "hiphop", [("Wed","4:30"),("Wed","5:30"),("Thu","6:00")]),
    ("Hip Hop — Beginning", "", "10 & up", "hiphop", [("Mon","5:30"),("Tue","5:30"),("Wed","7:30")]),
    ("Hip Hop — Beginning", "", "Adult", "hiphop adult", [("Mon","6:30"),("Wed","4:30")]),
    ("Hip Hop — Advanced", "", "by level", "hiphop", [("Thu","7:00")]),
    ("K-Pop — Beginning", "", "6 & up", "kpop", [("Wed","5:30"),("Thu","4:30"),("Sat","11:00")]),
    ("K-Pop — Beginning", "", "10 & up", "kpop", [("Tue","5:30"),("Thu","7:30"),("Fri","4:30"),("Sat","1:00")]),
    ("K-Pop — Beginning", "", "Adult", "kpop adult", [("Tue","8:30 PM")]),
    ("Acro for Dance — Beginning", "", "7 & up", "acro", [("Mon","4:30"),("Tue","5:30"),("Wed","5:30"),("Thu","5:30"),("Sat","11:00")]),
    ("Acro for Dance — Advanced", "", "12 & up", "acro", [("Mon","8:00")]),
    ("Musical Theatre", "", "7 & up", "jazz", [("Sat","10:00")]),
    ("Stretch & Conditioning", "", "10 – Adult", "technique adult", [("Sat","11:00")]),
    ("Pom", "", "12 & up", "technique", [("Fri","5:30")]),
]

ACCORDION_GROUPS = [
    ("Combo Classes · Ages 2\u20137",
     "One class, two or three styles \u2014 the classic first classes.",
     ["Mommy & Me", "Ballet/Tap Combo", "Ballet/Lyrical Combo", "Pre-Jazz Hop Tumble", "Pre-Hip Hop", "Pre-Ballet"]),
    ("Ballet",
     "The foundation \u2014 through pointe.",
     ["Ballet I", "Ballet II", "Ballet III", "Pre-Pointe"]),
    ("Jazz & Musical Theatre", "",
     ["Jazz I", "Jazz/Lyrical I", "Jazz/Musical Theatre II", "Musical Theatre"]),
    ("Lyrical & Contemporary", "",
     ["Lyrical I", "Lyrical \u2014 Advanced", "Contemporary II"]),
    ("Tap", "",
     ["Tap I"]),
    ("Hip Hop", "",
     ["Hip Hop \u2014 Beginning", "Hip Hop \u2014 Advanced"]),
    ("K-Pop", 'Friday nights regularly draw 40+ dancers — <a href="https://www.instagram.com/pacificdance/" style="color:var(--royal); font-weight:600">see them on Instagram</a>.',
     ["K-Pop \u2014 Beginning"]),
    ("Acro", "",
     ["Acro for Dance \u2014 Beginning", "Acro for Dance \u2014 Advanced"]),
    ("Technique & Conditioning", "",
     ["Turns & Technique I-B/II", "Stretch & Conditioning", "Pom"]),
    ("Adult Classes · to age 92",
     "Beginners genuinely welcome.",
     ["ADULT_ONLY"]),
]

def classes_page():
    def rows_for(names, adult_only=False):
        out = ""
        for name, lvl, ages, styles, times in SCHEDULE:
            if adult_only:
                if "adult" not in styles.split():
                    continue
            elif name not in names:
                continue
            tstr = " \u00b7 ".join(f"{d} {t}" for d, t in times)
            out += (f'<div class="srow"><div><b>{name}</b>'
                    f'<span class="sages"> \u00b7 Ages {ages}</span></div>'
                    f'<div class="stimes">{tstr}</div></div>\n')
        return out
    slugs = ["combo", "ballet", "jazz", "contemporary", "tap", "hip-hop",
             "k-pop", "acro", "technique", "adult"]
    accs = ""
    for i, (title, sub, names) in enumerate(ACCORDION_GROUPS):
        adult_only = names == ["ADULT_ONLY"]
        subline = f'<p style="color:var(--slate); font-size:.88rem; margin-bottom:12px">{sub}</p>' if sub else ""
        accs += (f'<details class="acc" id="{slugs[i]}"{" open" if i == 0 else ""}><summary>{title}</summary>'
                 f'<div class="inner">{subline}{rows_for(names, adult_only)}</div></details>\n')
    return head("Classes & Schedules \u2014 Pacific Dance, Irvine", "Dance classes for ages 2\u201392 in Irvine, CA \u2014 browse the schedule by style.") + nav("classes.html") + """
<div class="wrap" style="max-width:880px"><div class="opt-switch">Reviewing <b>two schedule options</b> \u2014 this is <b>Option 1: browse-by-style</b>. <a href="classes-doc.html">See Option 2: uploaded document (PDF) \u2192</a></div></div>
""" + page_hero(
        "Classes & Schedules",
        "Find the right class",
        "Eight styles, every level, seven days a week \u2014 open a style to see its classes and times. Ages 2\u201392, all ability levels and interests welcome.",
    ) + f"""
<section class="block">
  <div class="wrap" style="max-width:880px">
    <div class="sample-note"><b>Mock note:</b> a representative sample (about a third of the schedule). At launch, every style below lists all of its classes from the July 2026 schedule \u2014 and the studio can update times right in Squarespace, no code.</div>
    {accs}
    <div class="pull-review" style="margin-top:26px">"All the teachers here are so welcoming and friendly… My child dances here and I also take adult ballet here and love it!"<span>— Daphne · via Yelp · parent &amp; adult student</span></div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap twocol">
    <div class="card-p">
      <h3>Make-up classes</h3>
      <p style="margin-top:10px">Missed a class? Request a courtesy make-up in a comparable class \u2014 within one month of the absence, requested at least 48 hours ahead via the make-up form. Confirmation comes by email.</p>
      <ul>
        <li>You must be currently enrolled; make-ups are non-transferable</li>
        <li>Not every class is open for make-ups (size, age &amp; level fit)</li>
        <li>90-minute classes use two make-ups unless you're enrolled in one</li>
      </ul>
      <p style="margin-top:12px"><a href="policies.html" style="color:var(--royal); font-weight:600">Full make-up policy \u2192</a></p>
    </div>
    <div class="card-p">
      <h3>New classes</h3>
      <p style="margin-top:10px">Recently added to the schedule:</p>
      <ul>
        <li><b>K-Pop for Beginners</b> \u2014 new sections for ages 6+, 8+, and 10+ across the week</li>
        <li><b>Beginning Adult K-Pop</b> \u2014 Tuesdays 8:30 pm</li>
      </ul>
      <p style="margin-top:12px">New classes are announced here and in the studio each season.</p>
    </div>
  </div>
</section>
""" + cta_band("Not sure which class fits?", "Tell us your dancer's age and interests \u2014 Lori will point you to the right class, and the first one is free.") + FOOTER

# ============================================================ ENROLL
def enroll_page():
    styles_opts = "".join(f"<option>{s}</option>" for s in
        ["Not sure yet — help us pick", "Combo classes (ages 2–7)", "Ballet", "Jazz", "Lyrical / Contemporary", "Tap", "Hip Hop", "K-Pop", "Acro", "Musical Theatre", "Adult classes"])
    return head("Book a Free Class — Pacific Dance, Irvine", "The first class is free. Tell us about your dancer and Lori will help you find the perfect class.") + nav("enroll.html") + page_hero(
        "Free Class & Enrollment",
        "The first class is free",
        "That's usually all it takes. Tell us a little about your dancer, and Lori will personally help you find the right class — no commitment, no card.",
        bg="../assets/img/ba-studio-after.jpg", bg_alt="Inside one of Pacific Dance's ten studios",
    ) + """
<section class="block" style="padding-bottom:0">
  <div class="wrap" style="max-width:760px">""" + personal_help() + """
    <p style="text-align:center; margin-top:16px; font-size:.92rem; color:var(--slate)">Already know you want to enroll? <a href="how-to-enroll.html" style="color:var(--royal); font-weight:600">Skip straight to registration &amp; the waiver &rarr;</a></p>
  </div>
</section>
""" + f"""
<section class="block">
  <div class="wrap twocol form-first">
    <div>
      <div class="eyebrow">How it works</div>
      <h2 style="font-size:2rem; margin-top:10px">Three steps, one happy dancer</h2>
      <div style="margin-top:24px; display:flex; flex-direction:column; gap:18px">
        <div class="card-p"><h3>1 · Tell us about your dancer</h3><p style="margin-top:6px">The short form here — about a minute.</p></div>
        <div class="card-p"><h3>2 · Lori replies — within a day or two</h3><p style="margin-top:6px">Your form goes to Lori, our Owner / Director, who personally matches every dancer to the right class — age, level, and interest. She's placed thousands of students, and it's the thing families thank us for most.</p></div>
        <div class="card-p"><h3>3 · Come dance — free</h3><p style="margin-top:6px">Try the class. A quick waiver is required before your dancer takes the floor — we'll send it once your class is booked, so there's nothing to fill out up front. Love it? <a href="how-to-enroll.html" style="color:var(--royal); font-weight:600">Complete your registration →</a></p></div>
      </div>
    </div>
    <div>
      <div class="formcard" id="bookform">
        <h3 style="font-size:1.4rem">{CTA}</h3>
        <form onsubmit="event.preventDefault(); window.location.href='thank-you.html';">
          <label>Student's name</label><input required placeholder="Dancer's first &amp; last name">
          <label>Parent / guardian name</label><input required placeholder="Your name">
          <label>Email</label><input type="email" required placeholder="you@email.com">
          <label>Student's age</label><input required placeholder="e.g. 6">
          <label>Dance style interest</label><select>{styles_opts}</select>
          <label>How did you hear about us? <span style="font-weight:400; color:var(--slate)">(optional)</span></label><select><option></option><option>Google</option><option>Instagram / Facebook</option><option>TikTok</option><option>A friend or family</option><option>Drove by the studio</option><option>Other</option></select>
          <button class="btn btn-primary" type="submit">{CTA}</button>
          <p class="form-note">No card, no commitment — takes about a minute.</p>
          <div class="lori-promise">
            <img src="../assets/img/instr-lori.jpg" alt="Lori Murphy, Owner / Director of Pacific Dance">
            <p><b>Your form goes straight to Lori, our Owner / Director — she replies within a day or two, usually sooner.</b> She's matched thousands of dancers to the right class over thirty years, and families tell us she's the friendliest part of getting started.</p>
          </div>
        </form>
      </div>
      <div class="pull-review">"We mainly started because my daughter was so shy… Performing in front of hundreds of people would've terrified me as a child, but she has embraced it."<span>— Jen · via Yelp</span></div>
    </div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">Tuition</div>
      <h2>Simple monthly tuition</h2>
      <p>Billed monthly via Auto Pay. The more classes per week, the less each one costs.</p>
    </div>
    <div class="twocol">
      <div class="card-p">
        <div class="feehead">Monthly tuition · effective Jan 1, 2026</div>
        <p class="feeline"><b>1 class per week</b> — $95/mo</p>
        <p class="feeline"><b>2 classes per week</b> — $180/mo</p>
        <p class="feeline"><b>3 classes per week</b> — $230/mo</p>
        <p class="feeline"><b>4 classes per week</b> — $280/mo</p>
        <p class="feeline"><b>5 classes per week</b> — $310/mo</p>
        <p class="feeline"><b>6 classes per week</b> — $335/mo</p>
        <p class="feeline"><b>7 classes per week</b> — $360/mo</p>
        <p class="feeline"><b>8 classes per week</b> — $385/mo</p>
        <p class="feeline"><b>Each additional class</b> — +$25/mo</p>
      </div>
      <div class="card-p">
        <div class="feehead">Other rates</div>
        <p class="feeline"><b>Registration fee (annual)</b> — $35</p>
        <p class="feeline"><b>Single class</b> — $35</p>
        <p class="feeline"><b>Mommy &amp; Me card, 5 classes</b> — $75</p>
        <p class="feeline"><b>Teen/Adult card, 5 classes</b> — $135</p>
        <p class="feeline"><b>Teen/Adult card, 11 classes</b> — $270</p>
        <p style="margin-top:16px; font-size:.85rem; color:var(--slate)">Tuition runs on Auto Pay (charged around the 1st). Class cards expire 60 days from purchase. Performing Group &amp; competition fees are shared with current PG families on the <a href="performing-groups.html" style="color:var(--royal); font-weight:600">password-protected page</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap" style="max-width:820px">
    <div class="head-c">
      <div class="eyebrow">Good to know</div>
      <h2>What parents usually ask</h2>
    </div>
    <details class="acc" open><summary>How big are the classes?</summary><div class="inner"><p>Capped small on purpose — around 12 for our littlest dancers and about 15 for ages 4–6 — so every dancer gets individual corrections and is known by name.</p></div></details>
    <details class="acc"><summary>What does it cost?</summary><div class="inner"><p>$35 registration, then monthly tuition from $95 for one class per week (see the tables above — more classes per week cost less each). Auto Pay, no statements, no surprises.</p></div></details>
    <details class="acc"><summary>What if we miss a class?</summary><div class="inner"><p>You have 30 days to take a make-up in a comparable class — request it via the make-up form at least 48 hours ahead.</p></div></details>
    <details class="acc"><summary>Can I watch my dancer's class?</summary><div class="inner"><p>Yes — viewing windows on the studios, and a comfortable parent waiting area where siblings do homework between classes.</p></div></details>
    <details class="acc"><summary>Do you take beginners? Adults?</summary><div class="inner"><p>Always. Every ability level and interest, ages 2 to 92 — from first-ever classes to adult beginners who've meant to do this for years.</p></div></details>
    <details class="acc"><summary>When can we start?</summary><div class="inner"><p>Anytime — classes run year-round and enrollment is always open. Book the free class and you're in this week.</p></div></details>
  </div>
</section>
""" + """<section class="block dark">
  <div class="wrap" style="max-width:620px; text-align:center">
    <div class="eyebrow">Questions first?</div>
    <h2 style="font-size:clamp(1.8rem,4vw,2.4rem); margin-top:10px">Not ready to book? Just ask.</h2>
    <p style="margin-top:12px; color:rgba(255,255,255,.82)">Send a note and a real person answers — usually Lori. Or call <a href="tel:+17147311108" style="color:var(--sky); font-weight:600">714.731.1108</a>.</p>
    <div class="formcard" style="text-align:left; margin-top:30px">
      <form onsubmit="event.preventDefault(); this.innerHTML='<p style=\\'text-align:center; padding:30px 0; font-weight:600\\'>Thanks — we\\'ll get back to you shortly!</p>';">
        <label>Your name</label><input required>
        <label>Email</label><input type="email" required>
        <label>Your question</label><textarea rows="4" required placeholder="Ask us anything — schedules, ages, what to wear…"></textarea>
        <button class="btn btn-primary" type="submit">Send message</button>
      </form>
    </div>
  </div>
</section>
""" + FOOTER

# ============================================================ ABOUT
def about_page():
    instructors = json.load(open(os.path.join(HERE, 'instructors.json')))
    cards = ""
    for idx, ins in enumerate(instructors):
        name = ins['name'].split(' - ')[0]
        role = "Owner / Director" if "Owner" in ins['name'] else "Instructor"
        photo = ins.get('photo')
        if photo:
            ph = f'<img src="../{photo}" alt="{name}">'
        else:
            initials = "".join(w[0] for w in name.split()[:2])
            ph = f'<div class="mono">{initials}</div>'
        paras = ins['paras'] or ["Bio coming soon."]
        limit = len(paras) if role == "Owner / Director" else 2
        full = "".join(f"<p>{p}</p>" for p in paras[:limit])
        flip = " flip" if idx % 2 else ""
        cards += f"""<div class="instr-row{flip}"><div class="iph">{ph}</div><div><h3>{name}</h3><div class="irole">{role}</div>{full}</div></div>\n"""
    return head("About — Pacific Dance, Irvine", "Training dancers since 1994. Meet the instructors behind Irvine's home for dance.") + nav("about.html") + page_hero(
        "About Pacific Dance",
        "Training dancers since 1994",
        "Family-run by Tim & Lori — in a studio that has been part of Irvine since 1985.",
    ) + f"""
<section class="block">
  <div class="wrap twocol">
    <div>
      <div class="eyebrow">Our story</div>
      <h2 style="font-size:2.1rem; margin-top:10px">Joy first. Training always.</h2>
      <p style="margin-top:16px; color:#24405e">Lori started teaching at the Irvine School of Dance in 1985, and in 1994 she and Tim made it their own. Three decades later, Pacific Dance is the largest studio in the area — 18,000 square feet, ten studios with raised floors — and still runs like the family business it is.</p>
      <p style="margin-top:12px; color:#24405e">Our goal has never changed: professional training that's safe and individualized for every level of student, in a place kids genuinely love to be. Whether your dancer is training toward a career, keeping fit, or just having fun, they belong here — every ability level and interest, ages 2 to 92.</p>
      <p style="margin-top:12px; color:#24405e">Our teachers come from professional backgrounds across ballet companies, film, TV, music videos, universities, and the stage — and we regularly host master classes from industry professionals. Around Irvine, most families just call it "Pacific."</p>
      <div class="pull-review" style="margin-top:20px">"I have been at Pacific Dance for almost all my life and it is like a second home to me… such a positive and happy environment."<span>— Kerry · via Yelp · PD dancer</span></div>
    </div>
    <div>
      <img src="../assets/img/ba-studio-after.jpg" alt="Inside one of Pacific Dance's ten studios" style="border-radius:10px">
      <div class="card-p" style="margin-top:16px">
        <h3>Where our dancers go</h3>
        <p style="margin-top:8px">Many Pacific Dance students go on to lifelong careers in dance — teaching, performing professionally, and dancing on Broadway, in film &amp; TV, and with professional companies.</p>
      </div>
      <div class="card-p" style="margin-top:16px">
        <h3>Recent recognition</h3>
        <ul style="margin-top:8px">
          <li><b>Studio of the Year 2026</b> — KAR Nationals</li>
          <li>Primary Studio of Excellence 2026 — KAR Regionals</li>
          <li>Outstanding Studio Award 2026 — Activ8</li>
          <li>People's Choice nominee 2026 — Industry Dance Awards</li>
          <li>Studio of Excellence 2025 — Energy Nationals</li>
          <li>Scholarship winner &amp; Dancer of the Year finalist 2025 — Hollywood Vibe</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">The space</div>
      <h2>Tour the studio</h2>
      <p>Ten studios, a glass observation hallway with a downtown-storefront feel, and a parent waiting area built for real life.</p>
    </div>
    <div class="facgrid cols2">
      <figure><img src="../assets/img/ba-studio-after.jpg" alt="Inside one of ten studios"><figcaption>One of ten studios — raised floors, pro sound</figcaption></figure>
      <figure><img src="../assets/img/bts-studio.jpg" alt="A photo shoot inside a Pacific Dance studio"><figcaption>Studios doubling as shoot spaces</figcaption></figure>
      <figure><img src="../assets/img/ba-ediface-after.jpg" alt="The Pacific Dance building"><figcaption>The Northwood Town Center storefront</figcaption></figure>
      <figure><img src="../assets/img/ba-trophy-after.jpg" alt="The trophy wall"><figcaption>The trophy wall, by the front desk</figcaption></figure>
    </div>
    <div class="sample-note" style="margin-top:18px"><b>Mock note:</b> Tim's full studio shoot (all ten studios, the hallway, the observation windows) drops in here when it lands.</div>
  </div>
</section>

<section class="block mist-bg" id="instructors">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">The people</div>
      <h2>Meet the instructors</h2>
      <p>Working professionals from the Orange County and Los Angeles dance worlds — who know every dancer by name.</p>
    </div>
    <div class="instr-list">
{cards}    </div>
  </div>
</section>
""" + cta_band("Come meet us in person.", "The first class is free — and the viewing windows mean you see every minute of it.") + FOOTER

# ============================================================ PERFORMING GROUPS
def pg_page():
    return head("Performing Groups & Competition — Pacific Dance", "Audition-based performing groups from Mini Mini through PD Elite — competition teams with heart.") + nav("performing-groups.html") + page_hero(
        "Performing Groups & Competition",
        "Serious training, with heart.",
        "Our audition-based Performing Groups compete across Southern California — and win a lot. But the focus is never on winning: it's kids doing their best, together.",
    ) + f"""
<section class="block" style="padding-bottom:0">
  <div class="wrap">
    <img src="../assets/img/silk-blue.jpg" alt="A Pacific Dance performing group" style="width:100%; max-height:460px; object-fit:cover; border-radius:var(--radius)">
    <div class="sample-note" style="margin-top:12px"><b>Mock note:</b> placeholder image — swap in a photo of your current Performing Groups here.</div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">The groups</div>
      <h2>A team for every stage</h2>
    </div>
    <div class="stygrid">
      <div class="sty"><h3>Mini Mini PG</h3><p>The youngest performers get their first taste of the team — and the stage.</p><span class="age">Youngest dancers</span></div>
      <div class="sty"><h3>Mini Dance PG</h3><p>Dance foundations, performance polish.</p><span class="age">Ages 6 &amp; up</span></div>
      <div class="sty"><h3>Hip Hop &amp; Tap PGs</h3><p>Style-specific crews for dancers who've found their lane.</p><span class="age">All ages</span></div>
      <div class="sty"><h3>PD Elite</h3><p>Our pre-professional company and most committed track — home to our newest competitors through our most advanced dancers.</p></div>
    </div>
    <div class="twocol" style="margin-top:44px">
      <div class="card-p">
        <h3>How to join</h3>
        <ul style="margin-top:10px">
          <li><b>PG Parent Meeting</b> — each spring (2026–27 season: April 28)</li>
          <li><b>Application due mid-May</b> — dancer info, availability, and group commitments</li>
          <li>Placement follows — by submitting, you commit to all groups your dancer is chosen for</li>
        </ul>
      </div>
      <div class="card-p">
        <h3>Solos, duets &amp; trios</h3>
        <p style="margin-top:10px">Private dances are earned by commitment level — from one private for Mini Mini or Hip Hop-only dancers (with four weekly classes), up to unlimited privates for dancers committed to three or more groups. Full guidelines come with the application.</p>
      </div>
    </div>
    <div class="pull-review" style="margin-top:30px">"The teachers are top notch, technique comes first… the focus is never on winning — it's about the kids doing their best and having fun."<span>— Becky · via Google</span></div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap">
    <div class="gate">
      <div class="lock">🔒</div>
      <h3>Current PG Families</h3>
      <p>Competition schedules, fees, and group logistics live behind this password — so current families always have them handy, and they stay off the public internet.</p>
      <div class="row">
        <a class="btn" href="pg-family.html">Enter the PG Family page →</a>
      </div>
      <p style="font-size:.78rem; opacity:.7; margin-top:14px">Opens Squarespace's built-in password screen — the password changes each season.</p>
    </div>
  </div>
</section>
""" + cta_band("New to Pacific Dance?", "Every PG dancer started with a first class. Book one free and see where it goes.") + FOOTER

# ============================================================ RECITAL & EVENTS
def recital_page():
    return head("Recital & Events — Pacific Dance", "The annual recital at the Irvine Barclay Theater, summer workshops, and studio events.") + nav("recital.html") + page_hero(
        "Recital & Events",
        "Every dancer gets the big stage",
        "From the three-year-olds to the seniors — every June, every dancer performs at the Irvine Barclay Theater.",
    ) + f"""
<section class="block">
  <div class="wrap twocol">
    <div>
      <div class="eyebrow">Annual recital</div>
      <h2 style="font-size:2.1rem; margin-top:10px">Recital 2027 · June 7–11</h2>
      <p style="margin-top:16px; color:#24405e">A professional theater, real costumes, and a moment on stage for every single dancer — it's a lot of fun, and the highlight of the year. Participation is optional but beloved: good class attendance, the assigned costume, and the scheduled rehearsals are all it takes to have a great experience.</p>
      <div class="sample-note" style="margin-top:18px"><b>Swappable by design:</b> this section updates each season (2026 → 2027 → …) without rebuilding the page — same for the program, senior shout-outs, and schedules.</div>
    </div>
    <img src="../assets/img/scorpion-black.jpg" alt="A Pacific Dance student performing on stage" style="border-radius:10px">
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap twocol">
    <div>
      <div class="eyebrow">Also this season</div>
      <h2 style="font-size:2.1rem; margin-top:10px">In-Studio Holiday Performance · December 14, 2026</h2>
      <p style="margin-top:16px; color:#24405e">A warm in-studio holiday performance for family and friends — the first &ldquo;stage&rdquo; of the year, where every class gets a turn to shine. It's a lot of fun, and it gets dancers excited for recital season ahead.</p>
    </div>
    <img src="../assets/img/minis-barre.jpg" alt="Young Pacific Dance students at the barre" style="border-radius:10px">
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">Summer 2026</div>
      <h2>Workshops &amp; intensives</h2>
    </div>
    <div class="twocol">
      <div class="card-p">
        <h3>Summer Dance Party · Ages 4–6</h3>
        <ul style="margin-top:10px">
          <li>June 22–26 and August 3–7 · 9:30 am – 12:30 pm</li>
          <li>Jazz, lyrical, tumbling, hip hop, games &amp; crafts — a new summer theme daily</li>
          <li>$250 one week · $450 both weeks (or two siblings)</li>
        </ul>
      </div>
      <div class="card-p">
        <h3>Summer Workshops · Ages 7–12</h3>
        <ul style="margin-top:10px">
          <li>June 22–26 and August 3–7 · 9:00 am – 2:00 pm</li>
          <li>Full days of technique, styles, and performance</li>
          <li>$350 one week · $650 both weeks (or two siblings)</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">Plan around us</div>
      <h2>Holiday closures · 2026</h2>
    </div>
    <div class="card-p" style="max-width:640px; margin:0 auto">
      <ul>
        <li>Easter — Sunday, April 5</li>
        <li>Memorial Day — May 23–25</li>
        <li>Recital week — June 8–12</li>
        <li>Summer break — June 30 – July 6</li>
        <li>Labor Day — September 5–7</li>
        <li>Thanksgiving — November 26–29</li>
        <li>Winter break — December 21 – January 3</li>
      </ul>
      <p style="margin-top:12px; font-size:.85rem; color:var(--slate)">Applies to Pacific Dance and Pacific Dancewear. Tuition is monthly regardless of holidays — see <a href="policies.html" style="color:var(--royal); font-weight:600">policies</a>.</p>
    </div>
  </div>
</section>
""" + cta_band("Want to see a recital dancer up close?", "Start with a free class — recital season takes care of the rest.") + FOOTER

# ============================================================ POLICIES & INFO
def policies_page():
    return head("Policies & Info — Pacific Dance", "School policies, dance attire, Pacific Dancewear, and directions.") + nav("policies.html") + page_hero(
        "Policies & Info",
        "The practical stuff, in one place",
        "Policies, attire, the dancewear store, and how to find us.",
    ) + f"""
<section class="block">
  <div class="wrap" style="max-width:720px; text-align:center">
    <div class="eyebrow">School policies</div>
    <h2 style="font-size:clamp(1.8rem,4vw,2.4rem); margin-top:10px">The full policies, always current</h2>
    <p style="margin-top:14px; color:var(--slate)">Our complete studio policies and required dance attire are built right into the registration form — so what you read is always the current version, straight from the studio.</p>
    <p style="margin-top:24px"><a class="btn btn-primary" href="how-to-enroll.html">Read the full policies &rarr;</a></p>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap twocol">
    <div class="card-p">
      <h3>Pacific Dancewear — in the building</h3>
      <p style="margin-top:10px">Our full-service dancewear store at the rear entrance carries Capezio, Bloch, BunHeads, Mirella and more — with <b>20% off everything</b> for registered Pacific Dance students (plus high school &amp; college dance students). All sales final.</p>
      <ul style="margin-top:10px">
        <li>Mon–Fri · 12:30 – 6:00 pm</li>
        <li>Sat · 9:30 am – 12:30 pm · Sun · 9:30 am – 1:00 pm</li>
      </ul>
    </div>
    <div class="card-p">
      <h3>Directions &amp; parking</h3>
      <p style="margin-top:10px"><b>4880 Irvine Boulevard, Suite 101, Irvine, CA 92620</b> — in the retail center at Irvine Blvd &amp; Pueblo Norte, with plenty of parking.</p>
      <ul style="margin-top:10px">
        <li>From the 5 South: exit Culver, north (left), right on Irvine Blvd, right on Pueblo Norte</li>
        <li>From the 5 North: exit Jeffrey, north (right), left on Irvine Blvd, left on Pueblo Norte</li>
      </ul>
      <p style="margin-top:12px"><a href="https://goo.gl/maps/71tf8LPYSMy" style="color:var(--royal); font-weight:600">Open in Google Maps →</a></p>
    </div>
  </div>
</section>
""" + cta_band() + FOOTER

# ============================================================ CONTACT
def contact_page():
    return head("Contact — Pacific Dance, Irvine", "Call, email, or visit Pacific Dance — 4880 Irvine Blvd, Irvine, CA.") + nav("contact.html") + page_hero(
        "Contact",
        "A real person answers",
        "Questions about classes, enrollment, or anything else — reach out however you like.",
    ) + f"""
<section class="block">
  <div class="wrap twocol">
    <div class="formcard" id="cform">
      <h3 style="font-size:1.4rem">Send us a message</h3>
      <form onsubmit="event.preventDefault(); this.innerHTML='<p style=\\'text-align:center; padding:30px 0; font-weight:600\\'>Thanks — we\\'ll get back to you shortly!</p>';">
        <label>Your name</label><input required>
        <label>Email</label><input type="email" required>
        <label>Message</label><textarea rows="5" required placeholder="How can we help?"></textarea>
        <button class="btn btn-primary" type="submit">Send message</button>
        <p class="form-note">Looking to try a class? The fastest path is <a href="enroll.html" style="color:var(--royal); font-weight:600">booking a free class</a>.</p>
      </form>
    </div>
    <div>
      <div class="card-p">
        <h3>Reach us</h3>
        <ul style="margin-top:10px; list-style:none; margin-left:0">
          <li style="margin-bottom:8px">📞 <a href="tel:+17147311108" style="font-weight:600; color:var(--royal)">714.731.1108</a></li>
          <li style="margin-bottom:8px">✉️ <a href="mailto:info@pacificdance.net" style="font-weight:600; color:var(--royal)">info@pacificdance.net</a></li>
          <li style="margin-bottom:8px">📍 4880 Irvine Boulevard, Suite 101 · Irvine, CA 92620</li>
          <li>🕐 Mon–Thu 12:30–9 pm · Fri 12:30–8 pm · Sat 9 am–2 pm · Sun 9 am–1 pm</li>
        </ul>
      </div>
      <div class="card-p" style="margin-top:16px">
        <h3>Social &amp; media</h3>
        <p style="margin-top:10px">Follow along: <a href="https://www.instagram.com/pacificdance/" style="color:var(--royal); font-weight:600">Instagram</a> · <a href="https://www.facebook.com/PacificDanceIrvine/" style="color:var(--royal); font-weight:600">Facebook</a></p>
        <p style="margin-top:10px; font-size:.9rem">Have a great photo or video from class or recital? Send it in — we love featuring our dancers. Media inquiries: <a href="mailto:PacificDance1@gmail.com" style="color:var(--royal); font-weight:600">PacificDance1@gmail.com</a></p>
      </div>
      <div class="card-p" style="margin-top:16px; padding:0; overflow:hidden">
        <iframe title="Map to Pacific Dance" src="https://www.google.com/maps?q=4880+Irvine+Blvd+Suite+101,+Irvine,+CA+92620&output=embed" width="100%" height="240" style="border:0; display:block"></iframe>
      </div>
    </div>
  </div>
</section>
""" + cta_band() + FOOTER

# ============================================================ HOMEPAGE
# Canonical homepage source lives in _home_src.html — edit THAT file (or the
# other page functions above) and rerun build.py. Never read ../homepage.html
# (it is a redirect stub).
def homepage():
    return open(os.path.join(HERE, '_home_src.html')).read()



# ============================================================ FREE CLASS LANDING (Meta ads)
def landing_page():
    styles_opts = "".join(f"<option>{s}</option>" for s in
        ["Not sure yet — help us pick", "Combo classes (ages 2–7)", "Ballet", "Jazz", "Lyrical / Contemporary", "Tap", "Hip Hop", "K-Pop", "Acro", "Musical Theatre", "Adult classes"])
    return head("Free Dance Class in Irvine — Pacific Dance", "Ballet, jazz, hip hop, K-Pop & more for ages 2–92. The first class is free — no card, no commitment.") + nav("enroll.html") + f"""
<section class="page-hero lp-hero" style="padding-bottom:52px">
  <div class="hero-bg"><img src="../assets/img/ba-studio-after.jpg" alt="Inside one of Pacific Dance's ten studios"></div>
  <div class="wrap" style="position:relative">
    <div class="eyebrow">Irvine · ages 2–92</div>
    <h1>Your dancer's first class is free</h1>
    <p>Ballet, jazz, hip hop, K-Pop and more — taught by working professionals at the largest studio in the area. No card, no commitment.</p>
    <p style="margin-top:14px; color:var(--sky); font-weight:600; font-size:.95rem">★ 4.5 on Google · Irvine families since 1994</p>
    <p style="margin-top:10px; font-size:.92rem; color:rgba(255,255,255,.85)">📍 Northwood Town Center · 4880 Irvine Blvd, Suite 101, Irvine</p>
  </div>
</section>

<section class="block" style="padding-top:56px">
  <div class="wrap twocol">
    <div>
      <div class="formcard" id="bookform">
        <h3 style="font-size:1.4rem">{CTA}</h3>
        <form onsubmit="event.preventDefault(); window.location.href='thank-you.html';">
          <label>Student's name</label><input required placeholder="Dancer's first &amp; last name">
          <label>Parent / guardian name</label><input required placeholder="Your name">
          <label>Email</label><input type="email" required placeholder="you@email.com">
          <label>Student's age</label><input required placeholder="e.g. 6">
          <label>Dance style interest</label><select>{styles_opts}</select>
          <label>How did you hear about us? <span style="font-weight:400; color:var(--slate)">(optional)</span></label><select><option></option><option>Google</option><option>Instagram / Facebook</option><option>TikTok</option><option>A friend or family</option><option>Drove by the studio</option><option>Other</option></select>
          <button class="btn btn-primary" type="submit">{CTA}</button>
          <p class="form-note">No card, no commitment — takes about a minute.</p>
          <div class="lori-promise">
            <img src="../assets/img/instr-lori.jpg" alt="Lori Murphy, Owner / Director of Pacific Dance">
            <p><b>Your form goes straight to Lori, our Owner / Director — she replies within a day or two, usually sooner.</b> She's matched thousands of dancers to the right class over thirty years, and families tell us she's the friendliest part of getting started.</p>
          </div>
        </form>
      </div>
    </div>
    <div>
      <div class="card-p"><h3>Small classes, always</h3><p style="margin-top:6px">Capped at 12–15 dancers in the young groups — every kid is seen, corrected, and known by name.</p></div>
      <div class="card-p" style="margin-top:14px"><h3>The right-class promise</h3><p style="margin-top:6px">Lori, our Owner / Director, personally matches every dancer to the right class by age, level, and interest — she's placed thousands of dancers, and she replies within a day or two.</p></div>
      <div class="card-p" style="margin-top:14px"><h3>Watch every minute</h3><p style="margin-top:6px">Viewing windows on the studios and a comfortable parent waiting area — homework happens between classes.</p></div>
      <div class="card-p" style="margin-top:14px"><h3>Come see it first</h3><p style="margin-top:6px"><b>4880 Irvine Boulevard, Suite 101, Irvine, CA 92620</b> — in the Northwood Town Center, with easy parking. Open seven days. <a href="https://goo.gl/maps/71tf8LPYSMy" target="_blank" rel="noopener" style="color:var(--royal); font-weight:600">Get directions →</a></p></div>
      <div class="pull-review" style="margin-top:20px">"The focus is never on winning — it's about the kids doing their best and having fun."<span>— Becky · via Google</span></div>
    </div>
  </div>
</section>

<div class="trust">
  <div class="wrap row">
    <div class="t"><b>1994</b><span>training dancers since</span></div>
    <div class="t"><b>Studio of the Year</b><span>KAR Nationals 2026</span></div>
    <div class="t"><b>10 studios</b><span>18,000 square feet</span></div>
    <div class="t"><b>7 days</b><span>of classes, every week</span></div>
    <div class="t"><b>2–92</b><span>ages, every level</span></div>
  </div>
</div>

<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">The studio</div>
      <h2>The largest studio in the area — built for families</h2>
      <p>Ten studios in Irvine's Northwood Town Center, with viewing windows, a parent waiting area, and plenty of parking.</p>
    </div>
    <div class="facgrid">
      <figure><img src="../assets/img/ba-ediface-after.jpg" alt="The Pacific Dance building"><figcaption>4880 Irvine Blvd — easy drop-off</figcaption></figure>
      <figure><img src="../assets/img/ba-studio-after.jpg" alt="Inside one of ten studios"><figcaption>One of ten studios — raised floors, pro sound</figcaption></figure>
      <figure><img src="../assets/img/ba-trophy-after.jpg" alt="The trophy wall"><figcaption>Four decades of hardware by the front desk</figcaption></figure>
    </div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap">
    <div class="head-c" style="margin-bottom:30px">
      <div class="eyebrow">In their words</div>
      <h2>Irvine families keep saying the same thing</h2>
    </div>
    <div class="car">
      <div class="rev">
        <div class="stars">★★★★★</div>
        <blockquote>"Our family has been with Pacific Dance for the past 12 years… This studio is truly my daughter's second home and there's nowhere else we'd rather be."</blockquote>
        <div class="who"><b>Heidi</b> · via Yelp</div>
      </div>
      <div class="rev">
        <div class="stars">★★★★★</div>
        <blockquote>"We mainly started because my daughter was so shy… Performing in front of hundreds of people would've terrified me as a child, but she has embraced it."</blockquote>
        <div class="who"><b>Jen</b> · via Yelp</div>
      </div>
      <div class="rev">
        <div class="stars">★★★★★</div>
        <blockquote>"All the teachers here are so welcoming and friendly… My child dances here and I also take adult ballet here and love it!"</blockquote>
        <div class="who"><b>Daphne</b> · via Yelp</div>
      </div>
    </div>
    <p style="text-align:center; margin-top:22px; font-size:.85rem; color:var(--slate)">4.5★ on Google · 59 reviews on Yelp</p>
  </div>
</section>

<section class="block">
  <div class="wrap" style="max-width:820px">
    <div class="head-c" style="margin-bottom:24px"><h2 style="font-size:1.7rem">Quick answers</h2></div>
    <details class="acc" open><summary>Is it really free?</summary><div class="inner"><p>Yes — the first class is free, with no card and no commitment. Kids usually fall in love with the teacher; that's the whole plan.</p></div></details>
    <details class="acc"><summary>What does it cost if we continue?</summary><div class="inner"><p>$35 registration, then simple monthly tuition from $95 for one class a week — the more classes, the less each costs. <a href="enroll.html" style="color:var(--royal); font-weight:600">Full tuition table →</a></p></div></details>
    <details class="acc"><summary>What ages do you take?</summary><div class="inner"><p>2 to 92. Mommy &amp; Me through adult classes, every ability level and interest.</p></div></details>
    <details class="acc"><summary>When are classes?</summary><div class="inner"><p>Seven days a week, across eight styles — Lori will point you to the exact times that fit your schedule. <a href="classes.html" style="color:var(--royal); font-weight:600">Browse the schedule →</a></p></div></details>
    <details class="acc"><summary>Who teaches?</summary><div class="inner"><p>Working professionals from the Orange County and LA dance worlds, led by Owner / Director Lori Murphy (Masters of Fine Arts in Dance, UC Irvine) — plus master classes from industry professionals. <a href="about.html" style="color:var(--royal); font-weight:600">Meet the instructors →</a></p></div></details>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap">
    <div class="head-c" style="margin-bottom:30px">
      <div class="eyebrow">Still browsing?</div>
      <h2>Take the full tour</h2>
    </div>
    <div class="stygrid">
      <a class="sty" href="classes.html"><h3>Classes &amp; Schedules</h3><p>Eight styles, seven days a week — browse by style.</p></a>
      <a class="sty" href="about.html"><h3>Meet the Studio</h3><p>Our story, the space, and all 22 instructors.</p></a>
      <a class="sty" href="performing-groups.html"><h3>Performing Groups</h3><p>Competition teams, from Mini Mini to PD Elite.</p></a>
      <a class="sty" href="index.html"><h3>Homepage</h3><p>The whole picture, starting from the top.</p></a>
    </div>
  </div>
</section>
""" + cta_band("Ready when you are.", "One-minute form, free first class, and Lori takes it from there.", href="#bookform") + FOOTER

# ============================================================ THANK YOU
def thankyou_page():
    return head("You're in — Pacific Dance", "Thanks! Lori will follow up shortly to find the perfect class.") + nav("enroll.html") + """
<section class="block" style="min-height:60vh; display:flex; align-items:center">
  <div class="wrap" style="max-width:640px">
    <div class="formcard thanks">
      <img src="../assets/img/instr-lori.jpg" alt="Lori, Owner / Director of Pacific Dance">
      <h3>You're in — talk soon!</h3>
      <p>Hi, I'm Lori. I'll email you within a day or two — usually much sooner — to find the perfect class for your dancer. Want a head start? A few more details help me place them just right.</p>
      <a class="btn btn-primary" style="margin-top:18px" href="contact.html#cform">Add more details (optional)</a>
      <p class="form-note">Or just wait for my email — either works! <a href="index.html" style="color:var(--royal)">Back to the homepage</a></p>
    </div>
  </div>
</section>
""" + FOOTER

# ============================================================ PG FAMILY GATE (mock)
def pgfamily_page():
    return head("PG Families — Pacific Dance", "Password-protected page for current Performing Group families.") + nav("performing-groups.html") + """
<section class="block" style="min-height:62vh; display:flex; align-items:center">
  <div class="wrap" style="max-width:520px">
    <div class="formcard" style="text-align:center">
      <div style="font-size:2rem">🔒</div>
      <h3 style="font-size:1.4rem; margin-top:10px">PG Families only</h3>
      <p style="margin-top:10px; color:var(--slate); font-size:.95rem">This is a mock of Squarespace's built-in password screen. On the live site, current Performing Group families enter the seasonal password here to reach schedules, fees, and logistics.</p>
      <form onsubmit="event.preventDefault(); this.querySelector('p.gate-msg').style.display='block';">
        <label style="text-align:left">Password</label><input type="password" placeholder="Shared each season by the studio">
        <button class="btn btn-primary" type="submit">Enter</button>
        <p class="gate-msg" style="display:none; margin-top:12px; font-size:.85rem; color:var(--royal); font-weight:600">On the live site this unlocks the PG Family page.</p>
      </form>
      <p class="form-note" style="margin-top:14px"><a href="performing-groups.html" style="color:var(--royal)">← Back to Performing Groups</a></p>
    </div>
  </div>
</section>
""" + FOOTER

# ============================================================ CLASSES — OPTION 2 (document/PDF)
def classes_doc_page():
    return head("Class Schedule — Pacific Dance, Irvine", "The full Pacific Dance class schedule for Irvine, CA — view online or download the PDF.") + nav("classes.html") + f"""
<div class="wrap" style="max-width:1000px"><div class="opt-switch">Reviewing <b>two schedule options</b> — this is <b>Option 2: uploaded document</b> (matches the studio's current workflow). <a href="classes.html">See Option 1: browse-by-style →</a></div></div>
""" + page_hero(
        "Classes & Schedules",
        "The class schedule",
        "The full studio schedule, updated monthly. View it right here, or download to print for the fridge. Ages 2–92, seven days a week.",
    ) + f"""
<section class="block">
  <div class="wrap" style="max-width:1000px">
    <div class="sample-note"><b>Mock note — Option 2:</b> this mirrors how the studio works today. Each month Lori exports two files and swaps them in Squarespace — no grid to edit, no code. The schedule shows inline as an image below, with PDFs to print. (Sample = real July 2026 schedule.)</div>

    <div class="sched-head">
      <span class="sched-badge">Effective July 2026</span>
      <span class="sched-upd">Updated monthly by the studio</span>
    </div>

    <div class="sched-actions">
      <a class="btn btn-primary" href="../assets/schedule/schedule-by-studio.pdf" target="_blank" rel="noopener">Schedule by Studio + Teacher · PDF</a>
      <a class="btn btn-ghost-navy" href="../assets/schedule/list-by-class.pdf" target="_blank" rel="noopener">List by Class · PDF</a>
    </div>

    <div class="sched-frame">
      <img src="../assets/schedule/sbs-1.png" alt="Pacific Dance schedule — Studios One, Two, Three and Four, page 1" loading="lazy">
      <img src="../assets/schedule/sbs-2.png" alt="Pacific Dance schedule, page 2" loading="lazy">
      <img src="../assets/schedule/sbs-3.png" alt="Pacific Dance schedule, page 3" loading="lazy">
    </div>

    <p class="sched-tip">Tap either PDF above to zoom in or print. On the live site, only this schedule image and the two PDFs change each month — everything else stays put.</p>

    <div class="pull-review" style="margin-top:30px">"All the teachers here are so welcoming and friendly… My child dances here and I also take adult ballet here and love it!"<span>— Daphne · via Yelp · parent &amp; adult student</span></div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap" style="max-width:760px; text-align:center">
    <div class="eyebrow">Two ways to see it</div>
    <h2 style="font-size:clamp(1.7rem,3.4vw,2.3rem); margin-top:10px">Prefer to browse by style?</h2>
    <p style="margin-top:12px; color:var(--slate)">See the same classes in a tap-to-open list organized by dance style and age — no scanning a grid.</p>
    <p style="margin-top:20px"><a class="btn btn-primary" href="classes.html">Browse by style →</a></p>
  </div>
</section>
""" + cta_band("Not sure which class fits?", "Tell us your dancer's age and interests — Lori will point you to the right class, and the first one is free.") + FOOTER

# ============================================================ HOW TO ENROLL (full registration + waiver)
def how_to_enroll_page():
    hear_opts = "".join(f"<option>{o}</option>" for o in
        ["", "Friend / Family", "Walk by", "Google", "Facebook", "Instagram", "TikTok", "YouTube", "Mom's Group (Facebook)", "Yelp", "Other"])
    state_ph = 'placeholder="CA"'

    school_policies = """
      <h5>Registration</h5>
      <p>A registration form/waiver must be completed and submitted from our website by the parent or legal guardian before any class is taken. There is a $35 registration fee. If you discontinue classes for any reason for more than one month and then return, you will be required to pay the registration fee upon re-enrolling.</p>
      <h5>Tuition / Fees</h5>
      <p>Tuition for classes is a monthly tuition (regardless of the number of weeks or holidays in any month). Please see Holidays Closed on our website.</p>
      <p>All tuition must be set up for Auto Pay with a credit card. Your credit card will be charged on or about the 1st day of each month. Should your card be declined for any reason, you must pay by the 7th day of the month to avoid a $35 late fee and provide us with your new credit card information by the 7th day of the month in which it was declined.</p>
      <p>NO statements will be sent to you unless your tuition is late. A $35 late fee will be charged for all tuition payments received after the 1st day of the month. A $35 fee will be charged on all returned checks.</p>
      <p>NO credit or refund is given for absences, tuition, costumes, competition fees, workshop fees, or convention fees.</p>
      <p>If you are dropping any or all classes, you must notify us via e-mail at PacificDance1@gmail.com by the 20th day of the month preceding the month you would like to drop, or you will be responsible for paying your tuition for the following month.</p>
      <h5>Absences</h5>
      <p>If you are absent from a class, you may request a courtesy make-up in a comparable class after the class is missed. A make-up must be taken no later than one month from the date of the absence, and you must be currently registered in a class. Once you drop all classes, you lose all make-ups. Make-ups are non-transferrable. All make-ups must be requested at least 48 hours in advance of the class you are interested in making up in from our website Make-Up page. Pacific Dance will send a confirmation email. Not all classes will be open for make-ups. Pacific Dance has the right to refuse the use of a make-up should the class size be too large on the day of a make-up, or if the level/age is not appropriate for the student.</p>
      <p>If you are taking a make-up class in a 90 minute class and are not enrolled in a 90 minute class, you will need to use two make-ups to take a make-up in a 90 minute class. We cannot guarantee a make-up will be available for your schedule, age or level.</p>
      <h5>Attire</h5>
      <p>Proper dancewear and shoes are required for all classes (please see the Required Dance Attire page on our website for details).</p>
      <h5>Recital</h5>
      <p>Our annual Recital is optional. If you decide to participate in the Recital, you are required to have good attendance in your class(es), purchase the assigned costume(s), tights and shoes, and attend mandatory rehearsals and all scheduled recital performances. If your account balance is not paid in full prior to the Mandatory Dress Rehearsal date for the Recital, your child will not be able to participate in the Recital.</p>
      <h5>Supervision of Students</h5>
      <p>Children are supervised during class time only and should not be dropped off early or picked up late.</p>
      <h5>Photography and Videotaping</h5>
      <p>Unless prior parental and teacher authorization has been given, no photography or videotaping is allowed at Pacific Dance of any student other than your own.</p>
      <h5>Miscellaneous</h5>
      <p>Despite our safety precautions, there is a risk of contagion in any public place. By coming into the studio, you are acknowledging that you understand these risks and do not hold Pacific Dance or employees liable.</p>
      <p>In order to maintain the quality level of dance training at Pacific Dance, classes run year-round. Very often our classes are full, so space may be limited. If you drop your class(es), your space in that class cannot be held. If you have any questions, please feel free to e-mail us at PacificDance1@gmail.com.</p>"""

    waiver = """
      <p>I have chosen to have my child participate in dance instruction given by Pacific Dance, Inc. (&ldquo;Pacific Dance&rdquo;). I acknowledge that I understand the nature of the activities my child will be participating in and that my child is in the proper physical condition and capable of participating in the related activities, understanding that Pacific Dance is not in any way responsible for making such a determination. In consideration of my child&rsquo;s enrollment in any dance instruction program, I understand and agree on behalf of myself and my child, to release, hold harmless, and discharge Pacific Dance from all claims, costs, liabilities, expenses or judgments, including attorneys&rsquo; fees and court costs for any occurrences in connection with any dance instruction. I assume all risks to my child in connection with any instruction and further release Pacific Dance and its owners and employees from liability for any injury sustained by my child while he or she is enrolled in any dance instruction program, including all risks reasonably connected with such activity whether foreseen or unforeseen. I understand that despite precautions and policies put in place by Pacific Dance, there is a risk of any contagion, including Covid-19, to my minor child or myself. Participation is voluntary with knowledge of this risk. By executing this Waiver, you hereby release Pacific Dance from any and all liability and responsibility that may arise from any infection by, or exposure or suspected exposure to, the Coronavirus in connection with dance classes. I understand that Pacific Dance is not responsible for my child or other children under my supervision who are left unsupervised in the common areas and areas surrounding the dance studio and that Pacific Dance will only be supervising my child when he or she is participating in scheduled dance activities, programs or instruction. I understand that Pacific Dance is not responsible for personal property that is lost, damaged or stolen while I or my child is at or on Pacific Dance property. I acknowledge and agree that it is my responsibility to maintain my own accident and health insurance coverage that provides adequate coverage for myself and my child participating in Pacific Dance activities and that Pacific Dance does not provide accident or health insurance for those participating in its instruction, activities or programs. I authorize and agree that Pacific Dance may take and use photographs, videos or likenesses of myself or my child as needed for its record-keeping, advertising and/or public relations projects and that I have no rights to the same and will not be compensated for the same. By clicking the &ldquo;I Agree&rdquo; box I agree to execute a complete and unconditional waiver and release of all liability pursuant to the terms herein, and agreement as to all terms and conditions contained above. I am of lawful age and competent to execute this affirmation. I HAVE FULLY INFORMED MYSELF AS TO THE CONTENTS OF THIS RELEASE AND HAVE READ THE SAME PRIOR TO AGREEMENT OF TERMS.</p>
      <h5>Tuition Autopay</h5>
      <p>I understand and agree that Pacific Dance will charge my credit card provided by me in the amount of my current tuition on or about the 1st day of each month.</p>
      <p>I understand and agree that this charge is for monthly tuition, and the recurring charge will continue for 180 months or until I have provided Pacific Dance notice via e-mail at PacificDance1@gmail.com to drop all of my classes and terminate my recurring charge. This e-mail must be sent by the 20th day of the month preceding the month you want to drop all classes.</p>
      <p>I understand and agree that if my credit card is declined for any reason whatsoever (i.e., it has been declined, cancelled or changed), my account will be manually invoiced and will incur a late fee of $35 if my account has not been paid manually via check, cash or credit card prior to the 7th day of the month. It is my responsibility to contact you with my updated credit card information.</p>
      <p>I will not dispute Pacific Dance&rsquo;s recurring billing with my credit card issuer so long as the amount in question was for services rendered prior to my canceling my account in the manner required.</p>
      <p>I guarantee and warrant that I am the legal cardholder for this credit card and that I am legally authorized to enter into this one time or recurring billing agreement with Pacific Dance.</p>"""

    return head("How to Enroll — Pacific Dance, Irvine", "Register at Pacific Dance in Irvine — complete the registration form and waiver to enroll your dancer.") + nav("enroll.html") + page_hero(
        "How to Enroll",
        "Ready to make it official?",
        "Whether you've tried a free class or you already know you're ready — this is where you register your dancer. It takes about five minutes, and we're glad to help you through it.",
        bg="../assets/img/ba-studio-after.jpg", bg_alt="Inside a Pacific Dance studio",
    ) + f"""
<section class="block">
  <div class="wrap" style="max-width:760px">
    <div class="sample-note"><b>Mock note:</b> in Squarespace this is a native Form Block — same fields, dropdowns, and two agreement checkboxes as the studio's current form, plus the full legal text. Lori edits it in the form editor; no code.</div>

    <div class="steps3">
      <div class="step"><span class="stepn">1</span><h4>Try a free class</h4><p>New here? Start with a free class so your dancer finds the right fit — no card, no commitment.</p><a href="enroll.html" class="steplink">Book a free class →</a></div>
      <div class="step"><span class="stepn">2</span><h4>Register &amp; sign the waiver</h4><p>Fill out the form below — dancer details, classes of interest, and the two agreements. About five minutes.</p></div>
      <div class="step"><span class="stepn">3</span><h4>Set up autopay &amp; dance</h4><p>We'll set up monthly Auto Pay together and get your dancer on the schedule. We accept students year-round.</p></div>
    </div>

    """ + personal_help() + """

    <div class="formcard" id="registration" style="margin-top:30px">
      <h3 style="font-size:1.5rem">Registration Form</h3>
      <p style="font-size:.9rem; color:var(--slate); margin-top:6px">A parent or legal guardian must complete this form before the first class.</p>
      <form onsubmit="event.preventDefault(); this.style.display='none'; document.getElementById('reg-done').style.display='block'; document.getElementById('reg-done').scrollIntoView({{block:'center'}});">

        <div class="fsec">
          <h3>The dancer</h3>
          <div class="frow">
            <div><label>Student first name *</label><input required placeholder="First name"></div>
            <div><label>Student last name *</label><input required placeholder="Last name"></div>
          </div>
          <div class="frow thirds">
            <div><label>Date of birth *</label><input required placeholder="mm/dd/yyyy"></div>
            <div><label>Age *</label><input required placeholder="e.g. 6"></div>
            <div><label>Gender *</label><select required><option value=""></option><option>Girl</option><option>Boy</option><option>Other</option></select></div>
          </div>
        </div>

        <div class="fsec">
          <h3>Parent / guardian</h3>
          <div class="frow">
            <div><label>Parent first name *</label><input required placeholder="First name"></div>
            <div><label>Parent last name *</label><input required placeholder="Last name"></div>
          </div>
          <div class="frow">
            <div><label>Email *</label><input type="email" required placeholder="you@email.com"></div>
            <div><label>Cell phone *</label><input type="tel" required placeholder="(714) 555-0123"></div>
          </div>
          <label>Second phone <span style="font-weight:400; color:var(--slate)">(optional)</span></label><input type="tel" placeholder="Optional">
        </div>

        <div class="fsec">
          <h3>Address</h3>
          <label>Street address *</label><input required placeholder="Address line 1">
          <label>Apt / unit <span style="font-weight:400; color:var(--slate)">(optional)</span></label><input placeholder="Address line 2">
          <div class="frow thirds">
            <div><label>City *</label><input required placeholder="Irvine"></div>
            <div><label>State *</label><input required {state_ph}></div>
            <div><label>ZIP *</label><input required placeholder="92620"></div>
          </div>
        </div>

        <div class="fsec">
          <h3>Classes &amp; interests</h3>
          <label>What classes are you interested in? *</label>
          <textarea rows="3" required placeholder="Tell us the styles, days, or class names your dancer wants — or just their age and we'll help you choose."></textarea>
          <label>How did you hear about Pacific Dance? *</label>
          <select required>{hear_opts}</select>
        </div>

        <div class="fsec">
          <h3>School policies</h3>
          <p class="fsub">Please read our studio policies, then confirm below.</p>
          <div class="legal-box">{school_policies}</div>
          <label class="agree"><input type="checkbox" required> I agree — I am 18 years old or older, and I have read and accept the School Policies above. *</label>
        </div>

        <div class="fsec">
          <h3>Waiver / release from liability &amp; tuition autopay</h3>
          <p class="fsub">Please read the full waiver and autopay agreement, then confirm below.</p>
          <div class="legal-box">{waiver}</div>
          <label class="agree"><input type="checkbox" required> I agree — I am 18 years old or older, and I accept the Waiver / Release from Liability and the Tuition Autopay agreement above. *</label>
        </div>

        <button class="btn btn-primary" type="submit">Complete Registration</button>
        <p class="form-note">A $35 registration fee applies. We'll confirm your enrollment and set up Auto Pay with you personally.</p>
      </form>
      <div id="reg-done" style="display:none; text-align:center; padding:26px 10px">
        <div style="font-size:2rem">🎉</div>
        <h3 style="font-size:1.4rem; margin-top:8px">You're registered!</h3>
        <p style="margin-top:10px; color:#24405e">Thanks — we've got your registration. Lori or a team member will reach out within a day or two to confirm your classes and set up Auto Pay. Welcome to Pacific Dance!</p>
        <p style="margin-top:14px"><a href="classes.html" style="color:var(--royal); font-weight:600">Browse the schedule →</a></p>
      </div>
    </div>
  </div>
</section>
""" + cta_band("Not sure yet?", "Start with a free class — no card, no commitment. Register whenever your dancer's ready.") + FOOTER

PAGES = {
    'index.html': homepage,
    'classes.html': classes_page,
    'classes-doc.html': classes_doc_page,
    'how-to-enroll.html': how_to_enroll_page,
    'enroll.html': enroll_page,
    'about.html': about_page,
    'performing-groups.html': pg_page,
    'recital.html': recital_page,
    'policies.html': policies_page,
    'contact.html': contact_page,
    'thank-you.html': thankyou_page,
    'free-class.html': landing_page,
    'pg-family.html': pgfamily_page,
}

if __name__ == '__main__':
    for fname, fn in PAGES.items():
        with open(os.path.join(HERE, fname), 'w') as f:
            f.write(fn())
        print('wrote', fname)
