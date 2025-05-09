import PredictionForm from "./components/prediction-form";
import Navbar from "./components/navbar";

export default function Home() {
  return (
    <main>
      <Navbar />
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
            Prediksi Harga Beras
          </h1>
          <p className="text-center text-lg text-gray-600 mb-12">
            Gunakan model interpolasi numerik untuk memprediksi harga beras
            berdasarkan data historis
          </p>
          <PredictionForm />
        </div>
      </div>
    </main>
  );
}
