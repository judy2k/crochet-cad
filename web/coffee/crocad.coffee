class Crocad
    @divmod: (x, y) -> [Math.floor(x/y), x % y]

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

    @rows: (counts) ->
        result = []
        for index in [0...counts.length]
            result.push(Crocad.row(
                if index is 0 then null else counts[index-1],
                counts[index]
            ))
        result

    @row: (prev, count)->
        prev = if typeof prev is "number" then Math.round(prev) else null
        count = if typeof count is "number" then Math.round(count) else null
        result = new Crocad.InstructionGroup()
        if prev is null
            result.append(new Crocad.Instruction(count, 'ch'))
        else
            abs = Math.abs; floor = Math.floor
            divmod = Crocad.divmod

            diff = count - prev
            if diff is 0
                result.append(new Crocad.Instruction(count))
            else
                repeats = Crocad.gcd(count, prev)
                row_rem = 0
                if repeats is 1
                    repeats = abs(diff)
                prev = floor(prev/repeats)
                [count, row_rem] = divmod(count,repeats)
                diff = count - prev
                scs = Math.min(prev, count) - abs(diff)
                [stcount, sc_rem] = divmod(scs, abs(diff))
                if repeats > 1
                    rep = new Crocad.InstructionGroup()
                    rep.repeats = repeats
                    result.append(rep)
                else
                    rep = result
                part_count = floor(abs(diff))
                for i in [0...part_count]
                    rep.append(if diff > 0
                        new Crocad.MultipleStitches()
                    else
                        new Crocad.StitchTogether())
                    if i < abs(diff) - 1
                        if stcount > 0
                            rep.append(new Crocad.Instruction(stcount))
                    else
                        if (stcount + sc_rem) > 0
                            rep.append(new Crocad.Instruction(stcount + sc_rem))
                if row_rem > 0
                    result.append(new Crocad.Instruction(row_rem))
        result

    @sphere: (rows) ->
        rad = (rows + 1) / Math.PI
        row_angle = Math.PI / (rows + 1)
        result = []
        for row in [0...rows]
            row_rad = rad * Math.sin((row + 1) * row_angle)
            result.push(Math.round(2 * Math.PI * row_rad))
        result

    @torus: (init_stitches, rows, initial_angle=0) ->
        # Radius of the hole in 'stitches':
        hole_rad = init_stitches / (2 * Math.PI)
        # Radius of a donut vertical cross-section:
        xrad = rows / (2 * Math.PI)
        row_angle = 2 * Math.PI / rows
        result = []
        for row in [0...rows]
            rad = hole_rad + (xrad - (xrad * Math.cos(row * row_angle + initial_angle)))
            circ = rad * 2 * Math.PI
            result.push(Math.round(circ))
        result

    toString: ->
        "Crocad instance"
        
class Crocad.Instruction
    constructor: (@_multiple=1, @_stitchType='sc') ->
    merge: (ob)->
        if ob.constructor is @constructor and ob._stitchType is @_stitchType
            @_merge(ob) isnt false
        else
            false
    _merge: (ob)->
        @_multiple += ob._multiple
    stitches: ->
        @_multiple
    stitchesInto: @prototype.stitches
    toString: ->
        if @_multiple > 1
            "#{@_multiple}#{@_stitchType}"
        else
            @_stitchType.toString()

class Crocad.StitchTogether extends Crocad.Instruction
    constructor: (@_multiple=1, @_togetherCount=2, @_stitchType='sc') ->
    _merge: (ob)->
        if ob._togetherCount is @_togetherCount
            @_multiple += ob._multiple
        else
            false
    stitchesInto: ->
        @_multiple * @_togetherCount
    toString: ->
        inst = "#{@_stitchType}#{@_togetherCount}tog"
        if @_multiple > 1
            inst += " in next #{@_multiple}"
        inst

class Crocad.MultipleStitches extends Crocad.Instruction
    constructor: (@_multiple=1, @_stitchesInto=2, @_stitchType='sc') ->
    _merge: (ob)->
        if ob._stitchesInto is @_stitchesInto
            @_multiple += ob._multiple
        else
            false
    stitches: ->
        @_multiple * @_stitchesInto
    stitchesInto: ->
        @_multiple
    toString: ->
        inst = "#{@_stitchesInto}#{@_stitchType}"
        if @_multiple is 1
            inst += " into stitch"
        else
            inst += " into next #{@_multiple} stitches"
        inst

class Crocad.InstructionGroup extends Crocad.Instruction
    constructor: (_instructions, @repeats=1)->
        @_instructions = if _instructions then _instructions else []
    _merge: (ob) -> false
    append: (instruction)->
        last = @_instructions[@_instructions.length-1]
        if last isnt undefined and last.merge(instruction)
            return
        else
            @_instructions.push(instruction)
    stitches: ->
        Crocad.sum(x.stitches() for x in @_instructions) * @repeats
    stitchesInto: ->
        Crocad.sum(x.stitchesInto() for x in @_instructions) * @repeats
    toString: ->
        if @repeats is 1
            (x.toString() for x in @_instructions).join(', ')
        else
            '[' + (x.toString() for x in @_instructions).join(', ') + ". Repeat #{@repeats} times.]"

@Crocad = Crocad
