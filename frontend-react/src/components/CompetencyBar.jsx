// CompetencyBar Component
// Visual progress indicator for subsystem competency

import React from 'react';
import lmsAPI from '../api/lms';

const CompetencyBar = ({ subsystem, level, modulesCompleted }) => {
  const levels = ['orientation', 'competency', 'integration', 'autonomy'];
  const currentLevelIndex = levels.indexOf(level);
  const progress = ((currentLevelIndex + 1) / levels.length) * 100;

  const colorClass = lmsAPI.getCompetencyColor(level);

  return (
    <div className="mb-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
          {subsystem}
        </span>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {modulesCompleted} modules
        </span>
      </div>
      
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-500 ${colorClass}`}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      
      <div className="mt-1 text-xs text-gray-500 dark:text-gray-400 capitalize">
        {level}
      </div>
    </div>
  );
};

export default CompetencyBar;
