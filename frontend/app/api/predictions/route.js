import { NextResponse } from "next/server";
import axios from "axios";

export async function POST(request) {
  const { year, month } = await request.json();

  // Check if environment variable exists
  if (!process.env.NEXT_PUBLIC_API_URL) {
    console.error("Missing NEXT_PUBLIC_API_URL environment variable");
    return NextResponse.json(
      { error: "API configuration error" },
      { status: 500 }
    );
  }

  try {
    console.log(
      `Sending request to: ${process.env.NEXT_PUBLIC_API_URL}/predict`
    );

    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/predict`,
      {
        year,
        month,
      }
    );

    return NextResponse.json(response.data);
  } catch (error) {
    console.error("API request failed:", error.message);

    // More detailed error response
    return NextResponse.json(
      {
        error: "Failed to fetch predictions",
        details: error.response?.data || error.message,
      },
      { status: error.response?.status || 500 }
    );
  }
}
