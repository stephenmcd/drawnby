$(function() {

    // Set up the canvas context.
    var canvas = $('#canvas');
    var context = canvas.get()[0].getContext('2d');
    context.width = canvas.width();
    context.height = canvas.height();
    context.lineCap = 'round';
    context.lineJoin = 'round';

    var drawing = false; // Mousedown/drawing flag.
    var first = true; // First touch of the canvas flag.
    var dirty = false; // Flag to prompt for saving on exit.
    var color = [0,0,0]; // Current drawing rgb.
    var size = 1; // Current drawing size.

    // Stores actions that come through when the user is drawing,
    // to be called when drawing is complete.
    var queue = [];

    // Container that stores each of the actions so that they can
    // be referenced dynamically by name. Triggered client-side by
    // the current user, or from the server via Socket.IO for all
    // other users for this drawing.
    var actions = {

        // Start drawing.
        mousedown: function(x, y, r, g, b, size, username, userID) {
            context.lineWidth = size;
            context.strokeStyle = 'rgba(' + [r, g, b, 1].join(',') + ')';
            context.beginPath();
            context.moveTo(x, y);
        },

        // Draw.
        mousemove: function(x, y, r, g, b, size, username, userID) {
            context.lineWidth = size;
            context.strokeStyle = 'rgba(' + [r, g, b, 1].join(',') + ')';
            context.lineTo(x, y);
            context.stroke();
        },

        load: function(imageData) {
            img = new Image();
            var interval = setInterval(function() {
                if (img.complete) {
                    context.drawImage(img, 0, 0);
                    clearTimeout(interval);
                }
            }, 100);
            img.src = imageData;
        },

        // User joining - add their name to the user list.
        join: function(username, userID) {
            if ($('#user-' + userID).length == 0) {
                messages.add(username + ' has joined');
                data = {userID: userID, username: username};
                $('#user-template').tmpl(data).appendTo('#users');
                $('#user-' + userID + ' img').tooltip({offset: [-5, 0]});
            }
        },

        // User leaving - remove their name from the user list.
        leave: function(username, userID) {
            if (userID != window.userID) {
                messages.add(username + ' has left');
                $('#user-' + userID).remove();
            }
        }

    };

    // Takes an array of args that represent one or more actions to call.
    // First arg is always the drawing key as a guard to ensure actions are
    // only performed for the current drawing. Second arg is the act‭ion name
    // and the rest are args for that action. Since many sets of actions
    // can be sent from the server in one batch, we keep looping and test
    // for the argument length of the action being called, pulling the
    // required number of arguments off the list, until the entire list
    // is empty.
    var action = function(args) {
        while (args.length > 0) {
            if (args.shift() == window.drawingKey) {
                var action = actions[args.shift()];
                var argLength = action.prototype.constructor.length;
                action.apply(null, args.slice(0, argLength));
                args = args.slice(argLength);
            }
        }
    };

    // The main handler for actions triggered client-side.
    // First wrap the arguments with the drawing key and user vars,
    // perform the actual action client-side, and pass the action
    // and arguments off to the server via socket.io for broadcasting
    // to other users.
    var send = function() {
        var getArgs = function(args) {
            args = $.makeArray(args);
            args.unshift(window.drawingKey);
            args.push(window.username, window.userID);
            return args;
        };
        action(getArgs(arguments));
        socket.send(getArgs(arguments));
    };

    var save = function() {
        var title = prompt('Save as:');
        if (title) {
            messages.add('Sketch saved');
            socket.send([window.drawingKey, 'save', title,
                        canvas.get()[0].toDataURL('image/png')])
        }
        dirty = false;
    };

    // Socket.IO setup.
    var socket = new io.Socket();
    socket.connect();
    socket.on('connect', function() {
        send('join');
    });
    $(window).unload(function() {
        if (dirty && confirm('You have unsaved changed, would you like to save them?')) {
            save();
        }
        send('leave');
    });
    socket.on('message', function(args) {
        $('#loading').remove();
        if (drawing) {
            queue.push.apply(null, args);
        } else {
            action(args);
        }
    });

    // Cross-browser pixel offset.
    var getCoords = function(element, event) {
        var offset = $(element).offset();
        return {x: event.pageX - offset.left, y: event.pageY - offset.top};
    };

    // Stop drawing on mouseup and run any queued actions.
    canvas.mouseup(function() {
        drawing = false;
        if (queue.length > 0) {
            action(queue);
            queue = [];
        }
    });

    // Start drawing on mousedown.
    canvas.mousedown(function(event) {
        // Stops the cursor from reverting from the
        // custom cursor in Chrome.
        event.preventDefault();
        var coords = getCoords(this, event);
        drawing = true;
        send('mousedown', coords.x, coords.y,
                          color[0], color[1], color[2],
                          size, first);
        first = false;
        dirty = true;
    });

    // Draw on mousemove if drawing is currently on (eg mouse is down).
    canvas.mousemove(function(event) {
        if (drawing) {
            var coords = getCoords(this, event);
            send('mousemove', coords.x, coords.y,
                              color[0], color[1], color[2],
                              size);
        }
    });

    // Explict save.
    $('#save').click(save);

    // Brush size setup
    $('#size a').click(function() {
        size = (Number($(this).attr('id').split('size-')[1]) + 1) * 5;
        return false;
    });

    // Color picker.
    $(function() {
        $('#color').ColorPicker({onChange: function(hsb, hex, rgb) {
            color = [rgb.r, rgb.g, rgb.b];
            $('#color div').css({backgroundColor: '#' + hex});
		}});
    });

});
