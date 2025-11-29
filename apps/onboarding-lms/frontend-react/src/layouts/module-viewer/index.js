// Module Viewer - Shows individual module with section navigation

import { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import LinearProgress from "@mui/material/LinearProgress";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";
import VuiProgress from "components/VuiProgress";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

// React icons
import { IoArrowBack, IoArrowForward, IoCheckmarkCircle, IoTimeOutline } from "react-icons/io5";

function ModuleViewer() {
  const { moduleId } = useParams();
  const history = useHistory();
  const [module, setModule] = useState(null);
  const [sections, setSections] = useState([]);
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    // Fetch module and sections from Flask backend
    fetch(`http://localhost:5001/api/modules/${moduleId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Module not found');
        }
        return response.json();
      })
      .then(data => {
        setModule(data.module);
        setSections(data.sections);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading module:', err);
        setError(err.message);
        setLoading(false);
      });
  }, [moduleId]);

  useEffect(() => {
    // Track section view
    if (module && sections.length > 0) {
      trackProgress('section_view', currentSectionIndex);
    }
  }, [currentSectionIndex, module, sections]);

  const trackProgress = async (eventType, sectionNumber = null) => {
    try {
      await fetch(`http://localhost:5001/api/modules/${moduleId}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: eventType,
          section_number: sectionNumber,
          timestamp: new Date().toISOString(),
          time_elapsed: Math.floor((Date.now() - startTime) / 1000)
        })
      });
    } catch (err) {
      console.error('Error tracking progress:', err);
    }
  };

  const handleNext = () => {
    if (currentSectionIndex < sections.length - 1) {
      setCurrentSectionIndex(currentSectionIndex + 1);
      window.scrollTo(0, 0);
    } else {
      // Module completed
      trackProgress('complete');
      alert('Module completed! Great job!');
      history.push('/modules');
    }
  };

  const handlePrevious = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(currentSectionIndex - 1);
      window.scrollTo(0, 0);
    }
  };

  const handleBackToModules = () => {
    trackProgress('pause', currentSectionIndex);
    history.push('/modules');
  };

  const formatContent = (content) => {
    // Convert plain text with line breaks to formatted HTML
    return content
      .split('\n\n')
      .map((paragraph, i) => (
        <VuiTypography key={i} variant="body1" color="text" mb={2} sx={{ whiteSpace: 'pre-line' }}>
          {paragraph}
        </VuiTypography>
      ));
  };

  const progress = sections.length > 0 ? ((currentSectionIndex + 1) / sections.length) * 100 : 0;
  const currentSection = sections[currentSectionIndex];

  if (loading) {
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox py={3}>
          <VuiBox textAlign="center" py={6}>
            <VuiTypography variant="h6" color="text">
              Loading module...
            </VuiTypography>
          </VuiBox>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    );
  }

  if (error || !module) {
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox py={3}>
          <Card sx={{ p: 3 }}>
            <VuiBox textAlign="center">
              <VuiTypography variant="h6" color="error" mb={2}>
                Error loading module
              </VuiTypography>
              <VuiTypography variant="body2" color="text" mb={3}>
                {error || 'Module not found'}
              </VuiTypography>
              <VuiButton variant="contained" color="info" onClick={handleBackToModules}>
                Back to Modules
              </VuiButton>
            </VuiBox>
          </Card>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        {/* Module Header */}
        <VuiBox mb={3}>
          <VuiButton
            variant="text"
            color="white"
            startIcon={<IoArrowBack />}
            onClick={handleBackToModules}
            sx={{ mb: 2 }}
          >
            Back to Modules
          </VuiButton>

          <VuiTypography variant="h3" color="white" fontWeight="bold" mb={1}>
            {module.title}
          </VuiTypography>

          <VuiBox display="flex" alignItems="center" flexWrap="wrap" gap={2} mb={2}>
            <VuiTypography variant="body2" color="text">
              {module.category || 'General'}
            </VuiTypography>
            <VuiTypography variant="body2" color="text">
              •
            </VuiTypography>
            <VuiBox display="flex" alignItems="center">
              <IoTimeOutline size="16px" color="#fff" style={{ marginRight: '6px' }} />
              <VuiTypography variant="body2" color="text">
                {module.estimated_minutes} minutes
              </VuiTypography>
            </VuiBox>
            <VuiTypography variant="body2" color="text">
              •
            </VuiTypography>
            <VuiTypography variant="body2" color="text">
              Section {currentSectionIndex + 1} of {sections.length}
            </VuiTypography>
          </VuiBox>

          {/* Progress Bar */}
          <VuiBox mb={2}>
            <VuiBox mb={1}>
              <VuiTypography variant="caption" color="text">
                Progress: {Math.round(progress)}%
              </VuiTypography>
            </VuiBox>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 6,
                borderRadius: 3,
                background: 'rgba(255, 255, 255, 0.1)',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(127.09deg, rgb(6, 227, 245) 19.41%, rgb(4, 164, 177) 76.65%)',
                  borderRadius: 3,
                }
              }}
            />
          </VuiBox>
        </VuiBox>

        {/* Content Card */}
        <Card>
          <VuiBox p={4}>
            {currentSection && (
              <>
                {currentSection.title && (
                  <VuiTypography variant="h4" color="white" fontWeight="bold" mb={3}>
                    {currentSection.title}
                  </VuiTypography>
                )}

                <VuiBox mb={4}>
                  {formatContent(currentSection.content)}
                </VuiBox>
              </>
            )}

            {/* Navigation Buttons */}
            <VuiBox display="flex" justifyContent="space-between" alignItems="center" mt={4} pt={3} borderTop="1px solid rgba(255, 255, 255, 0.1)">
              <VuiButton
                variant="outlined"
                color="white"
                startIcon={<IoArrowBack />}
                onClick={handlePrevious}
                disabled={currentSectionIndex === 0}
              >
                Previous
              </VuiButton>

              <VuiButton
                variant="contained"
                color={currentSectionIndex === sections.length - 1 ? "success" : "info"}
                endIcon={currentSectionIndex === sections.length - 1 ? <IoCheckmarkCircle /> : <IoArrowForward />}
                onClick={handleNext}
              >
                {currentSectionIndex === sections.length - 1 ? 'Complete' : 'Next'}
              </VuiButton>
            </VuiBox>
          </VuiBox>
        </Card>
      </VuiBox>
      <Footer />
    </DashboardLayout>
  );
}

export default ModuleViewer;
