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

    @sum: (items) ->
        _.reduce(items, ((memo,num)-> memo + num), 0)

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


class MultipleStitches extends Instruction
    constructor: (@_stitches=2, @_stitchesInto=1, @_stitchType='sc') ->
    stitchesInto: ->
        @_stitchesInto
    toString: ->
        inst = "#{@_stitches}#{@_stitchType}"
        if @_stitchesInto is 1
            inst += " into stitch"
        else
            inst += " into next #{@_stitchesInto} stitches"
        inst
Crocad.MultipleStitches = MultipleStitches

class InstructionGroup
    constructor: (_instructions)->
        @_instructions = if _instructions then _instructions else []
    stitches: ->
        Crocad.sum(x.stitches() for x in @_instructions)
    stitchesInto: ->
        Crocad.sum(x.stitchesInto() for x in @_instructions)
    toString: ->
        (x.toString() for x in @_instructions).join(', ')
Crocad.InstructionGroup = InstructionGroup

@Crocad = Crocad
