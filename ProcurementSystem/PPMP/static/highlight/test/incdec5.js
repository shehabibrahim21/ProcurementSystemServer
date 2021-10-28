function increaseValue1() {
    var value = parseInt(document.getElementById('number11').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number11').value = value;
    document.getElementById('result1').value = amount.toFixed(2);

    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }        
    var total11 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total11.toFixed(2);
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

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }       
    var total22 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total22.toFixed(2);
  }







  function increaseValue2() {
    var value = parseInt(document.getElementById('number22').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number22').value = value;
    document.getElementById('result2').value = amount.toFixed(2);

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }       
    var total33 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total33.toFixed(2);
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

    
    var total1 = parseInt(document.getElementById('result1').value, 10);

    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    } 
    var total44 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total44.toFixed(2);
  }








  function increaseValue3() {
    var value = parseInt(document.getElementById('number33').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number33').value = value;
    document.getElementById('result3').value = amount.toFixed(2);

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }      
    var total55 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total55.toFixed(2);
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

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }      
    var total66 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total66.toFixed(2);
  }






  function increaseValue4() {
    var value = parseInt(document.getElementById('number44').value, 10);
    var price = parseInt(document.getElementById('number1').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    amount = value * price
    document.getElementById('number44').value = value;
    document.getElementById('result4').value = amount.toFixed(2);

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }      
    var total77 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total77.toFixed(2);

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

    
    var total1 = parseInt(document.getElementById('result1').value, 10);
    var total2 = parseInt(document.getElementById('result2').value, 10);
    var total3 = parseInt(document.getElementById('result3').value, 10);
    var total4 = parseInt(document.getElementById('result4').value, 10);
    if (isNaN(total1))
    {
        total1 = 0
    }   
    if (isNaN(total2))
    {
        total2 = 0
    } 
    if (isNaN(total3))
    {
        total3 = 0
    } 
    if (isNaN(total4))
    {
        total4 = 0
    }       
    var total88 = total1 + total2 + total3 + total4;
    document.getElementById('total').value = total88.toFixed(2);
  }
