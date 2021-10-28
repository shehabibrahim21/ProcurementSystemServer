var value_table = 0 

$('#myModal').modal({
    backdrop: 'static',
    keyboard: false
  });

  $("#table tr").click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');    
    var value_table =$(this).find('td:first').html();
    alert(value_table);
 });
 
 $('.ok').on('click', function(e){
     alert($("#table tr.selected td:first").html());
 });

