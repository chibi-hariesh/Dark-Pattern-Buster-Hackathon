import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './Url.css'; // Import your CSS file

function Url() {
  const [url, setUrl] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    setUrl(event.target.value);
  };

  const handleClick = () => {
    const flipkartPattern = /^(https?:\/\/)?(www\.)?flipkart\.com\/.*pid=[^&]+/;
    
    if (flipkartPattern.test(url.trim())) {
      navigate('/result',{state: url});
    } 
    else {
      alert('Please enter a valid Flipkart URL containing the pid parameter.');
    }
  };

  return (
    <div>
      <div className="url-component">
        <div className="url-container">
          <input
            type="text"
            placeholder="PLEASE ENTER A VALID FLIPKART PRODUCT URL"
            value={url}
            onChange={handleInputChange}
            className="url-input"
            required
          />
        </div>
        <div>
          <button type="button" onClick={handleClick} className="button">
            Detect
          </button>
        </div>
      </div>
    </div>
  );
}

export default Url;
