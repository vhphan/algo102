// Side bar functions

// tree views
$(function () {
    $.fn.extend({
        treed: function (o) {

            var openedClass = 'fa-folder-open';
            var closedClass = 'fa-folder-close';

            if (typeof o != 'undefined') {
                if (typeof o.openedClass != 'undefined') {
                    openedClass = o.openedClass;
                }
                if (typeof o.closedClass != 'undefined') {
                    closedClass = o.closedClass;
                }
            }

            //initialize each of the top levels
            var tree = $(this);
            tree.addClass('tree');
            tree.find('li').has('ul').each(function () {
                var branch = $(this); //li with children ul
                branch.prepend('<i class=\'indicator fas ' + closedClass + '\'></i>');
                branch.addClass('branch');
                branch.on('click', function (e) {
                    if (this == e.target) {
                        var icon = $(this).children('i:first');
                        icon.toggleClass(openedClass + ' ' + closedClass);
                        $(this).children().children().toggle();
                    }
                });
                branch.children().children().toggle();
            });
            //fire event from the dynamically added icon
            tree.find('.branch .indicator').each(function () {
                $(this).on('click', function () {
                    $(this).closest('li').click();
                });
            });
            //fire event to open branch if the li contains an anchor instead of text
            tree.find('.branch>a').each(function () {
                $(this).on('click', function (e) {
                    $(this).closest('li').click();
                    e.preventDefault();
                });
            });
            //fire event to open branch if the li contains a button instead of text
            tree.find('.branch>button').each(function () {
                $(this).on('click', function (e) {
                    $(this).closest('li').click();
                    e.preventDefault();
                });
            });
        }
    });

//Initialization of treeviews

// $('#tree1').treed();

    $('#tree2').treed({openedClass: 'fa-folder-open', closedClass: 'fa-folder-close'});

// $('#tree3').treed({openedClass:'fa-chevron-right', closedClass:'fa-chevron-down'});
});

$(function () {
    var tree = document.querySelectorAll('ul.tree a:not(:last-child)');
    for (var i = 0; i < tree.length; i++) {
        tree[i].addEventListener('click', function (e) {
            var parent = e.target.parentElement;
            var classList = parent.classList;
            if (classList.contains('open')) {
                classList.remove('open');
                var opensubs = parent.querySelectorAll(':scope .open');
                for (var i = 0; i < opensubs.length; i++) {
                    opensubs[i].classList.remove('open');
                }
            } else {
                classList.add('open');
            }
        });
    }
});
// end of tree views

// add style to selected links and update the header
$(function () {
    $('#sidebar a').click(function (e) {
        e.preventDefault();
        document.location.hash = this.id;
        if ($(this).parent().has('ul').length === 0) {
            $('#sidebar a').removeClass('active');
            $(this).addClass('active');
        }
        $('#current-page').html($(this).html());
    });
});
// end of add style

// End of Side bar functions


function clearContent() {

    let contentDiv = document.getElementById('selectedContent');
    while (contentDiv.firstChild) {
        contentDiv.removeChild(contentDiv.firstChild);
    }

}

function showSnackbar(message) {
    var x = document.getElementById("snackbar");
    x.innerHTML = '<p>' + message + '</p>';
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
}





