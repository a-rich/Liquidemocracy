import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser } from '../actions';
import { Link } from 'react-router-dom';

class Delegations extends Component {

	componentWillMount() {

	}

	logout() {
		this.props.logoutUser();
		window.location.assign('https://liquidemocracy.herokuapp.com');
	}

	render() {
		return (
				<div>
				<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                <Link className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</Link>
						<Link className="nav-item" style={{color: '#ffffff'}} to="/delegates">
						 Delegates
						</Link>
						<div className="nav-item active" style={{color: '#ffffff'}}>
						 Delegations
						</div>
						<div className="nav-item" 
						 	 style={{color: '#ffffff', cursor:'pointer'}} 
						 	 onClick={() => this.logout()}>
						 Log Out
						</div>
						 	
					</nav>
					<h1 className="border border-dark text-center">Policy Areas</h1>
				</div>
			)
	}

}

export default connect(null, {logoutUser})(Delegations);