import React from "react";
import { useLocation } from "react-router-dom";
import './Card.css'; // Import your CSS file for styling
import { useState } from "react";


const Urgency = () => {
    const location = useLocation();
    const Url = location.state;
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);
    const handleclick = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/urgency', {
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
            <h2>URGENCY ANALYSIS</h2>
            <strong><p className="usegreen">Click Here to Detect any Urgency behavior in the Given Product url</p></strong>
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
                <div>
                    <p className="usered">{resultData.result}</p>
                </div>
            )}
        </div>
    );
}

export default Urgency;
