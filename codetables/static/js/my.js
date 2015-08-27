	var lines = document.getElementById("divlines");
	var txtArea = document.getElementById("code_text");
	window.onload = function() {
	    refreshlines();
	    txtArea.onscroll = function () {
	        lines.style.top = -(txtArea.scrollTop) + "px";
	        return true;
	    }
	    txtArea.onkeyup = function () {
	        refreshlines();
	        return true;
	    }
	    txtArea.onkeydown = function(e){
	    	if(e.keyCode==9 || e.which==9){
	    	            e.preventDefault();
	    	            var s = this.selectionStart;
	    	            this.value = this.value.substring(0,this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
	    	            this.selectionEnd = s+1; 
	    }		
	}
}

	function refreshlines() {
	    var nLines = txtArea.value.split("\n").length;
	    lines.innerHTML = ""
	    for (i=1; i<=nLines; i++) {
	        lines.innerHTML = lines.innerHTML + i + "." + "<br />";
	    }
	    lines.style.top = -(txtArea.scrollTop) + "px";

	}
    function compile_and_run(){
    		var code_text = document.getElementById("code_text").value;
    		var user_input_check = document.getElementById("user_input").checked;
    		var user_input_value;
    		if(user_input_check)
    		{
    			user_input_value = document.getElementById("user_input_value").value;
    		}
    		var postForm = {
    			'code_text': code_text,
    			'user_input_value': user_input_value,
    			'check_uncheck': user_input_check,
    			csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    		}
    		$.ajax({
    			url: '/compile/',
    			type: 'POST',
    			data: postForm,
    			success: function(d) {
    				d = JSON.parse(d);
    		    	
    		    	create_output_or_error_div(d['output_code'], d['error_code'], d['time_taken'], d['compile_status'])
    	    	},
    	    	failure: function(d) { 	
    	    		alert('hi');
    	    	}
    		});}
    function create_output_or_error_div(output_code, error_code, time_taken, compile_status)
    {
    	var myNode = document.getElementById('code_error_output');
    	while (myNode.firstChild) {
    	    myNode.removeChild(myNode.firstChild);
    	}
		myNode.style.visibility = 'visible';
		if (compile_status != '')
    	{
    		l=document.createElement('label');
    		l.innerHTML="Compile Log";
    		l.id="compile_log";
    		document.getElementById('code_error_output').appendChild(l);	
    			
    		r=document.createElement('textarea');
    		r.id='compile_status';
    		r.rows='5';
    		r.cols='35';
    		r.value = compile_status;
    		r.style.backgroundColor = '#E67676';
    		r.style.color='white';
    		r.style.borderRadius='5px';
    		r.readOnly = true;
			document.getElementById('compile_log').appendChild(r);	
    	}
    	else
    	{
    		l=document.createElement('label');
    		l.innerHTML="Compile Log";
    		l.id="compile_log";
    		document.getElementById('code_error_output').appendChild(l);	
    			
    		r=document.createElement('textarea');
    		r.id='compile_status';
    		r.rows='1';
    		r.cols='35';
    		r.value = "Successful";
    		r.style.backgroundColor = 'green';
    		r.style.color='white';
    		r.style.borderRadius='5px';
    		r.readOnly = true;    		
    		document.getElementById('compile_log').appendChild(r);	
    		if(output_code != '')
    		{
    			l=document.createElement('label');
    			l.innerHTML="Output Code";
    			l.id="output_label";
    			document.getElementById('code_error_output').appendChild(l);	
    			r=document.createElement('textarea');
    			r.id='output_code';
    			r.rows='3';
    			r.cols='35';
    			r.value = output_code;
    			r.style.backgroundColor = '#F78828';
    			r.style.color='white';
    			r.style.borderRadius='5px';    		
    			r.readOnly = true;
    			document.getElementById('output_label').appendChild(r);    			
    		}
    		if(error_code != '')
    		{
    			l=document.createElement('label');
    			l.innerHTML="Error Code";
    			l.id="error_label";
    			document.getElementById('code_error_output').appendChild(l);	
    			r=document.createElement('textarea');
    			r.id='error_code';
    			r.rows='3';
    			r.cols='35';
    			r.value = error_code;
    			r.style.backgroundColor = '#E67676';
    			r.style.color='white';
    			r.style.borderRadius='5px';
    			r.readOnly = true;    		
    			document.getElementById('error_label').appendChild(r);    		
    		}
    			l=document.createElement('label');
    			l.innerHTML="Time Taken";
    			l.id="time_label";
    			document.getElementById('code_error_output').appendChild(l);	
    			r=document.createElement('div');
    			r.id='time_taken';
    			r.innerHTML = time_taken;
    			document.getElementById('time_label').appendChild(r);   

    	}
    }	
    function new_file(){
    	var code_text = document.getElementById("code_text").value;
    	var title = prompt("Please enter title to your file", "BubbleSorting");
    	var postForm = {
    		'code_text': code_text,
    		'title':title,
    		csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    	}
    	$.ajax({
    		url: '/save_file/',
    		type: 'POST',
    		data: postForm,
    		success: function(d) {
    			d= JSON.parse(d);
    			var confirm_check;
    			if(d['1'] == '3')
    			{
    				confirm_check = confirm('The file with same name exsist and if you wanna work on that code press OK')
    				if(confirm_check)
    				   	document.getElementById("code_text").value = d['2'];
    			}	
    			else
    				alert(d['2']);
    		},	
        	failure: function(d) { 	
        		alert('Ajax failed');
        	}
    	});}	
