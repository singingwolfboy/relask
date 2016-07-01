import React from "react";
import Relay from "react-relay";
import {RelayContainer, RedirectComponent} from "babel-loader!relask";
import {BasePage} from "../common";


class LoginMutation extends Relay.Mutation {
    getMutation() {
        return Relay.QL`mutation { login }`;
    }

    getVariables() {
        return {
            login: this.props.login,
            password: this.props.password
        }
    }

    getFatQuery() {
        return Relay.QL`fragment on LoginMutationPayload {
            viewer {
                currentUser,
                isAuthenticated,
                contact
            },
            msg
        }`
    }

    getConfigs() {
        return [{
            type: 'FIELDS_CHANGE',
            fieldIDs: {
                viewer: this.props.viewer.id,
                msg: null
            }
        }];
    }

    static fragments = {
        viewer: () => Relay.QL`
            fragment on Viewer {
                id,
            }
        `
    };
}

@RelayContainer
export default class Login extends React.Component {
    static relay = {
        fragments: {
            viewer: () => Relay.QL`fragment on Viewer {
                isAuthenticated,
                ${BasePage.getFragment('viewer')},
                ${LoginMutation.getFragment('viewer')}
            }`
        }
    };

    constructor(props, context) {
        super(props, context);
        this.state = {
            msg: ''
        };
    }

    submitLogin() {
        this.props.relay.commitUpdate(new LoginMutation({
            viewer: this.props.viewer,
            login: this.refs.login.value,
            password: this.refs.password.value
        }), {onSuccess: resp => {
            this.setState({msg: resp.login.msg});
        }});
    }

    render() {
        if (this.props.viewer.isAuthenticated) {
            return (
                <BasePage viewer={this.props.viewer}>
                    {this.state.msg}
                    <RedirectComponent to={this.props.location.query.next}/>
                </BasePage>
            );
        } else
            return (
                <BasePage viewer={this.props.viewer}>
                    <p>Please login:</p>
                    <label for="login">Login</label>
                    <input type="text" name="login" ref="login"/>
                    <br/>
                    <label for="password">Password</label>
                    <input type="password" name="password" ref="password"/>
                    <br/>
                    {this.state.msg}
                    <br/>
                    <button onClick={this.submitLogin.bind(this)}>Submit</button>
                </BasePage>
            )
    }
}
