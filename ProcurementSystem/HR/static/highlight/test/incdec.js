function increaseValue() {
    var value = parseInt(document.getElementById('number').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number').value = value;
    document.getElementById('number2').value = amount.toFixed(2);
  }
  
  function decreaseValue() {
    var value = parseInt(document.getElementById('number').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    amount = value * price
    document.getElementById('number').value = value;
    document.getElementById('number2').value = amount.toFixed(2);
  }