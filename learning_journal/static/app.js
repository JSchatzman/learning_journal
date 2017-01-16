$(document).ready(function() {
    console.log('first hello');
    // var new_post = $(".submit");
    // $(".submit").unbind("click");
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
                new_id = href[3];
                console.log(href);
                var new_html = '<h2>';
                new_html += ' <a href ="' + '/journal/' + new_id + '">' + title + '</a>';
                new_html += ' </h2>';
                new_html += ' <h3>';
                new_html += ' </h3>';
                new_html += ' <p class = "lead">by Jordan Schatzman</p>';
                new_html += ' <p>Posted on today blah</p>';
                new_html += ' <br/>';
                console.log(new_html);
            },
            // error: function(err){
            //    console.error(err);
            //    alert("This is a problem", err.message);

        });
    });

}
);



        // <h2>
        //     <a href = "{{ request.route_url('detail', id=entry.id) }}">{{ entry.title }}</a>
        // </h2>
        // <h3>
        // </h3>  
        // <p class = "lead">by Jordan Schatzman</p>
        // <p>Posted on {{entry.creation_date}}</p>
        // <br/>