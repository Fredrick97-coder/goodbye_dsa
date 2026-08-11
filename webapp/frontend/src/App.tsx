import { Navigate, Route, Routes } from "react-router-dom";
import { Shell } from "./components/Shell";
import Dashboard from "./routes/Dashboard";
import Problems from "./routes/Problems";
import Progress from "./routes/Progress";
import Solve from "./routes/Solve";

/**
 * Routes.
 *
 * The solve view lives at /problems/:id so a problem is a real URL -- it can be
 * bookmarked, opened in a second tab, and linked to from anywhere in the app.
 */
export default function App() {
  return (
    <Routes>
      <Route element={<Shell />}>
        <Route index element={<Dashboard />} />
        <Route path="problems" element={<Problems />} />
        <Route path="problems/:id" element={<Solve />} />
        <Route path="progress" element={<Progress />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
