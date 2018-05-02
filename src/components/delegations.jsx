import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser, fetchProfile } from '../actions';
import { Link } from 'react-router-dom';
import axios from 'axios';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

class Delegations extends Component {

	constructor(props) {
	    super(props);
	    this.state = {delegations: []};
  }

	componentWillMount() {
		if(localStorage.getItem("jwt") != null)
		{
			this.props.fetchProfile();

			let token = localStorage.getItem("jwt");

			const headers = {
				headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
				}
			}

			axios.get(`${ROOT_URL}/votes/active/`, headers).then((response) => this.setState({delegations: response.data}));
		}
	}

	renderDelegations() {
		return _.map(this.state.delegations, (delegate) => {
			return _.map(delegate.bills, (bill) => {
				let color;

				switch(bill.vote) {
					case "yay":
						color = "text-success";
						break;
					case "nay":
						color = "text-danger";
						break;
					case "None":
						color = "text-warning";
						break;
				}
				return(
				<tr>
					<td>{delegate.name}</td>
					<td><Link to={`/bill/${bill.bill_id.$oid}`}>{bill.bill_title}</Link></td>
					<td className={color}>{bill.vote}</td>
				</tr>
				);
			})
		})
	}

	logout() {
		this.props.logoutUser();
		window.location.assign('https://liquidemocracy.herokuapp.com');
	}

	render() {
		if(this.state.delegations.length == 0 )
		{
			return <div className="Loader"></div>
		}
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
					<h1 className="border border-dark text-center">Bills</h1>
					<table className="table table-bordered">
						<thead>
							<tr>
								<th scope="col">Delegate</th>
								<th scope="col">Bill</th>
								<th scope="col">Vote</th>
							</tr>
						</thead>
						<tbody>
							{this.renderDelegations()}
						</tbody>
					</table>
				</div>
			)
	}

}

export default connect(null, {logoutUser, fetchProfile})(Delegations);