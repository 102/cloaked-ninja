var projects = [{
  'name': 'test',
  'files': [{
    'name': 'test.cpp',
    'content': 'asdf',
  },{
    'name': 'test.cuda',
    'content': 'zxc',
  }],
}, {
  'name': 'test1',
}, {
  'name': 'hui s gory',
  'files': [{
    'name': 'zxc.zxc',
    'content': 'asdf',
  }],
}];

angular.module('app', ['ngRoute'])
  .config(function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'projects.html',
        controller: 'projectsController'
      })
      .when('/edit/:projectname/:filename', {
        templateUrl: 'edit.html',
        controller: 'editController'
      });
  })
  .controller('mainController', ['$scope', '$location', function($scope, $location){
    $scope.asd = 'asd';
    $scope.projects = projects;
    $scope.location = $location;
  }])
  .controller('editController', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.project = projects.filter(function(object) {
      return object.name === $routeParams.projectname; 
    })[0];
    $scope.file = $scope.project.files.filter(function(object) {
      return object.name === $routeParams.filename;
    })[0];
    $scope.save = function() {
      //TODO: $http.post query
    };
  }])
  .controller('projectsController', ['$scope', function($scope) {
    
  }]);

($( document ).ready(function(){
  $test = $( '.main-container' );
  $test.css('backgroundColor', 'red');
}));