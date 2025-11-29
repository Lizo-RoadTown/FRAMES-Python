import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ModulePlayer from './pages/ModulePlayer';
import Leaderboard from './pages/Leaderboard';

function App() {
  // TODO: Get from authentication system
  const studentId = 'student_001';

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard studentId={studentId} />} />
        <Route path="/leaderboard" element={<Leaderboard studentId={studentId} />} />
        <Route path="/module/:moduleId" element={<ModulePlayer studentId={studentId} />} />
        <Route path="/module/:moduleId/race" element={<ModulePlayer studentId={studentId} isRaceMode={true} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
