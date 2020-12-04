$('.js-vote').click(function (ev) {
    ev.preventDefault();

    console.log('VOTES HERE');

    let $this = $(this);
    let opinion = $this.data('opinion');
    let objid = $this.data('objid');
    let objtype = $this.data('objtype');
    let url = ''
    if (objtype == 'question') {
        url = '/question/' + objid + '/vote/';
    } else if (objtype == 'answer') {
        url = '/answervote/';
    }
    $.ajax(
        url,
        {
            method: 'POST',
            data: {
                opinion: opinion,
                obj_id: objid,
            },
        }).done((data) => {
            if (data.is_anonymous) {
                if (window.location.search === '') {
                    window.location = window.location.origin + '/login/?next=' + window.location.pathname;
                } else {
                    window.location = window.location.origin + '/login/' + window.location.search + '?next=' + window.location.pathname;
                }
            }
            if (!data.is_voted) {
                console.error('Wrong vote parameter, choose between like and dislike');
            }
            let likeid = '#' + objtype + 'like' + objid;
            let dislikeid = '#' + objtype + 'dislike' + objid;
            let scoreid = '#' + objtype + 'score' + objid;

            if (data.vote > 0) { //like
                $(likeid).addClass('btn-info');
                $(likeid).removeClass('btn-outline-info');
                $(dislikeid).addClass('btn-outline-danger');
                $(dislikeid).removeClass('btn-danger');
            }
            else if (data.vote < 0) { //dislike
                $(likeid).addClass('btn-outline-info');
                $(likeid).removeClass('btn-info');
                $(dislikeid).addClass('btn-danger');
                $(dislikeid).removeClass('btn-outline-danger');
            }
            else if (data.vote == 0) { //novote
                $(likeid).addClass('btn-outline-info');
                $(likeid).removeClass('btn-info');
                $(dislikeid).addClass('btn-outline-danger');
                $(dislikeid).removeClass('btn-danger');
            }

            $(scoreid).text(data.new_obj_score)

            console.log(data);
        });
    console.log('HERE: ' + opinion);
});