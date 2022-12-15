var button = document.getElementById("radio-2"),
value = button.form.radio1.value;
button.onclick = function() {
    alert(button.form.radio1.value);
}