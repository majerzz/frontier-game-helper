var button = document.getElementById("time"),
value = button.form.checkbox2.value;
button.onclick = function() {
	const list = document.getElementsByName("checkbox2")
	const outputList = []
	
	for (const hv of list.values()) {
		if (hv.checked) outputList.push(hv.value)
	}
	
	const outString = outputList.join(" ")
    alert(outString);

}