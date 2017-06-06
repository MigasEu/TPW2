function append_piece(pieceId) {
    if (pieceId >= 0) {
        $.get(playStory_url + pieceId, function (data) {
            var eventHTML = $(data).appendTo("#story-body");
        });
    }
}

function selectChoice(event) {
    var choice = $(this);                                                           //choice element
    choice.prop('disabled', true);                                                  //disable selected
    choice.off();                                                                   //turn off event handler
    $.when($(this).parent(".col").siblings().each(function (index) {            //for each sibling
        $(this).find(".choice").prop('disabled', true);                             //disable choice
        $(this).fadeOut(800, function () { $(this).detach(); });                    //animation of other choices fading out
    })).then(function () {                                                      //after siblings are gone
        append_piece(choice.attr('next'));
    });
}