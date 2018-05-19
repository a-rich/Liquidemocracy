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
import Delegations from './components/delegations';
import Delegates from './components/delegates';
import Profile from './components/profile';
import promise from 'redux-promise';
import Alert from 'react-s-alert';

import reducers from './reducers';

$(document).ready(function()
{
  $("tr:even").css("background-color", "rgb(245,248,250)");
});

$(document).ready(function()
{
  $("tr:odd").css("background-color", "#ffffff");
});

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
            <Route path="/profile" component={Profile} />
            <Route path="/delegations" component={Delegations} />
            <Route path="/delegates" component={Delegates} />
  	  			<Route path="/" component={Landing} />
  	  		</Switch>
          <Alert stack={{limit: 3}} />
  	  	</div>
    	</BrowserRouter>
  </Provider>
  , document.querySelector('.container'));
