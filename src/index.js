import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware} from 'redux';
import { persistStore, persistReducer} from 'redux-persist';
//import { PersistGate } from 'redux-persist/integration/react';
import storage from 'redux-persist/lib/storage';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import SignUp from './components/sign_up';
import Landing from './components/landing';
import BillDetail from './components/bill_detail';
import promise from 'redux-promise';

import reducers from './reducers';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['user']
};

const persistedReducer = persistReducer(persistConfig, reducers);
const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

let store = createStoreWithMiddleware(persistedReducer);
let persistor = persistStore(store);

ReactDOM.render(
  <Provider store={store}>
    	<BrowserRouter>
    		<div>
  	  		<Switch>
  	  			<Route path="/signup" component={SignUp} />
            <Route path="/bill/:id" component={BillDetail} />
  	  			<Route path="/" component={Landing} />
  	  		</Switch>
  	  	</div>
    	</BrowserRouter>
  </Provider>
  , document.querySelector('.container'));
