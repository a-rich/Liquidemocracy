import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { fetchDefaultBills } from '../actions';
import { connect } from 'react-redux';

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
	    this.billsDefaultSort = this.billsSort.bind(this);
  }

  	// Get the list of bills into reducer.	
	componentDidMount() {
		if(localStorage.getItem("jwt") == null) {
				this.props.fetchDefaultBills(this.state.option);
			}	
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
		return (
				<div className="container-fluid">
					<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                
	                <div className="login-form">
		                <form className="form-inline navbar-form">
							<input className="form-control mr-sm-2" type="email" placeholder="Email" />
							<input className="form-control mr-sm-2" type="password" placeholder="Password" />
							<button className="btn btn-success" type="submit">Sign in</button>
							<button className="btn btn-info" 
							onClick={() => this.props.history.push("/signup")}>Sign Up</button>
						</form>
					</div>
					</nav>

					<select className="form-control" id="Options" onChange={this.billsSort}>
						<option value="New">New</option>
						<option value="Time Until Vote">Time Until Vote</option>
						<option value="Popular">Popular</option>
					</select>
					
					<ul className="list-group">
						{this.renderBills()}
					</ul>
				</div>

			);
	}
}

/*
	Redux stuff. Used to map
	the state object from redux to
	the props of the Landing component.
*/
function mapStateToProps(state) {
	return {bills: state.bills};
}

/* 
	Connects the mapStateToProps function 
	and the fetchDefaultBills action to the
	Landing component.
*/
export default connect(mapStateToProps, {fetchDefaultBills})(Landing);