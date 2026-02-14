document.getElementById("hover-container").onmousemove = e => {
  for(const card of document.getElementsByClassName("hover-frame")) {
    const rect = card.getBoundingClientRect(),
          x = e.clientX - rect.left,
          y = e.clientY - rect.top;

    card.style.setProperty("--mouse-x", `${x}px`);
    card.style.setProperty("--mouse-y", `${y}px`);
  };
}

window.addEventListener('load', () => {
  for(frame of document.getElementsByClassName('hover-frame')) {
    var totalWidth = 0, maxHeight = 0;
    var content = frame.querySelector('.hover-content').children

    for (var i = 0; i < content.length; i++) {
      totalWidth += parseInt(content[i].offsetWidth, 0);
      maxHeight = Math.max(maxHeight, content[i].offsetHeight);
    }

    const sizer = frame.querySelector('.hover-frame-size');
    sizer.style.width = `${totalWidth}px`;
    sizer.style.height = `${maxHeight}px`;
  };
});
