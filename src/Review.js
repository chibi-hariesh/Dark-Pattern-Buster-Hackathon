import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import './Card.css'; // Import your CSS file for styling

const Review = () => {
    const location = useLocation();
    const Url = location.state;
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);
    const [reviewCount, setReviewCount] = useState(null); // State to store review count or "No Review Found" message

    const handledetectclick = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/review', {
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

            // Check if result has review counts
            if (result && Object.keys(result).length > 0) {
                setReviewCount(result); // Set review count data
            } else {
                setReviewCount({ "result": "No Review Found" }); // Set "No Review Found" message
            }

        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleViewClick = () => {
        const reviewTableUrl = '/reviewtable';
        window.open(reviewTableUrl, '_blank');
    };

    return (
        <div className="card">
            <h2>REVIEW ANALYSIS</h2>
            <h3>PROCESS MIGHT DELAY ACCORDING TO THE COUNT OF THE REVIEWS</h3>
            <strong><p className="usegreen">Click Here to Analyze the Review in the Given Product URL</p></strong>
            <button className="button" onClick={handledetectclick}>Detect</button>
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
                    {/* Display resultData here */}
                </div>
            )}

            {reviewCount ? ( // Check if reviewCount has data
                <>
                    {reviewCount.result ? ( // Check if reviewCount has "No Review Found" message
                        <p className="usered">{reviewCount.result}</p>
                    ) : (
                        <div className="result-container">
                            <h3>Review Counts:</h3>
                            <div className="review-counts">
                                <p>Negative Legitimate Review: {reviewCount["Negative Legitimate Review"]}</p>
                                <p>Negative Misleading Review: {reviewCount["Negative Misleading Review"]}</p>
                                <p>Positive Legitimate Review: {reviewCount["Positive Legitimate Review"]}</p>
                                <p>Positive Misleading Review: {reviewCount["Positive Misleading Review"]}</p>
                            </div>
                        </div>
                    )}
                </>
            ) : null}

            <button className="button" onClick={handleViewClick}>View Reviews</button>
        </div>
    );
}

export default Review;
