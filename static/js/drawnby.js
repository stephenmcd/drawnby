$(function() {

    var canvas = $('#canvas');
    var context = document.getElementById('canvas').getContext('2d');
    context.width = canvas.width();
    context.height = canvas.height();
    context.lineCap = 'round';
    context.lineJoin = 'round';
    drawing = false;
    actions = {};

    actions.mousedown = function(x, y, username, userID) {
        context.beginPath();
        context.moveTo(x, y);
    };

    actions.mousemove = function(x, y, username, userID) {
        context.lineTo(x, y);
        context.stroke();
    };

    actions.join = function(username, userID) {
        if ($('#user-' + userID).length == 0) {
            $('#users').append('<li id="user-' + userID + '">' +
                               '<img src="' + window.MEDIA_URL + 'photos/' + userID + '.20x20_q85_crop-smart.jpg">' +
                               username + '</li>');
        }
    };

    actions.leave = function(username, userID) {
        if (userID != window.userID) {
            $('#user-' + userID).remove();
        }
    };

    var action = function(args) {
        while (args.length > 0) {
            if (args.shift() == window.drawingID) {
                var action = actions[args.shift()];
                var argLength = action.prototype.constructor.length;
                action.apply(null, args.slice(0, argLength));
                args = args.slice(argLength);
            }
        }
    };

    var getCoords = function(event) {
        var offset = canvas.offset();
        return {x: event.pageX - offset.left, y: event.pageY - offset.top};
    };

    var socket = new io.Socket();
    socket.connect();
    socket.on('connect', function() {
        send('join');
    });
    $(window).unload(function() {
        send('leave');
    });
    socket.on('message', function(args) {
        console.log(args)
        action(args);
    });

    var send = function() {
        var getArgs = function(args) {
            args = $.makeArray(args);
            args.unshift(window.drawingID);
            args.push(window.username, window.userID);
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
