$('.bookmark_link').click(function(){
    $.ajax({
             type: 'POST',
             url:'{% url "post_detail" indiv_post.pk %}', 
             data: {'post_pk': $(this).attr('name'),'operation':'bookmark_update','csrfmiddlewaretoken': '{{ csrf_token }}'},
             dataType: "json",
             success: function(response) {
			  var bmkd=document.getElementById("bmk");
			  var icon = bmkd.querySelector('i');
                    if(response.bookmarked==true){
					   icon.classList.remove('bi-bookmark-plus-fill');
					   icon.classList.add('bi-bookmark-check-fill');
					  }
                    else if(response.bookmarked==false){
					  icon.classList.remove('bi-bookmark-check-fill');
					  icon.classList.add('bi-bookmark-plus-fill');
                    }


              }

        });

  })
