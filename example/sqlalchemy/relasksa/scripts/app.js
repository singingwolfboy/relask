import React from "react";
import ReactDOM from "react-dom";
import {Route, IndexRoute, Link} from "react-router";
import Relay from "react-relay";
import {Relask, RedirectComponent} from "babel-loader!relask";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Contact from "./pages/Contact";


const props = {
    queries: {viewer: () => Relay.QL` query { viewer }`},
    render: ({done, element, error, events, props, retry, routerProps, stale}) => {
        if (error) {
            for (let e of error.source.errors) {
                if (e.message == '401: Unauthorized') {
                    return <RedirectComponent to={'/login?next=' + routerProps.location.pathname}/>;
                } else if (e.message == '403: Forbidden') {
                    return (
                        <div>
                            <h1>Forbidden</h1>
                            <p>Access denied.</p>
                        </div>
                    );
                }
            }
        } else if (props) {
            return React.cloneElement(element, props);
        } else {
            return (<div>Loading</div>);
        }
    }
};

ReactDOM.render((
    <Relask>
        <Route path="/">
            <IndexRoute {...props} component={Index}/>
            <Route {...props} path="/login" component={Login}/>
            <Route {...props} path="/contact" component={Contact}/>
        </Route>
    </Relask>
), document.getElementById('app'));
