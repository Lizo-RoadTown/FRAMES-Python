import PropTypes from "prop-types";
import Card from "@mui/material/Card";
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";

function CadenceCalendarCard({ embedUrl, title }) {
  return (
    <Card sx={{ height: "100%" }}>
      <VuiBox p={3} height="100%" display="flex" flexDirection="column">
        <VuiTypography variant="button" fontWeight="bold" color="white" mb={2}>
          {title}
        </VuiTypography>
        {embedUrl ? (
          <VuiBox
            component="iframe"
            src={embedUrl}
            title="Cadence Calendar"
            width="100%"
            height="480px"
            sx={{ flexGrow: 1, border: 0, borderRadius: "16px" }}
          />
        ) : (
          <VuiTypography variant="caption" color="text">
            Embed the shared team calendar here. Paste the publish URL into the `embedUrl` prop or
            swap this card with a live Notion calendar block when you are ready.
          </VuiTypography>
        )}
      </VuiBox>
    </Card>
  );
}

CadenceCalendarCard.defaultProps = {
  embedUrl: "",
  title: "Cadence Calendar",
};

CadenceCalendarCard.propTypes = {
  embedUrl: PropTypes.string,
  title: PropTypes.string,
};

export default CadenceCalendarCard;
