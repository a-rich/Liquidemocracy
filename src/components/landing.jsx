import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { fetchDefaultBills, logoutUser, loginUser } from '../actions';
import { connect } from 'react-redux';
import { Field, reduxForm, SubmissionError } from 'redux-form';

const ROOT_URL = 'http://localhost:5000';

/**********************************
	Landing Page for Liquidemocracy


	A user will see an initial list
	of default bills if there isn't
	a JWT stored in localStorage. 

	If a JWT is found, user will be
	pushed to home route.
***********************************/
class Landing extends Component {
	 constructor(props) {
	    super(props);
	    this.state = {option: "New"};
	    this.billsSort = this.billsSort.bind(this);
  }

  	renderField(field) {
		const { touched , error }  = field.meta;
		const className = `form-group ${touched && error ? 'has-danger' : ''}`;
		let type;

		return (
				<div className={ className }>
					<input
						className="form-control"
						type={field.type}
						placeholder={field.label}
						{...field.input}
					/>
					<div className="text-help">
					{touched ? error : ''}
					</div>
				</div>
			);
	}

  	// Get the list of bills into reducer.	
	componentDidMount() {
			this.props.fetchDefaultBills(this.state.option);
		}

	logout() {
		this.props.logoutUser();
		this.props.history.push("/");
	}

	onSubmit(values) {

	const config = { headers: {
		'Content-Type': 'application/json'
	}}

	const request = axios.post(`${ROOT_URL}/api/login/`, values, config)
	.then( (response) => {
		if(response.data.error) {
			throw new error;
		}
		else {
			this.props.loginUser(values);
			this.props.history.push("/");
		}
	})
	.catch(error => {
		throw new SubmissionError({_error: 'Failed to login.'});
	});

	return request;
	}

	/*
		This function sets the state of
		the component to from the filter
		that was selected form the dropdown.

		Seems to work, but can't tell due
		to static bill values. Will test once
		filters actually filter bills 
		accordingly. 
	*/
	billsSort(e) {
		this.setState({option: e.target.value});
	}

	/*
		This functions renders the list of
		default bills. Only shows bill titles.

	*/
	renderBills() {
		//Displayed to user while bills are being fetched.
		if(!this.props.bills.bills)
		{
			return (
					<div>Loading...</div>
				)
		}

		/*
			So far this is the working solution I 
			could come up with to display bill list. 
			This may be a performance hit due to 3 lodash
			map functions, but can't tell due to 
			only 2 static bills. Will test 
			once there is a lot of bills to
			work with. 
		*/
		return _.map(this.props.bills.bills, billArray => {
			return _.map(billArray, bills => {
				return _.map(bills, bill => {
					return (
							<li className="list-group-item" key={Object.keys(bills)}>
								<Link to={`/bill/${Object.keys(bills)}`}>
								{bill.title}
								</Link>
							</li>
						);
				})
			})
		})
	}

	//Used to render the html
	render() {
	const { handleSubmit, error } = this.props;

	if(localStorage.getItem("jwt") == null || this.props.user.user.isUserLoggedIn == false) {
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

					<div className="row">
						<div className="col-9">
							<ul className="list-group">
								{this.renderBills()}
							</ul>
						</div>

						<div className="col-3">
							<h6 className="text-center">Level</h6>
								<select className="form-control" id="Options" onChange={this.billsSort}>
									<option disabled value="City">City</option>
									<option disabled value="County">County</option>
									<option disabled value="State">State</option>
									<option value="Federal">Federal</option>
									<option disabled value="All">All</option>
								</select>

							<h6 className="text-center">Filter</h6>
								<select className="form-control" id="Options" onChange={this.billsSort}>
									<option disabled value="Recommended">Recommended</option>
									<option disabled value="Actionable">Actionable</option>
									<option value="All">All</option>
								</select>

							<h6 className="text-center">Sort</h6>
								<select className="form-control" id="Options" onChange={this.billsSort}>
									<option value="Recommended">Recommended</option>
									<option value="New">New</option>
									<option value="Time Until Vote">Time Until Vote</option>
									<option value="Popular">Popular</option>
								</select>
						</div>
					
					</div>
				</div>

			);
		}
		else
		{
			return (
					<div className="container-fluid">
						<nav className="navbar bg-primary">
					 
					 	<Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                	<div className="nav-item" style={{color: '#ffffff'}}>
						 	Profile
						 </div>
						 <div className="nav-item" style={{color: '#ffffff'}}>
						 	Active Votes
						 </div>
						 <div className="nav-item" style={{color: '#ffffff'}}>
						 	Settings
						 </div>
						 <div className="nav-item" 
						 	  style={{color: '#ffffff', cursor:'pointer'}} 
						 	  onClick={() => this.logout()}>
						 	Log Out
						 </div>
						 	
						</nav>
						
						<div className="row">
							<div className="col-9">
								<ul className="list-group">
									{this.renderBills()}
								</ul>
							</div>

							<div className="col-3">
								<h6 className="text-center">Level</h6>
									<select className="form-control" id="Options" onChange={this.billsSort}>
										<option value="City">City</option>
										<option value="County">County</option>
										<option value="State">State</option>
										<option value="Federal">Federal</option>
										<option value="All">All</option>
									</select>

								<h6 className="text-center">Filter</h6>
									<select className="form-control" id="Options" onChange={this.billsSort}>
										<option value="Recommended">Recommended</option>
										<option value="Actionable">Actionable</option>
										<option value="All">All</option>
									</select>

								<h6 className="text-center">Sort</h6>
									<select className="form-control" id="Options" onChange={this.billsSort}>
										<option value="Recommended">Recommended</option>
										<option value="New">New</option>
										<option value="Time Until Vote">Time Until Vote</option>
										<option value="Popular">Popular</option>
									</select>
							</div>
					</div>

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
/*
	Redux stuff. Used to map
	the state object from redux to
	the props of the Landing component.
*/
function mapStateToProps(state) {
	return {bills: state.bills,
			user: state.user};
}

/* 
	Connects the mapStateToProps function 
	and the fetchDefaultBills action to the
	Landing component.
*/
export default reduxForm({
	validate,
	form: 'LoginForm'
})(
connect(mapStateToProps, {fetchDefaultBills, logoutUser, loginUser})(Landing)
);