const input = document.querySelector("input");
const label = document.querySelector("h3");

input.addEventListener("input", event => {
  const value = Number(input.value);
  let arr = [value, " минут"];
  input.style.setProperty("--thumb-rotate", `${value * 720}deg`);
  label.innerHTML = arr.join('');
});

var button = document.getElementById("time"),
value = button.form.slider.value;