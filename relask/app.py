# -*- coding: utf-8 -*-

import atexit
import json
import os
import subprocess

import flask
import graphene
from flask_graphql import GraphQLView


class Relask(object):
    def __init__(self, app=None, blueprint_options=None):
        self._schema = graphene.Schema()
        self._webpack = None
        if blueprint_options is None:
            blueprint_options = {}
        self._blueprint_options = blueprint_options
        self._blueprint = self._create_blueprint()
        self._add_url_rules()
        self.jwt = None
        if app is not None:
            self.init_app(app)

    @property
    def schema(self):
        return self._schema

    @property
    def blueprint_options(self):
        return self._blueprint_options

    @property
    def blueprint(self):
        return self._blueprint

    def init_app(self, app):
        """
        :type app: flask.Flask
        """
        app.register_blueprint(self.blueprint, **self.blueprint_options)
        flask.request_started.connect(self._run_webpack, app)
        if app.config.get('JWT_ENABLED', True):
            from .jwt import JWTSessionInterface
            self.jwt = JWTSessionInterface(app)

    # noinspection PyMethodMayBeStatic
    def index_view(self, path='/'):
        conf = {}
        if self.jwt:
            conf.update(
                jwt_header_name=self.jwt.header_name,
                jwt_schema=self.jwt.schema,
                jwt_header_set_bearer=self.jwt.header_set_bearer,
            )
        conf['jwt_enabled'] = bool(self.jwt)
        return flask.render_template('relask/index.html', relask_config=conf)

    # noinspection PyMethodMayBeStatic
    def _create_blueprint(self):
        return flask.Blueprint('relask', __name__,
                               template_folder='templates')

    def _add_url_rules(self):
        self.blueprint.add_url_rule('/', view_func=self.index_view)
        self.blueprint.add_url_rule('/<path:path>', view_func=self.index_view)
        self.blueprint.add_url_rule(
            '/graphql', view_func=GraphQLView.as_view(
                'graphql', schema=self.schema))

    # noinspection PyUnusedLocal
    def _run_webpack(self, sender, **extra):
        if flask.request.path != flask.url_for('static',
                                               filename='app.bundle.js'):
            return
        if self._webpack is not None:
            return

        query = subprocess.check_output(
            ['node', '-e',
             'console.log(require("graphql/utilities").introspectionQuery)'],
            cwd=flask.current_app.root_path,
        )
        schema = self.schema.execute(query.decode('utf-8'))
        env = os.environ.copy()
        env['RELASK_SCHEMA'] = json.dumps(schema.data)
        subprocess.check_call(['node_modules/webpack/bin/webpack.js'], env=env,
                              cwd=flask.current_app.root_path)
        self._webpack = subprocess.Popen(['webpack', '--watch'], env=env,
                                         cwd=flask.current_app.root_path)
        atexit.register(self._teardown)

    def _teardown(self, **extra):
        if self._webpack is None:
            return
        self._webpack.terminate()
        self._webpack = None
