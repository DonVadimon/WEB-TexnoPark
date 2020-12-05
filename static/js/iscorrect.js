$('.js-correct').click(function (ev) {
    ev.preventDefault();

    let ansid = $(this).data('ansid');

    console.log('HERE');

    console.log(ansid);

    $.ajax(
        '/iscorrect/',
        {
            method: 'POST',
            data: {
                ansid: ansid,
            },
        }).done((data) => {
            console.log(data);

            if (data.is_anonymous) {
                if (window.location.search === '') {
                    window.location = window.location.origin + '/login/?next=' + window.location.pathname;
                } else {
                    window.location = window.location.origin + '/login/' + window.location.search + '?next=' + window.location.pathname;
                }
            }

            ansid = '#ans' + ansid;
            $(ansid).toggleClass('correct');
            $(this).prop('checked', data.is_correct)
        });
});