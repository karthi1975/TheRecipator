import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './App.css';
import { Tabs, Tab, Panel } from '@bumaga/tabs';
import ratatouille from './ratatouille2.png';
import Ingsubs from './Ingsubs';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [addedIngredients, setAddedIngredients] = useState([]);
  const [removedIngredients, setRemovedIngredients] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const response = await axios.post(
      'http://34.28.150.158:5001/recommend',
      { include: addedIngredients.join(' '), exclude: removedIngredients.join(' ') }
    );

    const recommendedRecipes = response.data.recipes.map((recipe, index) => ({
      name: `Recipe ${index + 1}`,
      content: recipe,
    }));
    console.log('Recommended recipes:', recommendedRecipes);
    setRecipes(recommendedRecipes);
    console.log('Recipes state:', recipes);

    setLoading(false);
  };

  const handleClear = () => {
    setAddedIngredients([]);
    setRemovedIngredients([]);
    setRecipes([]);
  };

  const handleAdd = () => {
    const newIngredients = ingredients.split(' ').filter((ingredient) => {
      return ingredient.trim() !== '' && !addedIngredients.includes(ingredient);
    });
    setAddedIngredients([...addedIngredients, ...newIngredients]);
    setRemovedIngredients(removedIngredients.filter((ingredient) => !newIngredients.includes(ingredient)));
    setIngredients('');
  };

  const handleRemove = () => {
    const newRemovedIngredients = ingredients.split(' ').filter((ingredient) => {
      return ingredient.trim() !== '' && !removedIngredients.includes(ingredient);
    });
    setRemovedIngredients([...removedIngredients, ...newRemovedIngredients]);
    setAddedIngredients(addedIngredients.filter((ingredient) => !newRemovedIngredients.includes(ingredient)));
    setIngredients('');
  };

  return (
    <div className="container">
      <div className="form-container">
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formIngredients">
            <h4 style={{ color: "darkolivegreen" }}>
              Include / Exclude ingredients, then hit Submit, and let it simmer
              for a few seconds!
            </h4>
            <Form.Label></Form.Label>
            <Form.Control
              type="text"
              placeholder="oil garlic fish"
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
            />
            <Button variant="primary" type="submit" className="w-100" disabled={loading}>
              {loading ? 'Loading...' : 'Submit'}
            </Button>
            <Button variant="danger" onClick={handleClear} className="clear-button">
              Clear
            </Button>
          </Form.Group>
        </Form>
        <div>
          <Button variant="secondary" onClick={handleAdd} className="add-button">
            Include
          </Button>{' '}
          <Button variant="secondary" onClick={handleRemove} className="remove-button">
            Exclude
          </Button>
        </div>
        <div>
          {addedIngredients.length > 0 && (
            <div>
              <h5>Added Ingredients:</h5>
              {addedIngredients.map((ingredient, index) => (
                <li key={index} style={{ listStyle: "none" }}>
                  {'✔️ ' + ingredient}
                </li>
              ))}
            </div>
          )}
          {removedIngredients.length > 0 && (
            <div>
              <h5>Removed Ingredients:</h5>
              {removedIngredients.map((ingredient, index) => (
                <li key={index} style={{ listStyle: "none" }}>
                  {'✖️ ' + ingredient}
                </li>
              ))}
            </div>
          )}
        </div>

        <div className={recipes.length > 0 ? "recipes-container" : "hidden"}>
          {recipes.map((recipe, index) => (
            <div key={index} className="recipe-content">
              {recipe.content.title}
            </div>
          ))}
        </div>

        <h4 style={{ color: "darkolivegreen" }}>Ingredient Substitutions</h4>
        <Ingsubs />

        <a href="https://forms.gle/jefmYqPREqdFXYKk9">
          <p style={{ fontSize: 15 }}>
            Romain calm and chive on by answering our survey. <br /> Thanks a
            brunch!
          </p>
        </a>
      </div>

      <div className="tabs-container">
        <Tabs>
          <div className="tab-buttons">
            {recipes.map((recipe, index) => (
              <Tab key={index}>
                <button>{recipe.name}</button>
              </Tab>
            ))}
          </div>
          {recipes.map((recipe, index) => (
            <Panel key={index}>
              <h3>{recipe.content.title}</h3>
              <p>{recipe.content.description}</p>
              <img
                src={
                  recipe.content.image ===
                  "https://images.media-allrecipes.com/images/79590.png"
                    ? ratatouille
                    : recipe.content.image
                }
                alt="display image"
                width={300}
              />
              <p>
                <b>Prep time:</b> {recipe.content.preptime} <b>Ready time:</b>{" "}
                {recipe.content.readytime}
              </p>
              <h4>Ingredients</h4>
              <ul>
                {recipe.content.ingredients
                  .substring(1, recipe.content.ingredients.length - 1)
                  .split("\n")
                  .map((value, index) => (
                    <li key={index}>
                      {value}
                      <br />
                    </li>
                  ))}
              </ul>

              <h4>Directions</h4>
              <p>{recipe.content.directions}</p>
            </Panel>
          ))}
        </Tabs>
      </div>
      {loading && (
        <div className="loading-image-container">
          <img
            src="https://media.tenor.com/images/cKR69WkItb8bS2XRT0VJYKkCOm0D8VeN/tenor.gif"
            alt="Loading"
          />
        </div>
      )}

    </div>
  );
}

export default App;
