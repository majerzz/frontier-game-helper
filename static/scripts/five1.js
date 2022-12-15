var button = document.getElementById("radio-1"),
value = button.form.radio1.value;
button.onclick = function() {
    alert(button.form.radio1.value);
}