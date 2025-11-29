// CelebrationModal Component
// Module completion celebration with confetti/fireworks

import React, { useEffect, useState } from 'react';
import lmsAPI from '../api/lms';

const CelebrationModal = ({ data, isRaceMode, onClose }) => {
  const [confetti, setConfetti] = useState([]);
  
  useEffect(() => {
    // Generate confetti elements
    if (data.celebration && ['legendary', 'excellent'].includes(data.celebration)) {
      const pieces = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        left: Math.random() * 100,
        delay: Math.random() * 2,
        color: ['#fbbf24', '#8b5cf6', '#3b82f6', '#10b981'][Math.floor(Math.random() * 4)]
      }));
      setConfetti(pieces);
    }
  }, [data.celebration]);

  const celebrationData = lmsAPI.getCelebrationLevel(data.celebration || 'complete');

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
      {/* Confetti */}
      {confetti.map(piece => (
        <div
          key={piece.id}
          className="absolute w-2 h-2 animate-confetti"
          style={{
            left: `${piece.left}%`,
            backgroundColor: piece.color,
            animationDelay: `${piece.delay}s`
          }}
        ></div>
      ))}

      {/* Modal */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4 animate-slide-up">
        {/* Emoji */}
        <div className="text-6xl text-center mb-6 animate-fireworks">
          {celebrationData.emoji}
        </div>

        {/* Title */}
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-4">
          {isRaceMode ? 'Race Complete!' : 'Module Complete!'}
        </h2>

        {/* Stats */}
        <div className="space-y-3 mb-6">
          {data.mastery_score !== undefined && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Mastery Score</span>
              <span className="text-xl font-bold text-primary-600 dark:text-primary-400">
                {Math.round(data.mastery_score)}%
              </span>
            </div>
          )}

          {data.time_seconds !== undefined && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Time</span>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                {lmsAPI.formatTime(data.time_seconds)}
              </span>
            </div>
          )}

          {isRaceMode && data.rank && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Rank</span>
              <span className="text-xl font-bold text-yellow-600 dark:text-yellow-400">
                #{data.rank} of {data.total_completions}
              </span>
            </div>
          )}

          {isRaceMode && data.percentile !== undefined && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Percentile</span>
              <span className="text-xl font-bold text-green-600 dark:text-green-400">
                Top {Math.round(data.percentile)}%
              </span>
            </div>
          )}

          {data.competency_level && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Competency Level</span>
              <span className={`text-lg font-bold capitalize ${lmsAPI.getCompetencyColor(data.competency_level)} bg-clip-text text-transparent`}>
                {data.competency_level}
              </span>
            </div>
          )}

          {data.modules_completed !== undefined && (
            <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="text-gray-600 dark:text-gray-400">Subsystem Progress</span>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                {data.modules_completed} modules
              </span>
            </div>
          )}
        </div>

        {/* Ghost Comparison (Race Mode) */}
        {isRaceMode && data.ghost_comparison && (
          <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-center text-blue-800 dark:text-blue-200 font-medium">
              {data.ghost_comparison.improvement}
            </p>
          </div>
        )}

        {/* Celebration Message */}
        <div className={`mb-6 p-4 rounded-lg text-center font-semibold ${
          data.celebration === 'legendary'
            ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200'
            : data.celebration === 'excellent'
            ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200'
            : data.celebration === 'good'
            ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200'
            : 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200'
        }`}>
          {data.celebration === 'legendary' && '🏆 LEGENDARY PERFORMANCE!'}
          {data.celebration === 'excellent' && '⭐ EXCELLENT WORK!'}
          {data.celebration === 'good' && '👏 GREAT JOB!'}
          {data.celebration === 'complete' && '✅ MODULE COMPLETE!'}
        </div>

        {/* Close Button */}
        <button
          onClick={onClose}
          className="w-full py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 font-semibold transition-colors"
        >
          Continue Learning
        </button>
      </div>
    </div>
  );
};

export default CelebrationModal;
