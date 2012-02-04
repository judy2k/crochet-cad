patternVM =
    rows: ko.observable(25)
    innerStitches: ko.observable(12)
$.extend patternVM,
    instructions: ko.computed
        read: ->
            counts = Crocad.torus @innerStitches(), @rows()
            ({num: i+1, instructions: inst} for inst, i in Crocad.rows(counts))
        owner: patternVM
        toString: -> "PatternVM"

@patternVM = patternVM
$ ->
    ko.applyBindings(patternVM)
    $('.nav-tabs a:last').tab('show')
