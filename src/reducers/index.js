import { combineReducers } from 'redux';
import BillReducer from './reducer_bills';
import UserReducer from './reducer_user';
import { reducer as formReducer} from 'redux-form';

const rootReducer = combineReducers({
  form: formReducer,
  bills: BillReducer,
  user: UserReducer
});

export default rootReducer;
