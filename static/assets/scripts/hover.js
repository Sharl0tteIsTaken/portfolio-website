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
  for(frame of document.getElementsByClassName('hover-frame')) {
    var totalWidth = 0, maxHeight = 0;
    var content = frame.querySelector('.hover-content').children

    for (var i = 0; i < content.length; i++) {
      totalWidth += parseInt(content[i].offsetWidth, 0);
      maxHeight = Math.max(maxHeight, content[i].offsetHeight);
    }
    // FIXME: calculated size are wrong when the dropdown content is `show`

    const sizer = frame.querySelector('.hover-frame-size');
    sizer.style.width = `${totalWidth}px`;
    sizer.style.height = `${maxHeight}px`;
  };
};
window.addEventListener('load', syncFrameSize);
window.addEventListener('resize', syncFrameSize);
