import React, { Component} from 'react';
import { Field, reduxForm} from 'redux-form';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { createAccount } from '../actions';
import axios from 'axios';
import _ from 'lodash';
import { SubmissionError } from 'redux-form'

const ROOT_URL = 'http://localhost:5000';

class SignUp extends Component {

	renderField(field) {
		const { touched , error }  = field.meta;
		const className = `form-group ${touched && error ? 'has-danger' : ''}`;
		let type;

		return (
				<div className={ className }>
					<label>{field.label}</label>
					<input
						className="form-control"
						type={field.type}
						{...field.input}
					/>
					<div className="text-help">
					{touched ? error : ''}
					</div>
				</div>
			);
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

	return errors;
}

export default reduxForm({
	validate,
	form: 'SignUpForm'
})(
connect(null, { createAccount })(SignUp)
);