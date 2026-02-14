let index = 0, interval = 2500;

const rand = (min, max) => 
  Math.floor(Math.random() * (max - min + 1)) + min;

const animate = star => {
  star.style.setProperty("--star-horizontal", `${rand(-10, 100)}%`);
  star.style.setProperty("--star-vertical", `${rand(-40, 80)}%`);
  const img = star.querySelector("img");
  img.src = sources[Math.floor(sources.length * Math.random())]
  // TODO: get this to save, not request(get) everytime.
  star.style.animation = "none";
  star.offsetHeight;
  star.style.animation = "";
}

const sources = [
  "../static/assets/svg/magic-star.svg",
  "../static/assets/svg/magic-cross.svg",
];

window.addEventListener('load', () => {
  for(const star of document.getElementsByClassName("magic-star")) {
    setTimeout(() => {
      animate(star);
      setInterval(() => animate(star), interval);
    }, index++ * (interval / 1.75))
  }
});
