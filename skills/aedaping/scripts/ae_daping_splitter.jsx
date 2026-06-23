/*
AE 大屏拆分工具

使用方法：
1. 在 After Effects 里导入完整大屏视频。
2. 在项目面板选中这个视频。
3. 运行 文件 > 脚本 > 运行脚本文件...，选择这个 JSX 文件。
4. 输入每块屏幕的宽度或宽高：
   主要格式：名称,宽,高
   带名称宽度：名称,宽
   只填宽度：1536,2048,1536
   只填尺寸：1536x1152,2048x1152,1536x1152

快速示例：
1920,1920

带名称示例：
Left,1920
Right,1920
*/

(function aeDapingSplitter() {
    function trim(text) {
        return String(text).replace(/^\s+|\s+$/g, "");
    }

    function sanitizeName(text) {
        var cleaned = trim(text).replace(/[\\\/:\*\?"<>\|]/g, "_");
        return cleaned || "screen";
    }

    function splitFields(line) {
        return trim(line).replace(/\uFF0C/g, ",").split(/[\t,]+/);
    }

    function isNumericText(text) {
        return /^-?\d+(\.\d+)?$/.test(trim(text));
    }

    function isHeaderLine(parts) {
        var joined = parts.join(",").toLowerCase();
        return joined.indexOf("name") !== -1 &&
            (joined.indexOf("width") !== -1 || joined.indexOf("w") !== -1);
    }

    function pad2(value) {
        return value < 10 ? "0" + value : String(value);
    }

    function padIndex(value, total) {
        var width = String(total).length;
        if (width < 2) {
            width = 2;
        }
        var text = String(value);
        while (text.length < width) {
            text = "0" + text;
        }
        return text;
    }

    function parsePixelNumber(text, label, lineNumber) {
        var value = parseFloat(trim(text));
        if (isNaN(value)) {
            throw new Error("第 " + lineNumber + " 行：" + label + " 必须是数字。");
        }
        if (value % 1 !== 0) {
            throw new Error("第 " + lineNumber + " 行：" + label + " 必须是整数像素。");
        }
        return value;
    }

    function addScreen(screens, screen, lineNumber) {
        if (screen.width <= 0 || screen.height <= 0) {
            throw new Error("第 " + lineNumber + " 行：宽度和高度必须大于 0。");
        }
        screens.push(screen);
    }

    function parseSizeToken(text, lineNumber) {
        var match = trim(text).toLowerCase().match(/^(\d+)x(\d+)$/);
        if (!match) {
            return null;
        }
        return {
            width: parsePixelNumber(match[1], "width", lineNumber),
            height: parsePixelNumber(match[2], "height", lineNumber)
        };
    }

    function parseExactScreens(lines) {
        var screens = [];
        var sawContent = false;

        for (var i = 0; i < lines.length; i++) {
            var line = trim(lines[i]);
            if (!line || line.charAt(0) === "#") {
                continue;
            }

            var parts = splitFields(line);
            if (isHeaderLine(parts)) {
                continue;
            }

            sawContent = true;
            if (parts.length !== 5 || isNumericText(parts[0])) {
                return null;
            }

            addScreen(screens, {
                name: sanitizeName(parts[0]),
                x: parsePixelNumber(parts[1], "x", i + 1),
                y: parsePixelNumber(parts[2], "y", i + 1),
                width: parsePixelNumber(parts[3], "width", i + 1),
                height: parsePixelNumber(parts[4], "height", i + 1)
            }, i + 1);
        }

        if (sawContent) {
            screens._isExact = true;
        }
        return sawContent ? screens : null;
    }

    function parseAutoLine(line, source, columnStart, autoX, lineNumber) {
        var parts = splitFields(line);
        var parsed = [];

        if (isHeaderLine(parts)) {
            return { screens: [], nextX: autoX };
        }

        if (parts.length === 3 && !isNumericText(parts[0])) {
            parsed.push({
                name: sanitizeName(parts[0]),
                x: autoX,
                y: 0,
                width: parsePixelNumber(parts[1], "width", lineNumber),
                height: parsePixelNumber(parts[2], "height", lineNumber)
            });
        } else if (parts.length === 2 && !isNumericText(parts[0])) {
            parsed.push({
                name: sanitizeName(parts[0]),
                x: autoX,
                y: 0,
                width: parsePixelNumber(parts[1], "width", lineNumber),
                height: source.height
            });
        } else {
            for (var i = 0; i < parts.length; i++) {
                var size = parseSizeToken(parts[i], lineNumber);
                if (size) {
                    parsed.push({
                        name: "S" + pad2(columnStart + i),
                        x: autoX,
                        y: 0,
                        width: size.width,
                        height: size.height
                    });
                    autoX += size.width;
                    continue;
                }

                if (isNumericText(parts[i])) {
                    var width = parsePixelNumber(parts[i], "width", lineNumber);
                    parsed.push({
                        name: "S" + pad2(columnStart + i),
                        x: autoX,
                        y: 0,
                        width: width,
                        height: source.height
                    });
                    autoX += width;
                    continue;
                }

                throw new Error("第 " + lineNumber + " 行格式不对。请使用：名称,宽,高 / 名称,宽 / 1536x512 / 纯宽度。");
            }
        }

        var nextX = autoX;
        for (var j = 0; j < parsed.length; j++) {
            addScreen([], parsed[j], lineNumber);
            if (j === 0 && (parts.length === 3 || parts.length === 2) && !isNumericText(parts[0])) {
                nextX = parsed[j].x + parsed[j].width;
            }
        }

        return { screens: parsed, nextX: nextX };
    }

    function parseAutoScreens(lines, source) {
        var screens = [];
        var autoX = 0;
        var columnIndex = 1;

        for (var i = 0; i < lines.length; i++) {
            var line = trim(lines[i]);
            if (!line || line.charAt(0) === "#") {
                continue;
            }
            var parsedLine = parseAutoLine(line, source, columnIndex, autoX, i + 1);
            for (var s = 0; s < parsedLine.screens.length; s++) {
                addScreen(screens, parsedLine.screens[s], i + 1);
            }
            autoX = parsedLine.nextX;
            columnIndex += parsedLine.screens.length;
        }

        screens._isExact = false;
        return screens;
    }

    function parseScreens(text, source) {
        var lines = String(text).split(/\r\n|\r|\n/);
        var screens = parseExactScreens(lines);
        if (!screens) {
            screens = parseAutoScreens(lines, source);
        }

        if (screens.length === 0) {
            throw new Error("请至少输入一块屏幕。");
        }

        return screens;
    }

    function getSelectedSource() {
        if (!app.project) {
            throw new Error("请先打开一个 After Effects 项目。");
        }

        var selection = app.project.selection;
        if (!selection || selection.length !== 1) {
            throw new Error("请在项目面板里只选中一个完整大屏视频或合成。");
        }

        var item = selection[0];
        if (typeof item.width !== "number" || typeof item.height !== "number" || !item.duration) {
            throw new Error("选中的项目必须是带宽度、高度和时长的视频、序列素材或合成。");
        }

        return item;
    }

    function validateScreens(source, screens) {
        var messages = [];
        var maxRight = 0;
        var hasExact = screens._isExact === true;

        for (var i = 0; i < screens.length; i++) {
            var s = screens[i];
            if (s.x < 0 || s.y < 0) {
                messages.push(s.name + "：x/y 小于 0。");
            }
            if (s.x + s.width > source.width) {
                messages.push(s.name + "：x + 宽度超过原视频宽度 " + source.width + "。");
            }
            if (s.y + s.height > source.height) {
                messages.push(s.name + "：y + 高度超过原视频高度 " + source.height + "。");
            }
            if (s.height > source.height) {
                messages.push(s.name + "：高度超过原视频高度 " + source.height + "。");
            }
            if (s.x + s.width > maxRight) {
                maxRight = s.x + s.width;
            }
        }

        if (!hasExact && maxRight !== source.width) {
            messages.push("当前拆分总宽度是 " + maxRight + "，但原视频宽度是 " + source.width + "。所有块的宽度相加必须正好等于原视频宽度。");
        }

        if (!hasExact) {
            for (var j = 0; j < screens.length; j++) {
                if (screens[j].height !== source.height) {
                    messages.push(screens[j].name + "：高度是 " + screens[j].height + "，但原视频高度是 " + source.height + "。请使用完整高度，这样所有块才能拼回原画面。");
                }
            }
        }

        if (messages.length > 0) {
            throw new Error("无法创建合成：\n\n" + messages.join("\n"));
        }
    }

    function makeUi(source) {
        var win = new Window("dialog", "AE 大屏拆分工具");
        win.orientation = "column";
        win.alignChildren = ["fill", "top"];
        win.spacing = 10;
        win.margins = 14;

        var info = win.add("statictext", undefined, "当前素材：" + source.name + "  (" + source.width + " x " + source.height + ")");

        var prefixGroup = win.add("group");
        prefixGroup.orientation = "row";
        prefixGroup.alignChildren = ["left", "center"];
        prefixGroup.add("statictext", undefined, "合成名前缀：");
        var prefixInput = prefixGroup.add("edittext", undefined, sanitizeName(source.name).replace(/\.[^\.]+$/, ""));
        prefixInput.characters = 30;

        win.add("statictext", undefined, "输入：填写每块屏幕的宽度/宽高，x/y 会自动计算。");
        var screenInput = win.add("edittext", undefined, "", { multiline: true, scrolling: true });
        screenInput.preferredSize = [640, 220];
        if (source.width === 3840 && source.height === 2160) {
            screenInput.text = "1920,1920";
        } else if (source.width === 5120 && source.height === 1152) {
            screenInput.text = "1536,2048,1536";
        } else {
            screenInput.text = "Full," + source.width;
        }

        var hint = win.add("statictext", undefined, "提示：所有宽度相加必须等于原视频宽度。例如 3840x2160 输入 1920,1920。");
        hint.maximumSize.width = 560;

        var presetGroup = win.add("group");
        presetGroup.orientation = "row";
        presetGroup.alignment = "left";
        var horizontalExampleButton = presetGroup.add("button", undefined, "均分两块");
        var namedExampleButton = presetGroup.add("button", undefined, "带名称两块");

        horizontalExampleButton.onClick = function () {
            var half = source.width / 2;
            if (half % 1 === 0) {
                screenInput.text = half + "," + half;
            } else {
                screenInput.text = "Left," + Math.floor(half) + "\nRight," + Math.ceil(half);
            }
        };

        namedExampleButton.onClick = function () {
            var half = source.width / 2;
            if (half % 1 === 0) {
                screenInput.text = "Left," + half + "\nRight," + half;
            } else {
                screenInput.text = "Left," + Math.floor(half) + "\nRight," + Math.ceil(half);
            }
        };

        var buttons = win.add("group");
        buttons.orientation = "row";
        buttons.alignment = "right";
        var cancelButton = buttons.add("button", undefined, "取消", { name: "cancel" });
        var createButton = buttons.add("button", undefined, "创建合成", { name: "ok" });

        createButton.onClick = function () {
            try {
                win.result = {
                    prefix: sanitizeName(prefixInput.text),
                    screens: parseScreens(screenInput.text, source)
                };
                win.close(1);
            } catch (err) {
                alert(err.message);
            }
        };

        cancelButton.onClick = function () {
            win.close(0);
        };

        return win;
    }

    function createComps(source, prefix, screens) {
        var sourceCenterX = source.width / 2;
        var sourceCenterY = source.height / 2;
        var pixelAspect = source.pixelAspect || 1;
        var duration = source.duration || 1;
        var frameRate = source.frameRate || 25;
        var report = [];
        var masterName = prefix + "_MASTER_" + Math.round(source.width) + "x" + Math.round(source.height);

        app.beginUndoGroup("AE 大屏拆分工具");

        var masterComp = app.project.items.addComp(masterName, source.width, source.height, pixelAspect, duration, frameRate);

        for (var i = 0; i < screens.length; i++) {
            var s = screens[i];
            var order = padIndex(i + 1, screens.length);
            var compName = order + "_" + s.name + "_" + Math.round(s.width) + "x" + Math.round(s.height);
            var comp = app.project.items.addComp(compName, s.width, s.height, pixelAspect, duration, frameRate);
            var layer = comp.layers.add(source);

            layer.property("Anchor Point").setValue([sourceCenterX, sourceCenterY]);
            layer.property("Position").setValue([sourceCenterX - s.x, sourceCenterY - s.y]);
            layer.property("Scale").setValue([100, 100]);

            var masterLayer = masterComp.layers.add(comp);
            masterLayer.name = compName;
            masterLayer.property("Anchor Point").setValue([s.width / 2, s.height / 2]);
            masterLayer.property("Position").setValue([s.x + s.width / 2, s.y + s.height / 2]);
            masterLayer.property("Scale").setValue([100, 100]);
            masterLayer.moveToEnd();

            report.push(
                compName +
                "\n  合成尺寸: " + s.width + " x " + s.height +
                "\n  锚点: " + sourceCenterX + ", " + sourceCenterY +
                "\n  位置: " + (sourceCenterX - s.x) + ", " + (sourceCenterY - s.y) +
                "\n  缩放: 100%, 100%"
            );
        }

        app.endUndoGroup();

        alert("已创建 " + screens.length + " 个分屏合成和 1 个总合成：\n\n" + masterName + "\n\n" + report.join("\n\n"));
    }

    try {
        var source = getSelectedSource();
        var win = makeUi(source);
        if (win.show() !== 1 || !win.result) {
            return;
        }

        validateScreens(source, win.result.screens);
        createComps(source, win.result.prefix, win.result.screens);
    } catch (err) {
        alert("AE 大屏拆分工具：\n" + err.message);
    }
})();
