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
	library_data = ""
	
	return {
        get_library_data: function(callback) {
			if(library_data == "")
			{
				$http.get('/get_library').success(function(data)
				{
					callback(data)
					library_data = data
				});			
			}
			else
			{
				callback(library_data)
			}
				
		}		
    }
  });
  
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
	