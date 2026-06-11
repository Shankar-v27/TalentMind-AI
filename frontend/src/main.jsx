import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import { AppLayout } from "./components/layout/AppLayout";
import { Dashboard } from "./pages/Dashboard";
import { JobAnalysis } from "./pages/JobAnalysis";
import { Rankings } from "./pages/Rankings";
import { CandidateDetail } from "./pages/CandidateDetail";
import { Analytics } from "./pages/Analytics";

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: "/", element: <Dashboard /> },
      { path: "/job-analysis", element: <JobAnalysis /> },
      { path: "/rankings", element: <Rankings /> },
      { path: "/candidates/:id", element: <CandidateDetail /> },
      { path: "/analytics", element: <Analytics /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
