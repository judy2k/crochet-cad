
class Donut
    constructor:->
        @rows =  ko.observable(25)
        @innerStitches = ko.observable(12)
        @snap = ko.observable(true)
        @instructions = ko.computed
            read: ->
                counts = Crocad.torus @innerStitches(), @rows()
                if @snap()
                    counts = Crocad.roundToNearest(counts, 6, @innerStitches())
                ({num: i+1, instructions: inst} for inst, i in Crocad.rows(counts))
            owner:  @

class Sphere
    constructor:->
        @rows = ko.observable(14)
        @snap = ko.observable(true)
        @instructions = ko.computed
            read: ->
                counts = Crocad.sphere(@rows())
                if @snap()
                    counts = Crocad.roundToNearest(counts, 6, 6)
                ({num: i+1, instructions: inst} for inst, i in Crocad.rows(counts))
            owner:  @

patternVM =
    donut: new Donut()
    sphere: new Sphere()
    toString: -> "PatternVM"

@patternVM = patternVM
$ ->
    ko.applyBindings(patternVM)
    $('.nav-tabs a:first').tab('show')
