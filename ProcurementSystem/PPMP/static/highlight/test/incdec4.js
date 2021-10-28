function increaseValue1() {
    var value = parseInt(document.getElementById('number11').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number11').value = value;
    document.getElementById('result1').value = amount.toFixed(2);

    var total1 = parseInt(document.getElementById('result1').value, 10);
    

    document.getElementById('total').value = total1;
  }
  
  function decreaseValue1() {
    var value = parseInt(document.getElementById('number11').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    amount = value * price
    document.getElementById('number11').value = value;
    document.getElementById('result1').value = amount.toFixed(2);
  }







  function increaseValue2() {
    var value = parseInt(document.getElementById('number22').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number22').value = value;
    document.getElementById('result2').value = amount.toFixed(2);
  }
  
  function decreaseValue2() {
    var value = parseInt(document.getElementById('number22').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    amount = value * price
    document.getElementById('number22').value = value;
    document.getElementById('result2').value = amount.toFixed(2);
  }








  function increaseValue3() {
    var value = parseInt(document.getElementById('number33').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number33').value = value;
    document.getElementById('result3').value = amount.toFixed(2);
  }
  
  function decreaseValue3() {
    var value = parseInt(document.getElementById('number33').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    amount = value * price
    document.getElementById('number33').value = value;
    document.getElementById('result3').value = amount.toFixed(2);
  }






  function increaseValue4() {
    var value = parseInt(document.getElementById('number44').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number44').value = value;
    document.getElementById('result4').value = amount.toFixed(2);
  }
  
  function decreaseValue4() {
    var value = parseInt(document.getElementById('number44').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    amount = value * price
    document.getElementById('number44').value = value;
    document.getElementById('result4').value = amount.toFixed(2);
  }
