import React, { Component} from 'react';
import { Link } from 'react-router-dom';

class Landing extends Component {
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

					<ul className="list-group">
						<li className="list-group-item">Bill 1</li>
						<li className="list-group-item">Bill 2</li>
						<li className="list-group-item">Bill 3</li>
					</ul>
				</div>
			);
	}
}

export default Landing;