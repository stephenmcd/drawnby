
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
            location = this[this.selectedIndex].value;
        }
    });
});
