
   $(document).on("click", ".clickThis", function () {
     


     var string_ = $(this).data('id')
     var res = string_.split(",");
     var none_ = ""

    if (res[0] == null){
    $(".modal-title #generic").text(none_);
     }else{
    $(".modal-title #generic").text(res[0]);}

    if (res[1] == null){
    $(".modal-body #specs1").text(none_);
    }else{
    $(".modal-body #specs1").text(res[1]);}


    if (res[2] == null){
    $(".modal-body #specs2").text(none_);
  	}else{
    $(".modal-body #specs2").text(res[2]);}



    if (res[3] == null){
    $(".modal-body #specs3").text(none_);
     }else{
    $(".modal-body #specs3").text(res[3]);}


    if (res[4] == null){
    $(".modal-body #specs4").text(none_);
     }else{
    $(".modal-body #specs4").text(res[4]);}




    if (res[5] == null){
    $(".modal-body #specs5").text(none_);
     }else{
    $(".modal-body #specs5").text(res[5]);}


     
    });

    

$(document).ready(function(){
      $("#exampleModal").modal('show');
    });




$('.delete').on('click',function(){
  $('#DeleteModal').modal('hide');
  $("#frmStudent").submit();
});