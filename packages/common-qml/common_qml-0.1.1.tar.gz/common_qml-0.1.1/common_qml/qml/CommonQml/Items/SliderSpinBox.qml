// Copyright (C) 2024 twyleg
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import CommonQml.Helper 0.1

Item {
    id: sliderSpinBox

    property alias name: headerText.text
    property alias nameAngle: headerText.rotation

    property double value: 0
    property double to
    property double from
    property double stepSize: 0.1
    property list<double> ticks
    property alias ticksOpacity: ticksRepeater.opacity

    property int alignment: Qt.Vertical

    property alias header: header
    property alias slider: slider
    property alias spinBox: spinBox

    property Item background: null
    property alias backgroundWidth: sliderContainer.width
    property alias backgroundHeight: sliderContainer.height

    GridLayout {
        id: layout

        anchors.fill: parent

        columns: sliderSpinBox.alignment === Qt.Horizontal ? 3 : 1
        rows: sliderSpinBox.alignment === Qt.Vertical ? 3 : 1

        Item {
            id: header

            Layout.fillWidth: sliderSpinBox.alignment === Qt.Vertical
            Layout.fillHeight: sliderSpinBox.alignment === Qt.Horizontal

            height: Math.max(headerText.height, headerText.width)
            width: Math.max(headerText.height, headerText.width)

            Text {
                id: headerText

                anchors.centerIn: parent
                rotation: -45
                color: "white"
                font.bold: true
            }
        }

        Item {
            id: sliderContainer

            property alias alignment: sliderSpinBox.alignment
            property alias from: sliderSpinBox.from
            property alias to: sliderSpinBox.to
            property alias slider: slider

            Layout.fillWidth: true
            Layout.fillHeight: true

            Slider {
                id: slider

                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: sliderSpinBox.alignment === Qt.Vertical && sliderSpinBox.ticksAvailable() ? parent.horizontalCenter : parent.right
                anchors.bottom: sliderSpinBox.alignment === Qt.Horizontal && sliderSpinBox.ticksAvailable() ? parent.verticalCenter : parent.bottom

                orientation: sliderSpinBox.alignment === Qt.Vertical ? Qt.Vertical : Qt.Horizontal

                from: sliderSpinBox.from
                to: sliderSpinBox.to

                stepSize: sliderSpinBox.stepSize
                live: false

                bottomPadding: 0
                topPadding: 0
                leftPadding: 0
                rightPadding: 0

                anchors.margins: 0

                onValueChanged: sliderSpinBox.update(value)

                function update(newValue: double) {
                    if(Math.abs(value - newValue) >= stepSize * 0.9) {
                        value = newValue
                    }
                }

                function pixelFromValue(v) {
                    if (alignment === Qt.Vertical) {
                        return height - (bottomPadding + implicitHandleHeight/2.0 + ((height - bottomPadding - topPadding - implicitHandleHeight) / (to - from)) * (v - from))
                    } else {
                        return (leftPadding + implicitHandleWidth/2.0 + ((width - rightPadding - leftPadding - implicitHandleWidth) / (to - from)) * (v - from))
                    }
                }
            }

            Repeater {
                id: ticksRepeater

                model: sliderSpinBox.ticks

                visible: sliderSpinBox.ticksAvailable()

                opacity: 1.0

                Item {
                    id: tickmark

                    opacity: ticksRepeater.opacity

                    width: sliderSpinBox.alignment === Qt.Vertical ? parent.width : 1
                    height: sliderSpinBox.alignment === Qt.Horizontal ? parent.height : 1

                    y: sliderSpinBox.alignment === Qt.Vertical ? slider.pixelFromValue(modelData) : 0
                    x: sliderSpinBox.alignment === Qt.Horizontal ? slider.pixelFromValue(modelData) : 0

                    Rectangle {
                        id: tickmarkLabel

                        color: "white"

                        Component.onCompleted: {
                            if(sliderSpinBox.alignment === Qt.Vertical) {
                                anchors.verticalCenter = parent.verticalTop
                                anchors.left = parent.left
                                anchors.right = parent.horizontalCenter
                                height = 1
                            } else {
                                anchors.horizontalCenter = parent.horizontalLeft
                                anchors.top = parent.top
                                anchors.bottom = parent.verticalCenter
                                width = 1
                            }
                        }
                    }

                    Text {
                        id: tickmarkText

                        anchors.top: sliderSpinBox.alignment === Qt.Vertical ? parent.verticalCenter : parent.top
                        anchors.left: sliderSpinBox.alignment === Qt.Horizontal ? parent.left : parent.horizontalCenter
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom

                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        height: 20

                        color: "white"
                        text:  "%1".arg(modelData)
                    }
                }
            }

            Component.onCompleted: {
                if(sliderSpinBox.background) {
                    sliderSpinBox.background.parent = sliderContainer
                    sliderSpinBox.background.z = -1
                }
            }
        }

        DoubleSpinBox {
            id: spinBox

            to: sliderSpinBox.to
            from: sliderSpinBox.from
            stepSize: sliderSpinBox.stepSize

            value: sliderSpinBox.value

            // Layout.fillWidth: sliderSpinBox.alignment === Qt.Vertical
            // Layout.fillHeight: sliderSpinBox.alignment === Qt.Horizontal

            Layout.minimumHeight: 50
            Layout.minimumWidth: 200

            onValueChanged: sliderSpinBox.update(value)
        }
    }

    function update(value: double) {
        sliderSpinBox.value = value

        spinBox.update(value)
        slider.update(value)
    }

    function ticksAvailable() {
        return sliderSpinBox.ticks.length > 0
    }
}
