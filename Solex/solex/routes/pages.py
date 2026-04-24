# solex/routes/pages.py
from flask import Blueprint, render_template, abort

bp = Blueprint("pages", __name__)

_PAGES = {
    "about": {"title": "About Solex",
              "intro": "Frequency, wellness, and life-force technology — for yourself and your household."},
    "events": {"title": "Events",
               "intro": "Leadership Retreat 2026 · Day of Discovery 2026 · Regional gatherings."},
    "university": {"title": "Solex University",
                   "intro": "Practitioner training, device walkthroughs, and certification paths."},
    "blog": {"title": "Blog",
             "intro": "Stories, science notes, and community dispatches."},
    "resources": {"title": "Resources",
                  "intro": "Downloads, manuals, and reference materials."},
    "privacy": {"title": "Privacy Policy", "policy": True,
                "intro": "How we collect, store, and use information."},
    "refunds": {"title": "Refund Policy", "policy": True,
                "intro": "Our refund and return terms."},
    "shipping": {"title": "Shipping Policy", "policy": True,
                 "intro": "How and when we ship orders."},
    "terms": {"title": "Terms of Use", "policy": True,
              "intro": "The terms governing use of Solex."},
}


def _view(slug):
    meta = _PAGES.get(slug)
    if meta is None:
        abort(404)
    return render_template(f"pages/{slug}.html", meta=meta)


for slug in _PAGES:
    # Closure cell capture per slug
    def _make(slug=slug):
        return lambda: _view(slug)
    bp.add_url_rule(f"/{slug}", endpoint=slug, view_func=_make(),
                    methods=["GET"])
