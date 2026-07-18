$(document).ready(() => {
  const fillDecorRule = () => {
    const ruleWidth = $('body').outerWidth()

    const sideUnit = 32
    const midUnit = 40
    const leftChar = "∼ · "
    const midChar = "∼ • ∽"
    const rightChar = " · ∽"

    const sideWidth = (ruleWidth - midUnit) / 2
    const count = Math.floor(sideWidth / sideUnit)

    $('.decor-rule').text(leftChar.repeat(count) + midChar + rightChar.repeat(count))
  }

  fillDecorRule()
  $(window).on('resize', fillDecorRule)
})
