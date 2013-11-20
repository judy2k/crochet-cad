'use strict'

angular.module('webApp')
    .controller 'SphereCtrl', ($scope) ->
        $scope.snap = true
        $scope.rows = 12
        $scope.pattern = []

        $scope.updatePattern = ->
            rowCounts = Crocad.sphere $scope.rows
            if $scope.snap
                rowCounts = Crocad.roundToNearest(rowCounts, 6)
            $scope.pattern = Crocad.rows(rowCounts)
