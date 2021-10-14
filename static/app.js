const BASE_URL = "https://api.spoonacular.com"
const apiKey = "a1de5c39128c400a880f7e8337e23bc1"
const learn_more = "Click image to learn more"

function makeFoodHTML(item){
  if (item.missIngredient){
    let more = item.missIngredient.map(m => {
      return (m.name.toUpperCase())
    })
      let $items = (
          `
          <div class="p-3 mb-2 bg-primary text-white" id="${item.id}">
              <h1 class="card-title" id="${item.id}"><i class="far fa-heart text-muted"></i>${item.title}</h1>
              <img class="card-image" id="${item.id}" src="${item.img}">
              <p class="card-text" id="${item.id}">${item.summary? item.summary: learn_more}</p>
              <li>${item.missIngredient? more: ""} will be needed</li>
          </div>   
      `)
      
      $('#foodspace').append($items)
  } else{
    let $items = (
      `
      <div class="p-3 mb-2 bg-primary text-white" id="${item.id}">
          <h1 class="card-title" id="${item.id}"><i class="far fa-heart text-muted"></i>${item.title}</h1>
          <img class="card-image" id="${item.id}" src="${item.img}">
          <p class="card-text" id="${item.id}">${item.summary? item.summary: learn_more}</p>
      </div>   
  `)
  
  $('#foodspace').append($items)
  }
  
}

async function makefoodDetailHTML(item){
  // const item = await recipe_detail(4632)
  $("#dishImg").append(`<img src="${item.image}">`)
  $("#dishSummary").append(item.summary)
  
  for (let dish of item.dishTypes){
    const $dishtype = (
      `
        <li> ${dish}</li>
      `)
      $("#dishType").append($dishtype)
  }

  for (let ing of item.extendedIngredients){
    const $toBuy = (
    `
      <li>${ing.name.toUpperCase()}: ${ing.original}</li>
          
    `)
      $("#thingsToBuy").append($toBuy)
  }

  if (item.analyzedInstructions){
    const steps = item.analyzedInstructions[0].steps
    const arr = steps.map(s => {
      return {
        equipment: s.equipment,
        step: s.step
      }
    })
    let count = 1
    for (let step of arr){
      let equi = step.equipment
      const $steps = (
      `
        <h6>Step ${count}</h6>
        <li>In this step you need ${equi.length>0? equi[0].name: "nothing new"}</li>
        <p>${step.step} </p>
      `  
    )
    count++
    $("#steps").append($steps)
    }
  }
  else{
    $("#steps").append(item.instructions)
  }
}

async function foodList(){
  let food_list = await axios.get(`https://api.spoonacular.com/recipes/random?number=20&apiKey=${apiKey}`)
  let food = food_list.data.recipes.map(arr => {
    return {
      id: arr.id,
      title: arr.title,
      img: arr.image,
      summary: arr.summary
    }
  })
  return food
}


async function searchfood(query){
  const search_list = await axios.get(`https://api.spoonacular.com/recipes/complexSearch?query=${query}&number=20&instructionsRequired=true&apiKey=${apiKey}`)
  let food = search_list.data.results.map(arr => {
    return {
      id: arr.id,
      title: arr.title,
      img: arr.image,
    }
  })
  return food
}

async function getFoodByNutrient(){
  const nutrient = await axios.get(`https://api.spoonacular.com/recipes/findByNutrients?minCarbs=10&maxCarbs=50&minFat=10&maxFat=70&minAlcohol=20&apiKey=${apiKey}`)
  let food = nutrient.data.map(arr => {
    return {
      id: arr.id,
      title: arr.title,
      img: arr.image,
    }
  })
  return food
}

async function getFoodByIngredient(){
  const ingredient = await axios.get(`https://api.spoonacular.com/recipes/findByIngredients?ingredients=oil,+flour,+sugar&number=20&apiKey=${apiKey}`)
  let food = ingredient.data.map(arr => {
    return {
      id: arr.id,
      title: arr.title,
      img: arr.image,
      missIngredient: arr.missedIngredients
    }
  })
  return food
}

let food_id  = 716429
async function recipe_detail(food_id){
  const recipe_detail = await axios.get(`https://api.spoonacular.com/recipes/716429/information?includeNutrition=true&apiKey=${apiKey}`)
  console.log(recipe_detail.data)
  return recipe_detail.data
}

async function getData(){
  const my_foods = await getFoodByNutrient()
  for (let my_food of my_foods){
    makeFoodHTML(my_food)
  } 
}

// getFoodByIngredient()
// getFoodByNutrient()
// makefoodDetailHTML() 
// getfoodDetail()