import React from "react";
import Urgency from "./Urgency";
import Review from "./Review";
import Timerscarcity from "./Timescarcity";
import ProductInfo from "./ProductInfo";
import Discount from "./Discount";

const Result = () => {
    // const location = useLocation();
    // const Url = location.state;
    // const navigate = useNavigate();
    return (
        <div>
            <ProductInfo/>
            <Discount/>
            <Review/>
            <Timerscarcity/>
            <Urgency />
        </div>
    );
}

export default Result;
