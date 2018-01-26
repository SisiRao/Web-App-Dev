
window.onload = function(){

	var prevInputIsNum = false
	var new_val = 0, 
		prev_value = 0,
    prev_oper = '+';
	var result = document.getElementById("result");
	var numelems = document.querySelectorAll(".number");
	//add onClick event to all number buttons
	for(var i = 0; i < numelems.length; i++ ) 
	{
		numelems[i].addEventListener("click",function() {
			prevInputIsNum = true;
	    	var num = +this.value; //The unary plus (+) coerces its operand into a number
	    	new_val = new_val * 10 + num;
	    	result.innerHTML = new_val;
	    	if(Math.abs(new_val)>1000000)
				alert("exceed limit!");
		});
	}
	
	//add onClick event to all operator buttons
	var operelems = document.querySelectorAll(".operator")
	for(var i = 0; i < operelems.length; i++ ) 
	{
		operelems[i].addEventListener("click",function(){
			if(prevInputIsNum)
			{
				switch(prev_oper){
					case '+':
						prev_value = prev_value + new_val;
						break;

					case '-':
						prev_value = prev_value - new_val;
						break;

					case '*':
						prev_value = prev_value * new_val;
						break;

					case '/':
						prev_value = Math.floor(prev_value / new_val);
						break;

					case '=':
						prev_value = new_val;
						break;

					default: 
						break;

				}
			}
			//update value
			prev_oper = this.value;
			result.innerHTML = prev_value;
			prevInputIsNum = false;
			
			if(Math.abs(prev_value)>1000000)
				alert("exceed limit!");

			new_val = 0

		})
	}

}
