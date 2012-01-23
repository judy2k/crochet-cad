TWO_PI = Math.PI * 2

donut =
    boldAttr:
        'stroke-width': 2
        'fill': '#fff'
 
    drawXSection: (paper, x, y, bigR, littleR) ->
        paper
            .rect(x + littleR, y, bigR * 2 - littleR * 2, littleR * 2)
                .attr({
                    'stroke-width': 0.5,
                    'fill': '#eee'
                })
        paper
            .circle(littleR + x, littleR + y, littleR)
                .attr(this.boldAttr)
        paper
            .circle(x + (bigR * 2) - littleR, littleR + y, littleR)
                .attr(this.boldAttr)

        # Arrow:
        paper
            .circle(x, y + littleR, 5)
                .attr('fill', '#000')
        paper
            .path('M0 0L10 17.3L-10 17.3L0 0')
                .rotate(-15,0.001,0.001)
                .scale(0.5,0.5,0,0)
                .translate(x, y + littleR + 5)
                .attr('fill', '#000')

    drawTop: (paper, x, y, bigR, littleR) ->
        paper
            .circle(x + bigR, y + bigR, bigR)
        paper
            .circle(x + bigR, y + bigR, bigR - littleR * 2)
                .attr(this.boldAttr)

        # Arrow:
        paper
            .circle(x + bigR * 2 - littleR * 2, y + bigR, 5)
                .attr('fill', '#000')
        paper
            .path('M0 0L10 17.3L-10 17.3L0 0')
                .rotate(6,0.001,0.001)
                .scale(0.5,0.5,0,0)
                .translate(x + bigR * 2 - littleR * 2, y + bigR + 5)
                .attr('fill', '#000')

    calculateRadii: (rows, inner_circumference) ->
        littleR = rows / TWO_PI
        return [littleR, (inner_circumference / TWO_PI) + (littleR * 2)]

    calculateScale: (bigR, littleR, margin, w, h) ->
        bigD = bigR * 2
        littleD = littleR * 2

        rectProp = w / (h - margin)
        diagProp = bigD / (littleD + bigD)

        scale = if (diagProp > rectProp)
            # Wider - fit to width:
            w / bigD
        else
            # Taller - fit to height:
            (h - margin) / (littleD + bigD)
        return scale


draw_donut = (x, y, w, h, rows, inner_circumference) ->
    paper = this
    margin = 10

    [littleR, bigR] = donut.calculateRadii(rows, inner_circumference)

    # paper.rect(x, y , w, h).attr('stroke', '#f00').attr('stroke-width', 1)

    scale = donut.calculateScale(bigR, littleR, 10, w, h)
    bigR = scale * bigR
    littleR = scale * littleR

    diagWidth = bigR * 2
    diagHeight = (bigR * 2) + margin + (littleR * 2)

    midX = ((w-diagWidth) / 2) + x
    midY = ((h-diagHeight) / 2) + y

    # paper.rect(midX, midY, diagWidth, diagHeight, 15).attr('stroke', '#0f0').attr('stroke-width', 1)

    donut.drawXSection(paper, midX, midY, bigR, littleR)
    donut.drawTop(paper, midX, midY + littleR * 2 + margin, bigR, littleR)

Raphael.fn.donut = draw_donut
