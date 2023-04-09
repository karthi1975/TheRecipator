import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import { Tabs, Tab, Panel } from '@bumaga/tabs';
import './App.css';

function App() {
  // const [ prepTime, setPrepTime] = useState('');
  const [ingredients, setIngredients] = useState('');
  const [addedIngredients, setAddedIngredients] = useState([]);
  const [removedIngredients, setRemovedIngredients] = useState([]);
  const [excludeList, setExcludeList] = useState('')
  const [recipes, setRecipes] = useState([]);
  const [ subsIngredient, setSubsIngredient] = useState('');

  const handlePreptime = () => {

  }

  const handleSubmit = async (e) => {
    e.preventDefault();


    // Make an HTTP request to the Flask API with the ingredients
    const response = await axios.post('http://localhost:5001/recommend', { include: ingredients, exclude: removedIngredients.join(',') });

    // Update the state with the recommended recipes
    const recommendedRecipes = response.data.recipes.map((recipe, index) => ({
      name: `Recipe ${index + 1}`,
      content: recipe,
    }));
    setRecipes(recommendedRecipes);
  };


  const handleAdd = () => {
    // Add a new ingredient to the list of ingredients
    const newIngredient = prompt('Enter a new ingredient:');
    setIngredients(ingredients + ' ' + newIngredient);
    setAddedIngredients([...addedIngredients, newIngredient]);
  };
  const handleRemove = () => {
    // Remove an ingredient from the list of ingredients
    const ingredientToRemove = prompt('Enter an ingredient to remove:');
    setIngredients(ingredients.replace(ingredientToRemove, ''));
    setRemovedIngredients([...removedIngredients, ingredientToRemove]);
  };


  const handleSubstitute = async (e) => {
    e.preventDefault();

    // Make an HTTP request to the Flask API with the substitute ingredients
    const response = await axios.post('http://localhost:5001/recommend', { subsIngredient });

    // const response = await axios.post('http://localhost:5000/recommend', { include: 'beef broccoli', exclude: 'cheese'});

    // Update the state with substitute ingredient
    const recommendedSubstitutes = response.data.map((o, s) => ({
      original: o,
      substitute: s,
    }));
    setSubsIngredient(recommendedSubstitutes);
  };

  return (
    <div className="container">
      {/*<Form.Label>*/}
      {/*  <h1> The Recipator</h1>*/}
      {/*</Form.Label>*/}
      <div className="form-container">
        {/*<Form onSubmit={handlePreptime}>*/}
        {/*  <Form.Label>Preparation Time</Form.Label>*/}
        {/*</Form>*/}

        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formIngredients">
            <Form.Label>Ingredients</Form.Label>
            <Form.Control type="text" placeholder="Enter ingredients" value={ingredients} onChange={(e) => setIngredients(e.target.value)} />
          </Form.Group>
          <Button variant="primary" type="submit" className="w-100">
            Submit
          </Button>
        </Form>
        <div>

        <div>
          <Button variant="secondary" onClick={handleAdd} className="add-button">Include</Button>{' '}
          <Button variant="secondary" onClick={handleRemove} className="remove-button">Exclude</Button>
        </div>

        <div>
          {addedIngredients.length > 0 && (
            <div>
              <h5>Added Ingredients:</h5>
              <ul>
                {addedIngredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>
          )}
          {removedIngredients.length > 0 && (
            <div>
              <h5>Removed Ingredients:</h5>
              <ul>
                {removedIngredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className={recipes.length > 0 ? "recipes-container" : "hidden"}>
          {recipes.map((recipe, index) => (
            <div key={index} className="recipe-content">
              {recipe.title}
            </div>
          ))}
        </div>

        {/*<Form onSubmit={handleSubstitute}>*/}
        {/*  <Form.Label>Ingredient Substitution</Form.Label>*/}
        {/*  <Form.Group controlId="subsIngredients">*/}
        {/*    <Form.Control type="text" placeholder="Squirrel" value={subsIngredient} onChange={(e) => setSubsIngredient(e.target.value)} />*/}
        {/*  </Form.Group>*/}
        {/*    <Button variant="primary" type="submit" className="w-100">*/}
        {/*      Substitute*/}
        {/*    </Button>*/}
        {/*</Form>*/}

      </div>
      {/*<div className="container-separator"></div>*/}
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
              <p>{recipe.title}</p>
              <p>{recipe.ingredients}</p>
              <p>{recipe.directions}</p>
              <p>{recipe.description}</p>
            </Panel>
          ))}
        </Tabs>
      </div>
    </div>
  );
}

export default App;
