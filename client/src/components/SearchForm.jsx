import  { useState } from "react";
import PropTypes from "prop-types";

const SearchForm = ({ onSearch }) => {
  const [location, setLocation] = useState("");
  const [tags, setTags] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(
      location,
      tags.split(",").map((tag) => tag.trim())
    );
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Enter location"
        required
      />
      <input
        type="text"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        placeholder="Enter tags (comma separated)"
        required
      />
      <button type="submit">Get Recommendations</button>
    </form>
  );
};

SearchForm.propTypes = {
  onSearch: PropTypes.func.isRequired,
};

export default SearchForm;
