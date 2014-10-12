/*****************************************************************************/
/* Items Publish Functions
/*****************************************************************************/

Meteor.publish('items', function () {
  // you can remove this if you return a cursor
  return Items.find({ 'category': { $in: ['Chai Shai at 4', 'Desserts', 'Drinks', 'Dum A Dum Rice Combos', 'Halka Phulka', 'Indian Breads', 'Mast Curry Combos', 'Parantha Combos', 'Starters'] } });
});
