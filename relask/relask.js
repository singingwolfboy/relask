import React from "react";
import Relay from "react-relay";
import useRelay from "react-router-relay";
import {Router, browserHistory, applyRouterMiddleware, withRouter} from "react-router";
import {RelayNetworkLayer} from "react-relay-network-layer";


const SESSION_KEY = 'RELASK_BEARER';

export class Relask extends React.Component {
    componentDidMount() {
        let middlewares = [];
        if (relask_config.jwt_enabled) {
            middlewares.push(next => req => {
                let token = localStorage.getItem(SESSION_KEY);
                if (token)
                    req.headers[relask_config.jwt_header_name] =
                        relask_config.jwt_schema + ' ' + token;
                return next(req).then(res => {
                    let token = res.headers.get(relask_config.jwt_header_set_bearer);
                    if (token)
                        localStorage.setItem(SESSION_KEY, token);
                    else if (token === '')
                        localStorage.removeItem(SESSION_KEY);
                    return res;
                });
            });
        }
        Relay.injectNetworkLayer(new RelayNetworkLayer(middlewares));
    }

    render() {
        return (
            <Router
                {...this.props}
                history={this.props.history || browserHistory}
                render={applyRouterMiddleware(useRelay)}
                environment={Relay.Store}
            >
                {this.props.children}
            </Router>
        );
    }
}


export let RedirectComponent = withRouter(class extends React.Component {
    componentWillMount() {
        this.props.router.push(this.props.to);
    }

    render() {
        return this.props.children || null;
    }
});


export function RelayContainer(component) {
    return Relay.createContainer(component, component.relay);
}

export function logout() {
    localStorage.removeItem(SESSION_KEY);
}
