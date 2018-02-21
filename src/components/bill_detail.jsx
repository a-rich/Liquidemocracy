import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { fetchBill } from '../actions';
import { connect } from 'react-redux';

class BillDetail extends Component {
	constructor(props) {
	    super(props);
	    this.state = {button: ""};
  }

	componentDidMount() {
		if(localStorage.getItem("jwt") == null) {
			this.setState({button: "disabled"})
		}
		this.props.fetchBill(this.props.match.params.id);	
	}

	renderBillDefaultDetail() {
		return (
			<div>
				<div className="row no-gutters">
					<div className="col">
						<h5>Categories:</h5> {this.props.bill.categories.join(', ')}
						<br />
						<br />
						<h5>Keywords:</h5> {this.props.bill.keywords.join(', ')}
					</div>
					<div className="col-6 text-center card">
						<h1 className="card-header">{this.props.bill.title}</h1>
						<div className="card-body">
							{this.props.bill.description}
							<br />
						</div>
						<div className="card-footer text-muted">
							Vote Date: {this.props.bill.vote_info.vote_date}
						</div>
					</div>
					<div className="col">
						<h4 className="text-center">Vote</h4>
						<br />
						<div className="text-center">
							<b>Voter Count: </b>{this.props.bill.vote_info.voter_count}
						</div>
						<br />
						<div className="text-center">
							<span className="text-success">Yay: {this.props.bill.vote_info.yay} </span>
							| <span className="text-danger">Nay: {this.props.bill.vote_info.nay}</span>
						</div>
						<br />
						<div className="text-center">
							<button className={`btn btn-success col-3 ${this.state.button}`}>Yay</button>
							<button className={`btn btn-danger col-3 ${this.state.button}`}>Nay</button>
						</div>
						<br />
						<div className="text-center">
							<button className={`btn btn-info ${this.state.button}`}>Delegate?</button>
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
		if(!this.props.bill) {
			return <div>Loading...</div>
		}

		return (
				<div className="container-fluid">
					<nav className="navbar bg-primary">
					 
					 <Link className="navbar-brand" style={{color: '#ffffff'}} to="/">Liquidemocracy</Link>
	                
	                <div className="login-form">
		                <form className="form-inline navbar-form">
							<input className="form-control mr-sm-2" type="email" placeholder="Email" />
							<input className="form-control mr-sm-2" type="password" placeholder="Password" />
							<button className="btn btn-success" type="submit">Sign in</button>
							<button className="btn btn-info mx-2" 
							onClick={() => this.props.history.push("/signup")}>Sign Up</button>
						</form>
					</div>
					</nav>
					{this.renderBillDefaultDetail()}
				</div>
			)
	}
}

function mapStateToProps(state) {
	return {bill: state.bills.bill};
}

export default connect(mapStateToProps, {fetchBill})(BillDetail);