const starTypes = ["cross", "star"];

function rand (min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function animate(star) {
  star.style.setProperty("--effect-horizontal", `${rand(-10, 90)}%`);
  star.style.setProperty("--effect-vertical", `${rand(-10, 60)}%`);

  star.classList.remove(...starTypes);
  star.classList.add(starTypes[rand(0, starTypes.length - 1)]);
  star.style.animation = "scale 1250ms ease";

  star.addEventListener('animationend', () => {
    star.style.animation = "none";
    setTimeout(() => animate(star), rand(1100, 2100));
    }, { once: true }
  );
};

window.addEventListener('load', () => {
  for(const star of document.getElementsByClassName("magic-star")) {
    setTimeout(() => animate(star), rand(200, 1000));
  };
});
