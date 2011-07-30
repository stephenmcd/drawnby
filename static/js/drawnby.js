$(function() {

    var canvas = $('#canvas');
    var context = document.getElementById('canvas').getContext('2d');
    context.width = canvas.width();
    context.height = canvas.height();
    context.lineCap = 'round';
    context.lineJoin = 'round';

});
