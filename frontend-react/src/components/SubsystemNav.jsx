// SubsystemNav Component
// Navigation menu for subsystems with competency indicators

import React from 'react';
import lmsAPI from '../api/lms';

const SubsystemNav = ({ competencies, selectedSubsystem, onSelect }) => {
  const subsystemIcons = {
    power: '⚡',
    avionics: '📡',
    propulsion: '🚀',
    structures: '🏗️',
    thermal: '🌡️',
    communications: '📶',
    default: '📚'
  };

  return (
    <nav className="space-y-2">
      {competencies.map((comp) => {
        const isSelected = selectedSubsystem === comp.subsystem;
        const icon = subsystemIcons[comp.subsystem] || subsystemIcons.default;
        const colorClass = lmsAPI.getCompetencyColor(comp.competency_level);

        return (
          <button
            key={comp.subsystem}
            onClick={() => onSelect(comp.subsystem)}
            className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
              isSelected
                ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{icon}</span>
                <div>
                  <div className="font-medium capitalize">{comp.subsystem}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {comp.modules_completed} modules
                  </div>
                </div>
              </div>
              
              <div className={`w-2 h-2 rounded-full ${colorClass}`} title={comp.competency_level}></div>
            </div>
          </button>
        );
      })}
    </nav>
  );
};

export default SubsystemNav;
