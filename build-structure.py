#!/usr/bin/env python3
"""Structure build — six pages from one header/footer, every unwritten block a
labelled slot. Run once, then edit the HTML by hand; this is scaffolding, not
a build step the site depends on."""

PAGES = [
    ("index",      "Home",       "Libra Shipping B.V. — Ship brokers and agents, Rotterdam"),
    ("chartering", "Chartering", "Chartering — Libra Shipping B.V."),
    ("agency",     "Agency",     "Agency — Libra Shipping B.V."),
    ("cargo",      "Cargo",      "Cargo — Libra Shipping B.V."),
    ("about",      "About",      "About — Libra Shipping B.V."),
    ("contact",    "Contact",    "Contact — Libra Shipping B.V."),
]
NAV = [("chartering", "Chartering"), ("agency", "Agency"), ("cargo", "Cargo"), ("about", "About")]


def slot(kind, text, cls=""):
    return f'<div class="slot {cls}"><span class="slot-tag">{kind}</span><span class="slot-txt">{text}</span></div>'


def photo(tag, spec, cls="ph top"):
    return (f'<div class="{cls}"><span class="ph-tag">Photo slot &mdash; {tag}</span>'
            f'<span class="ph-spec">{spec}</span></div>')


def head(title):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Sans+Condensed:wght@500;700&family=Fira+Sans:wght@400;500;700&display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>
'''


def header(active):
    links = "\n".join(
        '      <a href="%s.html"%s>%s</a>' % (slug, ' aria-current="page"' if slug == active else '', label)
        for slug, label in NAV)
    cur = ' aria-current="page"' if active == "contact" else ""
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Libra Shipping B.V. — home">
      <img src="assets/libra-shipping.svg" alt="Libra Shipping B.V.">
    </a>
    <nav class="nav" aria-label="Main">
{links}
      <a class="btn small" href="contact.html"{cur}>Contact</a>
      <span class="lang" aria-label="Language"><a href="#" aria-current="true">EN</a><a href="#" title="Dutch version — to build">NL</a></span>
    </nav>
  </div>
</header>

<main>
'''


FOOTER = '''
</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="footgrid four">
      <div>
        <div class="ft">Libra Shipping B.V.</div>
        <p>Ship broker and ship agent, specialised in coastal shipping. A joint venture of Euro Nordic Logistics and Euro-Rijn. Since 1976.</p>
      </div>
      <div>
        <div class="ft">Rotterdam</div>
        <p>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br><a class="num" href="tel:+31180441151">+31 180 441 151</a><br><a href="mailto:chartering@librashipping.nl">chartering@librashipping.nl</a><br><a href="mailto:libra.agencies@librashipping.nl">libra.agencies@librashipping.nl</a></p>
      </div>
      <div>
        <div class="ft">Antwerp</div>
        <p class="todo">[address]<br>[telephone]<br><a href="mailto:libra.agencies@librashipping.nl">libra.agencies@librashipping.nl</a></p>
      </div>
      <div>
        <div class="ft">Pages</div>
        <p><a href="chartering.html">Chartering</a><br><a href="agency.html">Agency</a><br><a href="cargo.html">Cargo</a><br><a href="about.html">About</a><br><a href="contact.html">Contact</a></p>
        <p class="footsocial"><a href="#" class="todo">LinkedIn &rarr; [page URL]</a></p>
      </div>
    </div>
    <div class="footcerts">
      <span class="ft">Certifications</span>
      <div class="certrow">
        <span class="certbox todo">[cert logo]</span>
        <span class="certbox todo">[cert logo]</span>
        <span class="certbox todo">[cert logo]</span>
        <span class="certnote todo">Only the ones Libra holds, each with a number behind it. See <a href="about.html">About</a>.</span>
      </div>
    </div>
    <div class="footrule">
      <span>&copy; <span class="num">2026</span> Libra Shipping B.V. &mdash; Rotterdam &middot; Antwerp</span>
      <span class="footlegal"><a href="#">Terms &amp; Conditions</a><a href="#">Privacy</a><a href="#">Disclaimer</a><span class="todo">KvK [number] &middot; VAT [number]</span></span>
    </div>
  </div>
</footer>

</body>
</html>
'''


def person(initials, name, role, tel, mail, note="", mob="[mobile]"):
    return f'''        <article class="person framed">
          <div class="inner">
            <div class="portrait">
              {photo("portrait", "", "ph top")}
              <span class="ph-init" aria-hidden="true">{initials}</span>
            </div>
            <div class="who">
              <span class="nm">{name}</span>
              {f'<span class="rl">{role}</span>' if role else ''}
              {f'<span class="ln num"><a href="tel:{tel.replace(" ", "")}">{tel}</a></span>' if tel[0] == "+" else f'<span class="ln num todo">{tel}</span>'}
              <span class="ln num todo">mob. {mob}</span>
              {f'<span class="ln"><a href="mailto:{mail}">{mail}</a></span>' if "@" in mail and mail[0] != "[" else f'<span class="ln todo">{mail}</span>'}
              {f'<span class="ln todo">{note}</span>' if note else ''}
            </div>
          </div>
        </article>'''


def people(heading, note_rob="", note_joost="", mail="", sub="", note_sefa=""):
    return f'''  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>{heading}</h2>{f'<p class="muted">{sub}</p>' if sub else ''}</div>
      <div class="people three">
{person("RV", "Rob Vrauwdeunt", "", "+31 180 441 152", "rv@librashipping.nl", note_rob)}
{person("JE", "Joost van der Elburg", "", "+31 180 441 153", "je@librashipping.nl", note_joost)}
{person("S", "Sefa [surname]", "", "[office line]", "[s…@librashipping.nl]", note_sefa)}
      </div>
    </div>
  </section>
'''


OFFICES = '''      <div class="offices">
        <article class="office framed">
          <div class="inner">
            <div><span class="on">Rotterdam</span><span class="oc">The Netherlands</span></div>
            <address>Waalhaven Oostzijde 85<br><span class="num">3087 BM</span> Rotterdam<br><a class="num" href="tel:+31180441151">+31 180 441 151</a><br><a href="mailto:chartering@librashipping.nl">chartering@librashipping.nl</a><br><a href="mailto:libra.agencies@librashipping.nl">libra.agencies@librashipping.nl</a></address>
          </div>
        </article>
        <article class="office framed">
          <div class="inner">
            <div><span class="on">Antwerp</span><span class="oc">Belgium</span></div>
            <address class="todo">[address]<br>[telephone]<br><a href="mailto:libra.agencies@librashipping.nl">libra.agencies@librashipping.nl</a></address>
          </div>
        </article>
      </div>
'''


def hero(tag, spec, eyebrow, h1, lead, short=False, cta=None):
    return f'''  <section class="hero{' short' if short else ''}">
    <div class="media">
      {photo(tag, spec)}
    </div>
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {f'<p><a class="btn" href="{cta[1]}">{cta[0]}</a></p>' if cta else ''}
    </div>
  </section>
'''


def to_contact(h2, mail="chartering@librashipping.nl"):
    return f'''  <section>
    <div class="wrap">
      <div class="cpanel framed">
        <div class="inner">
          <h2>{h2}</h2>
          <p><a class="btn" href="contact.html">Send an enquiry</a></p>
          <div class="cdetails">
            <div><div class="lab">Rotterdam</div><div class="val num"><a href="tel:+31180441151">+31 180 441 151</a></div></div>
            <div><div class="lab">Antwerp</div><div class="val todo">[telephone]</div></div>
            <div><div class="lab">Email</div><div class="val"><a href="mailto:{mail}">{mail}</a></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''


# ------------------------------------------------------------------ pages
def page_index():
    return (
        hero("hero", "Loaded coaster under way, shot low and wide. Landscape, 2400 &times; 1350 or larger. Room on the left for the headline.",
             "Ship brokers and agents &middot; Rotterdam &middot; Antwerp &middot; since 1976",
             "[What you get when you work with Libra.]",
             "[One sentence: the promise in plain words. Euro Nordic does &ldquo;We deliver&hellip; quality / personal service&rdquo; as a changing line &mdash; Libra can do a fixed line, or its own changing one.]",
             cta=("What we do", "#services"))
        + '''  <section class="kv">
    <div class="wrap">
      <div class="sechead">
        <h2>[One line on how Libra works, and for how long.]</h2>
        ''' + slot("text", "One sentence under the heading. Three values, no more &mdash; the band stays quiet.") + '''
      </div>
      <div class="kvgrid">
        <div class="kvt dark"><span class="kvhead">Excellent services</span><span class="kvcap">with competitive rates and high-quality subcontractors</span></div>
        <div class="kvt green"><span class="kvfig">24/7</span><span class="kvcap">manned office by experienced operators</span></div>
        <div class="kvt"><span class="kvhead">Tailor-made solutions</span><span class="kvcap">for an efficient port turnaround</span></div>
      </div>
    </div>
  </section>

  <section id="services" class="band">
    <div class="wrap">
      <div class="sechead">
        <h2>What we do.</h2>
        ''' + slot("text", "One sentence: what Libra is, in one breath. Signposts only &mdash; the story lives on the service pages.") + '''
      </div>
      <div class="services link">
        <a class="svc" href="chartering.html">
          <h3>Chartering</h3>
          ''' + slot("text", "One sentence. What chartering means at Libra.") + '''
          <span class="more">Read more &rarr;</span>
        </a>
        <a class="svc" href="agency.html">
          <h3>Agency</h3>
          ''' + slot("text", "One sentence. Ports, offices, what the agency does.") + '''
          <span class="more">Read more &rarr;</span>
        </a>
      </div>
    </div>
  </section>

  <section id="cargo" class="carry">
    <div class="wrap">
      <p class="eyebrow">What we carry</p>
      <h2>[One line: the cargo all of this is for.]</h2>
      <div class="cargo">
        <span class="tag">Grain products</span><span class="tag">Minerals</span><span class="tag">Fertilisers</span>
        <span class="tag todo">[steel]</span><span class="tag todo">[&hellip;]</span>
      </div>
      <p class="aftertags"><a href="cargo.html">All cargo &rarr;</a></p>
    </div>
  </section>

  <section class="band-photo">
    ''' + photo("full width", "Vessel alongside, or cargo working. Wide crop, 2400 &times; 900 or larger.", "ph") + '''
  </section>

'''     + people("Our team.")
        + to_contact("Tell us the cargo. We will tell you the freight.")
    )


def service_page(slug):
    if slug == "chartering":
        h1, lead = "Dry cargo, fixed on sea-going vessels.", "[one sentence: what you get when you charter through Libra]"
        eyebrow = "Chartering &middot; freight calculation &middot; forwarding"
        cards = [("Voyage charter", ""), ("Time charter", ""), ("Freight calculation", "")]
        grid = "services six"
        where_h2, where_body = "Where we trade.", '''      <div class="areas">
        <div class="area"><span class="n">North Sea</span></div><div class="area"><span class="n">Baltic</span></div><div class="area"><span class="n">Atlantic</span></div>
        <div class="area"><span class="n">Mediterranean</span></div><div class="area"><span class="n">Black Sea</span></div><div class="area"><span class="n">West Africa</span></div>
      </div>
      ''' + slot("text", "One line under the map: what &ldquo;worldwide&rdquo; means for chartering, if it is claimed.")
        cta_h2 = "Give us the voyage. We will come back with a number."
        photo_spec = "Coaster loading or at sea. Landscape, 2400 &times; 1350 or larger."
    else:
        h1, lead = "[one promise, in port language]", "Libra Shipping offers chartering worldwide and has its own agencies in the Netherlands and Belgium."
        eyebrow = "Ship&rsquo;s agency &middot; the Netherlands and Belgium"
        cards = [("Husbandry agency", ""), ("Bunkering services", ""), ("Crewing services", ""), ("Lay-by services", ""),
                 ("Repair services", ""), ("Barge hire", ""), ("Brokering", ""), ("Terminal arrangements", "")]
        grid = "services eight"
        where_h2, where_body = "Where we work.", '''      <div class="sechead">''' + slot("text", "One sentence: the port range covered, from which offices.") + '''</div>
''' + OFFICES.replace('<address class="todo">', '<address class="todo">').replace('<address>Waalhaven', '<div class="ports todo">[ports served from here]</div><address>Waalhaven').replace('<address class="todo">[address]', '<div class="ports todo">[ports served from here]</div><address class="todo">[address]')
        cta_h2 = "Nominate a vessel, or ask what a call will cost."
        photo_spec = "Vessel alongside, agent on the quay. Landscape, 2400 &times; 1350 or larger."

    if slug == "agency":
        prose = '''        <p>We focus on a safe, smooth and efficient port turnaround. Our employees have specialised knowledge of all types of vessels and cargoes, and with a long track record they are a reliable source of information.</p>
        <p>At Libra Shipping we believe in a pro-active approach by dedicated staff, which should result in the optimisation of port rotations and a long-term reduction in the overall time spent in port. All of this is always aligned with the customer&rsquo;s requirements, without compromising on safety requirements or local laws.</p>
        ''' + slot("check", "Text as supplied in the feedback round, English polished only. Kees signs off.", "inline")
    else:
        prose = "        " + slot("text", "Paragraph 1 &mdash; what this service is, for whom. 60&ndash;90 words.") + "\n        " + slot("text", "Paragraph 2 &mdash; how Libra works: contact, speed, what makes it reliable. 60&ndash;90 words.")
    forwarding = '''  <section>
    <div class="wrap">
      <div class="sechead"><h2>Forwarding.</h2>''' + slot("text", "One sentence: what Libra arranges around the voyage &mdash; through Euro-Rijn / Euro Nordic or itself. [confirm who does what]") + '''</div>
      <div class="services six">
        <div class="svc"><h3>Transhipment</h3>''' + slot("text", "One sentence.") + '''</div>
        <div class="svc"><h3>On-carriage</h3>''' + slot("text", "One sentence. Onward transport by barge, rail or road.") + '''</div>
        <div class="svc"><h3>Storage</h3>''' + slot("text", "One sentence.") + '''</div>
      </div>
    </div>
  </section>

''' if slug == "chartering" else ""
    card_html = "\n".join(
        f'''        <div class="svc card">
          {photo("card", "3 : 2", "ph ratio")}
          <h3>{name}</h3>
          {slot("text", "One sentence.")}
        </div>''' for name, _ in cards)

    return (
        hero("service hero", photo_spec, eyebrow, h1, lead, short=True, cta=("Get in touch", "contact.html"))
        + ('''  <section class="scale">
    <div class="wrap">
      <p class="fig num">500 &ndash; 50,000 <span class="unit">mt</span></p>
      <p class="figcap">Whatever the parcel size, there is a ship for it &mdash; voyage charter or time charter, bulk, break-bulk or project cargo.</p>
    </div>
  </section>
''' if slug == "chartering" else "")
        + f'''  <section>
    <div class="wrap">
      <div class="sechead"><h2>[What it is, and how we do it.]</h2></div>
      <div class="prose">
{prose}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>{"Amongst other things, we can offer you:" if slug == "agency" else "[What falls under it.]"}</h2>{slot("cards", "Each card: a photo, a name, one sentence.")}</div>
      <div class="{grid}">
{card_html}
      </div>
    </div>
  </section>

{forwarding}  <section>
    <div class="wrap">
      <div class="sechead"><h2>{where_h2}</h2></div>
{where_body}
    </div>
  </section>

'''
        + people("Our team.", "[what Rob handles here]", "[what Joost handles here]", note_sefa="[what Sefa handles here]",
                 mail="libra.agencies@librashipping.nl" if slug == "agency" else "chartering@librashipping.nl")
        + to_contact(cta_h2, "libra.agencies@librashipping.nl" if slug == "agency" else "chartering@librashipping.nl")
    )


def page_cargo():
    groups = [
        ("Agri", ["Grain products", "[barley]", "[rapeseed (meal)]", "[soyabean meal]", "[&hellip;]"]),
        ("Steel", ["[pipes]", "[coils]", "[scrap]", "[&hellip;]"]),
        ("Minerals &amp; fertilisers", ["Minerals", "Fertilisers", "[&hellip;]"]),
    ]
    gh = "\n".join(
        f'''        <div class="cg">
          <span class="cg-lab">{lab}</span>
          <div class="cg-body">
            <div class="cargo">{''.join(f'<span class="tag{" todo" if t.startswith("[") else ""}">{t}</span>' for t in tags)}</div>
            {slot("text", "Two sentences: what Libra fixes in this family, typical parcel sizes, typical trades.")}
          </div>
        </div>''' for lab, tags in groups)
    return (
        hero("cargo hero", "Cargo in the hold, or on the quay. Landscape, 2400 &times; 1350 or larger.",
             "Cargo &middot; what we fix",
             "[one promise about the cargo]",
             "[one sentence: the families, the sizes, the trades]", short=True)
        + f'''  <section>
    <div class="wrap">
      <div class="sechead"><h2>Three families, one desk.</h2>{slot("text", "Intro, two sentences. Why the cargo list is here: this is what buyers search on.")}</div>
      <div class="cargogroups">
{gh}
      </div>
      <div class="cert">
        <span class="cert-mark">[cert]</span>
        <p>{slot("proof", "Certification, if any (e.g. GMP+): scheme, number, valid until. Only with the number.", "inline")}</p>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>Forms of cargo.</h2></div>
      <div class="cargo">
        <span class="tag">Bulk</span><span class="tag">Break-bulk</span><span class="tag">Project cargo</span>
      </div>
      {slot("text", "One sentence per form, or leave as tags.")}
    </div>
  </section>

'''
        + to_contact("Tell us the cargo. We will tell you the freight.")
    )


def page_about():
    return (
        hero("about hero", "The office, or the Waalhaven from the water. Landscape, 2400 &times; 1350 or larger.",
             "About &middot; since 1976",
             "[one line about who Libra is]",
             "[one sentence: the joint venture, the two desks, what has not changed]", short=True)
        + f'''  <section>
    <div class="wrap">
      <div class="sechead"><h2>Since 1976.</h2></div>
      <div class="prose">
        {slot("text", "Paragraph 1 &mdash; founding, the joint venture of Euro Nordic and Euro-Rijn, what Libra is inside that.")}
        {slot("text", "Paragraph 2 &mdash; how the desk works today: short lines, direct contact, who does what.")}
        {slot("text", "Paragraph 3 (optional) &mdash; how Libra works with Euro Nordic (in-house chartering broker) and Euro-Rijn.")}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>How we work.</h2>{slot("list", "Three to five values, each a heading plus one line. The place for &ldquo;safety first&rdquo;, &ldquo;24/7&rdquo;, &ldquo;pro-active&rdquo; &mdash; if kept.")}</div>
      <ul class="values">
        <li>[Value 1]<span>[one line]</span></li>
        <li>[Value 2]<span>[one line]</span></li>
        <li>[Value 3]<span>[one line]</span></li>
        <li>[Value 4]<span>[one line]</span></li>
      </ul>
    </div>
  </section>

'''
        + people("Our team.", "[role, since]", "[role, since]", note_sefa="[role, since]").replace('<section class="band">', '<section>')
        + f'''  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>Two offices.</h2></div>
{OFFICES}
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sechead"><h2>Certifications and conditions.</h2></div>
      <div class="cert">
        <span class="cert-mark">[cert]</span>
        <p>{slot("proof", "Each certification: name, scheme, number, valid until. Plus the link to the Terms &amp; Conditions PDF.", "inline")}</p>
      </div>
    </div>
  </section>

'''
    )


def page_contact():
    return (
        hero("contact hero", "The Waalhaven, or the office seen from the water. Landscape, 2400 &times; 1350 or larger. Keep the left third quiet.",
             "Contact",
             "Two desks. Either one picks up.",
             "For anything with a laycan or an ETA attached, call. It is faster than email.", short=True)
        + f'''  <section class="strip">
    <div class="wrap">
      <div class="item"><span class="lab">General &middot; chartering</span><span class="val"><a href="mailto:chartering@librashipping.nl">chartering@librashipping.nl</a></span></div>
      <div class="item"><span class="lab">General &middot; agency</span><span class="val"><a href="mailto:libra.agencies@librashipping.nl">libra.agencies@librashipping.nl</a></span></div>
      <div class="item"><span class="lab">Office</span><span class="val num"><a href="tel:+31180441151">+31 180 441 151</a></span></div>
      <div class="item"><span class="lab">Out of hours</span><span class="val num todo">[mobile 1] &middot; [mobile 2] &middot; [mobile 3]</span></div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="sechead"><h2>Rotterdam and Antwerp.</h2></div>
{OFFICES}
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sechead">
        <h2>Give us the voyage. We will come back with a number.</h2>
        <p class="muted">Name, email and cargo are all we need. The rest just helps us answer faster.</p>
        {slot("decision", "One form for both? Or a switch at the top: <em>freight enquiry</em> / <em>port call</em>. The port-call version asks for vessel, ETA, port, cargo, agent needs.")}
      </div>
      <form class="form" id="enquiry" novalidate>
        <div class="f"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
        <div class="f"><label for="company">Company</label><input id="company" name="company" type="text" autocomplete="organization"></div>
        <div class="f"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="f"><label for="phone">Telephone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="f"><label for="cargo">Cargo</label><input id="cargo" name="cargo" type="text" placeholder="Wheat, urea, steel coils&hellip;" required></div>
        <div class="f"><label for="quantity">Quantity</label><input id="quantity" name="quantity" type="text" placeholder="3,000 mt 10% moloo (500&ndash;50,000)"></div>
        <div class="f"><label for="loadport">Load port</label><input id="loadport" name="loadport" type="text"></div>
        <div class="f"><label for="dischport">Discharge port</label><input id="dischport" name="dischport" type="text"></div>
        <div class="f"><label for="laycan">Laycan</label><input id="laycan" name="laycan" type="text" placeholder="12&ndash;18 October"></div>
        <div class="f"><label for="terms">Load / discharge terms</label><input id="terms" name="terms" type="text" placeholder="1,000 mt sshex eiu"></div>
        <div class="f full"><label for="message">Anything else</label><textarea id="message" name="message"></textarea></div>
        <div class="f full">
          <p><button class="btn" type="submit">Send enquiry</button></p>
          <p class="formnote">{slot("decision", "No server yet (mailto in V1). Decide: Formspree, a small function, or what the host offers. Plus a tick-box for the conditions, as Euro Nordic has.", "inline")}</p>
        </div>
      </form>
    </div>
  </section>

'''
        + people("Or straight to one of us.", sub="Personal lines. Enquiries go to the desk mailboxes above, so they are seen whoever is in.")
    )


BUILDERS = {"index": page_index, "chartering": lambda: service_page("chartering"),
            "agency": lambda: service_page("agency"), "cargo": page_cargo,
            "about": page_about, "contact": page_contact}

for slug, label, title in PAGES:
    html = head(title) + header(slug) + BUILDERS[slug]() + FOOTER
    with open(f"{slug}.html", "w") as f:
        f.write(html)
    print("wrote", slug + ".html")
