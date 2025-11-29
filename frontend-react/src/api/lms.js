// LMS API Service Layer
// Consumes the 8 Ascent Basecamp endpoints created by Agent Beta

import axios from 'axios';

// Base configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/lms';

// Create axios instance with interceptors
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens (future enhancement)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token when implemented
    // const token = localStorage.getItem('authToken');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ========================================
// MODULE LIFECYCLE ENDPOINTS
// ========================================

/**
 * Start a learning module session
 * POST /students/{student_id}/modules/{module_id}/start
 * 
 * @param {string} studentId - Student identifier
 * @param {number} moduleId - Module ID
 * @returns {Promise} Response with log_id, attempt_number, started_at
 */
export const startModule = async (studentId, moduleId) => {
  try {
    const response = await apiClient.post(
      `/students/${studentId}/modules/${moduleId}/start`
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to start module: ${error.response?.data?.error || error.message}`);
  }
};

/**
 * Log activity during module (time spent, errors)
 * POST /students/{student_id}/modules/{module_id}/log_activity
 * 
 * @param {string} studentId - Student identifier
 * @param {number} moduleId - Module ID
 * @param {object} activityData - {time_spent_seconds, errors_count, attempt_number?}
 * @returns {Promise} Response with updated activity log
 */
export const logActivity = async (studentId, moduleId, activityData) => {
  try {
    const response = await apiClient.post(
      `/students/${studentId}/modules/${moduleId}/log_activity`,
      activityData
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to log activity: ${error.response?.data?.error || error.message}`);
  }
};

/**
 * Complete a module with final score
 * POST /students/{student_id}/modules/{module_id}/complete
 * 
 * @param {string} studentId - Student identifier
 * @param {number} moduleId - Module ID
 * @param {object} completionData - {time_spent_seconds, errors_count, mastery_score, attempt_number?}
 * @returns {Promise} Response with competency_level, modules_completed, completed_at
 */
export const completeModule = async (studentId, moduleId, completionData) => {
  try {
    const response = await apiClient.post(
      `/students/${studentId}/modules/${moduleId}/complete`,
      completionData
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to complete module: ${error.response?.data?.error || error.message}`);
  }
};

// ========================================
// COMPETITIVE FEATURES ENDPOINTS
// ========================================

/**
 * Get ghost cohort benchmark data for a module
 * GET /modules/{module_id}/ghost_cohorts
 * 
 * @param {number} moduleId - Module ID
 * @returns {Promise} Response with ghost_cohorts, time_targets, checkpoints
 */
export const getGhostCohorts = async (moduleId) => {
  try {
    const response = await apiClient.get(`/modules/${moduleId}/ghost_cohorts`);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get ghost cohorts: ${error.response?.data?.error || error.message}`);
  }
};

/**
 * Get leaderboard rankings
 * GET /students/{student_id}/leaderboard
 * 
 * @param {string} studentId - Student identifier
 * @param {object} filters - {subsystem?, module_id?}
 * @returns {Promise} Response with top_10, student_rank
 */
export const getLeaderboard = async (studentId, filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.subsystem) params.append('subsystem', filters.subsystem);
    if (filters.module_id) params.append('module_id', filters.module_id);
    
    const response = await apiClient.get(
      `/students/${studentId}/leaderboard?${params.toString()}`
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get leaderboard: ${error.response?.data?.error || error.message}`);
  }
};

/**
 * Get subsystem competency levels and recommendations
 * GET /students/{student_id}/subsystem_competency
 * 
 * @param {string} studentId - Student identifier
 * @returns {Promise} Response with competencies array (subsystem, level, modules_completed, recommended_modules)
 */
export const getSubsystemCompetency = async (studentId) => {
  try {
    const response = await apiClient.get(`/students/${studentId}/subsystem_competency`);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get competency: ${error.response?.data?.error || error.message}`);
  }
};

// ========================================
// RACE MODE ENDPOINTS
// ========================================

/**
 * Start a competitive race against ghost cohorts
 * POST /students/{student_id}/race/start
 * 
 * @param {string} studentId - Student identifier
 * @param {number} moduleId - Module ID
 * @returns {Promise} Response with race_id, session_id, ghost_data, time_targets, checkpoints
 */
export const startRace = async (studentId, moduleId) => {
  try {
    const response = await apiClient.post(
      `/students/${studentId}/race/start`,
      { module_id: moduleId }
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to start race: ${error.response?.data?.error || error.message}`);
  }
};

/**
 * Complete a race and get results
 * POST /students/{student_id}/race/complete
 * 
 * @param {string} studentId - Student identifier
 * @param {object} raceData - {module_id, time_seconds, errors_count, mastery_score}
 * @returns {Promise} Response with rank, percentile, celebration, ghost_comparison
 */
export const completeRace = async (studentId, raceData) => {
  try {
    const response = await apiClient.post(
      `/students/${studentId}/race/complete`,
      raceData
    );
    return response.data;
  } catch (error) {
    throw new Error(`Failed to complete race: ${error.response?.data?.error || error.message}`);
  }
};

// ========================================
// HELPER UTILITIES
// ========================================

/**
 * Format time in seconds to mm:ss display
 */
export const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

/**
 * Calculate completion percentage
 */
export const calculateProgress = (currentStep, totalSteps) => {
  return Math.round((currentStep / totalSteps) * 100);
};

/**
 * Get competency level color for UI
 */
export const getCompetencyColor = (level) => {
  const colors = {
    orientation: 'bg-blue-500',
    competency: 'bg-green-500',
    integration: 'bg-purple-500',
    autonomy: 'bg-gold-500'
  };
  return colors[level] || 'bg-gray-500';
};

/**
 * Get celebration animation level
 */
export const getCelebrationLevel = (celebration) => {
  const levels = {
    legendary: { emoji: '🏆', animation: 'fireworks', color: 'gold' },
    excellent: { emoji: '🎉', animation: 'confetti', color: 'purple' },
    good: { emoji: '👏', animation: 'applause', color: 'blue' },
    complete: { emoji: '✅', animation: 'checkmark', color: 'green' }
  };
  return levels[celebration] || levels.complete;
};

// Default export with all methods
const lmsAPI = {
  startModule,
  logActivity,
  completeModule,
  getGhostCohorts,
  getLeaderboard,
  getSubsystemCompetency,
  startRace,
  completeRace,
  formatTime,
  calculateProgress,
  getCompetencyColor,
  getCelebrationLevel
};

export default lmsAPI;
