import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import DocumentChatbot from "./pages/DocumentChatbot";
import MeetingNotes from "./pages/MeetingNotes";
import SeoAnalyzer from "./pages/SeoAnalyzer";

function App() {
  return (
    <BrowserRouter>

      <div className="d-flex">

        <Sidebar />

        <div className="container-fluid p-4">

          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chatbot" element={<DocumentChatbot />} />
            <Route path="/meeting-notes" element={<MeetingNotes />} />
            <Route path="/seo-analyzer" element={<SeoAnalyzer />} />
          </Routes>

        </div>

      </div>

    </BrowserRouter>
  );
}

export default App;