const ingredientList = [
  { ingredient: 'Oil', isMeat: false, id: 1 },
  { ingredient: 'Garlic', isMeat: false, id: 2 },
  { ingredient: 'Beef', isMeat: true, id: 3 },
];

export default function IngredientList() {
  const listIngredients = ingredientList.map(ing =>
    <li
      key={ing.id}
      style={{
        color: ing.isMeat ? 'darkred' : 'darkgreen'
      }}
    >
      {ing.ingredient}
    </li>
  );

  return (
    <ul>{listIngredients}</ul>
  );
}
