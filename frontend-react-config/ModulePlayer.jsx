// ModulePlayer Component
// Step-by-step module interface with checks, hints, timer, and race mode

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useModulePlayer from '../hooks/useModulePlayer';
import ProgressStepper from '../components/ProgressStepper';
import CheckValidation from '../components/CheckValidation';
import HintTooltip from '../components/HintTooltip';
import RaceTimer from '../components/RaceTimer';
import CelebrationModal from '../components/CelebrationModal';
import lmsAPI from '../api/lms';

const ModulePlayer = ({ studentId, moduleData, isRaceMode = false }) => {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  
  const {
    currentStep,
    elapsedTime,
    errorsCount,
    isLoading,
    error,
    checkResults,
    hints,
    completedSteps,
    isRaceMode: raceActive,
    ghostData,
    timeTargets,
    checkpoints,
    checkpointStatus,
    goToNextStep,
    goToPreviousStep,
    goToStep,
    validateCheck,
    requestHint,
    pauseTimer,
    resumeTimer,
    completeModule,
    progress,
    isCurrentStepComplete,
    canProceed,
    getGhostComparison,
    getTimeTargetStatus
  } = useModulePlayer(studentId, moduleId, moduleData, isRaceMode);

  const [userAnswers, setUserAnswers] = useState({});
  const [showCelebration, setShowCelebration] = useState(false);
  const [completionData, setCompletionData] = useState(null);
  const [isPaused, setIsPaused] = useState(false);

  const currentStepData = moduleData.steps[currentStep];

  // Handle check submission
  const handleCheckSubmit = (checkId, answer) => {
    setUserAnswers(prev => ({ ...prev, [checkId]: answer }));
    const result = validateCheck(checkId, answer);
    return result;
  };

  // Handle hint request
  const handleHintRequest = (checkId) => {
    return requestHint(checkId);
  };

  // Handle module completion
  const handleComplete = async () => {
    // Calculate mastery score based on errors and time
    const totalSteps = moduleData.steps.length;
    const baseScore = 100;
    const errorPenalty = errorsCount * 2;
    const timePenalty = Math.max(0, (elapsedTime - moduleData.estimatedTime) / 60);
    const masteryScore = Math.max(0, Math.min(100, baseScore - errorPenalty - timePenalty));

    try {
      const result = await completeModule(masteryScore);
      setCompletionData(result);
      setShowCelebration(true);
    } catch (err) {
      console.error('Failed to complete module:', err);
    }
  };

  // Handle pause/resume
  const handlePauseToggle = () => {
    if (isPaused) {
      resumeTimer();
    } else {
      pauseTimer();
    }
    setIsPaused(!isPaused);
  };

  // Navigate to dashboard
  const handleExit = () => {
    navigate('/dashboard');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading module...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500 text-center">
          <h2 className="text-2xl font-bold mb-2">Error Loading Module</h2>
          <p>{error}</p>
          <button 
            onClick={handleExit}
            className="mt-4 px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header with Timer and Controls */}
      <header className="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={handleExit}
                className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                ← Back
              </button>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  {moduleData.title}
                </h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Step {progress.current} of {progress.total}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Timer Display */}
              {raceActive ? (
                <RaceTimer
                  elapsedTime={elapsedTime}
                  timeTargets={timeTargets}
                  ghostComparison={getGhostComparison}
                  targetStatus={getTimeTargetStatus}
                />
              ) : (
                <div className="text-gray-600 dark:text-gray-400">
                  ⏱️ {lmsAPI.formatTime(elapsedTime)}
                </div>
              )}

              {/* Error Count */}
              <div className="text-gray-600 dark:text-gray-400">
                ❌ {errorsCount} errors
              </div>

              {/* Pause Button */}
              <button
                onClick={handlePauseToggle}
                className="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
              >
                {isPaused ? '▶️ Resume' : '⏸️ Pause'}
              </button>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-4">
            <ProgressStepper
              steps={moduleData.steps}
              currentStep={currentStep}
              completedSteps={completedSteps}
              onStepClick={goToStep}
            />
          </div>
        </div>
      </header>

      {/* Race Mode Checkpoints */}
      {raceActive && checkpoints.length > 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border-b border-yellow-200 dark:border-yellow-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                Race Checkpoints:
              </span>
              {checkpoints.map((checkpoint, index) => (
                <div
                  key={index}
                  className={`px-3 py-1 rounded text-sm ${
                    checkpointStatus[index]
                      ? 'bg-green-500 text-white'
                      : elapsedTime >= checkpoint.target_time
                      ? 'bg-red-500 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                  }`}
                >
                  Step {checkpoint.step}: {checkpoint.target_time}s
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isPaused ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-8 text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Module Paused
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Take a break. Click Resume when you're ready to continue.
            </p>
            <button
              onClick={handlePauseToggle}
              className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600"
            >
              Resume Module
            </button>
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card p-8 animate-fade-in">
            {/* Step Title */}
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {currentStepData.title}
            </h2>

            {/* Step Content */}
            <div className="prose dark:prose-invert max-w-none mb-6">
              <div dangerouslySetInnerHTML={{ __html: currentStepData.content }} />
            </div>

            {/* Checks */}
            {currentStepData.checks && currentStepData.checks.length > 0 && (
              <div className="space-y-4 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Checks
                </h3>
                {currentStepData.checks.map((check, index) => (
                  <CheckValidation
                    key={check.id}
                    check={check}
                    index={index}
                    result={checkResults[check.id]}
                    hint={hints[check.id]}
                    onSubmit={handleCheckSubmit}
                    onHintRequest={handleHintRequest}
                  />
                ))}
              </div>
            )}

            {/* Quiz/Reflection */}
            {currentStepData.quiz && (
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-200 mb-4">
                  {currentStepData.quiz.title}
                </h3>
                <p className="text-blue-800 dark:text-blue-300">
                  {currentStepData.quiz.question}
                </p>
                {/* Quiz form would go here */}
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={goToPreviousStep}
                disabled={currentStep === 0}
                className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Previous
              </button>

              {currentStep === moduleData.steps.length - 1 ? (
                <button
                  onClick={handleComplete}
                  disabled={!canProceed}
                  className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Complete Module ✓
                </button>
              ) : (
                <button
                  onClick={goToNextStep}
                  disabled={!canProceed}
                  className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next Step →
                </button>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Celebration Modal */}
      {showCelebration && completionData && (
        <CelebrationModal
          data={completionData}
          isRaceMode={raceActive}
          onClose={() => {
            setShowCelebration(false);
            handleExit();
          }}
        />
      )}
    </div>
  );
};

export default ModulePlayer;
