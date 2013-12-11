var controllers = angular.module('controllers', []);
 
controllers.controller('VideoListController', ['$scope', '$http',
  function ($scope, $http) {
      $http.get('/get_library').success(function(data) {
        $scope.libraries = data
      });
	  
	  
  }]);
 
controllers.controller('VideoDetailController', ['$scope', '$routeParams',
  function($scope, $routeParams) {
	  
  }]);