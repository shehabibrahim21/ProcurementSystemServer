

$('#myModal').modal({
    backdrop: 'static',
    keyboard: false
  });


  $("#table tr").click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');    
    var value_table =$(this).find('td:first').html();

 });
 
 $('.ok').on('click', function(e){
     alert($("#table tr.selected td:first").html());
 });

 function createPPMP() {
   alert('aw')
  return "<a href= {% url 'PPMP:ppmp' parameter" + value_table + "%}" ;
}