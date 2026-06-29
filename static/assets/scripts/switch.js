'use strict'
import { banners, cookieMap, cookieNameSetting, setCookie, getCookie } from './modules/common.mjs'

const menubutton = bootstrap.Dropdown.getOrCreateInstance(
  document.querySelector(".cookie-banner .float-dropdown-menubutton")
)

const cookiePrefCheckbox = ".cookie-banner-preference"
const settingSwitch = document.querySelector(cookiePrefCheckbox)

const switchCheckbox = ".cookie-banner-switch"
const allSwitches = document.querySelectorAll(switchCheckbox)

const switchExcludeElement = ["INPUT", "LABEL", "IMG"]

const toggleCookiePref = state => {
  settingSwitch.checked = state
}

// restore or show banner
const settingValue = JSON.parse(getCookie(cookieNameSetting))
if (settingValue) {
  toggleCookiePref(true)
  settingValue.forEach(setting => {
    const element = document.getElementById(setting.id)
    if (element) {
      element.checked = setting.checked
      element.dispatchEvent(new Event('change'))
    }
  })
} else {
  menubutton.show()
}

document.querySelector("#close-cookie-banner").addEventListener('click', () => {
  toggleCookiePref(true)
  menubutton.hide()
})

// switch accessibility
document.querySelectorAll(".cookie-banner ul .cookie-banner-switch-container")
  // parent container toggleable
  .forEach(element => {
    element.addEventListener('click', event => {
      if (!switchExcludeElement.includes(event.target.tagName)) {
        const checkbox = element.querySelector(switchCheckbox)
        checkbox.click()
        return null
      }
      if (event.target.tagName === "INPUT") {
        toggleCookiePref(true)
      }
    })
  })

allSwitches.forEach(element => {
  // extra keyboard support
  element.addEventListener('keydown', event => {
    if (event.key === "Enter") {
      element.click()
    }
  })
})

const toggleAllSwitch = state => {
  allSwitches.forEach(element => {
    element.checked = state
    element.dispatchEvent(new Event('change'))
  })
}

document.querySelectorAll('[data-action="toggle-all"]').forEach(element => {
  element.addEventListener('click', () => {
    toggleAllSwitch(element.dataset.state === "true")
    toggleCookiePref(true)
  })
})

const removeAllCookie = () => {
  toggleAllSwitch(false)
  toggleCookiePref(false)
  const remove = true
  document.cookie.split("; ").forEach(cookie => {
    setCookie(cookie.split("=")[0], "", remove)
  })
}

const handleKeydown = event => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault()
    removeAllCookie()
  } 
}

const removeLink = document.querySelector('[data-action="remove-all"]')
removeLink.addEventListener('click', removeAllCookie)
removeLink.addEventListener('keydown', event => handleKeydown(event))

// sync user setting
document.querySelectorAll(banners).forEach(element => {
  element.addEventListener("hidden.bs.dropdown", () => {
    const setting = Array.from(allSwitches).map(({ id, checked }) => ({id, checked}))

    if (settingSwitch.checked) {
      setCookie(cookieNameSetting, JSON.stringify(setting))
    }

    setting.forEach(rule => {
      const value = rule.checked ? cookieMap[rule.id] : ""
      const remove = rule.checked ? false : true
      setCookie(rule.id, value, remove)
    })
  })
})
// TODO: rename JS files, switch -> cookie-banner, hover -> navbar-hover, tooltip -> cookie-banner-tooltip
