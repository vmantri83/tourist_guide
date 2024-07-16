import { useState } from "react";
import "./App.css";
import SearchForm from "./components/SearchForm";
import Results from "./components/Results";

const App = () => {
  const [results, setResults] = useState([]);

  const fetchRecommendations = async (location, tags) => {
    const response = await fetch("/recommendations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ location, tags }),
    });

    if (response.ok) {
      const data = await response.json();
      setResults(data);
    } else {
      console.error("Error fetching recommendations");
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Tourist Guide</h1>
        <SearchForm onSearch={fetchRecommendations} />
        <Results results={results} />
      </div>
    </div>
  );
};

export default App;
