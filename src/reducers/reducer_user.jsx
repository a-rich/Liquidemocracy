import _ from 'lodash';
import { LOGIN_USER, LOGOUT_USER} from '../actions';

export default function(state = {user: {isUserLoggedIn: false}}, action) {
	switch (action.type) {
		case LOGIN_USER:
			return { ...state, user: action.payload};
		case LOGOUT_USER:
			return { ...state, user: action.payload};
		default:
			return state;
	}
}