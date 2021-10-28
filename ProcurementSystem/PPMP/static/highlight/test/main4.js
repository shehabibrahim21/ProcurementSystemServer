
   $(document).on("click", ".clickThis", function () {
     


     var string_ = $(this).data('id')
     var res = string_.split(",");
     var none_ = ""

 


     
    });

    

$(document).ready(function(){
      $("#exampleModal").modal('show');
    });




$('.delete').on('click',function(){
  $('#exampleModal').modal('hide');
  $("#confirmModal").modal('show');
});