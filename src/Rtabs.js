import { Tabs, Tab, Panel } from '@bumaga/tabs';
import ratatouille from './ratatouille.png';
import {props.recipes} from './App.js'
// import './App.css';

function Rtabs(props) {

    return (
        <div className="tabs-container">
        <Tabs>
          <div className="tab-buttons">
            {props.recipes.map((recipe, index) => (
              <Tab key={index}>
                <button>{recipe.name}</button>
              </Tab>
            ))}
          </div>
          {props.recipes.map((recipe, index) => (
            <Panel key={index}>
              <p>{recipe.content.title}</p>
              <img src = {recipe.content.image=='https://images.media-allrecipes.com/images/79590.png' ? ratatouille : recipe.content.image}
                   alt="display image"
                   width={300}/>

              {/*<ul>*/}
              {/*  {recipe.content.ingredients.substring().split("\n").map((value, index ) => (*/}
              {/*    <li key={index}>*/}
              {/*      {value}*/}
              {/*      <br />*/}
              {/*    </li>*/}
              {/*  ))}*/}
              {/*</ul>*/}

              <div style={{ whiteSpace: "pre-wrap"}}>
                {'\n🥄' + recipe.content.ingredients + '🥄' }
              </div>

              <p>{recipe.content.directions}</p>

              <p>{recipe.content.description}</p>
            </Panel>
          ))}
        </Tabs>
      </div>
    );
}

export default Rtabs;
