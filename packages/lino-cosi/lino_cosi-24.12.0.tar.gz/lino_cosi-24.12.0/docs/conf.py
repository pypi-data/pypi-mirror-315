# -*- coding: utf-8 -*-

from atelier.sphinxconf import configure

configure(globals())
from lino.sphinxcontrib import configure

configure(globals())

extensions += ["lino.sphinxcontrib.logo"]

# intersphinx_mapping['book'] = ('https://www.lino-framework.org', None)

project = "Lino Così User Guide"
html_title = "Lino Così"
import datetime

copyright = "2012-{} Rumma & Ko Ltd".format(datetime.date.today().year)

# intersphinx_mapping['cg'] = ('https://community.lino-framework.org/', None)
# intersphinx_mapping['ug'] = ('https://using.lino-framework.org/', None)

if html_theme == "insipid":
    html_theme_options = {
        # 'body_max_width': None,
        # 'breadcrumbs': True,
        "globaltoc_includehidden": False,
        "left_buttons": [
            "search-button.html",
            "home-button.html",
        ],
        "right_buttons": [
            "languages-button.html",
            "fullscreen-button.html",
            # 'repo-button.html',
            # 'facebook-button.html',
        ],
    }
