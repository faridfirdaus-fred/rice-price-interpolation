"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Button } from "./ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import PredictionResults from "./prediction-results";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Loader2 } from "lucide-react";

const formSchema = z.object({
  year: z.string().min(1, "Year is required"),
  month: z.string().min(1, "Month is required"),
});

const PredictionForm = () => {
  const [loading, setLoading] = useState(false);
  const [predictionData, setPredictionData] = useState(null);
  const [error, setError] = useState(null);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      year: new Date().getFullYear().toString(),
      month: (new Date().getMonth() + 1).toString(),
    },
  });

  const onSubmit = async (data) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/predictions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          year: parseInt(data.year),
          month: parseInt(data.month),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction data");
      }

      const result = await response.json();
      setPredictionData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Generate year options from 2013 to current year + 5
  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from(
    { length: currentYear - 2013 + 6 },
    (_, i) => 2013 + i
  );

  // Month names
  const months = [
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

  return (
    <div className="w-full max-w-xl mx-auto">
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-t-lg">
          <CardTitle className="text-2xl">Prediksi Harga Beras</CardTitle>
          <CardDescription className="text-blue-100">
            Masukkan tahun dan bulan untuk memprediksi harga beras
          </CardDescription>
        </CardHeader>

        <CardContent className="pt-6">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  control={form.control}
                  name="year"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Tahun</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Pilih tahun" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="max-h-[300px]">
                          {yearOptions.map((year) => (
                            <SelectItem key={year} value={year.toString()}>
                              {year}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="month"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Bulan</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Pilih bulan" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {months.map((month, index) => (
                            <SelectItem
                              key={index + 1}
                              value={(index + 1).toString()}
                            >
                              {month}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button
                type="submit"
                className="w-full font-medium"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Memproses...
                  </>
                ) : (
                  "Prediksi Harga"
                )}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          <p>Error: {error}</p>
        </div>
      )}

      {predictionData && !error && (
        <div className="mt-6">
          <PredictionResults data={predictionData} />
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
