// Dashboard Component
// Main student dashboard with subsystem navigation and module browser

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import lmsAPI from '../api/lms';
import ModuleCard from '../components/ModuleCard';
import SubsystemNav from '../components/SubsystemNav';
import CompetencyBar from '../components/CompetencyBar';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = ({ studentId }) => {
  const navigate = useNavigate();
  const [competencies, setCompetencies] = useState([]);
  const [selectedSubsystem, setSelectedSubsystem] = useState(null);
  const [modules, setModules] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    loadCompetencies();
  }, [studentId]);

  useEffect(() => {
    if (selectedSubsystem) {
      loadModulesForSubsystem(selectedSubsystem);
    }
  }, [selectedSubsystem]);

  const loadCompetencies = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await lmsAPI.getSubsystemCompetency(studentId);
      setCompetencies(data.competencies || []);
      
      // Auto-select first subsystem
      if (data.competencies && data.competencies.length > 0) {
        setSelectedSubsystem(data.competencies[0].subsystem);
      }
    } catch (err) {
      setError(err.message);
      console.error('Failed to load competencies:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadModulesForSubsystem = async (subsystem) => {
    // This would call an endpoint to get modules by subsystem
    // For now, using recommended modules from competency data
    const competency = competencies.find(c => c.subsystem === subsystem);
    setModules(competency?.recommended_modules || []);
  };

  const handleSubsystemSelect = (subsystem) => {
    setSelectedSubsystem(subsystem);
  };

  const toggleViewMode = () => {
    setViewMode(prev => prev === 'grid' ? 'list' : 'grid');
  };

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
    document.documentElement.classList.toggle('dark');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500 text-center">
          <h2 className="text-2xl font-bold mb-2">Error Loading Dashboard</h2>
          <p>{error}</p>
          <button 
            onClick={loadCompetencies}
            className="mt-4 px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Ascent Basecamp
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Student Dashboard
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/leaderboard')}
                className="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 flex items-center gap-2"
              >
                <span>🏆</span>
                <span>Leaderboard</span>
              </button>
              
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Toggle dark mode"
              >
                {darkMode ? '☀️' : '🌙'}
              </button>
              
              <button
                onClick={toggleViewMode}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                aria-label="Toggle view mode"
              >
                {viewMode === 'grid' ? '📋' : '🔲'}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Subsystem Navigation */}
          <aside className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-4">
              <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Subsystems
              </h2>
              <SubsystemNav
                competencies={competencies}
                selectedSubsystem={selectedSubsystem}
                onSelect={handleSubsystemSelect}
              />
            </div>

            {/* Competency Overview */}
            <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow-card p-4">
              <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Your Progress
              </h3>
              {competencies.map(comp => (
                <CompetencyBar
                  key={comp.subsystem}
                  subsystem={comp.subsystem}
                  level={comp.competency_level}
                  modulesCompleted={comp.modules_completed}
                />
              ))}
            </div>
          </aside>

          {/* Main Content - Module Browser */}
          <main className="lg:col-span-3">
            {selectedSubsystem && (
              <>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white capitalize">
                    {selectedSubsystem} Modules
                  </h2>
                  <p className="text-gray-500 dark:text-gray-400 mt-1">
                    {modules.length} modules available
                  </p>
                </div>

                {/* Module Grid/List */}
                <div className={
                  viewMode === 'grid'
                    ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                    : 'space-y-4'
                }>
                  {modules.map(module => (
                    <ModuleCard
                      key={module.id}
                      module={module}
                      viewMode={viewMode}
                      studentId={studentId}
                    />
                  ))}
                </div>

                {modules.length === 0 && (
                  <div className="text-center py-12">
                    <p className="text-gray-500 dark:text-gray-400">
                      No modules available for this subsystem yet.
                    </p>
                  </div>
                )}
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
