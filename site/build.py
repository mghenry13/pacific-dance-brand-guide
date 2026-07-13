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
<link rel="stylesheet" href="site.css?v=1">
</head>
<body>
"""

def nav(active):
    on = ' style="color:var(--royal)"'
    items = "".join(
        f'<li><a href="{href}"{on if href == active else ""}>{label}</a></li>'
        for href, label in NAV_ITEMS[1:]
    )
    return f"""<div class="annbar">Fall enrollment is open — the first class is free. <a href="enroll.html">Book now →</a></div>
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

def page_hero(eyebrow, h1, sub=""):
    p = f"<p>{sub}</p>" if sub else ""
    return f"""<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    {p}
  </div>
</section>
"""

def cta_band(h="The first class is free.", p="Tell us a little about your dancer and Lori will help you find the perfect class — no commitment, no card."):
    return f"""<section class="block dark finale">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{p}</p>
    <a class="btn" style="background:var(--sky); color:var(--navy)" href="enroll.html">{CTA}</a>
    <small>Takes about a minute · Lori follows up personally</small>
  </div>
</section>
"""

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
    accs = ""
    for i, (title, sub, names) in enumerate(ACCORDION_GROUPS):
        adult_only = names == ["ADULT_ONLY"]
        subline = f'<p style="color:var(--slate); font-size:.88rem; margin-bottom:12px">{sub}</p>' if sub else ""
        accs += (f'<details class="acc"{" open" if i == 0 else ""}><summary>{title}</summary>'
                 f'<div class="inner">{subline}{rows_for(names, adult_only)}</div></details>\n')
    return head("Classes & Schedules \u2014 Pacific Dance, Irvine", "Dance classes for ages 2\u201392 in Irvine, CA \u2014 browse the schedule by style.") + nav("classes.html") + page_hero(
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
    ) + f"""
<section class="block">
  <div class="wrap twocol form-first">
    <div>
      <div class="eyebrow">How it works</div>
      <h2 style="font-size:2rem; margin-top:10px">Three steps, one happy dancer</h2>
      <div style="margin-top:24px; display:flex; flex-direction:column; gap:18px">
        <div class="card-p"><h3>1 · Tell us about your dancer</h3><p style="margin-top:6px">The short form here — about a minute.</p></div>
        <div class="card-p"><h3>2 · The right-class promise</h3><p style="margin-top:6px">Lori personally matches every dancer to the right class — age, level, and interest. It's the thing families thank us for most.</p></div>
        <div class="card-p"><h3>3 · Come dance — free</h3><p style="margin-top:6px">Try the class. If your dancer loves it (they usually do), we'll get them enrolled. Registration and the waiver happen after you've scheduled — not before.</p></div>
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
          <p class="form-note">No card, no commitment — Lori follows up personally.</p>
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
""" + cta_band("Questions before you book?", "Call or email — a real person answers, and it's usually Lori.") + FOOTER

# ============================================================ ABOUT
def about_page():
    instructors = json.load(open('/tmp/instructors.json'))
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
        full = "".join(f"<p>{p}</p>" for p in paras[:2])
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
      <p style="margin-top:12px; color:#24405e">Our goal has never changed: professional training that's safe and individualized for every level of student, in a place kids genuinely love to be. Whether your dancer is training toward a professional track, keeping fit, or just having fun, they belong here — every ability level and interest, ages 2 to 92.</p>
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
    <div class="facgrid" style="grid-template-columns:repeat(2,1fr)">
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
<section class="block">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">The groups</div>
      <h2>A team for every stage</h2>
    </div>
    <div class="stygrid" style="grid-template-columns:repeat(4,1fr)">
      <div class="sty"><h3>Mini Mini PG</h3><p>The youngest performers get their first taste of the team — and the stage.</p><span class="age">Youngest dancers</span></div>
      <div class="sty"><h3>Hip Hop &amp; Tap PGs</h3><p>Style-specific crews for dancers who've found their lane.</p><span class="age">By audition</span></div>
      <div class="sty"><h3>Mini Ballet PG</h3><p>Classical foundations, performance polish.</p><span class="age">Ages 6 &amp; up</span></div>
      <div class="sty"><h3>PD Elite</h3><p>Our pre-professional company — the most committed track we offer.</p><span class="age">Advanced</span></div>
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
        <a class="btn" href="#">Enter the PG Family page →</a>
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
        "From the two-year-olds to the seniors — every June, every dancer performs at the Irvine Barclay Theater.",
    ) + f"""
<section class="block">
  <div class="wrap twocol">
    <div>
      <div class="eyebrow">Annual recital</div>
      <h2 style="font-size:2.1rem; margin-top:10px">Recital 2027 · June 7–11</h2>
      <p style="margin-top:16px; color:#24405e">A professional theater, real costumes, four full shows — and a moment on stage for every single dancer. Participation is optional but beloved: good class attendance, the assigned costume, and the scheduled rehearsals are all it takes.</p>
      <p style="margin-top:12px; color:#24405e">Closer to the date, this page carries everything families need: the director's welcome, show programs, ticket info, and our stage makeup &amp; hair bun demo video.</p>
      <div class="sample-note" style="margin-top:18px"><b>Swappable by design:</b> this section updates each season (2026 → 2027 → …) without rebuilding the page — same for the program, senior shout-outs, and schedules.</div>
    </div>
    <img src="../assets/img/scorpion-black.jpg" alt="A Pacific Dance student performing on stage" style="border-radius:10px">
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap">
    <div class="head-c">
      <div class="eyebrow">Summer 2026</div>
      <h2>Workshops &amp; intensives</h2>
    </div>
    <div class="twocol" style="grid-template-columns:1fr 1fr 1fr">
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
          <li>$350 one week · deposits hold your spot</li>
        </ul>
      </div>
      <div class="card-p">
        <h3>December Open House</h3>
        <ul style="margin-top:10px">
          <li>An in-studio holiday performance for family &amp; friends</li>
          <li>Every class can take part — a cozy first "stage" of the year</li>
          <li>Gets dancers excited for recital season ahead</li>
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
    def acc(title, inner, open_=False):
        return f'<details class="acc"{" open" if open_ else ""}><summary>{title}</summary><div class="inner">{inner}</div></details>'
    policies = (
        acc("Registration", "<p>A registration form and waiver must be completed by a parent or legal guardian before any class. The $35 registration fee applies again if you discontinue for more than a month and return.</p>", True)
        + acc("Tuition & Auto Pay", "<ul><li>Tuition is monthly, regardless of weeks or holidays in the month.</li><li>All tuition runs on Auto Pay — charged on or about the 1st. Declines must be resolved by the 7th to avoid a $35 late fee.</li><li>No credits or refunds for absences, tuition, costumes, competition, workshop, or convention fees.</li><li>Dropping a class? Email by the 20th of the prior month, or the next month's tuition applies.</li></ul>")
        + acc("Absences & make-ups", "<p>Request a courtesy make-up in a comparable class within one month of the absence, at least 48 hours ahead, via the make-up form. Make-ups are non-transferable, end when you drop all classes, and aren't guaranteed for every schedule, age, or level. 90-minute classes use two make-ups unless you're enrolled in one.</p>")
        + acc("Recital participation", "<p>The annual recital is optional. Participating dancers need good attendance, the assigned costume, tights and shoes, and the mandatory rehearsals and shows. Accounts must be paid in full before dress rehearsal.</p>")
        + acc("Supervision", "<p>Children are supervised during class time only — please don't drop off early or pick up late.</p>")
        + acc("Photography & video", "<p>No photographing or videotaping other people's children without prior parent and teacher authorization. Pacific Dance may use class photos and video for its website, social media, and advertising.</p>")
    )
    attire = (
        acc("Combo & Pre-Ballet (ages 2–7)", "<p>Tight-fitting dance attire — tights and leotard, bike shorts or leggings. No t-shirts, street clothes, or large tutus. Ballet and tap shoes for B/T combos.</p>", True)
        + acc("Ballet", "<p>Black leotard, pink tights, pink ballet shoes. Buns required. Upper levels: no skirts, black sports bras only. Male dancers: white tank or tee, black dance shorts, black ballet shoes.</p>")
        + acc("Jazz · Lyrical · Tap · Acro", "<p>Leggings or spandex shorts with a tight-fitting top or leotard — no street clothes. Jazz shoes for jazz, tap shoes for tap, bare feet for acro, jazz or half-sole shoes for lyrical.</p>")
        + acc("Hip Hop & K-Pop", "<p>Loose-fitting street clothes and sneakers — the one place street clothes belong.</p>")
        + acc("The fine print", "<p>No jewelry in class (safety). Hair pulled back and out of the eyes; buns in all ballet classes. Proper attire lets teachers see placement and train dancers safely.</p>")
    )
    return head("Policies & Info — Pacific Dance", "School policies, dance attire, Pacific Dancewear, and directions.") + nav("policies.html") + page_hero(
        "Policies & Info",
        "The practical stuff, in one place",
        "Policies, attire, the dancewear store, and how to find us.",
    ) + f"""
<section class="block">
  <div class="wrap twocol">
    <div>
      <div class="eyebrow">School policies</div>
      <h2 style="font-size:1.9rem; margin:10px 0 20px">Policies</h2>
      {policies}
    </div>
    <div>
      <div class="eyebrow">What to wear</div>
      <h2 style="font-size:1.9rem; margin:10px 0 20px">Dance attire</h2>
      {attire}
    </div>
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
<section class="page-hero" style="padding-bottom:52px">
  <div class="wrap">
    <div class="eyebrow">Irvine · ages 2–92</div>
    <h1>Your dancer's first class is free</h1>
    <p>Ballet, jazz, hip hop, K-Pop and more — taught by working professionals at the largest studio in the area. No card, no commitment.</p>
    <p style="margin-top:14px; color:var(--sky); font-weight:600; font-size:.95rem">★ 4.5 on Google · Irvine families since 1994</p>
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
          <p class="form-note">Takes about a minute — Lori follows up personally.</p>
        </form>
      </div>
    </div>
    <div>
      <div class="card-p"><h3>Small classes, always</h3><p style="margin-top:6px">Capped at 12–15 dancers in the young groups — every kid is seen, corrected, and known by name.</p></div>
      <div class="card-p" style="margin-top:14px"><h3>The right-class promise</h3><p style="margin-top:6px">Lori, our co-owner, personally matches every dancer to the right class by age, level, and interest.</p></div>
      <div class="card-p" style="margin-top:14px"><h3>Watch every minute</h3><p style="margin-top:6px">Viewing windows on the studios and a comfortable parent waiting area — homework happens between classes.</p></div>
      <div class="pull-review" style="margin-top:20px">"The focus is never on winning — it's about the kids doing their best and having fun."<span>— Becky · via Google</span></div>
    </div>
  </div>
</section>

<section class="block mist-bg">
  <div class="wrap" style="max-width:820px">
    <div class="head-c" style="margin-bottom:24px"><h2 style="font-size:1.7rem">Quick answers</h2></div>
    <details class="acc" open><summary>Is it really free?</summary><div class="inner"><p>Yes — the first class is free, with no card and no commitment. Kids usually fall in love with the teacher; that's the whole plan.</p></div></details>
    <details class="acc"><summary>What ages do you take?</summary><div class="inner"><p>2 to 92. Mommy &amp; Me through adult classes, every ability level and interest.</p></div></details>
    <details class="acc"><summary>When are classes?</summary><div class="inner"><p>Seven days a week, across eight styles — Lori will point you to the exact times that fit your schedule.</p></div></details>
  </div>
</section>
""" + cta_band("Ready when you are.", "One-minute form, free first class, and Lori takes it from there.") + FOOTER

# ============================================================ THANK YOU
def thankyou_page():
    return head("You're in — Pacific Dance", "Thanks! Lori will follow up shortly to find the perfect class.") + nav("enroll.html") + """
<section class="block" style="min-height:60vh; display:flex; align-items:center">
  <div class="wrap" style="max-width:640px">
    <div class="formcard thanks">
      <img src="../assets/img/instr-lori.jpg" alt="Lori, co-owner of Pacific Dance">
      <h3>You're in — talk soon!</h3>
      <p>Hi, I'm Lori. I'll email you shortly to find the perfect class for your dancer. Want a head start? A few more details help me place them just right.</p>
      <a class="btn btn-primary" style="margin-top:18px" href="#">Add more details (optional)</a>
      <p class="form-note">Or just wait for my email — either works! <a href="index.html" style="color:var(--royal)">Back to the homepage</a></p>
    </div>
  </div>
</section>
""" + FOOTER

PAGES = {
    'index.html': homepage,
    'classes.html': classes_page,
    'enroll.html': enroll_page,
    'about.html': about_page,
    'performing-groups.html': pg_page,
    'recital.html': recital_page,
    'policies.html': policies_page,
    'contact.html': contact_page,
    'thank-you.html': thankyou_page,
    'free-class.html': landing_page,
}

if __name__ == '__main__':
    for fname, fn in PAGES.items():
        with open(os.path.join(HERE, fname), 'w') as f:
            f.write(fn())
        print('wrote', fname)
