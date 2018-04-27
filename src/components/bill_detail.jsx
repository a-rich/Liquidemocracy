import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { fetchBill, logoutUser, loginUser, fetchProfile } from '../actions';
import { connect } from 'react-redux';
import { Field, reduxForm, SubmissionError} from 'redux-form';
import axios from 'axios';
import ReactModal from 'react-modal';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

class BillDetail extends Component {
	constructor(props) {
	    super(props);
	    this.state = {button: "",
	                  showModal: false,
	                  delegates: [],
	                  email: "",
	                  dele_id: "",
	                  name: "",
	                  error_message: ""};

    	this.handleOpenModal = this.handleOpenModal.bind(this);
    	this.handleCloseModal = this.handleCloseModal.bind(this);
  }

    handleOpenModal () {
    	this.setState({ showModal: true });
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
			delegate: this.state.dele_id,
			bill_id: this.props.match.params.id
		}

		axios.post(`${ROOT_URL}/bill/delegate/`, values, headers);

    	this.setState({ showModal: false });
  }
  

  	renderField(field) {
		const { touched , error }  = field.meta;
		const className = `form-control ${touched && error ? 'border border-danger' : ''}`;
		let type;

		return (
				<div className="form-group">
					<input
						className={ className }
						type={field.type}
						placeholder={field.label}
						{...field.input}
					/>
					<div className="text-help" style={{color: '#B80000'}}>
					{touched ? error : ''}
					</div>
				</div>
			);
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

	componentDidMount() {
		if(localStorage.getItem("jwt") == null) {
			this.setState({button: "disabled"});
		}
		else {
			this.setState({button: ""});
		}

		this.props.fetchBill(this.props.match.params.id, this.state.email);	
	}

	logout() {
		this.props.logoutUser();
		window.location.assign('https://liquidemocracy.herokuapp.com');
	}

	voteYay() {

		if(this.state.button == "disabled")
		{
			return;
		}

		const token = localStorage.getItem("jwt");

		const value = {
			'bill_id': this.props.match.params.id,
			'vote': 'yay'
		}

		const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
			}
		}

		axios.post(`${ROOT_URL}/bill/vote/`, value, headers)
		.then((response) => {if(response.data.msg == "You have already cast a vote on this bill."){this.setState({error_message: "You have already cast a vote on this bill."})}
							 else{location.reload()}});
	}

	voteNay() {

		if(this.state.button == "disabled")
		{
			return;
		}

		const token = localStorage.getItem("jwt");

		const value = {
			'bill_id': this.props.match.params.id,
			'vote': 'nay'
		}

		const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
			}
		}

		axios.post(`${ROOT_URL}/bill/vote/`, value, headers)
		.then((response) => {if(response.data.msg == "You have already cast a vote on this bill."){this.setState({error_message: "You have already cast a vote on this bill."})}
							 else{location.reload()}});
	}

	setDelegateId(userId, name) {
		this.setState({dele_id: userId[0], name: name});
	}

	onSubmit(values) {

	const config = { headers: {
		'Content-Type': 'application/json'
	}}

	const request = axios.post(`${ROOT_URL}/login/`, values, config)
	.then( (response) => {
		if(response.data.error) {
			throw new error;
		}
		else {
			this.props.loginUser(values);
		}
	})
	.catch(error => {
		throw new SubmissionError({_error: 'Failed to login.'});
	});

	return request;
	}

	renderBillDefaultDetail() {
		return (
			<div>
				<div className="row no-gutters">
					<div className="col-9 text-center card">
						<h3 className="card-header">{this.props.bill.bill.title}</h3>
						<p className="card-header">Categories: {this.props.bill.bill.category} 
						                           <br />
						                           Vote Date: {new Date(this.props.bill.bill.date.$date).toString()}</p>
						<div className="card-body" style={{'height':'300px', 'overflowY': 'auto'}}>
							{this.props.bill.bill.text}
							<br />
						</div>
					</div>
					<div className="col">
						<h4 className="text-center">Vote</h4>
						<br />
						<div className="text-center">
							<b>Voter Count: </b>{this.props.bill.bill.vote_info.voter_count}
						</div>
						<br />
						<div className="text-center">
							<span className="text-success">Yay: {this.props.bill.bill.vote_info.yay} </span>
							| <span className="text-danger">Nay: {this.props.bill.bill.vote_info.nay}</span>
						</div>
						<br />
						<div className="text-center">
							<button onClick={() => this.voteYay()} className={`btn btn-success col-3 ${this.state.button}`}>Yay</button>
							<button onClick={() => this.voteNay()} className={`btn btn-danger col-3 ${this.state.button}`}>Nay</button>
							<div style={{color: '#ff0000'}}>{this.state.error_message}</div>
						</div>
						<br />
						<ReactModal 
				           isOpen={this.state.showModal}
				           contentLabel="List of Delegates"
				           onRequestClose={this.handleCloseModal}
				           shouldCloseOnOverlayClick={false}
				           ariaHideApp={false}
				           className="Modal"
				        >
				        <div className="container-fluid text-center">
				          <h3 className="text-center">List of Delegates</h3>
				          <ul className="list-group delegate_list">
				          	{ _.map(this.state.delegates, delegate => {
				          		return(<li key={Object.keys(delegate)} onClick={() => this.setDelegateId(Object.keys(delegate),Object.values(delegate))} className="list-group-item">{Object.values(delegate)}</li>);
				          	})}
				          </ul>
				          <div>Selected: {this.state.name}</div>
				          <button className="btn btn-success" onClick={this.handleCloseModal}>Submit</button>
				          <button className="btn btn-danger" onClick={this.handleCloseModal}>Cancel</button>
				        </div>
				        </ReactModal>
						<div className="text-center">
							<button onClick={this.handleOpenModal} 
							        className={`btn btn-info ${this.state.button}`}>Delegate?</button>
						</div>
					</div>
				</div>

				<div className="row no-gutters">
					<div className="col">
			
					</div>
				</div>
			</div>
			)
	}

	render() {
		const { handleSubmit, error } = this.props;

		if(!this.props.bill) {
			
			return <div className="Loader"></div>
		}

		if(localStorage.getItem("jwt") == null) {
		return (
				<div className="container-fluid">
					<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                
	                <div className="login-form" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
		                <form className="form-inline navbar-form" >
							<Field 
								label="Email"
								name="email"
								type="email"
								component={this.renderField}
							/>
							<Field 
								label="Password"
								name="password"
								type="password"
								component={this.renderField}
							/>
							<button className="btn btn-success" type="submit">Sign in</button>
							<button className="btn btn-info mx-2" 
							onClick={() => this.props.history.push("/signup")}>Sign Up</button>
							<span style={{color: '#B80000'}}>{error}</span>
						</form>
					</div>
					</nav>
					{this.renderBillDefaultDetail()}
				</div>
			)
		}
		else
		{
			return (
					<div className="container-fluid">
						<nav className="navbar bg-primary">
					 
					 	<Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                	<Link className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</Link>
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
						{this.renderBillDefaultDetail()}
					</div>
				)
		}
	}
}

function validate(values) {

		const errors = {};

		if(!values.email) {
			errors.email = "Email blank.";
		}

		if(!values.password) {
			errors.password = "Password blank.";

		return errors;
	}
}

function mapStateToProps(state) {
	return {bill: state.bills.bill,
			user: state.user,
		    profile: state.profile};
}

export default reduxForm({
	validate,
	form: 'LoginForm'
})(
connect(mapStateToProps, {fetchBill, logoutUser, loginUser, fetchProfile})(BillDetail)
);