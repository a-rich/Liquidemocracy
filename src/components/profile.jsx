import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser } from '../actions';
import { Link } from 'react-router-dom';

class Profile extends Component {

	componentWillMount() {

	}

	logout() {
		this.props.logoutUser();
		this.props.history.push("/");
	}

	render() {
		return (
				<div>
				<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                <div className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</div>
						<Link className="nav-item active" style={{color: '#ffffff'}} to="/delegates">
						 Delegates
						</Link>
						<Link className="nav-item" style={{color: '#ffffff'}} to="/delegations">
						 Delegations
						</Link>
						<div className="nav-item" 
						 	 style={{color: '#ffffff', cursor:'pointer'}} 
						 	 onClick={() => this.logout()}>
						 Log Out
						</div>
						 	
					</nav>
					<h1 className="border border-dark text-center">Profile</h1>
				</div>
			)
	}

}

export default connect(null, {logoutUser})(Profile);