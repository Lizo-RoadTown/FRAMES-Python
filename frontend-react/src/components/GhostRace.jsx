// GhostRace Component
// Split-screen race visualization with ghost cohort comparison

import React from 'react';
import lmsAPI from '../api/lms';

const GhostRace = ({ 
  elapsedTime, 
  currentStep, 
  totalSteps, 
  ghostData, 
  checkpoints, 
  checkpointStatus 
}) => {
  // Calculate progress percentages
  const studentProgress = (currentStep / totalSteps) * 100;
  
  // Estimate ghost progress based on average time
  const ghostAverageTime = ghostData?.average_time || 300;
  const ghostProgress = Math.min(100, (elapsedTime / ghostAverageTime) * 100);

  // Determine who's ahead
  const studentAhead = studentProgress > ghostProgress;
  const progressDiff = Math.abs(studentProgress - ghostProgress);

  return (
    <div className="bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-800">
      <div className="mb-4">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
          👻 Ghost Race
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Racing against {ghostData?.cohort_name || 'Ghost Cohort'}
        </p>
      </div>

      {/* Split Screen Progress Bars */}
      <div className="space-y-4">
        {/* Student Progress */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-lg">🎓</span>
              <span className="font-semibold text-gray-900 dark:text-white">You</span>
            </div>
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {Math.round(studentProgress)}%
            </span>
          </div>
          <div className="relative h-8 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${
                studentAhead
                  ? 'bg-gradient-to-r from-green-500 to-green-600'
                  : 'bg-gradient-to-r from-blue-500 to-blue-600'
              }`}
              style={{ width: `${studentProgress}%` }}
            >
              <div className="h-full flex items-center justify-end pr-2">
                <span className="text-white font-bold text-xs">🏃</span>
              </div>
            </div>
          </div>
        </div>

        {/* Ghost Progress */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-lg">👻</span>
              <span className="font-semibold text-gray-900 dark:text-white">Ghost</span>
            </div>
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {Math.round(ghostProgress)}%
            </span>
          </div>
          <div className="relative h-8 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-purple-600 transition-all duration-500 opacity-70"
              style={{ width: `${ghostProgress}%` }}
            >
              <div className="h-full flex items-center justify-end pr-2">
                <span className="text-white font-bold text-xs">👻</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Gap Indicator */}
      <div className={`mt-4 p-3 rounded-lg text-center font-semibold ${
        studentAhead
          ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200'
          : 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-200'
      }`}>
        {studentAhead ? (
          <span>🔥 You're ahead by {Math.round(progressDiff)}%!</span>
        ) : progressDiff < 5 ? (
          <span>⚡ Neck and neck! Keep pushing!</span>
        ) : (
          <span>⚡ Ghost is ahead by {Math.round(progressDiff)}% - catch up!</span>
        )}
      </div>

      {/* Checkpoints */}
      {checkpoints && checkpoints.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
            Checkpoints
          </h4>
          <div className="grid grid-cols-3 gap-2">
            {checkpoints.map((checkpoint, index) => {
              const passed = checkpointStatus[index];
              const isCurrent = currentStep === checkpoint.step - 1;

              return (
                <div
                  key={index}
                  className={`p-2 rounded text-center text-xs font-medium ${
                    passed
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200'
                      : isCurrent
                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 ring-2 ring-blue-400'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                  }`}
                >
                  <div className="font-bold">Step {checkpoint.step}</div>
                  <div className="text-xs">{lmsAPI.formatTime(checkpoint.target_time)}</div>
                  {passed && <div className="text-lg">✓</div>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Ghost Stats */}
      {ghostData && (
        <div className="mt-4 pt-4 border-t border-purple-200 dark:border-purple-700">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="text-center">
              <div className="text-gray-500 dark:text-gray-400">Avg Time</div>
              <div className="font-bold text-gray-900 dark:text-white">
                {lmsAPI.formatTime(ghostData.average_time)}
              </div>
            </div>
            <div className="text-center">
              <div className="text-gray-500 dark:text-gray-400">Avg Score</div>
              <div className="font-bold text-gray-900 dark:text-white">
                {Math.round(ghostData.average_score)}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GhostRace;
