// Copyright (C) 2024 twyleg
import QtQuick 2.15

Item {
    id: sliderSpinBoxHighlightedBackground

    property var highlights
    property list<Rectangle> highlightRectangles

    property var alignment
    property var from
    property var to

    width: parent ? parent.width : 0
    height: parent ? parent.height : 0

    onWidthChanged: updateHighlights()
    onHeightChanged: updateHighlights()
    onParentChanged: {
        tryToInheritParametersFromParent()
        updateHighlights()
    }

    onHighlightsChanged: {
        updateHighlights()
    }

    function tryToInheritParametersFromParent() {
        if (parent) {
            if (parent.alignment !== undefined && sliderSpinBoxHighlightedBackground.alignment === undefined) {
                sliderSpinBoxHighlightedBackground.alignment = Qt.binding(function() { return parent.alignment })
                console.debug(`Inherited "alignment" from parent:  ${sliderSpinBoxHighlightedBackground.alignment}`)
            }
            if (parent.from !== undefined && sliderSpinBoxHighlightedBackground.from === undefined) {
                sliderSpinBoxHighlightedBackground.from = Qt.binding(function() { return parent.from })
                console.debug(`Inherited "from" from parent:  ${sliderSpinBoxHighlightedBackground.from}`)
            }
            if (parent.to !== undefined && sliderSpinBoxHighlightedBackground.to === undefined) {
                sliderSpinBoxHighlightedBackground.to = Qt.binding(function() { return parent.to })
                console.debug(`Inherited "to" from parent:  ${sliderSpinBoxHighlightedBackground.to}`)
            }
        }
    }

    function initHighlights() {

        for(var i=0; i<highlights.length; i++) {
            var highlight = highlights[i]
            var value = highlight[2]

            var component =  Qt.createComponent("QtQuick", "Rectangle", Component.PreferSynchronous, sliderSpinBoxHighlightedBackground)
            var obj = component.createObject(sliderSpinBoxHighlightedBackground, {
                "color": value ? "green" : "red"
            })

            highlightRectangles.push(obj)
        }
    }

    function clearHighlights() {
        for(var i=0; i<highlightRectangles.length; i++) {
            var hightlightRectangle = highlightRectangles[i]
            hightlightRectangle.destroy()
        }
        highlightRectangles = []
    }

    function updateHighlights() {

        if (parent) {
            if (highlights.length !== highlightRectangles.length) {
                clearHighlights()
                initHighlights()
            }

            for(var i=0; i<highlights.length; i++) {
                var highlight = highlights[i]
                var highlightRectangle = highlightRectangles[i]

                var from = highlight[0]
                var to = highlight[1]

                var pixelFrom = parent.slider.pixelFromValue(from)
                var pixelTo = parent.slider.pixelFromValue(to)

                if(alignment === Qt.Vertical) {
                    var height = pixelFrom - pixelTo
                    highlightRectangle.y = pixelTo
                    highlightRectangle.height = height

                    highlightRectangle.anchors.left = left
                    highlightRectangle.anchors.right = right
                } else if(alignment === Qt.Horizontal){
                    highlightRectangle.x = pixelFrom
                    highlightRectangle.width = pixelTo - pixelFrom

                    highlightRectangle.anchors.top = top
                    highlightRectangle.anchors.bottom = bottom
                }
            }
        }
    }

    Component.onCompleted: {
        tryToInheritParametersFromParent()
        initHighlights()
        updateHighlights()
    }
}
