import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
#translate = gettext.translation('emotion-diary-bot', localedir, fallback=True)
en = gettext.translation('en', localedir, fallback=True, languages=['en'])
ru = gettext.translation('ru', localedir, fallback=True, languages=['ru'])
en.install()
_ = ru.gettext
