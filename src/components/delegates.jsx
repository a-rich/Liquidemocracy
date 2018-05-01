import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser } from '../actions';
import { Link } from 'react-router-dom';
import axios from 'axios';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

class Delegates extends Component {

	constructor(props) {
	    super(props);
	    this.state = {query: "",
	                  delegate: []};
	    this.handleQuery = this.handleQuery.bind(this);
	    this.retrieve_delegate = this.retrieve_delegate.bind(this);
	    this.add_delegate = this.add_delegate.bind(this);
  }

  	handleQuery(e) {
		this.setState({query: e.target.value});
	}

	retrieve_delegate(query) {
		let token = localStorage.getItem("jwt");

		const values = {
			query: query
		}

		const headers = {
			headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
			}
		}

		axios.post(`${ROOT_URL}/delegate/search/`, values, headers).then((response) => this.setState({delegate: response.data}));
	}

	add_delegate(id) {
		let token = localStorage.getItem("jwt");

		const values = {
			delegate_id: id
		}

		const headers = {
			headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
			}
		}

		axios.post(`${ROOT_URL}/delegate/add/`, values, headers)
		.then(() => {alert("Added " + this.state.delegate[0].name + " to delegates list/"); window.location.reload();});
	}

	componentWillMount() {

	}

	logout() {
		this.props.logoutUser();
		window.location.assign('https://liquidemocracy.herokuapp.com');
	}

	render() {
		return (
				<div className="container-fluid">
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
					
					<div className="row">
						<div className="col-sm-4">
							<div className="input-group">
								<input value={this.state.query} onChange={this.handleQuery} className="form-control" placeholder="Search"></input>
								<button className="btn btn-secondary" 
								onClick={() => this.retrieve_delegate(this.state.query)}>
								<i className="fas fa-search"></i>
								</button>
							</div>
							{this.state.delegate[0] != undefined ? 
								(<ul className="list-group">
									<li className="list-group-item"
									onClick={() => this.add_delegate(this.state.delegate[0]._id.$oid)} 
									key={this.state.delegate[0].id}>{this.state.delegate[0].name}
									</li></ul>) : ""}
						</div>
						<div className="col-sm-8">
						</div>
					</div>

				</div>
			)
	}

}

export default connect(null, {logoutUser})(Delegates);