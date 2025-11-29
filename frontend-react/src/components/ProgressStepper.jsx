// ProgressStepper Component
// Visual step indicator for module progress

import React from 'react';

const ProgressStepper = ({ steps, currentStep, completedSteps, onStepClick }) => {
  return (
    <div className="flex items-center justify-between">
      {steps.map((step, index) => {
        const isCompleted = completedSteps.includes(index);
        const isCurrent = currentStep === index;
        const isAccessible = index <= currentStep || isCompleted;

        return (
          <React.Fragment key={index}>
            <button
              onClick={() => isAccessible && onStepClick(index)}
              disabled={!isAccessible}
              className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold transition-all ${
                isCompleted
                  ? 'bg-green-500 text-white'
                  : isCurrent
                  ? 'bg-primary-500 text-white ring-4 ring-primary-200 dark:ring-primary-800'
                  : isAccessible
                  ? 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-400 dark:hover:bg-gray-500'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
              }`}
              title={step.title}
            >
              {isCompleted ? '✓' : index + 1}
            </button>
            
            {index < steps.length - 1 && (
              <div className={`flex-1 h-1 mx-2 ${
                completedSteps.includes(index)
                  ? 'bg-green-500'
                  : 'bg-gray-300 dark:bg-gray-600'
              }`}></div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default ProgressStepper;
