import { useState, useEffect } from "react";
import axios from "axios";

const usePredictions = () => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchPredictions = async (year, month) => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/predict`,
        { year, month }
      );

      if (response.data && response.data.predictions) {
        setPredictions(response.data.predictions);
      } else {
        setError("Prediction data not found.");
      }
    } catch (err) {
      console.error(err);
      setError("Failed to fetch prediction.");
    } finally {
      setLoading(false);
    }
  };

  return { predictions, loading, error, fetchPredictions };
};

export default usePredictions;
