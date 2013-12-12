var controllers = angular.module('controllers', []);
 
controllers.controller('VideoListController', ['$scope', '$http', 'media_library',
  function ($scope, $http, media_library) {
      
      $scope.loading = true
	  media_library.get_library_data(function(data){
          $scope.libraries = data
          $scope.loading = false
	  })
  }]);
 
controllers.controller('VideoDetailController', ['$scope', '$routeParams', 'media_library',
  function($scope, $routeParams, media_library) {
	  video_id = atob($routeParams.videoId)
	  console.log(video_id)
	  library_data = ""
	  
	  media_library.get_library_data(function(data){
          $scope.libraries = data
		  result = null

		  angular.forEach($scope.libraries, function(library, library_key){
			  angular.forEach(library.library, function(item, item_key){
				  if(item.path == video_id)
				  {
					  console.log("found")
					  result = item
				  }
				  	
			  });		 
		  });
		  
		  $scope.video = result
		  		  
	  }) 

	  
  }]);