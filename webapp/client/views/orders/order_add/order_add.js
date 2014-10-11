
/*****************************************************************************/
/* OrderAdd: Event Handlers and Helpersss .js*/
/*****************************************************************************/
Template.OrderAdd.events({
  'keyup #posseSize': function(e) {
    Session.set('posseSize', parseInt( $(e.target).val() ) )
  },
  'change #itemSearch': function(e) {
    if( $(e.target).val() != '' ) {
      if( Orders.find({ item: $(e.target).val() }).count()) {
        // Item ordered already
        Orders.update({
          item: $(e.target).val()
        }, {
          $inc: {
            quantity: 1
          }
        });
      } else {
        // Item not ordered already
        Orders.insert({
          item: $(e.target).val(),
          quantity: 1,
          price: Items.findOne({ id: $(e.target).val() }).price
        });
      }
      $('#itemSearch')[0].selectize.clear();
    }
  },
  'click .addFromList': function(e) {
    if( Orders.find({ item: $(e.target).data('id') }).count()) {
      // Item ordered already
      Orders.update({
        item: $(e.target).data('id')
      }, {
        $inc: {
          quantity: 1
        }
      });
    } else {
      // Item not ordered already
      Orders.insert({
        item: $(e.target).data('id'),
        quantity: 1,
        price: Items.findOne({ id: $(e.target).data('id') }).price
      });
    }
  },
  'click .incrementQty': function() {
    Orders.update({
      item: this.item
    }, {
      $inc: {
        quantity: 1
      }
    });
  },
  'click .decrementQty': function() {
    if(this.quantity == 1) {
      Orders.remove({
        item: this.item
      });
    } else {
      Orders.update({
        item: this.item
      }, {
        $inc: {
          quantity: -1
        }
      });
    }
  },
  'click .removeItem': function() {
    Orders.remove({
      item: this.item
    });
  }
  /*
   * Example:
   *  'click .selector': function (e, tmpl) {
   *
   *  }
   */
});

Template.OrderAdd.helpers({
  items: function() {
    return Items.find()
  },
  orders: function() {
    return Orders.find()
  },
  ordersCount: function() {
    return Orders.find().count()
  },
  itemName: function(id) {
    return Items.findOne({ id: id }).name
  },
  categories: function() {
    return _.uniq( _.map(Items.find().fetch(), function(item){ return item.category } ) )
  },
  categoryID: function(category) {
    return Items.findOne({ category: category }).cid
  },
  productsInCategory: function(category) {
    return Items.find({ category: category })
  },
  multiply: function(a, b) {
    return a * b
  },
  totalQuantity: function() {
    return _.reduce( _.map(Orders.find().fetch(), function(order){ return order.quantity } ), function(a, b) { return a+b } )
  },
  totalBill: function() {
    return _.reduce( _.map(Orders.find().fetch(), function(order){ return order.quantity * order.price } ), function(a, b) { return a+b } )
  }
  /*
   * Example:
   *  items: function () {
   *    return Items.find();
   *  }
   */
});

/*****************************************************************************/
/* OrderAdd: Lifecycle Hooks */
/*****************************************************************************/
Template.OrderAdd.created = function () {
};

Template.OrderAdd.rendered = function () {
  $("#posseModalTrigger").trigger('click');
  ripples.initInputs();
  Meteor.setTimeout(function(){
    $("#itemSearch").selectize({});
  }, 500);
};

Template.OrderAdd.destroyed = function () {
};


