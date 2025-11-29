import Grid from "@mui/material/Grid";
import PropTypes from "prop-types";
import CadenceTileCard from "./CadenceTileCard";

function CadenceTilesGrid({ tiles }) {
  return (
    <Grid container spacing={3}>
      {tiles.map((tile) => (
        <Grid item xs={12} sm={6} lg={4} xl={3} key={tile.key}>
          <CadenceTileCard
            icon={tile.icon}
            title={tile.title}
            description={tile.description}
            href={tile.href}
          />
        </Grid>
      ))}
    </Grid>
  );
}

CadenceTilesGrid.propTypes = {
  tiles: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
      href: PropTypes.string,
      icon: PropTypes.elementType.isRequired,
    })
  ).isRequired,
};

export default CadenceTilesGrid;
