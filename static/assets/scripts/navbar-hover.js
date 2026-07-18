$(document).ready(() => {
  const frame = $('.hover-frame')

  $("#hover-container").on('mousemove', (event) => {
    frame.each(function() {
      const rect = this.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top

      // may have better performance than jQuery syntax
      this.style.setProperty("--mouse-x", `${x}px`)
      this.style.setProperty("--mouse-y", `${y}px`)
    })
  })

  const syncFrameSize = () => {
    frame.each(function() {
      const frame = $(this)
      const content = frame.find('.hover-content').children().first()
      const sizeHolder = frame.find('.hover-frame-size')

      sizeHolder.css({
        "width": `${content.outerWidth()}px`,
        "height": `${content.outerHeight()}px`,
      })
    })
  }

  syncFrameSize()
  $(window).on('resize', syncFrameSize)
})
