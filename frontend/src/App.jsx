import { Navigate, Route, Routes } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TicketsPage from './pages/TicketsPage';
import WorklogsPage from './pages/WorklogsPage';
import ReportsPage from './pages/ReportsPage';
import { useAuth } from './context/AuthContext';

function ProtectedRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <>
      <NavigationBar />
      <div className="container py-4">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/tickets" element={<ProtectedRoute><TicketsPage /></ProtectedRoute>} />
          <Route path="/worklogs" element={<ProtectedRoute><WorklogsPage /></ProtectedRoute>} />
          <Route path="/reports" element={<ProtectedRoute><ReportsPage /></ProtectedRoute>} />
        </Routes>
      </div>
    </>
  );
}
