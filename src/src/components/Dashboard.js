import React, { useState } from "react";
import axios from "axios";
import { Box, Button, Typography, Paper, CircularProgress, Alert } from "@mui/material";

const API_BASE_URL = "https://strattips.onrender.com"

const Dashboard = () => {
  const [insight, setInsight] = useState("");
  const [quickBooksData, setQuickBooksData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null); 
  const [error, setError] = useState(null);

  const connectQuickBooks = () => {
    setMessage("Redirecting to QuickBooks authentication...");
    window.location.replace(`${API_BASE_URL}/quickbooks/login`);
  };

  const fetchQuickBooksData = async () => {
    setLoading(true);
    setError(null);
    setMessage("Fetching QuickBooks data...");
    
    try {
      let response = await axios.get(`${API_BASE_URL}/quickbooks/data/reports/CashFlow`);

      if (response.data.error === "Access token expired, please re-authenticate") {
        await axios.get(`${API_BASE_URL}/quickbooks/refresh`);
        response = await axios.get(`${API_BASE_URL}/quickbooks/data/reports/CashFlow`);
      }

      setQuickBooksData(response.data);
      setMessage("QuickBooks data fetched successfully!");
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
      const response = await axios.get(`${API_BASE_URL}/ai-insights`);
      setInsight(response.data.insight);
    } catch (error) {
      setError(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box 
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 4,
        bgcolor: "black",
        color: "white",
        p: 4
      }}
    >
      <Typography variant="h2" fontWeight="bold">
        STRAT TIPS
      </Typography>

      <Typography variant="h4">The business dashboard that gives you quality insights.</Typography>
      <Typography variant="p">Connent with your QuickBooks, fetch the data, then generate the AI powered reccommendations.</Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 3, width: "100%", maxWidth: 600 }}>
        <Button 
          variant="contained" 
          color="primary"
          onClick={connectQuickBooks} 
          sx={{ fontSize: 20, py: 2 }}
          disabled={loading}
        >
          Connect with QuickBooks
        </Button>

        <Button 
          variant="contained" 
          color="primary"
          onClick={fetchQuickBooksData} 
          sx={{ fontSize: 20, py: 2 }}
          disabled={loading}
        >
          Fetch QuickBooks Data
        </Button>

        <Button 
          variant="contained" 
          color="primary"
          onClick={fetchInsights} 
          sx={{ fontSize: 20, py: 2 }}
          disabled={loading}
        >
          Get AI Recommendations
        </Button>
      </Box>

      {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

      {loading && <CircularProgress color="primary" />}

      {error && <Typography color="error" fontSize={18} mt={2}>{error}</Typography>}

      {insight && (
        <Paper elevation={6} sx={{ mt: 4, p: 4, width: "90%", maxWidth: "800px", minHeight: "200px", bgcolor: "gray.900" }}>
          <Typography variant="h5" fontWeight="bold" mb={2}>
            AI Recommendation
          </Typography>
          <Typography variant="body1">{insight}</Typography>
        </Paper>
      )}

      {quickBooksData && (
        <Paper elevation={6} sx={{ mt: 4, p: 4, width: "90%", maxWidth: "800px", minHeight: "200px", bgcolor: "gray.900" }}>
          <Typography variant="h5" fontWeight="bold" mb={2}>
            QuickBooks Data
          </Typography>
          <Typography component="pre" sx={{ fontSize: 14, whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
            {JSON.stringify(quickBooksData, null, 2)}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default Dashboard;
