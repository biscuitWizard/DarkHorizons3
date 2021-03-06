"""
Evennia settings file.

The available options are found in the default settings file found
here:

/srv/games/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *
from django.db import models

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Dark_horizons_3"

# Activate telnet service
TELNET_ENABLED = True

# A list of ports the Evennia telnet server listens on Can be one or many.
TELNET_PORTS = [4000]

# The webserver sits behind a Portal proxy. This is a list
# of tuples (proxyport,serverport) used. The proxyports are what
# the Portal proxy presents to the world. The serverports are
# the internal ports the proxy uses to forward data to the Server-side
# webserver (these should not be publicly open)
WEBSERVER_PORTS = [(8000, 5001)]

# Start the evennia webclient. This requires the webserver to be running and
# offers the fallback ajax-based webclient backbone for browsers not supporting
# the websocket one.
WEBCLIENT_ENABLED = True

# Activate SSL protocol (SecureSocketLibrary)
SSL_ENABLED = False

# Ports to use for SSL
SSL_PORTS = [4001]

######################################################################
# Django web features
######################################################################


# The secret key is randomly seeded upon creation. It is used to sign
# Django's cookies. Do not share this with anyone. Changing it will
# log out all active web browsing sessions. Game web client sessions
# may survive.
SECRET_KEY = '%-?S"7FKtgvhCVDzfMR8uN;=,_"L5iwAGY#*|j3n'

INSTALLED_APPS = INSTALLED_APPS + ("gamedb", )
