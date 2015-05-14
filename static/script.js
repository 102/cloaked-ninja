var s_addr = "http://127.0.0.1:5000";

function enableTab() {
  el = document.getElementById('content');
  el.onkeydown = function(e) {
    if (e.keyCode === 9) {
      var val = this.value;
      var start = this.selectionStart;
      var end = this.selectionEnd;
      this.value = val.substring(0, start) + '\t' + val.substring(end);
      this.selectionStart = this.selectionEnd = start + 1;
      return false;
    }
  };
}

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
  .controller('mainController', ['$scope', '$location', '$http', function($scope, $location, $http){
    $http.get('projects.json').
    success(function(data, status, headers, config) {
      $scope.projects = data.projects;
    }).
    error(function(data, status, headers, config) {
      console.log('something went wrong');
    });
    $scope.location = $location;
  }])
  .controller('editController', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.project = $scope.projects.filter(function(object) {
      return object.name === $routeParams.projectname;
    })[0];
    $scope.file = $scope.project.files.filter(function(object) {
      return object.name === $routeParams.filename;
    })[0];
    enableTab();
    $scope.save = function() {
      $http.post('edit/' + $scope.project.name + '/' + $scope.file.name, {'content': $scope.file.content})
        .success(function(data, status, headers, config) {
          alert('file was updated successfully');
        })
        .error(function(data, status, headers, config) {
          alert('fail');
        });
    };
  }])
  .controller('projectsController', ['$scope', '$http', '$window', function($scope, $http, $window) {
	  $scope.addFile = function(projectName, newFileName) {
      console.log($scope.newFileName);
      $http.get('add-file/' + projectName + '/' + (newFileName || 'new file'));
      $window.location.reload();
	  }
      $scope.addProject = function(projectName) {
      $http.get('add/' + (projectName || 'new project'));
      $window.location.reload();
	  }
  }]);


