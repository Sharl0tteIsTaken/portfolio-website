import { banners, cookieMap, cookieNameSetting, setCookie, getCookie } from './modules/common.mjs'

const menubutton = bootstrap.Dropdown.getOrCreateInstance(
  document.querySelector(".cookie-banner .float-dropdown-menubutton")
)

const cookiePrefCheckbox = ".cookie-banner-preference"
const settingSwitch = document.querySelector(cookiePrefCheckbox)

const switchCheckbox = ".cookie-banner-switch"
const allSwitches = $(switchCheckbox)

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
      $(element).change()
    }
  })
} else {
  menubutton.show()
}

$("#close-cookie-banner").on('click', () => {
  toggleCookiePref(true)
  menubutton.hide()
})

// switch accessibility
$(".cookie-banner ul .cookie-banner-switch-container").on('click', function(event) {
  // parent container toggleable
  if (!switchExcludeElement.includes(event.target.tagName)) {
    const checkbox = $(this).find(switchCheckbox)
    checkbox.click()
  } else if (event.target.tagName === "INPUT") {
    toggleCookiePref(true)
  }
})

allSwitches.on('keydown', function(event) {
  // extra keyboard support
  if (event.key === "Enter") {
    $(this).click()
  }
})

const toggleAllSwitch = state => {
  allSwitches.each(function() {
    this.checked = state
    $(this).change()
  })
}

$('[data-action="toggle-all"]').on('click', function() {
  toggleAllSwitch($(this).data('state') === true)
  toggleCookiePref(true)
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

const removeLink = $('[data-action="remove-all"]')
removeLink.on('click', removeAllCookie)
removeLink.on('keydown', event => handleKeydown(event))

// sync user setting
$(banners.join(", ")).on("hidden.bs.dropdown", () => {
  const setting = allSwitches.toArray().map(({ id, checked }) => ({ id, checked }))

  if (settingSwitch.checked) {
    setCookie(cookieNameSetting, JSON.stringify(setting))
  }

  setting.forEach(rule => {
    const value = rule.checked ? cookieMap[rule.id] : ""
    const remove = rule.checked ? false : true
    setCookie(rule.id, value, remove)
  })
})
