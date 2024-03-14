import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import './Card.css'; // Import your CSS file for styling

const ProductInfo = () => {
    const location = useLocation();
    const Url = location.state;
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);

    const handleclick = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/rating-review', {
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
            <h2>PRODUCT INFORMATION</h2>
            <strong><p className="usegreen">Click Here to Check the Product Information</p></strong>
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
                    {resultData.rating && resultData.rating_count && resultData.review_count ? (
                        <>
                            <strong><p className="useblue">Product Name: {resultData.product_title}</p></strong>
                            <p className="usered">Rating: {resultData.rating}</p>
                            <p className="usered">Rating Count: {resultData.rating_count}</p>
                            <p className="usered">Review Count: {resultData.review_count}</p>
                        </>
                    ) : (
                        <>
                            <strong><p className="useblue">Product Name: {resultData.product_title}</p></strong>
                            <p className="usered">Result: {resultData.result}</p>
                        </>
                    )}
                </div>
            )}
        </div>
    );
}

export default ProductInfo;
