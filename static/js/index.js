$(function() {
    $('.advancedsearchbutton').click(function() {
    	if ($(".advancedsearchitem").hasClass("nondisplay")) {
		$('#hasadvancedsearch').prop('checked', true);
		$('#hasadvancedsearch').prop('enabled', false);
        	$('.advancedsearchitem').attr('class', 'advancedsearchitem');
		$('.advancedsearchtext').attr('class', 'advancedsearchtext');
	    } else {
		$('#hasadvancedsearch').prop('checked', false);
		$('#hasadvancedsearch').prop('enabled', true);
        	$('.advancedsearchitem').attr('class', 'advancedsearchitem nondisplay');
		$('.advancedsearchtext').attr('class', 'advancedsearchtext nondisplay');
	    }
    });
});

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

$(document).ready( function() {
    $('#endDate').val(new Date().toDateInputValue());
});
