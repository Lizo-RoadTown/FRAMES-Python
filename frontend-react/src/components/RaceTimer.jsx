// RaceTimer Component
// Race mode timer with ghost comparison and targets

import React from 'react';
import lmsAPI from '../api/lms';

const RaceTimer = ({ elapsedTime, timeTargets, ghostComparison, targetStatus }) => {
  const formattedTime = lmsAPI.formatTime(elapsedTime);

  const getTargetColor = () => {
    switch (targetStatus) {
      case 'legendary':
        return 'text-yellow-500';
      case 'excellent':
        return 'text-purple-500';
      case 'good':
        return 'text-blue-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <div className="flex items-center gap-4">
      {/* Main Timer */}
      <div className={`text-2xl font-mono font-bold ${getTargetColor()}`}>
        ⏱️ {formattedTime}
      </div>

      {/* Ghost Comparison */}
      {ghostComparison && (
        <div className={`text-sm font-medium ${
          ghostComparison.ahead
            ? 'text-green-600 dark:text-green-400'
            : 'text-red-600 dark:text-red-400'
        }`}>
          {ghostComparison.ahead ? '↑' : '↓'} {ghostComparison.message}
        </div>
      )}

      {/* Target Badge */}
      {targetStatus && (
        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
          targetStatus === 'legendary'
            ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200'
            : targetStatus === 'excellent'
            ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200'
            : targetStatus === 'good'
            ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
        }`}>
          {targetStatus.toUpperCase()}
        </div>
      )}
    </div>
  );
};

export default RaceTimer;
