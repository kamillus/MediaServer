var controllers = angular.module('controllers', []);
 
controllers.controller('VideoListController', ['$scope', '$http',
  function ($scope, $http) {
      
      $scope.loading = true

      $http.get('/get_library').success(function(data) {
        $scope.libraries = data
        $scope.loading = false
      });
	  
	  
  }]);
 
controllers.controller('VideoDetailController', ['$scope', '$routeParams',
  function($scope, $routeParams) {
	  
  }]);