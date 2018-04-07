import axios from 'axios';
import _ from 'lodash';
import { SubmissionError } from 'redux-form';

export const FETCH_DEFAULT_BILLS = 'fetch_default_bills';
export const FETCH_BILLS = 'fetch_bills';
export const FETCH_BILL = 'fetch_bill';
export const LOGIN_USER = 'login_user';
export const LOGOUT_USER = 'logout_user';
export const FETCH_PROFILE = 'fetch_profile';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

export function fetchDefaultBills(category) {

	let c = "";

	if(category != "All") {
		c = category;
	}

	const bodyOption = {
		category: c,
		index: 0
	}

	const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Access-Control-Allow-Origin': '*'
		}
	}

	const request = axios.post(`${ROOT_URL}/bills/default/`, bodyOption, headers);

	return {
		type: FETCH_DEFAULT_BILLS,
		payload: request
	}
}

export function fetchBills(category, filter, level, jwt) {

	let c = "";

	if(category != "All") {
		c = category;
	}

	const bodyOption = {
			level: level,
			filter: filter,
			category: c,
			index: 0
	}

	const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${jwt}`
		}
	}

	const request = axios.post(`${ROOT_URL}/bills/`, bodyOption, headers);

	return {
		type: FETCH_BILLS,
		payload: request
	}
}

export function fetchBill(id) {
	const request = axios.get(`${ROOT_URL}/bills/${id}`);

	return {
		type: FETCH_BILL,
		payload: request
	}
}

export function loginUser(values) {
	axios.post(`${ROOT_URL}/login/`, values)
	.then((response) => localStorage.setItem("jwt", response.data.jwt));

	return {
		type: LOGIN_USER,
		payload: {isUserLoggedIn: true}
	}
}

export function logoutUser() {
	localStorage.removeItem("jwt");

	return {
		type: LOGOUT_USER,
		payload: {isUserLoggedIn: false}
	}
}

export function fetchProfile() {
	let token = localStorage.getItem("jwt");
	let profile;

	const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
		}
	}

	const request = axios.get(`${ROOT_URL}/profile/`, headers).then((response) => profile = response.data);

	return {
		type: FETCH_PROFILE,
		payload: request
	}
}