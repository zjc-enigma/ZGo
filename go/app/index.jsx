// Enbale React debugging inside webpack-dev-server
if (window.parent !== window) {
	window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = window.parent.__REACT_DEVTOOLS_GLOBAL_HOOK__;
}
import { createDevTools } from 'redux-devtools'
import LogMonitor from 'redux-devtools-log-monitor'
import DockMonitor from 'redux-devtools-dock-monitor'


const DevTools = createDevTools(
  <DockMonitor toggleVisibilityKey="ctrl-h" changePositionKey="ctrl-q">
    <LogMonitor theme="tomorrow" preserveScrollTop={false} />
  </DockMonitor>
)

// Master css
require("./styles/style.scss")

import React from "react";
import ReactDOM from "react-dom";
import { createStore, applyMiddleware } from "redux";
import { Provider, connect } from "react-redux";
import thunk from 'redux-thunk';

import Board from "./components/Board"
import game from "./reducers/reducers"

const store = createStore(
	game,
  applyMiddleware(thunk),
  DevTools.instrument()
);

if (process.env.NODE_ENV !== 'production') {
	let unsubscribe = store.subscribe(() => {
		console.log(
			"----------------\n",
			store.getState(),
			"\n----------------"
		)
	})
}

ReactDOM.render(
	<Provider store={store}>
    <div>
		<Board />
    <DevTools />
    </div>
	</Provider>,
	document.getElementById('root')
);
