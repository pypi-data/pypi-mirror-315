#
# The path for the modules loaded needs to be in PYTHONPATH. For instance:
# export PYTHONPATH="$PYTHONPATH:/var/www/siteX/server_modules"
#
# Below is an example of a configuration.  The files `index.md`,
# `index_import.py` and `index.tsl` needs to be created. See the 
# documentation for more information.
#

from tsl.server import create_app

app = create_app('./index.md',            # index_file
                 '/var/www/tsldb',        # tslfolder
                 'duckdb',                # tslbackend
                 'tsldb',                 # tsldbname
                 './index_imports',       # pyfile
                 './index',               # tslscript
                 None                     # custom modules
      )

app.run()
