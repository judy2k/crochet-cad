class Crocad
    @gcd: (num1, num2) ->
        while num2 isnt 0
            [num1, num2] = [num2, num1 % num2]
        num1

    @roundToNearest: (val, nearest, min_val=0) ->
        if typeof val is "number"
            val = (Math.floor(val / nearest) + Math.round((val % nearest) / nearest)) * nearest
            Math.max(min_val, val)
        else
            Crocad.roundToNearest(v, nearest, min_val) for v in val

    toString: ->
        "Crocad instance"
        
class Instruction
    constructor: (@_stitches=1, @_stitchType='sc') ->
    stitches: ->
        @_stitches
    stitchesInto: @prototype.stitches
    toString: ->
        if @_stitches > 1
            "#{@_stitches}#{@_stitchType}"
        else
            @_stitchType.toString()
Crocad.Instruction = Instruction


class StitchTogether extends Instruction
    constructor: (@_stitches=1, @_togetherCount=2, @_stitchType='sc') ->
    stitchesInto: ->
        @_stitches * @_togetherCount
    toString: ->
        inst = "#{@_stitchType}#{@_togetherCount}tog"
        if @_stitches > 1
            inst += " in next #{@_stitches}"
        inst
Crocad.StitchTogether = StitchTogether


@Crocad = Crocad
