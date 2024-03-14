import React from "react";
import { useLocation } from "react-router-dom";
import './Card.css'; // Import your CSS file for styling
import { useState } from "react";

const Timerscarcity = () => {
    const location = useLocation();
    const Url = location.state;
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);

    const handleclick = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/delivery-time', {
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

        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <h2>TIME SCARCITY ANALYSIS</h2>
            <h3>THIS PROCESS NEEDS ATMOST 60 SECONDS TO CHECK</h3>
            <strong><p className="usegreen">Click Here to Detect any Fake timers in the Given Product url</p></strong>
            <button className="button" onClick={handleclick}>Detect</button>
            <span>
                {loading && (
                    <div className="loading-screen">
                        This Might Take some minutes
                        <div className="loader"></div>
                    </div>
                )}
            </span>
            {resultData && (  
                resultData.res === 1 ? (
                    <div>
                        <p className="usered">Promised to Deliver by {resultData.delivery_date},  {resultData.initial_timer}</p>
                        <p className="usered">Change to Deliver by {resultData.delivery_date}, {resultData.updated_timer}</p>
                        <p className="usered">{resultData.result}</p>
                    </div>
                ) : (
                    <div>
                        Promised to Deliver by {resultData.delivery_date} <p className="usegreen">{resultData.initial_timer}</p>
                        <p className="usegreen">NO CHANGE RECORDED</p>
                        <p className="usegreen">{resultData.result}</p>
                    </div>
                )
            )}
        </div>
    );
}

export default Timerscarcity;
