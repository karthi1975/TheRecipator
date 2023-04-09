const excludeList = [
  { ingredient: 'Garlic', isMeat: false, id: 4 },
  { ingredient: 'Fish', isMeat: true, id: 5 },
];

export default function ExcludeList() {
  const listExclude = excludeList.map(ing =>
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
      <ul>{listExclude}</ul>
  );
}
