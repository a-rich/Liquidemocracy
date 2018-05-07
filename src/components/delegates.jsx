import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser, fetchProfile } from '../actions';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ReactModal from 'react-modal';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

const categories = ["Taxation", "Health", "Armed Forces and National Security", "Foreign Trade and International Finance", 
                    "International Affairs", "Crime and Law Enforcement", "Transportation and Public Works", 
                    "Education", "Energy", "Agriculture and Food", "Economics and Public Finance", 
                    "Labor and Employment", "Environmental Protection", "Science, Technology, Communications", 
                    "Immigration", "Other"];

class Delegates extends Component {

	constructor(props) {
	    super(props);
	    this.state = {query: "",
	                  showModal: false,
	                  delegate: [],
	                  delegates: [],
	                  category: "",
	                  dele_id: ""};
	    this.handleQuery = this.handleQuery.bind(this);
	    this.retrieve_delegate = this.retrieve_delegate.bind(this);
	    this.add_delegate = this.add_delegate.bind(this);
	    this.remove_delegate = this.remove_delegate.bind(this);
	    this.delegate_category = this.delegate_category.bind(this);
	    this.handleOpenModal = this.handleOpenModal.bind(this);
    	this.handleCloseModal = this.handleCloseModal.bind(this);
    	this.handleCloseModalOnCancel = this.handleCloseModalOnCancel.bind(this);
  }

  handleOpenModal (id) {

    	this.setState({ showModal: true, dele_id: id });
  }
  
  handleCloseModal () {

     let token = localStorage.getItem("jwt");

     const headers = {
	 headers: {
	 'Content-Type': 'application/json',
	 'Authorization': `Bearer ${token}`
		 }
	 }

	 const values = {
		 category: this.state.category,
		 delegate_id: this.state.dele_id
	 }

	 axios.post(`${ROOT_URL}/category/delegate/`, values, headers);

    this.setState({ showModal: false });
  }

  handleCloseModalOnCancel () {
  	this.setState({ showModal: false });
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

	remove_delegate(id, name) {
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

		let input = confirm("Are you sure you want to remove the delegate " + name);

		if(input == true)
		{
			axios.post(`${ROOT_URL}/delegate/remove/`, values, headers)
			.then(() => {alert(name + " removed."); window.location.reload();});
			alert(name + " removed.");
		}
		else
		{
			return;
		}

	}

	delegate_category(id, name) {

	}

	setCategory(category) {
		this.setState({category: category});
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

			axios.get(`${ROOT_URL}/retrieve_delegates/`, headers).then((response) => this.setState({delegates: response.data}));
		}
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
							<h2 className="text-center">List of Delegates</h2>
							<ul className="list-group">
				          	{ _.map(this.state.delegates, delegate => {
				          		return(<li key={Object.keys(delegate)} 
				          			className="list-group-item">{Object.values(delegate)}
				          			<button onClick={() => this.remove_delegate(Object.keys(delegate), Object.values(delegate))} 
				          					className="btn btn-danger" style={{float: 'right'}}>Remove</button>
				          			<button onClick={() => this.handleOpenModal(Object.keys(delegate))} 
				          					className="btn btn-primary" style={{float: 'right'}}>Delegate Category</button></li>);
				          	})}
				          </ul>
				          <ReactModal 
				           isOpen={this.state.showModal}
				           contentLabel="Category List"
				           onRequestClose={this.handleCloseModal}
				           shouldCloseOnOverlayClick={false}
				           ariaHideApp={false}
				           className="Modal"
				        >
				        <div className="container-fluid text-center">
				          <h3 className="text-center">Categories</h3>
				          <ul className="list-group delegate_list">
				          	{ _.map(categories, category => {
				          		return(<li className="list-group-item" key={category} 
				          			onClick={() => this.setCategory(category)}>{category}</li>);
				          	})}
				          </ul>
				          <div>Selected: {this.state.category}</div>
				          <button className="btn btn-success" onClick={this.handleCloseModal}>Submit</button>
				          <button className="btn btn-danger" onClick={this.handleCloseModalOnCancel}>Cancel</button>
				        </div>
				        </ReactModal>
						</div>
					</div>

				</div>
			)
	}

}

export default connect(null, {logoutUser, fetchProfile})(Delegates);