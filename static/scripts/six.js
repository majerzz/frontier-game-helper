var button = document.getElementById("time"),
value = button.form.checkbox1.value;
button.onclick = function() {
	const list = document.getElementsByName("checkbox1")
	const outputList = []
	
	for (const hv of list.values()) {
		if (hv.checked) outputList.push(hv.value)
	}
	
	const outString = outputList.join(" ")
    alert(outString);

}