import React from 'react';
import reviews from './reviewresult/reviews_with_sentiment.json'; // Import the JSON data
import './ReviewTable.css'; // Import your CSS file for styling

const ReviewTable = () => {
    return (
        <div className="review-table-container">
            <h2 className="review-table-heading">Reviews</h2>
            <table className="review-table">
                <thead>
                    <tr>
                        <th>User Name</th>
                        <th>Title</th>
                        <th>Review</th>
                        <th>Response</th>
                    </tr>
                </thead>
                <tbody>
                    {reviews.map(review => (
                        <tr key={review.id}>
                            <td>{review['User Name']}</td>
                            <td>{review.Title}</td>
                            <td>{review.Review}</td>
                            <td>{review.Response}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ReviewTable;
