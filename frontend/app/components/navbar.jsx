import Link from "next/link";
import { Button } from "./ui/button";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-white text-2xl font-bold">Rice Price Predictor</h1>
        <div className="flex space-x-4">
          <Link href="/" className="text-white hover:text-blue-200">
            Home
          </Link>
          <Link href="/predictions" className="text-white hover:text-blue-200">
            Predictions
          </Link>
          <Button className="bg-white text-blue-600 hover:bg-gray-200">
            Get Started
          </Button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
