import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Url from "./Url.js";
import Home from "./Home.js"
import Result from "./Result.js"
import Navibar from "./Navibar.js";
import Urgency from "./Urgency.js";
import ReviewTable from "./Reviewtable.js";

const App = () => {
  return (
    <Router>
      <div>
      <Navibar/>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/detect" element={<Url/>}/>
          <Route path="/result" element={<Result/>}/>
          <Route path="/urgency" element={<Urgency/>}/>
          <Route path="/reviewtable" element={<ReviewTable/>}/>
          {/* <Route path="/about" element={<About/>}/> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
