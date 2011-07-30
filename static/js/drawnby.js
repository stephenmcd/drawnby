$(function() {

    var canvas = $('#canvas');
    var context = document.getElementById('canvas').getContext('2d');
    context.width = canvas.width();
    context.height = canvas.height();
    context.lineCap = 'round';
    context.lineJoin = 'round';
    drawing = false;
    actions = {};

    actions.mousedown = function(x, y) {
        context.beginPath();
        context.moveTo(x, y);
    };

    actions.mousemove = function(x, y) {
        context.lineTo(x, y);
        context.stroke();
    };

    var action = function(args) {
        if (args.shift() == window.drawingID) {
            var action = actions[args.shift()];
            action.apply(null, args);
        }
    };

    var getCoords = function(event) {
        var offset = canvas.offset();
        return {x: event.pageX - offset.left, y: event.pageY - offset.top};
    };

    var socket = new io.Socket();
    socket.connect();
    socket.on('message', function(args) {
        action(args);
    });

    var send = function() {
        var getArgs = function(args) {
            args = $.makeArray(args);
            args.unshift(window.drawingID);
            return args;
        };
        action(getArgs(arguments));
        socket.send(getArgs(arguments));
    };

    canvas.mouseup(function() {
        drawing = false;
    });

    canvas.mousedown(function(event) {
        var coords = getCoords(event);
        drawing = true;
        send('mousedown', coords.x, coords.y);
    });

    canvas.mousemove(function(event) {
        if (drawing) {
            var coords = getCoords(event);
            send('mousemove', coords.x, coords.y);
        }
    });

});
