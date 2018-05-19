import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser, fetchProfile } from '../actions';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Alert from 'react-s-alert';

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
						color = "text-muted";
						break;
				}
				return(
				<tr>
					<td>{delegate.name}</td>
					<td><Link to={`/bill/${bill.bill_id.$oid}`}>{bill.bill_title}</Link></td>
					<td className={color}>{bill.vote}</td>
					<td><button className="btn btn-sm btn-danger"
					onClick={
					() => this.remove_bill_delegation(bill.bill_id.$oid, delegate.user_id.$oid, delegate.name, bill.bill_title)}>
					Remove</button></td>
				</tr>
				);
			})
		})
	}

	renderCategories() {
		return _.map(this.state.delegations, (delegate) => {
			return _.map(delegate.categories, (category) => {
				return (
				<tr>
					<td>{delegate.name}</td>
					<td>{category}</td>
					<td><button className="btn btn-sm btn-danger"
					onClick={
					() => this.remove_category_delegation(category, delegate.user_id.$oid, delegate.name)}>
					Remove</button></td>
				</tr>
				);
			})
		})
	}

	remove_bill_delegation(bill_id, delegate_id, name, bill_title) {
		let token = localStorage.getItem("jwt");

		const values = {
			'item': bill_id,
			'type': "bill",
			'delegate': delegate_id
		}

		const headers = {
			headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
			}
		}

		let input = confirm("Are you sure you want to remove the delegate " + name + " from bill: " + bill_title);

		if(input == true)
		{
			axios.post(`${ROOT_URL}/remove/delegation/`, values, headers)
			.then(() => {let msg = name + " removed.";
				Alert.success(msg, {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.reload();
    								}
								});
			});
		}
		else
		{
			return;
		}
	}

	remove_category_delegation(category, delegate_id, name) {
		let token = localStorage.getItem("jwt");

		const values = {
			'item': category,
			'type': "category",
			'delegate': delegate_id
		}

		const headers = {
			headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
			}
		}

		let input = confirm("Are you sure you want to remove the delegate " + name + " from category: " + category);

		if(input == true)
		{
			axios.post(`${ROOT_URL}/remove/delegation/`, values, headers)
			.then(() => {let msg = name + " removed.";
				Alert.success(msg, {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.reload();
    								}
								});
			});
		}
		else
		{
			return;
		}
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
					<h1 className="text-center customH1"><span className="customSpan">Categories</span></h1>
					<table className="table table-bordered">
						<thead>
							<tr>
								<th scope="col">Delegate</th>
								<th scope="col">Category</th>
								<th scope="col">Remove</th>
							</tr>
						</thead>
						<tbody>
							{this.renderCategories()}
						</tbody>
					</table>
					<h1 className="text-center customH1"><span className="customSpan">Bills</span></h1>
					<table className="table table-bordered">
						<thead>
							<tr>
								<th scope="col">Delegate</th>
								<th scope="col">Bill</th>
								<th scope="col">Vote</th>
								<th scope="col">Remove</th>
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
