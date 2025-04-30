"use client";

import { useState } from "react";
import axios from "axios";
import CountUp from "react-countup";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const PredictionForm = () => {
  const [year, setYear] = useState(2025);
  const [month, setMonth] = useState(4);
  const [predictions, setPredictions] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPredictions(null);

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

  const chartData = predictions
    ? [
        {
          name: "Harga Sebelumnya",
          premium: predictions.premium.previous_price,
          medium: predictions.medium.previous_price,
          low_quality: predictions.low_quality.previous_price,
        },
        {
          name: "Prediksi",
          premium: predictions.premium.estimated_price,
          medium: predictions.medium.estimated_price,
          low_quality: predictions.low_quality.estimated_price,
        },
      ]
    : [];

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md mt-2">
      <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
        Prediksi Harga Beras
      </h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="year" className="block text-gray-700 mb-1">
            Tahun
          </label>
          <select
            id="year"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            required
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {Array.from({ length: 15 }, (_, i) => {
              const y = 2013 + i;
              return (
                <option key={y} value={y}>
                  {y}
                </option>
              );
            })}
          </select>
        </div>

        <div>
          <label htmlFor="month" className="block text-gray-700 mb-1">
            Bulan
          </label>
          <select
            id="month"
            value={month}
            onChange={(e) => setMonth(Number(e.target.value))}
            required
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={1}>Januari</option>
            <option value={2}>Februari</option>
            <option value={3}>Maret</option>
            <option value={4}>April</option>
            <option value={5}>Mei</option>
            <option value={6}>Juni</option>
            <option value={7}>Juli</option>
            <option value={8}>Agustus</option>
            <option value={9}>September</option>
            <option value={10}>Oktober</option>
            <option value={11}>November</option>
            <option value={12}>Desember</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 font-semibold rounded-md transition-colors
            ${
              loading
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600"
            }
            text-white focus:outline-none focus:ring-2 focus:ring-blue-500`}
        >
          {loading ? "Memprediksi..." : "Submit"}
        </button>
      </form>

      {predictions && (
        <div className="mt-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {["premium", "medium", "low_quality"].map((quality) => (
              <div
                key={quality}
                className="p-4 bg-green-100 text-green-800 rounded-md text-center"
              >
                <h2 className="text-lg font-semibold capitalize">
                  {quality.replace("_", " ")}
                </h2>
                <p className="text-sm text-gray-600">Harga Prediksi</p>
                <p className="text-2xl font-bold">
                  Rp.{" "}
                  <CountUp
                    end={predictions[quality].estimated_price}
                    duration={1}
                    separator="."
                    decimal=","
                    decimals={2}
                  />
                </p>
              </div>
            ))}
          </div>

          <div className="mt-6 w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip
                  formatter={(value) =>
                    `Rp. ${value.toLocaleString("id-ID", {
                      minimumFractionDigits: 2,
                    })}`
                  }
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="premium"
                  stroke="#3b82f6"
                  activeDot={{ r: 8 }}
                  name="Premium"
                />
                <Line
                  type="monotone"
                  dataKey="medium"
                  stroke="#10b981"
                  name="Medium"
                />
                <Line
                  type="monotone"
                  dataKey="low_quality"
                  stroke="#f59e0b"
                  name="Low Quality"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {error && <div className="mt-4 text-red-500 text-center">{error}</div>}
    </div>
  );
};

export default PredictionForm;
