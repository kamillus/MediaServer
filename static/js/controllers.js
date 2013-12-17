var controllers = angular.module('controllers', []);
 
controllers.controller('VideoListController', ['$scope', '$http', 'media_library', 'search', 'media_player',
  function ($scope, $http, media_library, search, media_player) {  
    $scope.loading = true
    $scope.header = "/static/partials/header.html"

    
	  media_library.get_library_data(function(data){
      $scope.libraries = data
      $scope.loading = false
      $scope.column = "none"
      $scope.search = search

		  
		  $scope.total_count = 0
	  
		  angular.forEach($scope.libraries, function(library, library_key){
			  $scope.total_count += library.library.length
		  });
	  })	 

    $scope.add_to_playlist = function(item) {
      media_player.playlist.push(item)
    }

  }]);
 
controllers.controller('VideoDetailController', ['$scope', '$http', '$routeParams', 'media_library', 'media_player',
  function($scope, $http, $routeParams, media_library, media_player) {
	  video_id = $routeParams.videoId
	  console.log(video_id)
	  library_data = ""
	  
	  media_library.get_library_item_data(video_id, function(data){
      $scope.libraries = data
		  result = data
      result.static_path = result.path.replace(result.library, "")
      
      result.music = result.filename.indexOf(".mp3")>0? true: false;
      result.video = result.filename.indexOf(".mp4")>0? true: false;
	  
      if(result.music)
      	result.music_url = "http://" + location.host + "/stream_file/" + result.hash

      if(result.video)
        result.video_url = "http://" + location.host + "/stream_file/" + result.hash

		  $scope.video = result
      $scope.host = location.host
      result.vlc_udp_path = "rtsp://" + $scope.host + "/" + "static_media" + result.static_path

      $scope.vlc_player_copy = "http://" + $scope.host + "/stream_file/" + $scope.video.hash

      $scope.open_clipboard = function()
      {
          window.prompt ("Copy to clipboard:", "http://" + $scope.host + "/stream_file/" + $scope.video.hash);
      }

      $scope.open_vlc = function(){
        //window.location = result.vlc_udp_path
        playback = "vlc://" + "http://" + $scope.host + "/stream_file/" + $scope.video.hash;
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

      $scope.add_to_playlist = function() {
        console.log(media_library)
        media_player.playlist.push($scope.video)
      }
		  		  
	  }) 

	  
  }]);
  
controllers.controller('MusicPlayerController', ['$scope', '$http', 'media_player',
    function ($scope, $http, media_player) {  
		
      $scope.playlist = media_player.playlist
    	$scope.player = "/static/partials/music_player.html"
      $scope.show_playlist = 1

  	  }

]);