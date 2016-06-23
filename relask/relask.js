import React from "react";
import Relay from "react-relay";
import useRelay from "react-router-relay";
import {Router, browserHistory, applyRouterMiddleware} from "react-router";


export default class Relask extends React.Component {
    render() {
        return (
            <Router
                history={browserHistory}
                routes={this.props.children}
                render={applyRouterMiddleware(useRelay)}
                environment={Relay.Store}
            />
        );
    }
}
