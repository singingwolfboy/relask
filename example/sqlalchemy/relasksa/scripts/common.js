import React from "react";
import Relay from "react-relay";
import {Link, withRouter} from "react-router";
import {RelayContainer, logout} from "babel-loader!relask";


@RelayContainer
export let BasePage = withRouter(class extends React.Component {
    static relay = {
        fragments: {
            viewer: () => Relay.QL`fragment on Viewer {
                website,
                contact { 
                    name 
                },
                currentUser {
                    name,
                    email
                },
                isAuthenticated
            }`
        }
    };

    logout() {
        logout();
        location.reload();
    }

    render() {
        let accountInfo = this.props.viewer.isAuthenticated ? (
            <div>
                <p>Welcome, {this.props.viewer.currentUser.name}</p>
                <p>Your email is: {this.props.viewer.currentUser.email}</p>
                <button onClick={this.logout.bind(this)}>Logout</button>
            </div>
        ) : null;
        return (
            <div>
                <h1><Link to="/">{this.props.viewer.contact.name}</Link></h1>
                <p><a href={this.props.viewer.website}>{this.props.viewer.website}</a></p>
                {accountInfo}
                {this.props.children}
            </div>
        );
    }
});
