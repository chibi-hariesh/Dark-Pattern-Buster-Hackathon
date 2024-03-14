import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import './Card.css'; // Import your CSS file for styling

const Discount = () => {
    const location = useLocation();
    const Url = location.state;
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);

    const handleclick = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/discount', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: Url }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch');
            }

            const result = await response.json();
            setResultData(result);
        }
        catch (error) {
            console.error('Error fetching data:', error);
        }
        finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <h2>DISCOUNT ANALYZER</h2>
            <strong><p className="usegreen">Click Here to Analyze the Discount Details</p></strong>
            <button className="button" onClick={handleclick}>Find</button>
            <span>
                {loading && (
                    <div className="loading-screen">
                        Just a moment
                        <div className="loader"></div>
                    </div>
                )}
            </span>
            {resultData && (
                <div>
                    <p className="useblue">MRP :  {resultData["MRP"]}</p>
                    <p className="useblue">Selling Price :  {resultData["Selling Price"]}</p>
                    <p className="useblue">Special Price :  {resultData["Special Price"]}</p>
                    
                    <p className={resultData["Given Discount Percentage"] === resultData["Real Discount Percentage"] ? "usegreen" : "usered"}>
                        Given Discount Percentage :  {resultData["Given Discount Percentage"]}
                    </p>
                    <p className="usegreen">Real Discount Percentage :  {resultData["Real Discount Percentage"]}</p>
                    <p className="usegreen">Discount Amount:  {resultData["Discount Amount"]}</p>

                    <strong><p className={resultData["Result"].startsWith("Dark") ? "usered" : "usegreen"}>
                        {resultData["Result"]}
                    </p></strong>
                </div>
            )}
        </div>
    );
}

export default Discount;
