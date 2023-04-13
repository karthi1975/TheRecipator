import { useState } from "react";
import { Button, Form } from "react-bootstrap";
import axios from "axios";
import "./App.css";

export default function Ingsubs() {
  const [subsIng, setSubsIng] = useState("");
  const [subsResults, setSubsResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await axios.post("http://34.28.150.158:5001/substitute", {
      substitutes: subsIng,
    });

    setSubsResults(response.data.substitutes);
    setHasSearched(true);
  };

  const handleClear = () => {
    setSubsIng("");
    setSubsResults([]);
    setHasSearched(false);
  };

  return (
    <div>
      <div>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="subsIngredients">
            <Form.Label></Form.Label>
            <Form.Control
              type="text"
              placeholder="flour"
              value={subsIng}
              onChange={(e) => setSubsIng(e.target.value)}
            />
            <Button variant="primary" type="submit" className="w-100 mt-2">
              Find substitutes
            </Button>
          </Form.Group>
        </Form>
        <Button variant="secondary" onClick={handleClear} className="w-100 mt-2">
          Clear
        </Button>
      </div>
      <div>
        {subsResults.length > 0 ? (
          <div>
            <ul>
              {subsResults.map((substitute, index) => {
                const hasSubstitutions = substitute.Substitution1 || substitute.Substitution2 || substitute.Substitution3 || substitute.Substitution4 || substitute.Substitution5 || substitute.Substitution6;
                if (!hasSubstitutions) {
                  return (
                    <li key={index} style={{ listStyle: "none" }}>
                      {substitute.Ingredient}: Sorry, no substitutions found for this item
                    </li>
                  );
                } else {
                  return (
                    <li key={index} style={{ listStyle: "none" }}>
                      {substitute.Ingredient}: {substitute.Substitution1}, {substitute.Substitution2}, {substitute.Substitution3}, {substitute.Substitution4}, {substitute.Substitution5}, {substitute.Substitution6}
                    </li>
                  );
                }
              })}
            </ul>
          </div>
        ) : hasSearched ? (
          <div>No Substitues found to display</div>
        ) : null}
      </div>
    </div>
  );
}
