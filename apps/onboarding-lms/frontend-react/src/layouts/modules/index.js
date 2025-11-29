// Module Library - Shows all available training modules

import { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import Icon from "@mui/material/Icon";

// Vision UI Dashboard React components
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";

// Vision UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";

// React icons
import { IoBookSharp, IoTimeOutline, IoCheckmarkCircle } from "react-icons/io5";

function Modules() {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const history = useHistory();

  useEffect(() => {
    // Fetch modules from Flask backend
    fetch('http://localhost:5001/api/modules')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load modules');
        }
        return response.json();
      })
      .then(data => {
        setModules(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading modules:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleModuleClick = (moduleId) => {
    history.push(`/modules/${moduleId}`);
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox py={3}>
        <VuiBox mb={3}>
          <VuiTypography variant="h3" color="white" fontWeight="bold" mb={1}>
            Training Modules
          </VuiTypography>
          <VuiTypography variant="body2" color="text">
            Complete these modules to prepare for working in the FRAMES laboratory
          </VuiTypography>
        </VuiBox>

        {loading && (
          <VuiBox textAlign="center" py={6}>
            <VuiTypography variant="h6" color="text">
              Loading modules...
            </VuiTypography>
          </VuiBox>
        )}

        {error && (
          <Card sx={{ p: 3 }}>
            <VuiBox textAlign="center">
              <VuiTypography variant="h6" color="error" mb={1}>
                Error loading modules
              </VuiTypography>
              <VuiTypography variant="body2" color="text">
                {error}
              </VuiTypography>
            </VuiBox>
          </Card>
        )}

        {!loading && !error && modules.length === 0 && (
          <Card sx={{ p: 3 }}>
            <VuiBox textAlign="center">
              <VuiTypography variant="h6" color="text" mb={1}>
                No modules available yet
              </VuiTypography>
              <VuiTypography variant="body2" color="text">
                Check back soon for training modules!
              </VuiTypography>
            </VuiBox>
          </Card>
        )}

        {!loading && !error && modules.length > 0 && (
          <Grid container spacing={3}>
            {modules.map((module) => (
              <Grid item xs={12} md={6} lg={4} key={module.module_id}>
                <Card
                  sx={{
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    }
                  }}
                  onClick={() => handleModuleClick(module.module_id)}
                >
                  <VuiBox p={3}>
                    <VuiBox display="flex" alignItems="center" mb={2}>
                      <VuiBox
                        display="flex"
                        justifyContent="center"
                        alignItems="center"
                        width="3rem"
                        height="3rem"
                        borderRadius="lg"
                        sx={{ background: 'linear-gradient(127.09deg, rgba(6, 11, 40, 0.94) 19.41%, rgba(10, 14, 35, 0.49) 76.65%)' }}
                        mr={2}
                      >
                        <IoBookSharp size="20px" color="white" />
                      </VuiBox>
                      <VuiTypography variant="caption" color="text" textTransform="uppercase">
                        {module.category || 'General'}
                      </VuiTypography>
                    </VuiBox>

                    <VuiTypography variant="h5" color="white" fontWeight="bold" mb={1}>
                      {module.title}
                    </VuiTypography>

                    <VuiTypography variant="body2" color="text" mb={2}>
                      {module.description || 'No description available'}
                    </VuiTypography>

                    <VuiBox display="flex" alignItems="center" flexWrap="wrap" gap={2}>
                      <VuiBox display="flex" alignItems="center">
                        <IoTimeOutline size="16px" color="#fff" style={{ marginRight: '6px' }} />
                        <VuiTypography variant="caption" color="text">
                          {module.estimated_minutes} min
                        </VuiTypography>
                      </VuiBox>

                      {module.tags && module.tags.length > 0 && (
                        <VuiBox display="flex" alignItems="center" gap={1}>
                          {module.tags.slice(0, 2).map((tag, index) => (
                            <VuiBox
                              key={index}
                              px={1.5}
                              py={0.5}
                              borderRadius="md"
                              sx={{
                                background: tag === 'required'
                                  ? 'linear-gradient(127.09deg, rgba(255, 67, 54, 0.94) 19.41%, rgba(252, 82, 3, 0.49) 76.65%)'
                                  : 'linear-gradient(127.09deg, rgba(6, 11, 40, 0.94) 19.41%, rgba(10, 14, 35, 0.49) 76.65%)'
                              }}
                            >
                              <VuiTypography variant="caption" color="white" fontWeight="medium">
                                {tag}
                              </VuiTypography>
                            </VuiBox>
                          ))}
                        </VuiBox>
                      )}
                    </VuiBox>

                    <VuiBox mt={3}>
                      <VuiButton
                        variant="contained"
                        color="info"
                        fullWidth
                        onClick={(e) => {
                          e.stopPropagation();
                          handleModuleClick(module.module_id);
                        }}
                      >
                        Start Module
                      </VuiButton>
                    </VuiBox>
                  </VuiBox>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </VuiBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Modules;
