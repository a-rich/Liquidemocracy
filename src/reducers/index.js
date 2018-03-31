import { combineReducers } from 'redux';
import BillReducer from './reducer_bills';
import UserReducer from './reducer_user';
import ProfileReducer from './reducer_profile';
import { reducer as formReducer} from 'redux-form';

const rootReducer = combineReducers({
  form: formReducer,
  bills: BillReducer,
  user: UserReducer,
  profile: ProfileReducer
});

export default rootReducer;
