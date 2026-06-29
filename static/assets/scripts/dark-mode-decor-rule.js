function fillDecorRule() {
  const ruleWidth = document.body.offsetWidth;

  const sideUnit = 32;
  const midUnit = 40;
  const leftChar = "∼ · ";
  const midChar = "∼ • ∽";
  const rightChar = " · ∽";

  var sideWidth = (ruleWidth - midUnit) / 2;
  var count = Math.floor(sideWidth / sideUnit);

  for (decorRule of document.getElementsByClassName('decor-rule')) {
    decorRule.textContent = leftChar.repeat(count) + midChar + rightChar.repeat(count);
  };
}

window.addEventListener('load', fillDecorRule);
window.addEventListener('resize', fillDecorRule);
