/*****************************************************************************/
/* Client and Server Routes */
/*****************************************************************************/
Router.configure({
  layoutTemplate: 'MasterLayout',
  loadingTemplate: 'Loading',
  notFoundTemplate: 'NotFound',
  templateNameConverter: 'upperCamelCase',
  routeControllerNameConverter: 'upperCamelCase'
});

Router.map(function () {
  /*
    Example:
      this.route('home', {path: '/'});
  */
  this.route('items.index', {
    path: '/items'
  });
  this.route('order.add', {
    path: '/order/new',
    waitOn: function() {
      return Meteor.subscribe('items');
    }
  });
  this.route('orders.index', {path: '/'});
});
