// ModuleCard Component
// Displays module information in grid or list view

import React from 'react';
import { useNavigate } from 'react-router-dom';
import lmsAPI from '../api/lms';

const ModuleCard = ({ module, viewMode = 'grid', studentId }) => {
  const navigate = useNavigate();

  const handleStartModule = () => {
    navigate(`/module/${module.id}`);
  };

  const handleStartRace = () => {
    navigate(`/module/${module.id}/race`);
  };

  if (viewMode === 'list') {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card hover:shadow-card-hover transition-shadow p-4 flex items-center justify-between">
        <div className="flex items-center gap-4 flex-1">
          <div className="text-3xl">📚</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {module.title}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              ⏱️ {module.estimated_minutes} minutes
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleStartModule}
            className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            Start
          </button>
          <button
            onClick={handleStartRace}
            className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            title="Race Mode"
          >
            🏁
          </button>
        </div>
      </div>
    );
  }

  // Grid view
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card hover:shadow-card-hover transition-shadow p-6 animate-fade-in">
      <div className="text-4xl mb-4 text-center">📚</div>
      
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {module.title}
      </h3>
      
      <div className="space-y-2 mb-4">
        <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
          <span className="mr-2">⏱️</span>
          <span>{module.estimated_minutes} minutes</span>
        </div>
        
        {module.difficulty && (
          <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <span className="mr-2">📊</span>
            <span className="capitalize">{module.difficulty}</span>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <button
          onClick={handleStartModule}
          className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
        >
          Start Module
        </button>
        
        <button
          onClick={handleStartRace}
          className="w-full px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors flex items-center justify-center gap-2"
        >
          <span>🏁</span>
          <span>Race Mode</span>
        </button>
      </div>
    </div>
  );
};

export default ModuleCard;
