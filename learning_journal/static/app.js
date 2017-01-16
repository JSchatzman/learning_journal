$(document).ready(function() {
    console.log('first hello');
    $(".submit").on("click", function(e) {
        console.log('hello');
        var title = $(this).parent().find("input[name='title']")[0].value;
        var body = $(this).parent().find("textarea[name='body']")[0].value;
        $.ajax({
            url: '/',
            type: "POST",
            data: {
                "csrf_token": $(this).parent().find("input[name='csrf_token']")[0].value,
                "title": title,
                "body": body
            },
            success: function(){
                var href = $('h2 a').attr('href').split('/').slice(1);
                var d = new Date().toISOString().slice(0,10);
                new_id = Number(href[3]) + 1;
                console.log(href);
                var new_html = '<h2>';
                new_html += ' <a href ="' + '/journal/' + new_id + '">' + title + '</a>';
                new_html += ' </h2>';
                new_html += ' <h3>';
                new_html += ' </h3>';
                new_html += ' <p class = "lead">by Jordan Schatzman</p>';
                new_html += ' <p>Posted on ' + d + '</p>';
                new_html += ' <br/>';
                $('#list').prepend(new_html);
                console.log(new_html);
            },
            error: function(err){
               console.error(err);
               alert("There was a problem", err.message);

        });
    });

}
);
