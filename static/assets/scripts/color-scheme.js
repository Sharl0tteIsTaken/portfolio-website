/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2025 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 * 
 * This is a modified version of the color mode toggler from Bootstrap,
 * visit the following URL to see the original version:
 * https://getbootstrap.com/docs/5.3/customize/color-modes/#javascript
 */

import { setCookie, getCookie, cookieNameSetting } from './modules/common.mjs'

const cookieName = "scheme"
const allowTheme = ["light", "dark", "auto"]

const storeTheme = theme => {
  const cookieSetting = getCookie(cookieNameSetting)

  const allowStore = JSON.parse(cookieSetting)?.find(item => item.id === cookieName)?.checked
  if (allowStore) {
    setCookie(cookieName, theme)
  }
}

/**
 * Note:
 * The following code is duplicated in `scripts/preload-color-scheme.js` to prevent screen flickering.
 * Any modifications here must also be reflected in the code there.
 */
// duplication start
const getTheme = () => {
  const prefer = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  const theme = getCookie(cookieName) ?? prefer
  return allowTheme.includes(theme) ? theme : prefer
}

const setTheme = theme => {
  $('html').attr('data-bs-theme', theme)
}

setTheme(getTheme())
// duplication end

const showActiveTheme = (theme, focus = false) => {
  const themeSwitcher = $('#theme-switcher')

  if (!themeSwitcher.exists()) {
    return
  }

  $('[data-bs-theme-value]').each(function() {
    const element = $(this)
    const isSelected = element.attr("data-bs-theme-value") === theme

    element.toggleClass('active', isSelected)
           .toggleClass('disabled', isSelected)
           .attr('aria-pressed', isSelected)
           .attr('tabindex', isSelected ? "-1" : "0")
  })

  if (focus) {
    themeSwitcher.focus()
  }
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  setTheme(getTheme())
})

$(document).ready(() => {
  showActiveTheme(getTheme())

  $('[data-bs-theme-value]').on('click', function() {
    const theme = $(this).attr('data-bs-theme-value')
    storeTheme(theme)
    setTheme(theme)
    showActiveTheme(theme, true)
  })
})
