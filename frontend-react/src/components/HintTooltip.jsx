// HintTooltip Component
// Displays contextual hints with tooltip styling

import React, { useState } from 'react';

const HintTooltip = ({ hint, children }) => {
  const [isVisible, setIsVisible] = useState(false);

  if (!hint) return children;

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onClick={() => setIsVisible(!isVisible)}
      >
        {children}
      </div>

      {isVisible && (
        <div className="absolute z-50 w-64 p-3 mt-2 text-sm bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 rounded-lg shadow-lg animate-fade-in">
          <div className="flex items-start gap-2">
            <span className="text-lg">💡</span>
            <p>{hint}</p>
          </div>
          
          {/* Arrow */}
          <div className="absolute -top-2 left-4 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-gray-900 dark:border-b-gray-100"></div>
        </div>
      )}
    </div>
  );
};

export default HintTooltip;
