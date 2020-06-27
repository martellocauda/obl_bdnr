$(function() {
    $('.links').click(function() {
	$('.active').attr('class', 'links');
        $(this).attr('class', 'links active');
    });
});

$(function() {
    $('#feed_btn').click(function() {
	$('#notimplementedcontainer').attr('class', 'container_not_active');
	$('#searchcontainer').attr('class', 'container_not_active');
	$('#searchescontainer').attr('class', 'container_not_active');
        $('#feedscontainer').attr('class', 'container_active');
    });
});

$(function() {
    $('#search_btn').click(function() {
	$('#notimplementedcontainer').attr('class', 'container_not_active');
        $('#feedscontainer').attr('class', 'container_not_active');
	$('#searchcontainer').attr('class', 'container_active');
	$('#searchescontainer').attr('class', 'container_active');
    });
});

$(function() {
    $('.notimplemented_btn').click(function() {
	$('#searchcontainer').attr('class', 'container_not_active');
	$('#searchescontainer').attr('class', 'container_not_active');
	$('#feedscontainer').attr('class', 'container_not_active');
        $('#notimplementedcontainer').attr('class', 'container_active');
    });
});

