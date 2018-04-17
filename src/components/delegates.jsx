import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser } from '../actions';
import { Link } from 'react-router-dom';

class Delegates extends Component {

	componentWillMount() {

	}

	logout() {
		this.props.logoutUser();
		window.location.assign('https://liquidemocracy.herokuapp.com');

	render() {
		return (
				<div>
				<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                <Link className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</Link>
						<div className="nav-item active" style={{color: '#ffffff'}}>
						 Delegates
						</div>
						<Link className="nav-item" style={{color: '#ffffff'}} to="/delegations">
						 Delegations
						</Link>
						<div className="nav-item" 
						 	 style={{color: '#ffffff', cursor:'pointer'}} 
						 	 onClick={() => this.logout()}>
						 Log Out
						</div>
						 	
					</nav>
					<h1 className="border border-dark text-center">Delegates</h1>
				</div>
			)
	}

}

export default connect(null, {logoutUser})(Delegates);