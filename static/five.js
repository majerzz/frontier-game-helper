var button = document.getElementById("time"),
value = button.form.radio1.value;
button.onclick = function() {
    alert(button.form.radio1.value);
}