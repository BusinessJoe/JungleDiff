import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from './components/Home';
import SummonerPage from './components/SummonerPage';

function App() {
  return (
    <Router>
      <Route path="/" exact component={Home} />
      <Route path="/summonerPage/:summonerName" component={SummonerPage} />
    </Router>
  );
}

export default App;
