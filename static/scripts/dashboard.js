// Create 'replaceAll' string function that replaces all 'search' string instances with 'replacement' string
String.prototype.replaceAll = function(search, replacement) {
    return this.replace(new RegExp(search, 'g'), replacement);
};

// On document ready
document.addEventListener("DOMContentLoaded", function(){
// $(function() {

	// Timeout 0 hack inside 'onready' event prevents some instructions from not working properly
	setTimeout(function() {

		// // Hide toolbar
		// $('.react-grid-Toolbar').hide();

		// // Show filter toolbar
		// $('.tools').children('.btn').click();

		// // Translate filter inputs placeholders
		// $('.form-control.input-sm').attr('placeholder', 'Pesquisar');

		// // Remove (extra) border from table container
		// $('.react-grid-Main').css({'outline-style': 'none'});

		// // Remove bottom border from table grid
		// $('.react-grid-Grid').css({'border-bottom-style': 'none'});

		// Export button function
		// $('#export-button').click(function() {
		// 	$.getJSON('2018.1_SA_ical.json', function(data) {
		// 		alert(1);
		// 		// var items = [];
		// 		// $.each(data, function(key, val) {
		// 		// 	items.push( "<li id='" + key + "'>" + val + "</li>" );
		// 		// });
		// 		// alert(data);
		// 		// $("<ul/>", {
		// 		// 	"class": "my-new-list",
		// 		// 	html: items.join( "" )
		// 		// }).appendTo( "body" );
		// 	});
		// 	// $.get('2018.1_SA_ical.json', function(data) {
		// 	// 	// alert(1);
		// 	// 	alert(data);
		// 	// 	// alert(2);
		// 	// }, 'text');
		// 	alert(0);
		// });
		
		// This function is intended to be called only when the page content is changed
		function bodyNodeInserted() {
			// Translate 'undo' and 'redo' buttons
			element = $('._dash-undo-redo div span');
		    if (element && element != null && element.length != 0)
		    	element.each(function() {
		    		child = $(this).children('div:nth-child(2)')
			    	if (child.html() === 'undo')
			        	child.html('desfazer');
			    	else if (child.html() === 'redo')
			        	child.html('refazer');
		    	});

			// Prevent infinite recursion due to string replace function activate 'DOMNodeInserted' event
		    $('body').off('DOMNodeInserted');

			// Correct '&lt' (less-than) and '&gt' (greater-than) HTML symbols with their equivalent chars ('<' and '>', respectively)
		    $('.react-grid-Cell__value div span div').each(function() {
				if (!$(this).children().length)
					$(this).html($(this).html()
						.replaceAll('&lt;', '<')
						.replaceAll('&gt;', '>'));
			});

			// Reactivate 'DOMNodeInserted' event after changes are made
		   	$('body').on('DOMNodeInserted', bodyNodeInserted);
		}
		// Call 'bodyNodeInserted' every time something is inserted in the DOM
		$('body').on('DOMNodeInserted', bodyNodeInserted);
		bodyNodeInserted();

	}, 100);

});
