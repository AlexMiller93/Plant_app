$(document).ready(function(){
    $(".like").click(function(){
        $(this).toggleClass("heart");
        var pk = $(this).find('input[id="abc"]').val();
        var data = {
            'music_id': pk
            };
        $.ajax({
                type: 'POST',
                url: '../wishlist/',
                data: data,
                success: function(json) {
                    alert(json); // your actions after save, you can just pop-up some ui element that added to wishlist
                }
            })
    });
});