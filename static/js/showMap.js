$(document).ready(function (event) {
    $(document).on('click', '.list-group-item', function (event) {
        $.ajax({
            url: $(this).attr("data-ajax-target"),
            success: function (html) {
                $("#content").html(html);
            },
            failure: function (data) {
                alert('Got an error dude');
            }
        });
    })
})