var app = angular.module('app', [
  'ngRoute',
  'controllers',
  'encoding',
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
  
app.factory('media_library', function($http) {
	lib_data = null
	service = {}
	
	service.get_library_data = function(callback)
	{
		
		if(lib_data== null)
		{
			console.log("getting library")
			$http.get('/get_library').success(function(data)
			{
				callback(data)
				lib_data = data
			});			
		}
		else
		{
			callback(lib_data)
		}		
	}
	
	
	service.get_library_item_data = function(hash, callback) 
	{
      $http.get('/get_file?file_hash=' + hash).success(function(data)
      {
        callback(data)
      });     
    }
	
	return service
  }
);
  
angular.module('encoding', []).
	filter('encode_url', function() {               // filter is a factory function
	 return function(string) { // first arg is the input, rest are filter params
		 return btoa(string)
	 }
	}).
	filter('decode_url', function() {               // filter is a factory function
	 return function(string) { // first arg is the input, rest are filter params
		 return atob(string)
	 }
	});


  app.directive('selectOnClick', function () {
    // Linker function
    return function (scope, element, attrs) {
        element.bind('click', function () {
            //this.select();
            e = this
            setTimeout(function() {
              e.setSelectionRange(0, 9999);
            }, 1);
        });
    };
});
	