import React, { useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [insight, setInsight] = useState("");
  const [quickBooksData, setQuickBooksData] = useState(null); // Store QuickBooks data
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const connectQuickBooks = () => {
    window.location.href = "http://127.0.0.1:8000/quickbooks/login"; // Redirect user for authentication
  };

  const fetchQuickBooksData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let response = await axios.get("http://127.0.0.1:8000/quickbooks/data/reports/CashFlow");

      if (response.data.error === "Access token expired, please re-authenticate") {
        await axios.get("http://127.0.0.1:8000/quickbooks/refresh");
        response = await axios.get("http://127.0.0.1:8000/quickbooks/data/reports/CashFlow");
      }

      setQuickBooksData(response.data); // Store the fetched data in state
    } catch (error) {
      setError(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchInsights = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get("http://127.0.0.1:8000/ai-insights");
      setInsight(response.data.insight);
    } catch (error) {
      setError(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 flex flex-col items-center space-y-6">
      <h1 className="text-2xl font-bold">Business Insights</h1>

      <button 
        onClick={connectQuickBooks} 
        className="w-full max-w-sm bg-blue-500 text-white p-2 rounded"
        disabled={loading}
      >
        Connect with QuickBooks
      </button>

      <button 
        onClick={fetchQuickBooksData} 
        className="w-full max-w-sm bg-indigo-500 text-white p-2 rounded"
        disabled={loading}
      >
        Fetch QuickBooks Data
      </button>

      <button 
        onClick={fetchInsights} 
        className="w-full max-w-sm bg-green-500 text-white p-2 rounded"
        disabled={loading}
      >
        Get AI Recommendations
      </button>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {insight && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg w-full max-w-lg text-center">
          <h2 className="text-lg font-semibold">AI Recommendation</h2>
          <p>{insight}</p>
        </div>
      )}

      {quickBooksData && (
        <div className="mt-4 p-4 bg-gray-200 rounded-lg w-full max-w-lg">
          <h2 className="text-lg font-semibold">QuickBooks Data</h2>
          <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(quickBooksData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
