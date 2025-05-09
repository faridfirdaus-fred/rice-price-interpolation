import { useEffect, useState } from "react";
import PredictionForm from "@/components/prediction-form";
import PriceChart from "@/app/components/price-chart";
import PriceCard from "@/app/components/price-card";

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchPredictions = async (year, month) => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`/api/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ year, month }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch predictions");
      }

      const data = await response.json();
      setPredictions(data.predictions);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Rice Price Predictions</h1>
      <PredictionForm onSubmit={fetchPredictions} />
      {loading && <p>Loading predictions...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {predictions && (
        <div className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {["premium", "medium", "low_quality"].map((quality) => (
              <PriceCard
                key={quality}
                quality={quality}
                data={predictions[quality]}
              />
            ))}
          </div>
          <PriceChart data={predictions} />
        </div>
      )}
    </div>
  );
};

export default PredictionsPage;
