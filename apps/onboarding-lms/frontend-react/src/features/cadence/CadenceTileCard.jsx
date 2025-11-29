import PropTypes from "prop-types";
import Card from "@mui/material/Card";
import VuiBox from "components/VuiBox";
import VuiTypography from "components/VuiTypography";
import VuiButton from "components/VuiButton";

function CadenceTileCard({ icon: IconComponent, title, description, href }) {
  return (
    <Card sx={{ height: "100%", padding: "20px" }}>
      <VuiBox display="flex" flexDirection="column" height="100%">
        <VuiBox display="flex" alignItems="center" mb={1.5}>
          <VuiBox
            bgColor="info"
            color="#fff"
            width="38px"
            height="38px"
            borderRadius="lg"
            display="flex"
            justifyContent="center"
            alignItems="center"
            mr={1.5}
            shadow="md"
          >
            <IconComponent size="18px" color="#fff" />
          </VuiBox>
          <VuiTypography variant="button" fontWeight="bold" color="white">
            {title}
          </VuiTypography>
        </VuiBox>

        <VuiTypography variant="caption" color="text" mb="auto">
          {description}
        </VuiTypography>

        {href ? (
          <VuiButton
            component="a"
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            color="info"
            variant="outlined"
            sx={{ mt: 2, alignSelf: "flex-start" }}
          >
            Open
          </VuiButton>
        ) : (
          <VuiTypography variant="caption" color="text" mt={2}>
            Link coming soon
          </VuiTypography>
        )}
      </VuiBox>
    </Card>
  );
}

CadenceTileCard.defaultProps = {
  href: "",
};

CadenceTileCard.propTypes = {
  icon: PropTypes.elementType.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  href: PropTypes.string,
};

export default CadenceTileCard;
