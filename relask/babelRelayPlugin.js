var babelRelayPlugin = require('babel-relay-plugin');
var schema = JSON.parse(process.env.RELASK_SCHEMA);

module.exports = babelRelayPlugin(schema, {
    abortOnError: true
});
