'use strict'

angular.module('webApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute'
]).config ($routeProvider) ->
    $routeProvider
        .when '/',
            templateUrl: 'views/main.html'
            controller: 'MainCtrl'
        .when '/sphere',
            templateUrl: 'views/sphere.html'
            controller: 'SphereCtrl'
        .otherwise
            redirectTo: '/'
