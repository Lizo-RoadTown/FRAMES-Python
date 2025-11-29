import React from 'react';
import ModulePage from '../components/ModulePage';

const ExampleModule = () => {
  const handleProgress = (progressData) => {
    console.log('Progress update:', progressData);
    // TODO: send to backend endpoint when ready
  };

  return <ModulePage moduleId="example-module-1" onProgress={handleProgress} />;
};

export default ExampleModule;
