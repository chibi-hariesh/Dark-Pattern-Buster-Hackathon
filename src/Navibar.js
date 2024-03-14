import React from 'react';
import { Link } from 'react-router-dom';
import './Navibar.css';

function Navibar() {

  const handleclick = () => {
    // Send a DELETE request to the server to delete the JSON file
    fetch('http://localhost:5000/deletejson', {
      method: 'DELETE'
    })
    .then(response => {
      if (response.ok) {
        console.log('JSON file deleted successfully');
        
      } else {
        console.error('Failed to delete JSON file');
      }
    })
    .catch(error => console.error('Error occurred:', error));
  }

  return (
    <nav className="navbar">
      <div className="left">
        <Link  to="/" className="link" onClick={handleclick}>HOME</Link>
      </div>
      <div className="center">
        <img src="logo.png" alt="Logo" className="logo" />
      </div>
      <div className="right">
        <Link to="/about" className="link">ABOUT</Link>
      </div>
    </nav>
  );
}

export default Navibar;
