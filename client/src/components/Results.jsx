// import React from "react";
import PropTypes from "prop-types";

const Results = ({ results }) => {
  return (
    <div className="results">
      {results.length === 0 && <p className="no-results">No results found</p>}
      {results.map((item, index) => (
        <div key={index} className="result">
          <h3>{item.name}</h3>
          <p>
            <strong>Type:</strong> {item.type}
          </p>
          <p>
            <strong>Address:</strong> {item.address}
          </p>
          <p>
            <strong>Coordinates:</strong> ({item.latitude}, {item.longitude})
          </p>
          <div className="photos">
            {item.photos.map((photo, idx) => (
              <img key={idx} src={photo} alt={`${item.name} photo`} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

Results.propTypes = {
  results: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      address: PropTypes.string.isRequired,
      latitude: PropTypes.number.isRequired,
      longitude: PropTypes.number.isRequired,
      photos: PropTypes.arrayOf(PropTypes.string).isRequired,
    })
  ).isRequired,
};

export default Results;
