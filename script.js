let car = document.getElementById("car");
let position = 125;

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft" && position > 0) {
    position -= 25;
  }
  if (e.key === "ArrowRight" && position < 250) {
    position += 25;
  }
  car.style.left = position + "px";
});

function startGame() {
  alert("Game Started! Use Arrow Keys ← →");
}