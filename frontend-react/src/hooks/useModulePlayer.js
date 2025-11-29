// useModulePlayer Hook
// Manages state for the module player component
// Handles progress tracking, timer, activity logging, and race mode

import { useState, useEffect, useRef, useCallback } from 'react';
import lmsAPI from '../api/lms';

/**
 * Custom hook for managing module player state
 * 
 * @param {string} studentId - Current student ID
 * @param {number} moduleId - Module being played
 * @param {object} moduleData - Module configuration (steps, checks, etc.)
 * @param {boolean} isRaceMode - Whether this is a competitive race
 * @returns {object} State and methods for module player
 */
const useModulePlayer = (studentId, moduleId, moduleData, isRaceMode = false) => {
  // ========================================
  // STATE MANAGEMENT
  // ========================================
  
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState(new Set());
  const [elapsedTime, setElapsedTime] = useState(0);
  const [errorsCount, setErrorsCount] = useState(0);
  const [sessionId, setSessionId] = useState(null);
  const [attemptNumber, setAttemptNumber] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [checkResults, setCheckResults] = useState({});
  const [hints, setHints] = useState({});
  
  // Race mode specific state
  const [raceId, setRaceId] = useState(null);
  const [ghostData, setGhostData] = useState(null);
  const [timeTargets, setTimeTargets] = useState(null);
  const [checkpoints, setCheckpoints] = useState([]);
  const [checkpointStatus, setCheckpointStatus] = useState([]);
  
  // Refs for timers and intervals
  const timerRef = useRef(null);
  const activityLogRef = useRef(null);
  const startTimeRef = useRef(null);
  
  // ========================================
  // INITIALIZATION
  // ========================================
  
  useEffect(() => {
    const initializeModule = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (isRaceMode) {
          // Start race mode
          const raceData = await lmsAPI.startRace(studentId, moduleId);
          setRaceId(raceData.race_id);
          setSessionId(raceData.session_id);
          setAttemptNumber(raceData.attempt_number);
          setGhostData(raceData.ghost_data);
          setTimeTargets(raceData.time_targets);
          setCheckpoints(raceData.checkpoints || []);
          setCheckpointStatus(new Array(raceData.checkpoints?.length || 0).fill(false));
        } else {
          // Start normal module
          const startData = await lmsAPI.startModule(studentId, moduleId);
          setSessionId(startData.log_id);
          setAttemptNumber(startData.attempt_number);
        }
        
        startTimeRef.current = Date.now();
        startTimer();
        startActivityLogging();
      } catch (err) {
        setError(err.message);
        console.error('Failed to initialize module:', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    initializeModule();
    
    // Cleanup on unmount
    return () => {
      stopTimer();
      stopActivityLogging();
    };
  }, [studentId, moduleId, isRaceMode]);
  
  // ========================================
  // TIMER MANAGEMENT
  // ========================================
  
  const startTimer = useCallback(() => {
    if (timerRef.current) return; // Already running
    
    timerRef.current = setInterval(() => {
      setElapsedTime((prev) => prev + 1);
      
      // Check race checkpoints
      if (isRaceMode && checkpoints.length > 0) {
        checkpoints.forEach((checkpoint, index) => {
          if (elapsedTime >= checkpoint.target_time && !checkpointStatus[index]) {
            const newStatus = [...checkpointStatus];
            newStatus[index] = true;
            setCheckpointStatus(newStatus);
          }
        });
      }
    }, 1000);
  }, [isRaceMode, checkpoints, checkpointStatus, elapsedTime]);
  
  const stopTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);
  
  const pauseTimer = useCallback(() => {
    stopTimer();
  }, [stopTimer]);
  
  const resumeTimer = useCallback(() => {
    startTimer();
  }, [startTimer]);
  
  // ========================================
  // ACTIVITY LOGGING
  // ========================================
  
  const startActivityLogging = useCallback(() => {
    if (activityLogRef.current) return; // Already running
    
    // Log activity every 30 seconds
    activityLogRef.current = setInterval(async () => {
      try {
        await lmsAPI.logActivity(studentId, moduleId, {
          time_spent_seconds: elapsedTime,
          errors_count: errorsCount,
          attempt_number: attemptNumber
        });
      } catch (err) {
        console.error('Failed to log activity:', err);
        // Don't show error to user for background logging
      }
    }, 30000); // 30 seconds
  }, [studentId, moduleId, elapsedTime, errorsCount, attemptNumber]);
  
  const stopActivityLogging = useCallback(() => {
    if (activityLogRef.current) {
      clearInterval(activityLogRef.current);
      activityLogRef.current = null;
    }
  }, []);
  
  // ========================================
  // STEP NAVIGATION
  // ========================================
  
  const goToNextStep = useCallback(() => {
    if (currentStep < moduleData.steps.length - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  }, [currentStep, moduleData.steps.length]);
  
  const goToPreviousStep = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  }, [currentStep]);
  
  const goToStep = useCallback((stepIndex) => {
    if (stepIndex >= 0 && stepIndex < moduleData.steps.length) {
      setCurrentStep(stepIndex);
    }
  }, [moduleData.steps.length]);
  
  // ========================================
  // CHECK VALIDATION
  // ========================================
  
  const validateCheck = useCallback((checkId, userAnswer) => {
    const step = moduleData.steps[currentStep];
    const check = step.checks?.find(c => c.id === checkId);
    
    if (!check) {
      return { success: false, message: 'Check not found' };
    }
    
    const isCorrect = check.validation(userAnswer);
    
    setCheckResults((prev) => ({
      ...prev,
      [checkId]: {
        correct: isCorrect,
        userAnswer,
        timestamp: Date.now()
      }
    }));
    
    if (!isCorrect) {
      setErrorsCount((prev) => prev + 1);
    } else {
      // Mark step as completed if all checks pass
      const stepChecks = step.checks || [];
      const allChecksPassed = stepChecks.every(c => 
        checkResults[c.id]?.correct || c.id === checkId
      );
      
      if (allChecksPassed) {
        setCompletedSteps((prev) => new Set([...prev, currentStep]));
      }
    }
    
    return {
      success: isCorrect,
      message: isCorrect ? check.successMessage : check.errorMessage,
      hint: !isCorrect && check.hint ? check.hint : null
    };
  }, [currentStep, moduleData.steps, checkResults]);
  
  // ========================================
  // HINTS SYSTEM
  // ========================================
  
  const requestHint = useCallback((checkId) => {
    const step = moduleData.steps[currentStep];
    const check = step.checks?.find(c => c.id === checkId);
    
    if (check?.hint) {
      setHints((prev) => ({
        ...prev,
        [checkId]: check.hint
      }));
      return check.hint;
    }
    
    return null;
  }, [currentStep, moduleData.steps]);
  
  // ========================================
  // MODULE COMPLETION
  // ========================================
  
  const completeModule = useCallback(async (masteryScore) => {
    setIsLoading(true);
    setError(null);
    stopTimer();
    stopActivityLogging();
    
    try {
      let result;
      
      if (isRaceMode) {
        // Complete race
        result = await lmsAPI.completeRace(studentId, {
          module_id: moduleId,
          time_seconds: elapsedTime,
          errors_count: errorsCount,
          mastery_score: masteryScore
        });
      } else {
        // Complete normal module
        result = await lmsAPI.completeModule(studentId, moduleId, {
          time_spent_seconds: elapsedTime,
          errors_count: errorsCount,
          mastery_score: masteryScore,
          attempt_number: attemptNumber
        });
      }
      
      return result;
    } catch (err) {
      setError(err.message);
      console.error('Failed to complete module:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [studentId, moduleId, elapsedTime, errorsCount, attemptNumber, isRaceMode, stopTimer, stopActivityLogging]);
  
  // ========================================
  // PROGRESS CALCULATIONS
  // ========================================
  
  const progress = useCallback(() => {
    const totalSteps = moduleData.steps.length;
    const completed = completedSteps.size;
    return {
      current: currentStep + 1,
      total: totalSteps,
      completed,
      percentage: Math.round((completed / totalSteps) * 100)
    };
  }, [currentStep, moduleData.steps.length, completedSteps]);
  
  const isCurrentStepComplete = useCallback(() => {
    return completedSteps.has(currentStep);
  }, [completedSteps, currentStep]);
  
  const canProceed = useCallback(() => {
    // Can proceed if current step is complete or has no checks
    const step = moduleData.steps[currentStep];
    return !step.checks || step.checks.length === 0 || isCurrentStepComplete();
  }, [currentStep, moduleData.steps, isCurrentStepComplete]);
  
  // ========================================
  // RACE MODE HELPERS
  // ========================================
  
  const getGhostComparison = useCallback(() => {
    if (!isRaceMode || !ghostData) return null;
    
    const averageTime = ghostData.average_time || 0;
    const difference = elapsedTime - averageTime;
    
    return {
      ahead: difference < 0,
      difference: Math.abs(difference),
      message: difference < 0 
        ? `${Math.abs(difference)}s ahead of ghost` 
        : `${difference}s behind ghost`
    };
  }, [isRaceMode, ghostData, elapsedTime]);
  
  const getTimeTargetStatus = useCallback(() => {
    if (!isRaceMode || !timeTargets) return null;
    
    if (elapsedTime <= timeTargets.legendary) return 'legendary';
    if (elapsedTime <= timeTargets.excellent) return 'excellent';
    if (elapsedTime <= timeTargets.good) return 'good';
    return 'complete';
  }, [isRaceMode, timeTargets, elapsedTime]);
  
  // ========================================
  // RETURN HOOK INTERFACE
  // ========================================
  
  return {
    // State
    currentStep,
    elapsedTime,
    errorsCount,
    sessionId,
    attemptNumber,
    isLoading,
    error,
    checkResults,
    hints,
    completedSteps: Array.from(completedSteps),
    
    // Race mode state
    isRaceMode,
    raceId,
    ghostData,
    timeTargets,
    checkpoints,
    checkpointStatus,
    
    // Navigation
    goToNextStep,
    goToPreviousStep,
    goToStep,
    
    // Check validation
    validateCheck,
    requestHint,
    
    // Timer controls
    pauseTimer,
    resumeTimer,
    
    // Completion
    completeModule,
    
    // Progress helpers
    progress: progress(),
    isCurrentStepComplete: isCurrentStepComplete(),
    canProceed: canProceed(),
    
    // Race mode helpers
    getGhostComparison: getGhostComparison(),
    getTimeTargetStatus: getTimeTargetStatus()
  };
};

export default useModulePlayer;
