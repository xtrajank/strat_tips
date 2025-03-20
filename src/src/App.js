import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import EULA from "./pages/EULA";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import Dashboard from "./components/Dashboard";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/eula" element={<EULA />} />
                <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            </Routes>
        </Router>
    );
}

export default App;
