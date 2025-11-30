function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
}

/* ============================
   🔥 Backend Integration Hooks
   ============================ */

let allRecipes = []; // cached list for filtering

async function loadRecipes() {
    const res = await fetch('/api/recipes'); // backend returns {name, ingredients}
    allRecipes = await res.json();
    renderRecipeList(allRecipes);
}

function renderRecipeList(recipes) {
    const list = document.getElementById('recipe-list');
    list.innerHTML = "";

    recipes.forEach(r => {
        let li = document.createElement('li');
        li.textContent = r.name;
        li.onclick = () => loadRecipeDetails(r.name);
        list.appendChild(li);
    });
}

document.getElementById("ingredient-filter").addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().split(",").map(s => s.trim());

    const filtered = allRecipes.filter(recipe =>
        query.every(ing => ing === "" || recipe.ingredients.toLowerCase().includes(ing))
    );

    renderRecipeList(filtered);
});


// Fetch full recipe
async function loadRecipeDetails(name) {
    const res = await fetch(`/api/recipe/${name}`); // 🟢 TODO backend route
    const data = await res.json();

    document.getElementById('recipe-details').innerHTML = `
        <h2>${data.name}</h2>
        <h4>Ingredients</h4>
        <p>${data.ingredients}</p>
        <h4>Instructions</h4>
        <p>${data.instructions}</p>
    `;
}

loadRecipes();
