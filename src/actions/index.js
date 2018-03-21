import axios from 'axios';
import _ from 'lodash';
import { SubmissionError } from 'redux-form';

export const FETCH_DEFAULT_BILLS = 'fetch_default_bills';
export const FETCH_BILLS = 'fetch_bills';
export const FETCH_BILL = 'fetch_bill';
export const LOGIN_USER = 'login_user';
export const LOGOUT_USER = 'logout_user';

const ROOT_URL = 'http://localhost:5000/api';

export function fetchDefaultBills(sort) {
	const bodyOption = {
		options: {
			sort: sort
		}
	}
	const request = axios.post(`${ROOT_URL}/bills/default/`, bodyOption);

	return {
		type: FETCH_DEFAULT_BILLS,
		payload: request
	}
}

export function fetchBills(sort, filter, level, jwt) {
	const bodyOption = {
		options: {
			level: level,
			filter: filter,
			sort: sort
		}
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