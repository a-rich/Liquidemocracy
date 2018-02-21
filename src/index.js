import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import SignUp from './components/sign_up';
import Landing from './components/landing';
import BillDetail from './components/bill_detail';
import promise from 'redux-promise';

import reducers from './reducers';

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
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
