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

      result.cover = "/get_cover_art?file_hash=" + result.hash

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

      $scope.playlist_empty = $scope.playlist.count > 0? false: true;
      $scope.currently_playing = ""


      $scope.time_update = function(e, elem, attr)
      {

        $scope.$apply() 
      }

      $scope.ended = function(e, elem, attr)
      { 
            $scope.play_next(e, elem, attr)
      }

      $scope.play = function(hash)
      {
        angular.forEach($scope.playlist, function(library, library_key){
          console.log(library)

          if(hash == library.hash)
          {
            $scope.music_url = "http://" + location.host + "/stream_file/" + library.hash
            $scope.currently_playing = library.hash
          }
        });
      } 

      $scope.play_next = function(e, elem, attr)
      {
        index = 0
        found_item = false

        angular.forEach($scope.playlist, function(library, library_key){
          console.log(library)

          if($scope.currently_playing == library.hash && !found_item)
          {
            index = library_key
            console.log(index)
            found_item = true
          }
        });   

        $scope.currently_playing = $scope.playlist[index+1].hash
        $scope.music_url = "http://" + location.host + "/stream_file/" + $scope.playlist[index+1].hash
        $scope.$apply() 
        elem.context.play()

      }

      $scope.remove = function(hash)
      {
        angular.forEach(media_player.playlist, function(library, library_key){
          console.log(library)

          if(hash == library.hash)
          {
            console.log(library_key)
            delete media_player.playlist.splice(library_key,1)
          }
        });        
      }
  	}

]);

controllers.controller('DirectoryListController', ['$scope', '$http', 'media_library', 'search', 'media_player',
  function ($scope, $http, media_library, search, media_player) {  
    $scope.loading = true
    $scope.header = "/static/partials/header.html"

    
    media_library.get_library_data(function(data){
      $scope.libraries = data
      $scope.loading = false
      $scope.search = search
      $scope.listing = []
      $scope.last_directory = ""
      $scope.browse_history = [""]
      
      $scope.total_count = 0
    
      angular.forEach($scope.libraries, function(library, library_key){
        $scope.total_count += library.library.length
      });




    })   

    $scope.find_files = function(path, skip_history){
        $scope.listing = []
        $scope.found_dirs = []
        console.log(path)

        if(!skip_history) $scope.browse_history.push(path)

       angular.forEach($scope.libraries, function(library, library_key){
        angular.forEach(library.library, function(item, item_key){
          if(item.directory[item.directory.length - 1] != "/")
          {
            item.directory = item.directory + "/"
          }  

          if(path + "/" == item.directory)
          {
            item_with_type = item
            item_with_type["type"] = "file"
            $scope.listing.push(item) 
          }
          //console.log(new RegExp(path + "\/" + ".+?\/",'g') + " " + item.directory)
          matches = item.directory.match(new RegExp(path + "\/" + ".+?\/",'g'))
          if(matches && matches[0] && !$scope.found_dirs[matches[0]])
          {
            directory = matches[0].substring(0, matches[0].length - 1);

            $scope.back = ""
            $scope.found_dirs[matches[0]] = true
            $scope.listing.push({directory:directory, type:"directory"})
          }
        })
      });
            console.log($scope.browse_history)
 
    }

    $scope.go_back = function()
    {
      $scope.browse_history.pop()
      $scope.find_files($scope.browse_history[$scope.browse_history.length-1], true)
    }

    $scope.set_current_item = function(item)
    {
      $scope.current_item = item
    }

    $scope.add_to_playlist = function(item) {
      media_player.playlist.push(item)
    }
}]);