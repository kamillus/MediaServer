var controllers = angular.module('controllers', []);
 
controllers.controller('VideoListController', ['$scope', '$http', 'media_library',
  function ($scope, $http, media_library) {  
    $scope.loading = true
	  media_library.get_library_data(function(data){
          $scope.libraries = data
          $scope.loading = false
		  
		  $scope.total_count = 0
	  
		  angular.forEach($scope.libraries, function(library, library_key){
			  $scope.total_count += library.library.length
		  });
	  })	  
  }]);
 
controllers.controller('VideoDetailController', ['$scope', '$http', '$routeParams', 'media_library',
  function($scope, $http, $routeParams, media_library) {
	  video_id = $routeParams.videoId
	  console.log(video_id)
	  library_data = ""
	  
	  media_library.get_library_data(function(data){
      $scope.libraries = data
		  result = null

		  angular.forEach($scope.libraries, function(library, library_key){
			  angular.forEach(library.library, function(item, item_key){
				  if(item.hash == video_id)
				  {
					  console.log("found")
					  result = item
            result.library = library_key
				  }
				  	
			  });		 
		  });

      result.static_path = result.path.replace(result.library, "")
		  $scope.video = result
      $scope.host = location.host
      result.vlc_udp_path = "rtsp://" + $scope.host + "/" + "static_media" + result.static_path


      console.log(result)

      $scope.vlc_player_copy = "http://" + $scope.host + "/get_file/" + $scope.video.hash

      $scope.open_clipboard = function()
      {
          window.prompt ("Copy to clipboard:", "http://" + $scope.host + "/get_file/" + $scope.video.hash);
      }

      $scope.open_vlc = function(){
        //window.location = result.vlc_udp_path
        playback = "vlc://" + "http://" + $scope.host + "/get_file/" + $scope.video.hash;
        console.log(playback)
        window.location = playback
      }

      $scope.open_rtsp = function(){
        /*$http.get('/start_stream?path=' + $scope.video.path).success(function(data)
        {
        });*/   

        setTimeout(function() {
              window.location = "vlc://" + "http://" + $scope.host + "/static_media" + $scope.video.static_path;
        }, 2);
        
      }
		  		  
	  }) 

	  
  }]);