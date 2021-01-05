import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from './components/Home';
import SearchTest from './components/SearchBarTest'

function App() {
  return (
    <Router>
      <Route path="/" exact component={Home} />
      <Route path="/test/<str:summonerName" component={SearchTest} />
    </Router>
  );
}

export default App;
