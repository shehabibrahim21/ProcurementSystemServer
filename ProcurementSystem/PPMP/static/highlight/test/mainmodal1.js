$('#myModal').modal({
    backdrop: 'static',
    keyboard: false
  });

  $("#table tr").click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');    
    var value=$(this).find('td:first').html();
 });
 
 $('.ok').on('click', function(e){
     alert($("#table tr.selected td:first").html());
 });

 var url = $( '#selection-form' ).attr( 'action' );
$("selection-button").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: url,
        data: { 
            id: $('#company-list').val();, 
            },
        success: function(result) {
            alert('ok');
        },
        error: function(result) {
            alert('error');
        }
    });
});