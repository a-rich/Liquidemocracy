import axios from 'axios';
import _ from 'lodash';
import { SubmissionError } from 'redux-form';

export const FETCH_DEFAULT_BILLS = 'fetch_default_bills';
export const FETCH_BILLS = 'fetch_bills';
export const FETCH_BILL = 'fetch_bill';
export const LOGIN_USER = 'login_user';
export const LOGOUT_USER = 'logout_user';
export const FETCH_PROFILE = 'fetch_profile';
export const SEARCH_DEFAULT_BILLS = 'search_default_bills';
export const SEARCH_BILLS = 'search_bills';

const ROOT_URL = 'https://liquidemocracy-api.herokuapp.com/api';

export function fetchDefaultBills(category, query) {

	let c = "";

	if(category != "All") {
		c = category;
	}

	const bodyOption = {
		category: c,
		query: query
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

export function fetchBills(category, filter, level, query, jwt) {

	let c = "";
	let l = "";

	if(category != "All") {
		c = category;
	}

	if(level != "All") {
		l = level;
	}

	const bodyOption = {
			level: l,
			filter: filter,
			category: c,
			query: query
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

export function searchBillsDefault(query, category, index) {

	let c = "";

	if(category != "All") {
		c = category;
	}

	const values = {
		query: query,
		category: c,
		index: index
	}

	const headers = {
		headers: {
		'Content-Type': 'application/json'
		}
	}

	const request = axios.post(`${ROOT_URL}/bills/search/default/`, values, headers);

	return {
		type: SEARCH_DEFAULT_BILLS,
		payload: request
	}
}

export function searchBills(query, category, index, level, filter) {

	let c = "";
	let l = "";
	let token = localStorage.getItem("jwt");

	if(category != "All") {
		c = category;
	}

	if(level != "All") {
		c = level;
	}

	const values = {
		query: query,
		level: l,
		filter: filter,
		category: c,
		index: index
	}

	const headers = {
		headers: {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${token}`
		}
	}

	const request = axios.post(`${ROOT_URL}/bills/search/`, values, headers);

	return {
		type: SEARCH_BILLS,
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