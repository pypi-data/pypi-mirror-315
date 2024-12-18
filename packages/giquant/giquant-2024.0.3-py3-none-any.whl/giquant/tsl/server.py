#!/usr/bin/env python3
#
# NOTE: `flask run` does not work. Local modules are *not* found!
#
# Resources:
# - https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
#

import os
import re
import sys
import argparse
import importlib

from flask import Flask
from flask_misaka import Misaka

from pathlib import Path


def create_args_parser():
  parser = argparse.ArgumentParser(prog='server.py', description='Start web server.')
  parser.add_argument('folder',       help='Folder with tsl data.')
  parser.add_argument('index_file',   help='Markdown file to use as first page.')
  parser.add_argument('--modules',    help='Modules to load. These are implemented as Flask Blueprints.')
  parser.add_argument('--backend',    help='Backend to use. Supported are: parquet, duckdb and csv]', default='parquet')
  parser.add_argument('--dbname',     help='Name of database (used as filename for duckdb)', default='tsldb')
  parser.add_argument('--py',         help='Python file to import. Functions that can be used in FUNC items (as part of expressions)')
  parser.add_argument('--tsl',        help='Script with tsl, ie. expr, gg or sql statements.')
  return parser

def create_app():
  parser = create_args_parser()
  args = parser.parse_args()
  print(args)

  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.environ['SERVER_SECRET_KEY']
  Misaka(app)

  # POST request have no data when this is enabled!
  #from flask_wtf.csrf import CSRFProtect
  #csrf = CSRFProtect(app)

  app.config.update(
    INDEX_FILE = args.index_file,
    INDEX_PAGE = Path(args.index_file).read_text(),
    TSLFOLDER  = args.folder,
    TSLBACKEND = args.backend,
    TSLDBNAME  = args.dbname,
    PYFILE     = args.py,
    TSLSCRIPT  = args.tsl
  )

  import tsl.index
  app.register_blueprint(tsl.index.route)

  if not args.modules is None:
    mods = []
    for module in args.modules.split(','):
      mod = importlib.import_module(module)
      app.register_blueprint(mod.route)
      mods.append(mod)
    print(f'Loaded: {mods}')

  return app

if __name__ == '__main__':
  app = create_app()    
  app.run() 

