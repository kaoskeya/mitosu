// Paste in console

var jq = document.createElement('script');
jq.src = "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min.js";
document.getElementsByTagName('head')[0].appendChild(jq);


var _cats = $(".menu-category")

var categories = []
var items = []

_.each(_cats, function(cat){
  
  var el = $(cat)
  var cat_name = el.find(".category-title").text().trim()
  var cat_id = cat.id

  categories.push({
    id : cat_id,
    name : cat_name,
    description : el.find(".category-description").text().trim()
  })

  var _items = el.find(".menu-item")

  _.each(_items, function(item){

    var iel = $(item)

    items.push({
      category_id : cat_id,
      category_name : cat_name,

      id : iel.id,
      name : iel.find(".title").text().trim(),
      description : iel.find(".description").text().trim(),
      price : iel.find(".price").text().trim()
    })
  })
})
