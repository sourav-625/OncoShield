import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import Nav from './components/nav';
import Home from './components/Home';
import About from './components/About';
import Device from './components/Devices';

function App() {
  return (
    <>
      <Router>
        <Nav />
        <div className='container'>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/About" element={<About />} />
            <Route path="/Devices" element={<Device />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
