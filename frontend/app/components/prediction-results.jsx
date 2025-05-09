import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import PriceCard from "./price-card";
import PriceChart from "./price-chart";

const PredictionResults = ({ data }) => {
  if (!data || !data.predictions) {
    return null;
  }

  const { year, month, predictions } = data;

  const monthNames = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
  ];

  const monthName = monthNames[month - 1];

  // Prepare chart data
  const chartData = [
    {
      name: "Previous",
      premium: predictions.premium?.previous_price || 0,
      medium: predictions.medium?.previous_price || 0,
      low_quality: predictions.low_quality?.previous_price || 0,
    },
    {
      name: "Predicted",
      premium: predictions.premium?.estimated_price || 0,
      medium: predictions.medium?.estimated_price || 0,
      low_quality: predictions.low_quality?.estimated_price || 0,
    },
  ];

  return (
    <Card className="shadow-lg">
      <CardHeader className="bg-gradient-to-r from-green-600 to-green-800 text-white rounded-t-lg">
        <CardTitle className="text-xl">
          Hasil Prediksi: {monthName} {year}
        </CardTitle>
      </CardHeader>

      <CardContent className="pt-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {Object.entries(predictions).map(([quality, prices]) => (
            <PriceCard
              key={quality}
              quality={quality}
              estimatedPrice={prices.estimated_price}
              previousPrice={prices.previous_price}
            />
          ))}
        </div>

        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-3">Perbandingan Harga</h3>
          <div className="h-[350px] border rounded-lg p-3">
            <PriceChart data={chartData} />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictionResults;
