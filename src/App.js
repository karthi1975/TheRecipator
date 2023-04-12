import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './App.css';
import { Tabs, Tab, Panel } from '@bumaga/tabs';
import ratatouille from './ratatouille2.png';
// import Rtabs from './Rtabs';
// <<<<<<< HEAD
// import Dtime from './Dtime';
// import Ingsubs from './Ingsubs';
// =======
// //import Dtime from './Dtime';
// >>>>>>> 93e68ac36164eda349dc62911f35f0d472437e0f


function App() {
  // const [ prepTime, setPrepTime] = useState('');
  const [ingredients, setIngredients] = useState('');
  const [addedIngredients, setAddedIngredients] = useState([]);
  const [removedIngredients, setRemovedIngredients] = useState([]);
  const [recipes, setRecipes] = useState([]);
  // const [ subsIngredient, setSubsIngredient] = useState('');

const handleSubmit = async (e) => {
    e.preventDefault();

    // Make an HTTP request to the Flask API with the ingredients
    const response = await axios.post(
      'http://34.28.150.158:5001/recommend',
      { include: addedIngredients.join(' '), exclude: removedIngredients.join(' ') }
    );

    // Update the state with the recommended recipes
    const recommendedRecipes = response.data.recipes.map((recipe, index) => ({
      name: `Recipe ${index + 1}`,
      content: recipe,
    }));
    console.log('Recommended recipes:', recommendedRecipes);
    setRecipes(recommendedRecipes);
    console.log('Recipes state:', recipes);

    // Clear the addedIngredients and removedIngredients arrays
    // setAddedIngredients([]);
    // setRemovedIngredients([]);
  };

const handleClear = () => {
    setAddedIngredients([]);
    setRemovedIngredients([]);
    setRecipes([]);
};

const handleAdd = () => {
  // Add new ingredients to the list of ingredients
  const newIngredients = ingredients.split(' ').filter((ingredient) => {
    return ingredient.trim() !== '' && !addedIngredients.includes(ingredient);
  });
  setAddedIngredients([...addedIngredients, ...newIngredients]);
  setRemovedIngredients(removedIngredients.filter((ingredient) => !newIngredients.includes(ingredient)));
  setIngredients('');
};

const handleRemove = () => {
  // Remove ingredients from the list of ingredients
  const newRemovedIngredients = ingredients.split(' ').filter((ingredient) => {
    return ingredient.trim() !== '' && !removedIngredients.includes(ingredient);
  });
  setRemovedIngredients([...removedIngredients, ...newRemovedIngredients]);
  setAddedIngredients(addedIngredients.filter((ingredient) => !newRemovedIngredients.includes(ingredient)));
  setIngredients('');
};

<Form.Control
  type="text"
  placeholder="oil garlic fish"
  value={ingredients}
  onChange={(e) => setIngredients(e.target.value)}
/>


  // const handleSubstitute = async (e) => {
  //   e.preventDefault();
  //
  //   // Make an HTTP request to the Flask API with the substitute ingredients
  //   const response = await axios.post('http://localhost:5001/recommend', { subsIngredient });
  //
  //   // Update the state with substitute ingredient
  //   const recommendedSubstitutes = response.data.map((o, s) => ({
  //     original: o,
  //     substitute: s,
  //   }));
  //   setSubsIngredient(recommendedSubstitutes);
  // };

  return (
    <div className="container">

      <div className="form-container">


        {/*<h4>⏳ Preparation time h:mm</h4><Dtime />*/}


        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formIngredients">
            {/*<h4>Ingredients</h4>*/}
            <h4>Include / Exclude ingredients then Submit</h4>
            <Form.Label></Form.Label>
            <Form.Control type="text" placeholder="oil garlic fish" value={ingredients} onChange={(e) => setIngredients(e.target.value)} />
            <Button variant="primary" type="submit" className="w-100">
              Submit
            </Button>
            <Button variant="danger" onClick={handleClear} className="clear-button">
              Clear
            </Button>
          </Form.Group>
        </Form>
        <div>
          <Button
              variant="secondary"
              onClick={handleAdd}
              className="add-button">
            Include
          </Button>{' '}
          <Button variant="secondary" onClick={handleRemove} className="remove-button">Exclude</Button>
        </div>
        <div>
          {addedIngredients.length > 0 && (
            <div>
              <h5>Added Ingredients:</h5>
              <ul>
                {addedIngredients.map((ingredient, index) => (
                  <li key={index}>
                    {ingredient}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {removedIngredients.length > 0 && (
            <div>
              <h5>Removed Ingredients:</h5>
              <ul>
                {removedIngredients.map((ingredient, index) => (
                  <li key={index}>
                    {ingredient}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className={recipes.length > 0 ? "recipes-container" : "hidden"}>
          {recipes.map((recipe, index) => (
            <div key={index} className="recipe-content">
                  {recipe.content.title}
            </div>
          ))
          }
        </div>

        <h4>Ingredient Substitutions</h4>
        {/*<Ingsubs/>*/}

      </div>

      {/*<span role="presentation" className="resizer-vertical "></span>*/}
      {/*<Rtabs recipes={props.recipes}/>*/}

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
              <img src = {recipe.content.image === 'https://images.media-allrecipes.com/images/79590.png' ? ratatouille : recipe.content.image}
                   alt="display image"
                   width={300}/>
              <p><b>Prep time:</b>   h:mm   <b>Ready time:</b>  h:mm  </p>
              <h4>Ingredients</h4>
              <ul>
                {recipe.content.ingredients.substring(1, recipe.content.ingredients.length -1).split("\n").map((value, index ) => (
                  <li key={index}>
                    {value}
                    <br />
                  </li>
                ))}
              </ul>

              {/*<div style={{ whiteSpace: "pre-wrap"}}>*/}
              {/*  {'\n🥄' + recipe.content.ingredients + '🥄' }*/}
              {/*</div>*/}

              <h4>Directions</h4>
              <p>{recipe.content.directions}</p>

            </Panel>
          ))}
        </Tabs>
      </div>

    </div>
  );
}

export default App;

