from flask import Flask, render_template_string, abort, url_for, request
import textwrap

app = Flask(__name__)

ABOUT_IMAGE = None

FRUITS = [
    {
        'id': 'mango',
        'name': 'Mango',
        'botanical': 'Mangifera indica',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmgfExstNMpVm0dVH-xKurYdLlQpZpgJxHaw&s',
        'description': 'Mango is a tropical fruit known for its sweet, juicy flesh and aromatic flavor. It is rich in vitamins A and C, and provides dietary fiber.',
        'top_country': 'India',
        'days_to_harvest': '100 - 150 days (varies by variety)',
        'availability': 'May - September (varieties and regions differ)',
        'products': ['Juice', 'Dried mango', 'Jam', 'Pickles (achar)', 'Purees'],
        'pests': ['Mango weevil', 'Fruit flies', 'Mango seed weevil'],
        'medicinal_uses': 'Traditionally used to aid digestion, contains antioxidants that support immune health.',
        'other_uses': 'Wood used for furniture in some regions; leaves used in livestock fodder and traditional ceremonies.'
    },
    {
        'id': 'banana',
        'name': 'Banana',
        'botanical': 'Musa × paradisiaca',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSP9_eFo4cl5PcbBnw-5CAZkMx2m1aQPFTMUQ&shttps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSP9_eFo4cl5PcbBnw-5CAZkMx2m1aQPFTMUQ&s',
        'description': 'Bananas are a soft, sweet fruit eaten raw or used in cooking. They are a fast source of energy and are high in potassium and vitamin B6.',
        'top_country': 'India (largest producer), but per-capita consumption varies',
        'days_to_harvest': '9 - 12 months from planting for bunch harvest',
        'availability': 'Year-round in many tropical countries',
        'products': ['Banana chips', 'Banana bread', 'Flour', 'Baby food', 'Beer (in some cultures)'],
        'pests': ['Banana weevil', 'Nematodes', 'Thrips'],
        'medicinal_uses': 'May help soothe stomach upset; high potassium helps blood pressure management.',
        'other_uses': 'Leaves used for serving food; fibres used for textiles in some regions.'
    },
    {
        'id': 'apple',
        'name': 'Apple',
        'botanical': 'Malus domestica',
        'image': 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?auto=format&fit=crop&w=800&q=60&ixlib=rb-4.0.3',
        'description': 'Apples are temperate-climate fruits known for their crisp texture and sweet-tart flavor. They are high in fiber and vitamin C.',
        'top_country': 'China (largest producer)',
        'days_to_harvest': '100 - 200 days depending on cultivar and season',
        'availability': 'Late summer through winter for many varieties in temperate zones',
        'products': ['Cider', 'Jam', 'Sauce', 'Dried apple', 'Vinegar'],
        'pests': ['Codling moth', 'Aphids', 'Apple maggot'],
        'medicinal_uses': 'Dietary fiber supports digestion; some studies link apple consumption to reduced cardiovascular risk.',
        'other_uses': 'Ornamental rootstocks; wood used for smoking meats in cuisine.'
    },
    {
        'id': 'pineapple',
        'name': 'Pineapple',
        'botanical': 'Ananas comosus',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn3pdiM4Sr6DZfpSsK_v1JDArrjnNUi5v26w&s',
        'description': 'Pineapple is a tropical fruit praised for its vibrant sweet-tart flavor and high vitamin C content. It contains bromelain, an enzyme with digestive properties.',
        'top_country': 'Costa Rica (major exporter), Philippines, Thailand',
        'days_to_harvest': '18 - 24 months from planting to first harvest (varies by method)',
        'availability': 'Year-round in tropical producing regions, with peak seasons depending on country',
        'products': ['Canned pineapple', 'Juice', 'Dried pineapple', 'Enzyme extracts (bromelain)'],
        'pests': ['Mealybugs', 'Nematodes', 'Fruit flies'],
        'medicinal_uses': 'Bromelain may aid digestion and reduce inflammation; vitamin C helps immune function.',
        'other_uses': 'Leaves used in fiber production in some cultures; ornamental value.'
    },
    {
        'id': 'avocado',
        'name': 'Avocado',
        'botanical': 'Persea americana',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSUTLnNmBl6bn8uLnBfa3QwOPRaX6nAvpKLQ&s',
        'description': 'Avocado is a creamy-textured fruit high in healthy monounsaturated fats, fiber, potassium, and several vitamins.',
        'top_country': 'Mexico (largest producer and consumer)',
        'days_to_harvest': '6 - 12 months after flowering (varies by variety and climate)',
        'availability': 'Varies by region; many regions offer multiple harvest windows across the year',
        'products': ['Oil', 'Guacamole', 'Baby food', 'Cosmetic products'],
        'pests': ['Avocado thrips', 'Persea mites', 'Seed weevil'],
        'medicinal_uses': 'Healthy fats support heart health; contains nutrients that support vision and skin health.',
        'other_uses': 'Pit used in some crafts; leaves used in traditional medicine in some cultures.'
    }
]

# Quick lookup by id
FRUITS_BY_ID = {f['id']: f for f in FRUITS}

# === TEMPLATES ===
BASE_HTML = textwrap.dedent('''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Praise's Fruit Nutrition Blog</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <style>
      .botanical { font-style: italic; color: #555; }
      .fruit-card img { height: 180px; object-fit: cover; }
      .about-img { max-width: 220px; border-radius: 8px; }
      .tag { background:#f1f1f1; padding:4px 8px; border-radius:4px; margin-right:6px; }
      .navbar-custom { background-color: #28a745 !important; } /* Bootstrap green */
      .navbar-custom .navbar-brand,
      .navbar-custom .nav-link,
      .navbar-custom .form-control,
      .navbar-custom .btn {
        color: #fff !important;
      }
      .navbar-custom .form-control {
        background-color: #218838 !important;
        border: none;
        color: #fff !important;
      }
      .navbar-custom .btn-outline-success {
        border-color: #fff !important;
        color: #fff !important;
        background: #218838 !important;
      }
      .navbar-custom .btn-outline-success:hover {
        background: #fff !important;
        color: #28a745 !important;
      }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light navbar-custom">
      <a class="navbar-brand" href="/">Praise's Fruit Blog</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="/about">About</a></li>
        </ul>
        <form class="form-inline my-2 my-lg-0" action="/">
          <input name="q" class="form-control mr-sm-2" type="search" placeholder="Search fruits" aria-label="Search" value="{{ q|default('') }}">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>

    <div class="container mt-4">
      {{ content|safe }}
    </div>

    <footer class="text-center mt-5 mb-4 text-muted">
      &copy; {{ year }} Praise Akinwole — Nutritional tips & fruit knowledge.
    </footer>
  </body>
</html>
''')


HOME_HTML = textwrap.dedent('''
<div class="row">
  <div class="col-md-8">
    <h1>Fruits catalog</h1>
    <p class="text-muted">Browse fruit profiles — botanical name, harvest info, products and more.</p>
    <div class="row">
      {% for fruit in fruits %}
        <div class="col-md-6 mb-4">
          <div class="card fruit-card">
            <img src="{{ fruit.image }}" class="card-img-top" alt="{{ fruit.name }}">
            <div class="card-body">
              <h5 class="card-title">{{ fruit.name }} <small class="botanical">{{ fruit.botanical }}</small></h5>
              <p class="card-text">{{ fruit.description[:140] }}{% if fruit.description|length > 140 %}...{% endif %}</p>
              <a href="/fruit/{{ fruit.id }}" class="btn btn-primary btn-sm">View profile</a>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
  <div class="col-md-4">
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">About Praise</h5>
        <p class="card-text">Praise Akinwole is a nutrition-minded blogger who highlights fruit-centered tips, recipes, and the science behind nutritious choices. <a href="/about">Read more</a>.</p>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <h6 class="card-title">Quick filters</h6>
        <p class="card-text">Filter ideas (not functional filters in this demo). You can later add real filtering by season, product, or region.</p>
        <div class="mb-2">
          <span class="tag">High Vitamin C</span>
          <span class="tag">Tropical</span>
          <span class="tag">Heart-healthy</span>
        </div>
      </div>
    </div>
  </div>
</div>
''')

FRUIT_HTML = textwrap.dedent('''
<div class="row">
  <div class="col-md-8">
    <h2>{{ fruit.name }} <small class="botanical">{{ fruit.botanical }}</small></h2>
    <img src="{{ fruit.image }}" class="img-fluid mb-3" alt="{{ fruit.name }}">
    <p>{{ fruit.description }}</p>

    <dl class="row">
      <dt class="col-sm-4">Country with most consumption</dt>
      <dd class="col-sm-8">{{ fruit.top_country }}</dd>

      <dt class="col-sm-4">Time to harvest</dt>
      <dd class="col-sm-8">{{ fruit.days_to_harvest }}</dd>

      <dt class="col-sm-4">Availability</dt>
      <dd class="col-sm-8">{{ fruit.availability }}</dd>

      <dt class="col-sm-4">Products</dt>
      <dd class="col-sm-8">
        <ul>
          {% for p in fruit.products %}
            <li>{{ p }}</li>
          {% endfor %}
        </ul>
      </dd>

      <dt class="col-sm-4">Common pests</dt>
      <dd class="col-sm-8">
        <ul>
          {% for pest in fruit.pests %}
            <li>{{ pest }}</li>
          {% endfor %}
        </ul>
      </dd>

      <dt class="col-sm-4">Medicinal / health notes</dt>
      <dd class="col-sm-8">{{ fruit.medicinal_uses }}</dd>

      <dt class="col-sm-4">Other uses</dt>
      <dd class="col-sm-8">{{ fruit.other_uses }}</dd>
    </dl>
  </div>
  <div class="col-md-4">
    <div class="card mb-3">
      <div class="card-body">
        <h6 class="card-title">At a glance</h6>
        <p><strong>Harvest:</strong> {{ fruit.days_to_harvest }}</p>
        <p><strong>Peak:</strong> {{ fruit.availability }}</p>
        <p><strong>Top consumer country:</strong> {{ fruit.top_country }}</p>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <h6 class="card-title">Related reads</h6>
        <p class="card-text">You can add blog posts or tips here later — e.g., "How to pick ripe fruit" or "Preserving fruit at home".</p>
      </div>
    </div>
  </div>
</div>
''')

ABOUT_HTML = textwrap.dedent('''
<div class="row">
  <div class="col-md-8">
    <h1>About Praise Akinwole</h1>
    <p>Praise Akinwole is a nutrition-focused blogger and virtual assistant who writes about fruit-based nutrition, simple food hacks, and practical tips for healthier living. With a background in digital assistance and an eye for shareable, evidence-informed content, Praise aims to make nutritious choices easy, affordable, and delicious for readers.</p>

    <p>On this site, Praise publishes clear fruit profiles (covering botanical names, harvest timelines, common pests, nutritional and medicinal notes, and typical products made from each fruit). The goal is to empower readers — home gardeners, cooks, parents, and health-conscious individuals — to make the most of seasonal fruits and incorporate them into daily nutrition.</p>

    <p>Praise also experiments with recipes, preservation methods, and practical guides for sourcing and storing fruit in different climates. The site is designed to grow: you can expect more how-tos, printable guides, and short evidence summaries in future updates.</p>

    
    
    <div class="card" style="background-color:#90EE90;">
      <div class="card-body">
        <h6>Contact</h6>
        <p class="mb-0">Email: <a href="mailto:praiseakinwole@gmail.com">praiseakinwole@gmail.com</a></p>
        <p>Twitter: <a href="https://x.com/PraiseA25363"target="_blank">@PraiseA25363</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/praiseeakinwole/"target="_blank">linkedin.com/in/praiseeakinwole/</a></p>                     
      </div>
    </div>
  </div>
</div>
''')

# === ROUTES ===
def render_with_base(content_html, **context):
    """Helper to render content inside the base template."""
    return render_template_string(
        BASE_HTML,
        content=render_template_string(content_html, **context),
        **context
    )

@app.route('/')
def home():
    q = request.args.get('q', '').strip().lower()
    if q:
        filtered = [f for f in FRUITS if q in f['name'].lower() or q in f['botanical'].lower() or q in f['description'].lower()]
    else:
        filtered = FRUITS
    return render_with_base(HOME_HTML, fruits=filtered, q=q, year=2025)

@app.route('/fruit/<fruit_id>')
def fruit_profile(fruit_id):
    fruit = FRUITS_BY_ID.get(fruit_id)
    if not fruit:
        abort(404)
    return render_with_base(FRUIT_HTML, fruit=fruit, year=2025)

@app.route('/about')
def about():
    about_image_url = None
    if ABOUT_IMAGE:
        about_image_url = url_for('static', filename=f'uploads/{ABOUT_IMAGE}')
    return render_with_base(ABOUT_HTML, about_image_url=about_image_url, year=2025)

# === Error handlers ===
@app.errorhandler(404)
def not_found(e):
    not_found_html = "<h3>Page not found</h3><p>We couldn't find that page.</p>"
    return render_with_base(not_found_html, year=2025), 404

if __name__ == '__main__':
    app.run(debug=True)
