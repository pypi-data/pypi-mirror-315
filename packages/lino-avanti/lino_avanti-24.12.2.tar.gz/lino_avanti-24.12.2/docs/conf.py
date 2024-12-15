# -*- coding: utf-8 -*-

from atelier.sphinxconf import configure

configure(globals())
from lino.sphinxcontrib import configure

configure(globals())

extensions += ['lino.sphinxcontrib.help_texts_extractor']
help_texts_builder_targets = {'lino_avanti.': 'lino_avanti.lib.avanti'}

project = "Lino Avanti"
copyright = '2017-2021 Rumma & Ko Ltd'
html_title = "Lino Avanti"
# html_context.update(public_url='https://avanti.lino-framework.org')
