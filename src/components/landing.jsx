import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { fetchDefaultBills, fetchBills, logoutUser, loginUser, searchBillsDefault } from '../actions';
import { connect } from 'react-redux';
import { Field, reduxForm, SubmissionError } from 'redux-form';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com';

/**********************************
	Landing Page for Liquidemocracy


	A user will see an initial list
	of default bills if there isn't
	a JWT stored in localStorage. 

***********************************/
class Landing extends Component {
	 constructor(props) {
	    super(props);
	    this.state = {category: "All",
					  level: "",
					  filter: "All",
					  type: "default",
					  index: 0,
					  query: ""};
		this.defaultBillsCategory = this.defaultBillsCategory.bind(this);
	    this.billsCategory = this.billsCategory.bind(this);
	    this.billsLevel = this.billsLevel.bind(this);
	    this.billsFilter = this.billsFilter.bind(this);
	    this.handleQuery = this.handleQuery.bind(this);
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
					<div className="text-help text-danger">
					{touched ? error : ''}
					</div>
				</div>
			);
	}

  	// Get the list of bills into reducer.	
	componentDidMount() {
			if(localStorage.getItem("jwt") == null || this.props.user.user.isUserLoggedIn == false) {
				this.props.fetchDefaultBills(this.state.category);
			}
			else
			{
				this.props.fetchBills(this.state.category, this.state.filter, this.state.level, localStorage.getItem("jwt"));
			}
		}

	logout() {
		this.props.logoutUser();
		this.props.history.push("/");
	}

	handleQuery(e) {
		this.setState({query: e.target.value});
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
	defaultBillsCategory(e) {
		this.setState({category: e.target.value}, () => {
			this.props.fetchDefaultBills(this.state.category);
		});
	}

	billsCategory(e) {
		this.setState({category: e.target.value}, () => {
			this.props.fetchBills(this.state.category, this.state.filter, this.state.level, localStorage.getItem("jwt"));
		});
	}

	billsLevel(e) {
		this.setState({level: e.target.value}, () => {
			this.props.fetchBills(this.state.category, this.state.filter, this.state.level, localStorage.getItem("jwt"));
		});
	}

	billsFilter(e) {
		this.setState({filter: e.target.value}, () => {
			this.props.fetchBills(this.state.category, this.state.filter, this.state.level, localStorage.getItem("jwt"));
		});
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
				return(
						<li className="list-group-item" key={bills._id.$oid}>
							<Link to={`/bill/${bills._id.$oid}`}>
							{bills.title}
							</Link>
						</li>
					);
			})
		})
	}

	//Used to render the html
	render() {
	const { handleSubmit, error } = this.props;

	if(localStorage.getItem("jwt") == null || this.props.user.user.isUserLoggedIn == false) {
		return (
				<div className="container-fluid">
					<nav className="navbar bg-primary sticky-top">
					 
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

							<div className="input-group">
								<input value={this.state.query} onChange={this.handleQuery} className="form-control" placeholder="Search"></input>
								<button className="btn btn-secondary" 
								onClick={() => this.props.searchBillsDefault(this.state.query, this.state.category, this.state.index)}>
								<i className="fas fa-search"></i>
								</button>
							</div>

							<h6 className="text-center">Level</h6>
								<select className="form-control" id="Options">
									<option disabled value="City">City</option>
									<option disabled value="County">County</option>
									<option disabled value="State">State</option>
									<option value="Federal">Federal</option>
									<option disabled value="All">All</option>
								</select>

							<h6 className="text-center">Filter</h6>
								<select className="form-control" id="Options">
									<option disabled value="Recommended">Recommended</option>
									<option disabled value="Actionable">Actionable</option>
									<option value="All">All</option>
								</select>

							<h6 className="text-center">Category</h6>
								<select className="form-control" id="Options" onChange={this.defaultBillsCategory} value={this.props.value}>
									<option value="All">All</option>
									<option value="Taxation">Taxation</option>
									<option value="Health">Health</option>
									<option value="Armed Forces and National Security">Armed Forces and National Security</option>
									<option value="Foreign Trade and International Finance">Foreign Trade and International Finance</option>
									<option value="International Affairs">International Affairs</option>
									<option value="Crime and Law Enforcement">Crime and Law Enforcement</option>
									<option value="Transportation and Public Works">Transportation and Public Works</option>
									<option value="Education">Education</option>
									<option value="Energy">Energy</option>
									<option value="Agriculture and Food">Agriculture and Food</option>
									<option value="Economics and Public Finance">Economics and Public Finance</option>
									<option value="Labor and Employement">Labor and Employement</option>
									<option value="Environmental Protection">Environmental Protection</option>
									<option value="Science, Technology, and Communications">Science, Technology, and Communications</option>
									<option value="Immigration">Immigration</option>
									<option value="Other">Other</option>
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
					 
					 	<Link className="navbar-brand active" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                	<Link className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 	Profile
						 </Link>
						 <Link className="nav-item" style={{color: '#ffffff'}} to="/delegates">
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
						
						<div className="row">
							<div className="col-9">
								<ul className="list-group">
									{this.renderBills()}
								</ul>
							</div>

							<div className="col-3">

								<div className="input-group">
									<input className="form-control" placeholder="Search"></input>
									<button className="btn btn-secondary"><i className="fas fa-search"></i></button>
								</div>

								<h6 className="text-center">Level</h6>
									<select className="form-control" id="Options" onChange={this.billsLevel} value={this.props.value}>
										<option value="All">All</option>
										<option value="City">City</option>
										<option value="County">County</option>
										<option value="State">State</option>
										<option value="Federal">Federal</option>
									</select>

								<h6 className="text-center">Filter</h6>
									<select className="form-control" id="Options" onChange={this.billsFilter} value={this.props.value}>
										<option value="All">All</option>
										<option value="Recommended">Recommended</option>
										<option value="Actionable">Actionable</option>
									</select>

								<h6 className="text-center">Category</h6>
									<select className="form-control" id="Options" onChange={this.billsCategory} value={this.props.value}>
										<option value="All">All</option>
										<option value="Taxation">Taxation</option>
										<option value="Health">Health</option>
										<option value="Armed Forces and National Security">Armed Forces and National Security</option>
										<option value="Foreign Trade and International Finance">Foreign Trade and International Finance</option>
										<option value="International Affairs">International Affairs</option>
										<option value="Crime and Law Enforcement">Crime and Law Enforcement</option>
										<option value="Transportation and Public Works">Transportation and Public Works</option>
										<option value="Education">Education</option>
										<option value="Energy">Energy</option>
										<option value="Agriculture and Food">Agriculture and Food</option>
										<option value="Economics and Public Finance">Economics and Public Finance</option>
										<option value="Labor and Employement">Labor and Employement</option>
										<option value="Environmental Protection">Environmental Protection</option>
										<option value="Science, Technology, and Communications">Science, Technology, and Communications</option>
										<option value="Immigration">Immigration</option>
										<option value="Other">Other</option>
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
connect(mapStateToProps, {fetchDefaultBills, fetchBills, logoutUser, loginUser, searchBillsDefault})(Landing)
);