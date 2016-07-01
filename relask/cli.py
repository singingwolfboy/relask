# -*- coding: utf-8 -*-

import os
import subprocess

import click
from flask import cli


@click.command()
@cli.pass_script_info
def init(info):
    """Initialize current app with Relask.

    :type info: cli.ScriptInfo
    """
    app = info.load_app()
    relask_dir = os.path.dirname(__file__)

    package_json = os.path.join(app.root_path, 'package.json')
    if not os.path.isfile(package_json):
        with open(package_json, 'w') as f:
            f.write('{}')

    subprocess.check_call(
        ['npm', 'install', '--save', relask_dir],
        cwd=app.root_path)

    babel_rc = os.path.join(app.root_path, '.babelrc')
    if not os.path.isfile(babel_rc):
        with open(babel_rc, 'w') as f:
            f.write('''\
{
  "presets": [
    "es2015",
    "react"
  ],
  "plugins": [
    "relask/babelRelayPlugin",
    "transform-decorators-legacy",
    "transform-class-properties"
  ]
}
''')

    webpack_config = os.path.join(app.root_path, 'webpack.config.js')
    if not os.path.isfile(webpack_config):
        with open(webpack_config, 'w') as f:
            f.write('''\
module.exports = {
    entry: './scripts/app.js',
    output: {
        path: './static',
        filename: 'app.bundle.js',
    },
    module: {
        loaders: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
        }]
    }
}
''')
