$(document).ready(() => {
  const starTypes = ["cross", "star"]

  const rand = (min, max) => (Math.floor(Math.random() * (max - min + 1)) + min)

  const animate = (star) => {
    const $star = $(star)

    $star.css({
      "--effect-horizontal": `${rand(-10, 90)}%`,
      "--effect-vertical": `${rand(-10, 60)}%`,
      "animation": "scale 1250ms ease",
    })

    $star.removeClass(starTypes.join(" "))
         .addClass(starTypes[rand(0, starTypes.length - 1)])

    $star.one('animationend', () => {
      $star.css("animation", "none")
      setTimeout(() => animate(star), rand(1100, 2100))
    })
  }

  $(".magic-star").each(function() {
    setTimeout(() => animate(this), rand(200, 1000))
  })
})
