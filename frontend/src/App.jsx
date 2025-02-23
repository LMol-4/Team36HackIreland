import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home"; 
import Feedback from "./pages/Feedback"
import Navbar from "./components/Navbar"

function App() {
  return (
    <Router>
      <Navbar/>
      <Routes>
        <Route path="/" element={<Home />} /> {/* Route to Home */}
        <Route path="/feedback" element={<Feedback/>}/>
      </Routes>
    </Router>
  );
}

export default App;
