import React, { Component} from 'react';
import { Field, reduxForm, SubmissionError } from 'redux-form';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { createAccount, loginUser } from '../actions';
import axios from 'axios';
import _ from 'lodash';

const ROOT_URL = 'http://localhost:5000';

class SignUp extends Component {

	renderField(field) {
		const { touched , error }  = field.meta;
		const className = `form-control ${touched && error ? 'border border-danger' : ''}`;
		
		switch(field.type) {
			case 'select': 
				return (
				<div className="form-group">
					<label>{field.label}</label>
					<select
						className={ className }
						{...field.input}
					>
						<option defaultValue="--Select A State--">--Select A State--</option>
						<option value="AL">Alabama</option>
						<option value="AK">Alaska</option>
						<option value="AZ">Arizona</option>
						<option value="AR">Arkansas</option>
						<option value="CA">California</option>
						<option value="CO">Colorado</option>
						<option value="CT">Connecticut</option>
						<option value="DE">Delaware</option>
						<option value="DC">District Of Columbia</option>
						<option value="FL">Florida</option>
						<option value="GA">Georgia</option>
						<option value="HI">Hawaii</option>
						<option value="ID">Idaho</option>
						<option value="IL">Illinois</option>
						<option value="IN">Indiana</option>
						<option value="IA">Iowa</option>
						<option value="KS">Kansas</option>
						<option value="KY">Kentucky</option>
						<option value="LA">Louisiana</option>
						<option value="ME">Maine</option>
						<option value="MD">Maryland</option>
						<option value="MA">Massachusetts</option>
						<option value="MI">Michigan</option>
						<option value="MN">Minnesota</option>
						<option value="MS">Mississippi</option>
						<option value="MO">Missouri</option>
						<option value="MT">Montana</option>
						<option value="NE">Nebraska</option>
						<option value="NV">Nevada</option>
						<option value="NH">New Hampshire</option>
						<option value="NJ">New Jersey</option>
						<option value="NM">New Mexico</option>
						<option value="NY">New York</option>
						<option value="NC">North Carolina</option>
						<option value="ND">North Dakota</option>
						<option value="OH">Ohio</option>
						<option value="OK">Oklahoma</option>
						<option value="OR">Oregon</option>
						<option value="PA">Pennsylvania</option>
						<option value="RI">Rhode Island</option>
						<option value="SC">South Carolina</option>
						<option value="SD">South Dakota</option>
						<option value="TN">Tennessee</option>
						<option value="TX">Texas</option>
						<option value="UT">Utah</option>
						<option value="VT">Vermont</option>
						<option value="VA">Virginia</option>
						<option value="WA">Washington</option>
						<option value="WV">West Virginia</option>
						<option value="WI">Wisconsin</option>
						<option value="WY">Wyoming</option>
					</select>
					<div className="text-help text-danger">
					{touched ? error : ''}
					</div>
				</div>
			);
				break;
			default: 
				return (
				<div className="form-group">
					<label>{field.label}</label>
					<input
						className={ className }
						type={field.type}
						{...field.input}
					/>
					<div className="text-help text-danger">
					{touched ? error : ''}
					</div>
				</div>
			);
		}

	}

	onSubmit(values) {
	var values = _.omit(values, 'confirmPassword');

	const config = { headers: {
		'Content-Type': 'application/json'
	}}

	const request = axios.post(`${ROOT_URL}/api/test_create_user/`, values, config)
	.then( (response) => {
		if(response.data.error) {
			throw new error;
		}
		else {
			this.props.loginUser(values);
			alert('Account Created.');
			this.props.history.push("/");
		}
	})
	.catch(error => {
		throw new SubmissionError({email: 'Email already in use.', _error: 'Failed to create an account.'});
	});

	return request;
	}
	
	render() {
		const { handleSubmit } = this.props;

		return (
			<div>
				<h1 className="signup-header">Sign Up</h1>

				<form className="signup-form" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
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
					<Field 
						label="Confirm Password"
						name="confirmPassword"
						type="password"
						component={this.renderField}
					/>
					<Field 
						label="Name"
						name="name"
						type="text"
						component={this.renderField}
					/>
					<Field 
						label="City"
						name="city"
						type="text"
						component={this.renderField}
					/>
					<Field 
						label="County"
						name="county"
						type="text"
						component={this.renderField}
					/>
					<Field 
						label="State"
						name="state"
						type="select"
						component={this.renderField}
					/>
					<button type="submit" className="btn btn-primary">Submit</button>
					<Link to="/" className="btn btn-danger">Cancel</Link>
				</form>
			</div>
			);
	}
}

function validate(values) {

	const errors = {};

	if(!values.email) {
		errors.email = "Email blank.";
	}

	if(!values.password) {
		errors.password = "Password blank.";
	}
	else if(values.password.length < 8) {
		errors.password = "Password must be at least 8 characters."
	}

	if(!values.confirmPassword) {
		errors.confirmPassword = "Confirm password blank.";
	}
	else if(values.password != values.confirmPassword) {
		errors.confirmPassword = "Password must match."
	}

	if(!values.name) {
		errors.name = "Name blank.";
	}

	if(!values.city) {
		errors.city = "City blank.";
	}

	if(!values.county) {
		errors.county = "County blank.";
	}

	if(values.state == '--Select A State--') {
		errors.state = "Please select state of residency."
	}

	return errors;
}

export default reduxForm({
	validate,
	form: 'SignUpForm'
})(
connect(null, { createAccount, loginUser })(SignUp)
);