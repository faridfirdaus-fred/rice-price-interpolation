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

const PriceChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="premium"
          stroke="#3b82f6"
          name="Premium"
        />
        <Line type="monotone" dataKey="medium" stroke="#10b981" name="Medium" />
        <Line
          type="monotone"
          dataKey="low_quality"
          stroke="#f59e0b"
          name="Low Quality"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;