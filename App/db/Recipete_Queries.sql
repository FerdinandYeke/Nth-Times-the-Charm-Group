Select title
From recipes
Where total_time_min < 30;

Select title
From recipes;

Select title.recipes
From recipes
Join meal_plan_items on meal_plan_items.recipe_id = recipes.recipe_id
Where meal_plan_items.meal_type = 'BREAKFAST';

Select title.recipes
From recipes
Join meal_plan_items on meal_plan_items.recipe_id = recipes.recipe_id
Where meal_plan_items.meal_type = 'LUNCH';

Select title.recipes
From recipes
Join meal_plan_items on meal_plan_items.recipe_id = recipes.recipe_id
Where meal_plan_items.meal_type = 'DINNER';

Select title.recipes
From recipes
Join meal_plan_items on meal_plan_items.recipe_id = recipes.recipe_id
Where meal_plan_items.meal_type = 'SNACK';

Select title.recipes
From recipes
Where not Exists (
    Select 1
    From recipe_ingredients
    Join ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id
    Where recipe_ingredients.recipe_id = recipes.recipe_id
      and ingredients.name = 'Wheat'
);

Select title.recipes
From recipes
Where not Exists (
    Select 1
    From recipe_ingredients
    Join ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id
    Where recipe_ingredients.recipe_id = recipes.recipe_id
      and ingredients.name = 'Milk'
);

Select title.recipes
From recipes
Where not Exists (
    Select 1
    From recipe_ingredients
    Join ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id
    Where recipe_ingredients.recipe_id = recipes.recipe_id
      and ingredients.name = 'Peanuts'
);