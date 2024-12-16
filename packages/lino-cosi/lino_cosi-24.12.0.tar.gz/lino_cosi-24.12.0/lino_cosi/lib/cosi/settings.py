# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Default settings module for a :ref:`cosi` project.

"""

from lino_cosi import __version__
from lino.projects.std.settings import *


class Site(Site):
    """Base class for a :ref:`cosi` application."""

    verbose_name = "Lino Così"
    version = __version__

    # migrations_package = 'lino_cosi.lib.cosi'

    demo_fixtures = "std minimal_ledger \
    furniture demo demo2 demo3 checkdata".split()

    # languages = 'en de fr'
    languages = "en"

    # use_shopping = False
    # """Whether to install the shopping plugin."""

    user_types_module = "lino_cosi.lib.cosi.user_types"
    custom_layouts_module = "lino_cosi.lib.cosi.layouts"

    default_build_method = "weasy2pdf"

    # textfield_format = 'html'

    def get_installed_plugins(self):
        yield super().get_installed_plugins()
        yield "lino_cosi.lib.users"
        yield "lino.modlib.gfks"
        # yield 'lino.modlib.system'
        yield "lino.modlib.help"
        yield "lino_xl.lib.countries"
        yield "lino_cosi.lib.contacts"
        # ~ yield 'lino_xl.lib.households'
        yield "lino_xl.lib.phones"

        yield "lino_xl.lib.excerpts"

        # yield 'lino_xl.lib.outbox'
        yield "lino.modlib.uploads"
        # yield 'lino.modlib.files'
        yield "lino.modlib.weasyprint"
        yield "lino.modlib.export_excel"
        yield "lino.modlib.tinymce"
        # yield 'lino.modlib.wkhtmltopdf'

        # accounting must come before trading because its demo fixture
        # creates journals (?)
        yield "lino_xl.lib.accounting"
        yield "lino_xl.lib.sepa"
        # yield 'lino_xl.lib.vat'
        yield "lino_cosi.lib.products"
        yield "lino_cosi.lib.trading"
        yield "lino_xl.lib.invoicing"
        yield "lino_xl.lib.finan"
        # yield 'lino_xl.lib.bevat'
        yield "lino_xl.lib.sheets"
        # if self.use_shopping:
        #     yield 'lino_xl.lib.shopping'
        # ~ 'lino.modlib.journals',
        # ~ 'lino_xl.lib.projects',
        # ~ yield 'lino_xl.lib.blogs'
        # ~ yield 'lino.modlib.tickets'
        # ~ 'lino.modlib.links',
        # ~ 'lino_xl.lib.thirds',
        # ~ yield 'lino_xl.lib.postings'
        # yield 'lino_xl.lib.pages'
        # yield 'lino_cosi.lib.cosi'

    def get_plugin_configs(self):
        """
        Change the default value of certain plugin settings.

        """
        yield super().get_plugin_configs()
        yield ("countries", "hide_region", True)
        yield ("countries", "country_code", "BE")
        yield ("accounting", "use_pcmn", True)
        yield ("products", "menu_group", "trading")
        # if self.get_plugin_setting('accounting', 'has_payment_methods'):
        #     # yield ('invoicing', 'voucher_model', 'trading.CashInvoice')
        #     yield ('invoicing', 'voucher_type', 'trading.CashInvoicesByJournal')
