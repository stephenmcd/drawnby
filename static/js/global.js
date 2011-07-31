
var messages = {

    add: function(msg) {
        $('#message-template').tmpl({msg: msg}).appendTo('#messages');
        messages.show();
    },

    show: function() {
        $('.message').slideDown();
        clearTimeout(messages.timeout);
        messages.timeout = setTimeout(function() {
            $('.message').fadeOut();
        }, 5000);
    },

    timeout: null

};

$(function() {
    $('.message a').live('click', function() {
        $('.message').fadeOut();
        return false;
    });
    messages.show();
    $('#progress').chosen().change(function() {
        if (this.selectedIndex > 0) {
            location = this[this.selectedIndex].value + '?join';
        }
    });
    $('.stars a').mouseover(function() {
        var stars = $(this).parent().find('a');
        stars.addClass('star-off');
        stars.removeClass('star-on');
        for (var i = 0; i < stars.length; i++) {
            $(stars[i]).addClass('star-on');
            $(stars[i]).removeClass('star-off');
            if (stars[i] == this) {
                break;
            }
        }
    });
    $('.stars a').mouseout(function() {
        var stars = $(this).parent().find('a');
        stars.addClass('star-off');
        stars.removeClass('star-on');
        for (var i = 0; i < stars.length; i++) {
            $(stars[i]).addClass('star-on');
            $(stars[i]).removeClass('star-off');
            if ($(stars[i]).hasClass('actual')) {
                return;
            }
        }
        stars.addClass('star-off');
        stars.removeClass('star-on');
    });
});
