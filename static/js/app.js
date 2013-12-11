var app = angular.module('app', [
  'ngRoute',
  'controllers'
]);

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '/static/partials/video-list.html',
        controller: 'VideoListController'
      }).
      when('/videos/:videoId', {
        templateUrl: '/static/partials/video-detail.html',
        controller: 'VideoDetailController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);