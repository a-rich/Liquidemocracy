import _ from 'lodash';
import { FETCH_DEFAULT_BILLS, FETCH_BILL, FETCH_BILLS } from '../actions';

export default function(state = {}, action) {
	switch (action.type) {
		case FETCH_DEFAULT_BILLS:
			return { ...state, bills: action.payload.data};
		case FETCH_BILLS:
			return { ...state, bills: action.payload.data};
		case FETCH_BILL:
			return {...state, bill: action.payload.data};
		default:
			return state;
	}
}