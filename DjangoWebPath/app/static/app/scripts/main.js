////////////////////////////////////////////////////////////////////////////////
// Global Variables
var stories;                                                                        //stores all the stories
var sTitle;                                                                         //stores title element

//new story
var newStory;                                                                       //stores new story
var prevPieces;
var presentId;
var presentChoice;
var nextId;

function loadCreation() {
    newStory = {
        "title": "",
        "pieces": []
    };
    prevPieces = []
    presentId = 0;
    nextId = 0;
    autosize($('.create-story .story-title'));                                      //enable text area auto size
    $("#create-save").click(saveStory);
    loadCreatePiece();
}

function saveStory() {
    newStory.title = $(".create-story .story-title").val();
    $.ajax({
        url:base_url+"/api/story",
        type:"POST",
        data: JSON.stringify(newStory),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        statusCode: {
            201: function (response) {
                window.location.replace(base_url);
            }
        }
    });
}

function loadCreatePiece() {
    $.get(base_url+"/template/createPiece", function (data) {                               //load html
        createPieceHTML = $(data).appendTo(".create-pieces");                       //append html
        createPieceHTML.find(".dropdown-menu").on('click', 'a', function () {
            var pieceType = Number($(this).attr("piecetype"));
            createSelectType(createPieceHTML, pieceType);
            createPieceHTML.find('.dropdown-toggle').html($(this).text() + '<span class="caret"></span>');
            createPieceHTML.find('.create-ok').off('click');
            createPieceHTML.find('.create-ok').on('click',
                function () { addStoryPiece(createPieceHTML, pieceType); });
        });
    });
}

function createSelectType(createPiece, selectedType) {
    switch (selectedType) {
        case 0:
            loadCreateEvent(createPiece);
            break;
        case 1:
            loadCreateChoices(createPiece);
            break;
        case 2:
            loadCreateLoss(createPiece);
            break;
        case 3:
            loadCreateWin(createPiece);
            break;
    }
}

function loadCreateEvent(createPiece) {
    createPiece.find(".create-piece-middle").load(base_url+"/template/createEvent", function () {
        autosize($(this).find(".create-event"));
        checkCreateInput($(this), 0);
        $(this).on('keyup', '.create-event', (function () { checkCreateInput($(this), 0) }));
    });
}

function loadCreateLoss(createPiece) {
    createPiece.find(".create-piece-middle").load(base_url+"/template/createFinal", function () {
        autosize($(this).find(".create-final"));
        $(this).find(".create-final").addClass("event-lose");
        checkCreateInput($(this), 2);
        $(this).on('keyup', '.create-final', (function () { checkCreateInput($(this), 0) }));
    });
}

function loadCreateWin(createPiece) {
    createPiece.find(".create-piece-middle").load(base_url+"/template/createFinal", function () {
        autosize($(this).find(".create-final"));
        $(this).find(".create-final").addClass("event-win");
        checkCreateInput($(this), 3);
        $(this).on('keyup', '.create-final', (function () { checkCreateInput($(this), 0) }));
    });
}

function loadCreateChoices(createPiece) {
    var mid = createPiece.find(".create-piece-middle");
    mid.load(base_url+"/template/createChoices", function () {
        appendCreateChoice(mid.find('.choices'));
        mid.find('.create-choice-more').on('click',
                function () { appendCreateChoice(mid.find('.choices')) });
        mid.find('.create-choice-less').on('click',
                function () { removeCreateChoice(mid.find('.choices')) });
    });
}

function appendCreateChoice(elem) {
    var nChoices = elem.children().length;
    if (nChoices+1 <= 3) {
        $.get(base_url+"/template/createChoice", function (data) {                      //load html
            var choiceHTML = $(data).appendTo(elem);                                //append html
            choiceHTML.addClass("choice-" + nChoices);
            autosize(choiceHTML);
            checkCreateInput(choiceHTML, 1);
            choiceHTML.on('keyup',
                (function () { checkCreateInput($(this), 1); }));

            if (nChoices + 1 == 2)
                elem.parent().find(".create-choice-less").prop('disabled', false);           //disabled false for -
            if (nChoices + 1 == 3)
                elem.parent().find(".create-choice-more").prop('disabled', true);            //disabled true for +
        });
    }
}

function removeCreateChoice(elem) {
    var nChoices = elem.children().length;
    if (nChoices > 1) {
        elem.find(":last-child").remove();

        if (nChoices - 1 == 1)
            elem.parent().find(".create-choice-less").prop('disabled', true);                //disabled true for -
        if (nChoices - 1 == 2)
            elem.parent().find(".create-choice-more").prop('disabled', false);                //disabled false for +
    }
}

function addStoryPiece(elem, pieceType) {
    switch (pieceType) {
        case 0:
            addStoryEvent(elem);
            break;
        case 1:
            addChoicesEvent(elem);
            break;
        case 2:
            addStoryFinal(elem, 2);
            break;
        case 3:
            addStoryFinal(elem, 3);
            break;
    }
    elem.find(".select-piece-type .btn").prop('disabled', true);
    elem.find(".create-ok").prop('disabled', true);
}

function addStoryEvent(elem) {
    var id = nextId;
    var json = {
        "pId": id,
        "text": elem.find(".create-piece-middle .create-event").val(),
        "next": null,
        "type": 0
    };
    elem.find(".create-piece-middle .create-event").prop('readonly', true);
    elem.data("json", json);
    prevPieces.push(json);
    newStory.pieces[id] = json;
    nextId = presentId + 1
    newStory.pieces[id].next = nextId;
    presentId++;
    loadCreatePiece();
}

function addStoryFinal(elem,pieceType) {
    var id = nextId;
    var json = {
        "pId": id,
        "text": elem.find(".create-piece-middle .create-final").val(),
        "type": pieceType
    };
    elem.find(".create-piece-middle .create-final").prop('readonly', true);
    elem.data("json", json);
    prevPieces.push(json);
    newStory.pieces[id] = json;
    nextId = presentId + 1
    newStory.pieces[id].next = nextId;
    presentId++;
}

function addChoicesEvent(elem) {
    var id = nextId;
    var choices = []
    elem.find(".choices").children().each(function (index) {
        choices.push({
            "text": $(this).val(),
            "next": null
        });
        $(this).prop('readonly', true);
        $(this).on("dblclick", function () { selectCreateChoice($(this), id, index); });
    });
    elem.find(".create-choice-quantity").empty();
    var json = {
        "pId": id,
        "choices": choices,
        "type": 1
    };
    elem.data("json", json);
    prevPieces.push(json);
    newStory.pieces[id] = json;
    presentChoice = 0;
    nextId = presentId + 1;
    newStory.pieces[id].choices[presentChoice].next = nextId;
    presentId++;
    loadCreatePiece();
}

function selectCreateChoice(elem, p, choiceIndex) {
    elem.parents(".create-piece").nextAll().remove();
    if (newStory.pieces[p].choices[choiceIndex].next == null) {
        nextId = presentId + 1;
        presentId++;
        newStory.pieces[p].choices[choiceIndex].next = nextId;
        loadCreatePiece();
    } else {
        reloadPath(p, choiceIndex);
    }
}

function reloadPath(p, choiceIndex) {
    var nextP;
    if (newStory.pieces[p].type == 0) {
        nextP = newStory.pieces[p].next;
    } else if (newStory.pieces[p].type == 1) {
        nextP = newStory.pieces[p].choices[choiceIndex].next;
    }

    if (nextP != null) {
        var createPieceHTML;

        $.get(base_url+"/template/createPiece", function (data) {                               //load html
            createPieceHTML = $(data).appendTo(".create-pieces");                       //append html
            createPieceHTML.find(".dropdown-menu").on('click', 'a', function () {
                var pieceType = Number($(this).attr("piecetype"));
                createSelectType(createPieceHTML, pieceType);
                createPieceHTML.find('.dropdown-toggle').html($(this).text() + '<span class="caret"></span>');
                createPieceHTML.find('.create-ok').on('click',
                    function () { addStoryPiece(createPieceHTML, pieceType); });
            });
            if (newStory.pieces[nextP] != undefined) {
                createPieceHTML.find(".select-piece-type .btn").prop('disabled', true);

                if (newStory.pieces[nextP].type == 1) {
                    var mid = createPieceHTML.find(".create-piece-middle");
                    mid.load(base_url+"/template/createChoices", function () {
                        mid.find('.create-choice-more').on('click',
                                function () { appendCreateChoice(mid.find('.choices')) });
                        mid.find('.create-choice-less').on('click',
                                function () { removeCreateChoice(mid.find('.choices')) });
                        $.each(newStory.pieces[nextP].choices, function (index) {
                            var choiceJson = this;
                            $.get(base_url+"/template/createChoice", function (data) {                      //load html
                                var elem = mid.find('.choices');
                                var choiceHTML = $(data).appendTo(elem);                                //append html
                                choiceHTML.addClass("choice-" + index);
                                autosize(choiceHTML);
                                choiceHTML.on("dblclick", function () { selectCreateChoice(choiceHTML, nextP, index); });
                                if (newStory.pieces[nextP].next != null) {
                                    checkCreateInput(choiceHTML, 1);                                    
                                    choiceHTML.on('keyup',
                                        (function () { checkCreateInput($(this), 1); }));

                                    if (index + 1 == 2)
                                        elem.parent().find(".create-choice-less").prop('disabled', false);           //disabled false for -
                                    if (index + 1 == 3)
                                        elem.parent().find(".create-choice-more").prop('disabled', true);            //disabled true for +
                                } else {
                                    choiceHTML.prop('readonly', true);
                                    elem.parent().find(".create-choice-quantity").empty();
                                }

                                choiceHTML.text(choiceJson.text);
                            });
                        });
                    });
                } else {
                    createPieceHTML.find(".create-piece-middle").load(base_url+"/template/createEvent", function () {
                        autosize($(this).find(".create-event"));
                        checkCreateInput($(this), 0);
                        $(this).on('keyup', '.create-event', (function () { checkCreateInput($(this), 0) }));                            
                        $(this).find(".create-event").text(newStory.pieces[nextP].text);

                        if (newStory.pieces[nextP].type == 2) {                                            //if it's a lose event
                            $(this).find(".create-event").addClass("event-lose");                //add event-lose class
                        } else if (newStory.pieces[nextP].type == 3) {                                     //if it's a win event
                            $(this).find(".create-event").addClass("event-win");                 //add event-win class
                        }

                        $(this).find(".create-event").prop('readonly', true);
                        $(this).find(".create-event").prop('readonly', true);
                    });
                }
                reloadPath(nextP, 0);
            } else {
                nextId = nextP;
            }
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
        sTitle.data("index", choice.data("choice").next);                          //update de index of the piece to 
        loadNextPiece();                                                           //load next piece (of the selected choice)
    });
}

////////////////////////////////////////////////////////////////////////////////
// Load JSON and its processment









////////////////////////////////////////////////////////////////////////////////
// General Functions

function checkCreateInput(inp, pieceType) {
    var regex;
    if (pieceType == 1) {
        regex = new RegExp("^[\\w \\-\\.\\,\\?\\!\\:\\;\\n]{5,100}$");
    } else {
        regex = new RegExp("^[\\w \\-\\.\\,\\?\\!\\:\\;\\n]{5,200}$");
    }
    
    var checkAll = true;
    if (pieceType == 1) {
        $.when(inp.parent().children().each(function () {
            var newLines = $(this).val().split("\n").length;
            var check = regex.test($(this).val()) && newLines <= 5;
            if (!check) {                                                        //event text check
                $(this).addClass("form-control-danger");
            } else {
                $(this).removeClass("form-control-danger");
            }
            checkAll = checkAll && check;
        })).then(function () {
            if (!checkAll) {
                inp.parents(".create-piece").find(".create-ok").prop('disabled', true);
            } else {
                inp.parents(".create-piece").find(".create-ok").prop('disabled', false);
            }
        });
    } else {
        var newLines = inp.val().split("\n").length;
        var check = regex.test(inp.val()) && newLines <= 5;
        if (!check) {                                                        //event text check
            inp.addClass("form-control-danger");
            inp.parents(".create-piece").find(".create-ok").prop('disabled', true);
        } else {
            inp.removeClass("form-control-danger");
            inp.parents(".create-piece").find(".create-ok").prop('disabled', false);
        }
    }
}

function scrollTo(elem) {                                                       //scroll to element (with animation)
    $("hetml, body").animate({
        scrollTop: elem.offset().top
    }, 300);
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});