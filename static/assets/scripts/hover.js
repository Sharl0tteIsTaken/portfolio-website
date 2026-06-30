document.getElementById("hover-container").onmousemove = e => {
  for (const frame of document.getElementsByClassName("hover-frame")) {
    const rect = frame.getBoundingClientRect(),
          x = e.clientX - rect.left,
          y = e.clientY - rect.top;

    frame.style.setProperty("--mouse-x", `${x}px`);
    frame.style.setProperty("--mouse-y", `${y}px`);
  };
}

function syncFrameSize() {
  for (const frame of document.getElementsByClassName('hover-frame')) {
    const content = frame.querySelector('.hover-content').children[0]
    const sizeHolder = frame.querySelector('.hover-frame-size');
    sizeHolder.style.width = `${content.offsetWidth}px`;
    sizeHolder.style.height = `${content.offsetHeight}px`;
  }
}

window.addEventListener('load', syncFrameSize);
window.addEventListener('resize', syncFrameSize);
