(() => {
  document.getElementById("hover-container").onmousemove = event => {
    for (const frame of document.getElementsByClassName("hover-frame")) {
      const rect = frame.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top

      frame.style.setProperty("--mouse-x", `${x}px`)
      frame.style.setProperty("--mouse-y", `${y}px`)
    }
  }
})()

const syncFrameSize = () => {
  for (const frame of document.getElementsByClassName('hover-frame')) {
    const content = frame.querySelector('.hover-content').children[0]
    const sizeHolder = frame.querySelector('.hover-frame-size');
    sizeHolder.style.width = `${content.offsetWidth}px`;
    sizeHolder.style.height = `${content.offsetHeight}px`;
  }
}

window.addEventListener('load', syncFrameSize);
window.addEventListener('resize', syncFrameSize);
