import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import NotionPage from './NotionPage';

/**
 * ModulePage - Displays a learning module with Notion content
 *
 * Props:
 *   moduleId (string, required) - Module identifier
 *   onProgress (function) - Callback when user makes progress
 */
const ModulePage = ({ moduleId, onProgress }) => {
  const [moduleData, setModuleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentSection, setCurrentSection] = useState(0);

  useEffect(() => {
    fetchModuleData(moduleId);
  }, [moduleId]);

  const fetchModuleData = async (id) => {
    try {
      // TODO: Replace with real API call e.g., /api/modules/
      const mockData = {
        id,
        title: 'Sample Module',
        description: 'Learning module content',
        sections: [
          { id: 1, title: 'Introduction', recordMap: null },
          { id: 2, title: 'Core Concepts', recordMap: null },
        ],
        progress: ((currentSection + 1) / 2) * 100,
      };
      setModuleData(mockData);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch module:', error);
      setLoading(false);
    }
  };

  const handleNextSection = () => {
    if (!moduleData || currentSection >= moduleData.sections.length - 1) {
      return;
    }

    const nextSection = currentSection + 1;
    setCurrentSection(nextSection);

    if (onProgress) {
      onProgress({
        moduleId,
        sectionId: moduleData.sections[nextSection].id,
        progress: ((nextSection + 1) / moduleData.sections.length) * 100,
      });
    }
  };

  const handlePrevSection = () => {
    if (currentSection === 0) {
      return;
    }
    setCurrentSection((prev) => prev - 1);
  };

  if (loading) {
    return <div className="loading">Loading module...</div>;
  }

  if (!moduleData) {
    return <div className="error">Module not found</div>;
  }

  const section = moduleData.sections[currentSection];

  return (
    <div className="module-page">
      <header className="module-header">
        <h1>{moduleData.title}</h1>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: ${moduleData.progress || 0}% }} />
        </div>
      </header>

      <nav className="section-nav">
        <span className="section-indicator">
          Section {currentSection + 1} of {moduleData.sections.length}
        </span>
        <h2>{section.title}</h2>
      </nav>

      <main className="module-content">
        {section.recordMap ? (
          <NotionPage recordMap={section.recordMap} darkMode={true} />
        ) : (
          <div className="placeholder">
            Content for "{section.title}" will be loaded from Notion API
          </div>
        )}
      </main>

      <footer className="module-nav-buttons">
        <button onClick={handlePrevSection} disabled={currentSection === 0} className="btn-prev">
          ? Previous
        </button>
        <button
          onClick={handleNextSection}
          disabled={currentSection === moduleData.sections.length - 1}
          className="btn-next"
        >
          Next ?
        </button>
      </footer>
    </div>
  );
};

ModulePage.propTypes = {
  moduleId: PropTypes.string.isRequired,
  onProgress: PropTypes.func,
};

export default ModulePage;
