import React from 'react';
import PropTypes from 'prop-types';
import { NotionRenderer } from 'react-notion-x';

import 'react-notion-x/src/styles.css';
import 'prismjs/themes/prism-tomorrow.css';
import 'katex/dist/katex.min.css';
import '../styles/notion-overrides.css';

/**
 * NotionPage - Wrapper component for rendering Notion content.
 *
 * @param {object} recordMap - Notion API recordMap object (required)
 * @param {boolean} darkMode - Enables dark theme styling (default true)
 */
const NotionPage = ({ recordMap, darkMode = true }) => {
  if (!recordMap) {
    return <div className="notion-error">No content to display</div>;
  }

  return (
    <div className={
otion-container }>
      <NotionRenderer
        recordMap={recordMap}
        fullPage={false}
        darkMode={darkMode}
        disableHeader={false}
        className="space-tech-notion"
      />
    </div>
  );
};

NotionPage.propTypes = {
  recordMap: PropTypes.object,
  darkMode: PropTypes.bool,
};

export default NotionPage;
