console.log('first prefunction');
$(document).ready(function() {
    console.log('first hello');
    var new_post = $(".submit");
    new_post.on("click", function(e) {
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
                console.log(href);
            }

        });
    });
}
);




// $(document).ready(function(){
//     var deleters = $(".delete");
//     deleters.on("click", function(){
//         // send ajax request to delete this expense
//         $.ajax({
//             url: 'delete/' + $(this).attr("data"),
//             data: {
//                 "item": "some name",
//                 "paid_to": "some company"
//             }
//             success: function(){
//                 console.log("deleted");
//             }
//         });        
//         // fade out expense
//         this_row = $(this.parentNode.parentNode);
//         // delete the containing row
//         this_row.animate({
//             opacity: 0
//         }, 500, function(){
//             $(this).remove();
//         })
//     });
// });