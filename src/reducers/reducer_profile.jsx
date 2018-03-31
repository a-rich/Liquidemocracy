import _ from 'lodash';
import { FETCH_PROFILE } from '../actions';

export default function(state = {}, action) {
	switch (action.type) {
		case FETCH_PROFILE:
			return { ...state, profile: action.payload};
		default:
			return state;
	}
}