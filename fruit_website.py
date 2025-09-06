from flask import Flask, render_template_string, abort, url_for, request, make_response
import textwrap

app = Flask(__name__)

# You do NOT need to set the image URL manually.
# Just place your image file 'Me.png' in static/uploads/ and this will work.
ABOUT_IMAGE = 'Me.png'  # Only the filename, not a path or URL

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
    },
    {
        'id': 'orange',
        'name': 'Orange',
        'botanical': 'Citrus × sinensis',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmJ2h1VoRLj9jgkstAS7Sy-3aj-3nggDo5Cg&s',
        'description': 'Oranges are citrus fruits known for their bright color and sweet-tart flavor. They are an excellent source of vitamin C and dietary fiber.',
        'top_country': 'Brazil (largest producer)',
        'days_to_harvest': '7 - 15 months depending on variety and climate',
        'availability': 'Winter through spring in many temperate regions',
        'products': ['Juice', 'Marmalade', 'Essential oils', 'Candied peel'],
        'pests': ['Citrus leafminer', 'Aphids', 'Citrus psyllid'],
        'medicinal_uses': 'High vitamin C content supports immune health; antioxidants may reduce inflammation.',
        'other_uses': 'Peel used for zest in cooking; essential oils used in aromatherapy and cleaning products.'
    },    
    {    
        'id': 'strawberry',
        'name': 'Strawberry',
        'botanical': 'Fragaria × ananassa',
        'image': 'https://fruitsandveggies.org/wp-content/uploads/2007/01/jacek-dylag-559115-unsplash-1440x658.jpg',
        'description': 'Strawberries are bright red, juicy fruits known for their sweet flavor and high vitamin C content. They also provide dietary fiber and antioxidants.',
        'top_country': 'United States (California is a major producer)',
        'days_to_harvest': '4 - 6 weeks from flowering to fruiting',
        'availability': 'Spring and early summer in temperate regions; year-round in some climates with multiple harvests',
        'products': ['Jam', 'Desserts', 'Smoothies', 'Dried strawberries'],
        'pests': ['Aphids', 'Spider mites', 'Slugs'],
        'medicinal_uses': 'Rich in antioxidants and vitamin C, which support immune health and skin health.',
        'other_uses': 'Leaves used in teas; flowers attract pollinators in gardens.'
    },
    {
        'id': 'grape',
        'name': 'Grape',
        'botanical': 'Vitis vinifera',
        'image': 'https://cdn.pixabay.com/photo/2021/01/05/05/30/grapes-5889697_1280.jpg',
        'description': 'Grapes are small, juicy berries that grow in clusters and come in red, green, and black varieties. They are rich in antioxidants, especially resveratrol.',
        'top_country': 'China (largest producer)',
        'days_to_harvest': '150 - 180 days after flowering',
        'availability': 'Summer to early autumn in most regions',
        'products': ['Wine', 'Raisins', 'Juice', 'Jelly'],
        'pests': ['Grape berry moth', 'Powdery mildew', 'Phylloxera'],
        'medicinal_uses': 'Resveratrol supports heart health; antioxidants protect against oxidative stress.',
        'other_uses': 'Leaves used in cooking (e.g., stuffed grape leaves in Mediterranean cuisine).'
    },
    {
        'id': 'papaya',
        'name': 'Papaya',
        'botanical': 'Carica papaya',
        'image': 'https://plantura.garden/uk/wp-content/uploads/sites/2/2022/06/eating-papaya.jpg',
        'description': 'Papayas are tropical fruits with orange flesh and black seeds. They are high in vitamin C, folate, and the digestive enzyme papain.',
        'top_country': 'India (largest producer)',
        'days_to_harvest': '6 - 12 months after planting',
        'availability': 'Available year-round in tropical climates',
        'products': ['Juice', 'Dried papaya', 'Papain enzyme', 'Candied papaya'],
        'pests': ['Fruit flies', 'Aphids', 'Whiteflies'],
        'medicinal_uses': 'Papain enzyme aids digestion; rich in antioxidants and vitamin C for immunity.',
        'other_uses': 'Papain used in meat tenderizers; seeds sometimes used as a natural dewormer.'
    },
    {
        'id': 'pear',
        'name': 'Pear',
        'botanical': 'Pyrus communis',
        'image': 'https://images.healthshots.com/healthshots/en/uploads/2022/12/16102013/pear-for-skincare.jpg',
        'description': 'Pears are sweet, bell-shaped fruits with soft, juicy flesh. They are a good source of dietary fiber, vitamin C, and potassium.',
        'top_country': 'China (largest producer)',
        'days_to_harvest': '90 - 150 days depending on variety',
        'availability': 'Late summer through winter depending on variety',
        'products': ['Juice', 'Jam', 'Canned pears', 'Desserts'],
        'pests': ['Pear psylla', 'Codling moth', 'Pear leaf blister mite'],
        'medicinal_uses': 'High fiber supports digestion and heart health; antioxidants may reduce inflammation.',
        'other_uses': 'Wood used in fine furniture and musical instruments.'
    },
    {
        'id': 'kiwi',
        'name': 'Kiwi',
        'botanical': 'Actinidia deliciosa',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Kiwi_aka.jpg',
        'description': 'Kiwis are small, brown-skinned fruits with bright green or yellow flesh and tiny black seeds. They are rich in vitamin C and dietary fiber.',
        'top_country': 'China (native and largest producer)',
        'days_to_harvest': '6 - 7 months after flowering',
        'availability': 'Autumn and winter in temperate regions',
        'products': ['Juice', 'Dried kiwi', 'Jam', 'Desserts'],
        'pests': ['Armored scale insects', 'Leafrollers', 'Root-knot nematodes'],
        'medicinal_uses': 'Vitamin C supports immunity; fiber aids digestion and heart health.',
        'other_uses': 'Extract used in skincare for its antioxidant properties.'
    },
    {
        'id': 'watermelon',
        'name': 'Watermelon',
        'botanical': 'Citrullus lanatus',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoHLnenQKdhz19ApHVgb0SSfziDN3YDBmLQg&s',
        'description': 'Watermelons are large, refreshing fruits with high water content and sweet red or yellow flesh. They are an excellent source of hydration and contain lycopene.',
        'top_country': 'China (largest producer)',
        'days_to_harvest': '70 - 100 days from planting',
        'availability': 'Summer in most regions',
        'products': ['Juice', 'Sorbet', 'Pickled rind'],
        'pests': ['Cucumber beetles', 'Aphids', 'Fusarium wilt'],
        'medicinal_uses': 'Lycopene supports heart health; high water content helps hydration.',
        'other_uses': 'Seeds roasted as snacks; rind sometimes used in preserves.'
    },
    {
        'id': 'pomegranate',
        'name': 'Pomegranate',
        'botanical': 'Punica granatum',
        'image': 'https://images.indianexpress.com/2022/09/pomegranate_1200_getty.jpg?w=414',
        'description': 'Pomegranates are round fruits with tough red skin and clusters of juicy, ruby-red seeds called arils. They are rich in antioxidants and vitamin C.',
        'top_country': 'India and Iran (major producers)',
        'days_to_harvest': '5 - 7 months after flowering',
        'availability': 'Autumn and winter in temperate regions',
        'products': ['Juice', 'Molasses', 'Dried arils', 'Syrup'],
        'pests': ['Fruit borers', 'Aphids', 'Whiteflies'],
        'medicinal_uses': 'Polyphenols support heart health and may reduce inflammation.',
        'other_uses': 'Peel used in tanning leather and natural dyes.'
    },
    {
        'id': 'guava',
        'name': 'Guava',
        'botanical': 'Psidium guajava',
        'image': 'data:image/jpeg;base64,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',
        'description': 'Guavas are tropical fruits with green or yellow skin and pink or white flesh. They are rich in vitamin C, fiber, and antioxidants.',
        'top_country': 'India (largest producer)',
        'days_to_harvest': '4 - 8 months depending on season and climate',
        'availability': 'Year-round in tropical regions',
        'products': ['Juice', 'Jam', 'Candies', 'Dried guava'],
        'pests': ['Fruit flies', 'Aphids', 'Scale insects'],
        'medicinal_uses': 'Vitamin C supports immunity; leaves traditionally used to treat diarrhea.',
        'other_uses': 'Leaves used for herbal teas; wood used for fuel and tool handles.'
    }
  
]

FRUITS_BY_ID = {f['id']: f for f in FRUITS}

BASE_HTML = textwrap.dedent('''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Praise's Fruit Nutrition Blog</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
    <style>
      body.light-theme {
        background: #fff;
        color: #212529;
      }
      body.dark-theme {
        background: #181a1b;
        color: #e0e0e0;
      }
      .navbar-custom.light-theme {
        background-color: #28a745 !important;
      }
      .navbar-custom.dark-theme {
        background-color: #222 !important;
      }
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
      .card.light-theme { background: #fff; color: #212529; }
      .card.dark-theme { background: #23272b; color: #e0e0e0; }
      .botanical { font-style: italic; color: #555; }
      .fruit-card img { height: 180px; object-fit: cover; }
      .about-img { max-width: 220px; border-radius: 8px; }
      .tag { background:#f1f1f1; padding:4px 8px; border-radius:4px; margin-right:6px; }
      .tag.dark-theme { background: #333; color: #fff; }
      .footer.light-theme { color: #888; }
      .footer.dark-theme { color: #aaa; }
      .theme-toggle-btn {
        margin-left: 1rem;
        border: none;
        background: transparent;
        color: #fff;
        font-weight: bold;
        cursor: pointer;
      }
    </style>
    <script>
      // Theme toggle logic
      function setTheme(theme) {
        document.body.className = theme + '-theme';
        document.querySelector('.navbar-custom').className = 'navbar navbar-expand-lg navbar-light navbar-custom ' + theme + '-theme';
        document.querySelectorAll('.card').forEach(function(card) {
          card.classList.remove('light-theme', 'dark-theme');
          card.classList.add(theme + '-theme');
        });
        document.querySelectorAll('.tag').forEach(function(tag) {
          tag.classList.remove('light-theme', 'dark-theme');
          tag.classList.add(theme + '-theme');
        });
        document.querySelector('.footer').className = 'text-center mt-5 mb-4 footer ' + theme + '-theme';
        document.cookie = "theme=" + theme + ";path=/";
      }
      function getThemeFromCookie() {
        var match = document.cookie.match(/theme=(light|dark)/);
        return match ? match[1] : 'light';
      }
      window.addEventListener('DOMContentLoaded', function() {
        var theme = getThemeFromCookie();
        setTheme(theme);
        document.getElementById('theme-toggle').onclick = function() {
          var newTheme = (getThemeFromCookie() === 'light') ? 'dark' : 'light';
          setTheme(newTheme);
        };
      });
    </script>
  </head>
  <body class="light-theme">
    <nav class="navbar navbar-expand-lg navbar-light navbar-custom light-theme">
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
        <button id="theme-toggle" class="theme-toggle-btn" title="Toggle theme">🌙</button>
      </div>
    </nav>

    <div class="container mt-4">
      {{ content|safe }}
    </div>

    <!-- AI Agent Chatbot Widget -->
    <elevenlabs-convai agent-id="agent_3201k49xk37qe2nae4w8nhp2chm1"></elevenlabs-convai>
    <script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>

    <footer class="text-center mt-5 mb-4 footer light-theme">
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
          <div class="card light-theme">
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
    <div class="card mb-3 light-theme">
      <div class="card-body">
        <h5 class="card-title">About Praise</h5>
        <p class="card-text">Praise Akinwole is a nutrition-minded blogger who highlights fruit-centered tips, recipes, and the science behind nutritious choices. <a href="/about">Read more</a>.</p>
      </div>
    </div>
    <div class="card light-theme">
      <div class="card-body">
        <h6 class="card-title">Quick filters</h6>
        <p class="card-text">Filter ideas (not functional filters in this demo). You can later add real filtering by season, product, or region.</p>
        <div class="mb-2">
          <span class="tag light-theme">High Vitamin C</span>
          <span class="tag light-theme">Tropical</span>
          <span class="tag light-theme">Heart-healthy</span>
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
    <div class="card mb-3 light-theme">
      <div class="card-body">
        <h6 class="card-title">At a glance</h6>
        <p><strong>Harvest:</strong> {{ fruit.days_to_harvest }}</p>
        <p><strong>Peak:</strong> {{ fruit.availability }}</p>
        <p><strong>Top consumer country:</strong> {{ fruit.top_country }}</p>
      </div>
    </div>

    <!--
                             <div class="card light-theme">
      <div class="card-body">
        <h6 class="card-title">Related reads</h6>
        <p class="card-text">You can add blog posts or tips here later — e.g., "How to pick ripe fruit" or "Preserving fruit at home".</p> 
                             -->
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
  </div>
  <div class="col-md-4 text-center">
    {% if about_image_url %}
      <img src="{{ about_image_url }}" class="about-img mb-3" alt="Praise Akinwole">
    {% else %}
      <div class="border p-4 mb-3">
        <p><strong>Image placeholder</strong></p>
        <p class="text-muted">Add your image to <code>static/uploads/</code> and set <code>ABOUT_IMAGE</code> in the script to the filename (e.g. <code>Me.png</code>) or a direct image URL.</p>
      </div>
    {% endif %}

    <div class="card light-theme" style="background-color:#90EE90;">
      <div class="card-body">
        <h6><b>Contact</b></h6>
        <p class="mb-0">Email: <a href="mailto:praiseakinwole@gmail.com">praiseakinwole@gmail.com</a></p>
        <p>Twitter: <a href="https://x.com/PraiseA25363" target="_blank">@PraiseA25363</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/praiseeakinwole/" target="_blank">linkedin.com/in/praiseeakinwole/</a></p>
        </div>
    </div>
  </div>
</div>
''')

def get_about_image_url():
    if ABOUT_IMAGE and (ABOUT_IMAGE.startswith('http://') or ABOUT_IMAGE.startswith('https://')):
        return ABOUT_IMAGE
    elif ABOUT_IMAGE:
        return url_for('static', filename=f'uploads/{ABOUT_IMAGE}')
    return None

def render_with_base(content_html, **context):
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
    about_image_url = get_about_image_url()
    return render_with_base(ABOUT_HTML, about_image_url=about_image_url, year=2025)

@app.errorhandler(404)
def not_found(e):
    not_found_html = "<h3>Page not found</h3><p>We couldn't find that page.</p>"
    return render_with_base(not_found_html, year=2025), 404

if __name__ == '__main__':
    app.run(debug=True)
