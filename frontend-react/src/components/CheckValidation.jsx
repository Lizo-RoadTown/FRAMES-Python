// CheckValidation Component
// Input and validation feedback for module checks

import React, { useState } from 'react';

const CheckValidation = ({ check, index, result, hint, onSubmit, onHintRequest }) => {
  const [answer, setAnswer] = useState('');
  const [showHint, setShowHint] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(check.id, answer);
  };

  const handleHintClick = () => {
    onHintRequest(check.id);
    setShowHint(true);
  };

  return (
    <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <h4 className="font-medium text-gray-900 dark:text-white">
          Check {index + 1}: {check.label || check.id}
        </h4>
        
        {check.hint && !showHint && (
          <button
            onClick={handleHintClick}
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            💡 Hint
          </button>
        )}
      </div>

      {showHint && hint && (
        <div className="mb-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded text-sm text-blue-800 dark:text-blue-200">
          💡 {hint}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Enter your answer..."
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
          disabled={result?.correct}
        />

        {!result?.correct && (
          <button
            type="submit"
            className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50"
            disabled={!answer.trim()}
          >
            Check Answer
          </button>
        )}
      </form>

      {result && (
        <div className={`mt-3 p-3 rounded-lg ${
          result.correct
            ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-800 dark:text-green-200'
            : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200'
        }`}>
          <div className="flex items-start gap-2">
            <span className="text-lg">{result.correct ? '✓' : '✗'}</span>
            <div className="flex-1">
              <p className="font-medium">{result.message}</p>
              {result.hint && (
                <p className="text-sm mt-1 opacity-80">{result.hint}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CheckValidation;
