// Leaderboard Component
// Rankings display with filtering and student position

import React, { useState, useEffect } from 'react';
import lmsAPI from '../api/lms';
import LoadingSpinner from '../components/LoadingSpinner';

const Leaderboard = ({ studentId }) => {
  const [leaderboardData, setLeaderboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    subsystem: '',
    module_id: ''
  });

  useEffect(() => {
    loadLeaderboard();
  }, [studentId, filters]);

  const loadLeaderboard = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await lmsAPI.getLeaderboard(studentId, filters);
      setLeaderboardData(data);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load leaderboard:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner message="Loading leaderboard..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-500 text-center">
          <h2 className="text-2xl font-bold mb-2">Error Loading Leaderboard</h2>
          <p>{error}</p>
          <button 
            onClick={loadLeaderboard}
            className="mt-4 px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            🏆 Leaderboard
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            See how you rank against other students
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-4 mb-6">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Filter by Subsystem
              </label>
              <select
                value={filters.subsystem}
                onChange={(e) => handleFilterChange('subsystem', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
              >
                <option value="">All Subsystems</option>
                <option value="power">Power</option>
                <option value="avionics">Avionics</option>
                <option value="propulsion">Propulsion</option>
                <option value="structures">Structures</option>
                <option value="thermal">Thermal</option>
                <option value="communications">Communications</option>
              </select>
            </div>

            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Filter by Module
              </label>
              <input
                type="number"
                value={filters.module_id}
                onChange={(e) => handleFilterChange('module_id', e.target.value)}
                placeholder="Module ID (optional)"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white"
              />
            </div>

            <button
              onClick={() => setFilters({ subsystem: '', module_id: '' })}
              className="mt-7 px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
            >
              Clear Filters
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Top 10 Leaderboard */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Top 10 Students
                </h2>
              </div>

              <div className="divide-y divide-gray-200 dark:divide-gray-700">
                {leaderboardData?.top_10?.map((student, index) => (
                  <div
                    key={student.student_id}
                    className={`p-4 flex items-center gap-4 ${
                      index < 3 ? 'bg-yellow-50 dark:bg-yellow-900/10' : ''
                    }`}
                  >
                    {/* Rank Badge */}
                    <div className={`flex items-center justify-center w-12 h-12 rounded-full font-bold text-lg ${
                      index === 0
                        ? 'bg-yellow-400 text-yellow-900'
                        : index === 1
                        ? 'bg-gray-300 text-gray-900'
                        : index === 2
                        ? 'bg-orange-400 text-orange-900'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}>
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${student.rank}`}
                    </div>

                    {/* Student Info */}
                    <div className="flex-1">
                      <div className="font-semibold text-gray-900 dark:text-white">
                        Student {student.student_id}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {student.attempts} attempt{student.attempts !== 1 ? 's' : ''}
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="text-right">
                      <div className="text-lg font-bold text-primary-600 dark:text-primary-400">
                        {Math.round(student.best_score)}%
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {lmsAPI.formatTime(student.best_time)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Your Position */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-6 sticky top-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Your Position
              </h2>

              {leaderboardData?.student_rank ? (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-5xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                      #{leaderboardData.student_rank.rank}
                    </div>
                    <div className="text-gray-500 dark:text-gray-400">
                      out of {leaderboardData.top_10?.length || 0}+ students
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-gray-600 dark:text-gray-400">Best Score</span>
                      <span className="text-lg font-bold text-gray-900 dark:text-white">
                        {Math.round(leaderboardData.student_rank.best_score)}%
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-gray-600 dark:text-gray-400">Best Time</span>
                      <span className="text-lg font-bold text-gray-900 dark:text-white">
                        {lmsAPI.formatTime(leaderboardData.student_rank.best_time)}
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-gray-600 dark:text-gray-400">Attempts</span>
                      <span className="text-lg font-bold text-gray-900 dark:text-white">
                        {leaderboardData.student_rank.attempts}
                      </span>
                    </div>
                  </div>

                  {leaderboardData.student_rank.rank > 10 && (
                    <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg text-center">
                      <p className="text-sm text-blue-800 dark:text-blue-200">
                        Keep going! You're doing great! 🚀
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center text-gray-500 dark:text-gray-400">
                  <p>Complete a module to see your ranking!</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
