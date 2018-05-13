import React, { Component } from 'react';
import { connect } from 'react-redux';
import { logoutUser, fetchProfile } from '../actions';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Field, reduxForm, SubmissionError, initialize } from 'redux-form';
import Alert from 'react-s-alert';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

class Profile extends Component {
	constructor(props) {
	    super(props);
	    this.state = {editing: false,
	    			  isEditing: false};

	    //this.logout = this.logout.bind(this);
  }

  renderField(field) {
		const { touched , error }  = field.meta;
		const className = `form-control ${touched && error ? 'border border-danger' : ''}`;
		let type;

		return (
				<div className="form-group">
					<label>{field.label}</label>
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

	onSubmit(values) {
		let token = localStorage.getItem("jwt");

		const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
			}
		}

		axios.post(`${ROOT_URL}/profile/update/`, values, headers)
		.then((response) => 
			{
				if(response.data.msg.residence_update != null)
				{
					if(response.data.msg.residence_update.includes("Cannot update residence"))
					{
						Alert.error(response.data.msg.residence_update, {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.reload();
    								}
								});
						return false;
					}
					else
					{
						Alert.success(response.data.msg.residence_update, {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.reload();
    								}
								});
					}
				}
				else if(response.data.msg.email_update != null)
				{
					this.setState({editing: false}, () => {
						this.logout();
						Alert.info("Sent confirmation link to new email. You will be logged out and asked to login using new email.", {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.replace("https://liquidemocracy.herokuapp.com/");
    								}
								});
					});
				}
				else
				{
					this.setState({editing: false}, () => {
						this.props.fetchProfile();
						Alert.success("Name successfully updated.", {
								    effect: 'genie',
								    position: 'bottom-right',
								    preserveContext: true,
								    onClose: function () {
        							window.location.reload();
    								}
								});
					});
				}
	});
}

	componentWillMount() {
		this.props.fetchProfile();
	}

	shouldComponentUpdate() {
		if(this.state.isEditing == false)
		{
			this.setState({isEditing: true});
			this.handleInitialize();
			return true;
		}

		return true;
	}

	handleInitialize() {
		if(this.props.profile.profile != null)
		{
			this.props.initialize({email: this.props.profile.profile.email,
								   name: this.props.profile.profile.name,
								   county: this.props.profile.profile.county,
								   city: this.props.profile.profile.city,
								   state: this.props.profile.profile.state});
		}
	}

	logout() {
		this.props.logoutUser();
	}

	render() {
		const { handleSubmit, error } = this.props;
		if(this.props.profile.profile == null) {
			return (
					<div className="Loader"></div>
				)
		}

		if(this.state.editing = false)
		{
		return (
				<div>
				<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                <div className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</div>
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
					<div className="container-fluid">
						<h4>Email: {this.props.profile.profile.email}</h4>
						<h4>Name: {this.props.profile.profile.name}</h4>
						<h4>County: {this.props.profile.profile.county}</h4>
						<h4>City: {this.props.profile.profile.city}</h4>
						<h4>State: {this.props.profile.profile.state}</h4>

						<button className="btn btn-warning" onClick={() => this.setState({editing: true})}>Edit</button>
					</div>
				</div>
			)
		}
		else
		{
			return (
				<div>
				<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                	
	                <div className="nav-item" style={{color: '#ffffff'}} to="/profile">
						 Profile
						</div>
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
					<h1 className="text-center customH1"><span className="customSpan">Profile</span></h1>
						<div style={{'backgroundColor': '#ffffff', 'padding': '5px'}} className="profile-form" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
							<form>
								<Field 
									label="Email"
									name="email"
									type="email"
									component={this.renderField}
								/>
								<Field 
									label="Name"
									name="name"
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
									label="City"
									name="city"
									type="text"
									component={this.renderField}
								/>
								<Field 
									label="State"
									name="state"
									type="text"
									component={this.renderField}
								/>
								<button className="btn btn-success" type="submit">Save</button>
							</form>
						</div>
				</div>
			)
		}
	}

}

function mapStateToProps(state) {
	return {
		profile: state.profile
	} 
}

function validate(values) {

		const errors = {};

		if(!values.email) {
			errors.email = "Email blank.";
		}

		if(!values.name) {
			errors.name = "Name blank.";
		}

		if(!values.county) {
			errors.county = "County blank.";
		}

		if(!values.city) {
			errors.city = "City blank.";
		}

		if(!values.state) {
			errors.state = "State blank.";
		}

		return errors;
	
}

export default reduxForm({
	validate,
	form: 'ProfileForm',
	keepDirtyOnReinitialize: true
})(
connect(mapStateToProps, {logoutUser, fetchProfile})(Profile)
);