/*****************************************************************************/
/* Items Publish Functions
/*****************************************************************************/

Meteor.publish('items', function () {
  // you can remove this if you return a cursor
  return Items.find();
});
