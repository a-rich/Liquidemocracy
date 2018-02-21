import { combineReducers } from 'redux';
import BillReducer from './reducer_bills';
import { reducer as formReducer} from 'redux-form';

const rootReducer = combineReducers({
  form: formReducer,
  bills: BillReducer
});

export default rootReducer;
