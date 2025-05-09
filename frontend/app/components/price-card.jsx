import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

const PriceCard = ({ quality, estimatedPrice, previousPrice }) => {
  const priceDifference = estimatedPrice - previousPrice;
  const percentageChange = ((priceDifference / previousPrice) * 100).toFixed(2);
  const isIncrease = priceDifference > 0;

  const qualityDisplayNames = {
    premium: "Premium",
    medium: "Medium",
    low_quality: "Kualitas Rendah",
  };

  return (
    <Card className="shadow-sm hover:shadow-md transition-shadow">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg capitalize">
          {qualityDisplayNames[quality] || quality.replace("_", " ")}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div>
            <p className="text-sm text-muted-foreground">Harga Prediksi</p>
            <p className="text-2xl font-bold text-blue-700">
              Rp{" "}
              {estimatedPrice.toLocaleString("id-ID", {
                minimumFractionDigits: 0,
              })}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Harga Sebelumnya</p>
            <p className="text-lg text-gray-700">
              Rp{" "}
              {previousPrice.toLocaleString("id-ID", {
                minimumFractionDigits: 0,
              })}
            </p>
          </div>

          <div
            className={`flex items-center mt-2 ${
              isIncrease ? "text-red-600" : "text-green-600"
            }`}
          >
            {isIncrease ? (
              <TrendingUp className="h-4 w-4 mr-1" />
            ) : (
              <TrendingDown className="h-4 w-4 mr-1" />
            )}
            <span className="font-medium">
              {isIncrease ? "+" : ""}
              {percentageChange}%
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceCard;
