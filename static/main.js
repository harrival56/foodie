const $foodlist = $("#foodlist")
const $detail = $("#detail")
const $searchForm = $("#search-form")

async function start(){
    $detail.hide()
    foods = await foodList()
    for (let food of foods){
        makeFoodHTML(food)
    }
    
}

start()
async function getfoodDetail(e){
    const food_id = e.target.id
    $foodlist.hide()
    $detail.show()
    const food = await recipe_detail(food_id)
    makefoodDetailHTML(food)
}
$("#foodlist").on("click", "#foodspace", getfoodDetail)

$searchForm.on("submit", async function handleQuery(e){
    e.preventDefault()
    const data = $("#search-query").val()
    const foods = await searchfood(data)
    $detail.hide()
    $foodlist.show()
    for (let food of foods){
        makeFoodHTML(food)
    }
    data = ""

})