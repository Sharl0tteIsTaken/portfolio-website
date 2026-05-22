const cookieSettingName = "setting"
const switchCheckbox = ".cookie-banner-switch"
const cookiePrefCheckbox = ".cookie-banner-preference"
const switchExcludeElement = ["INPUT", "LABEL", "IMG"]

const toggleAllSwitch = state => {
  document.querySelectorAll(switchCheckbox)
    .forEach(element => {
      // Intentionally no check as this is an interaction with the panel,
      // event should be dispatched.
      element.checked = state
      element.dispatchEvent(new Event('change'))
    }
  )
}

const toggleCookiePref = state => {
  const settingCheckbox = document.querySelector(cookiePrefCheckbox)
  settingCheckbox.checked = state
  }

const removeAllCookie = () => {
  toggleAllSwitch(false)
  toggleCookiePref(false)
  document.cookie.split("; ").forEach(cookie => {
    document.cookie = cookie.split("=")[0] + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
  })
}

window.addEventListener('DOMContentLoaded', () => {
  const settingValue = JSON.parse(
    document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookieSettingName + "="))
    ?.split("=")[1] ?? null
  )
  if (settingValue) {
    // restore user setting in cookie banner
    toggleCookiePref(true)
    settingValue.forEach(setting => {
      const element = document.getElementById(setting.id)
      if (element) {
        element.checked = setting.checked
        element.dispatchEvent(new Event('change'))
      }
    })
  } else {
    // show cookie banner
    const menubutton = bootstrap.Dropdown.getOrCreateInstance(
      document.querySelector(".cookie-banner .float-dropdown-menubutton")
    )
    menubutton.show()
  }

  // parent container toggleable
  document.querySelectorAll(".cookie-banner ul .cookie-banner-switch-container")
    .forEach(element => {
      element.addEventListener('click', click => {
        if (!switchExcludeElement.includes(click.target.tagName)) {
          const checkbox = element.querySelector(switchCheckbox)
          checkbox.click()
          toggleCookiePref(true)
        }
      })
    })

  const allSwitches = document.querySelectorAll(switchCheckbox)

  const updateCookie = () => {
    const setting = Array.from(allSwitches).map(({ id, checked }) => ({id, checked}))
    const date = new Date()
    date.setTime(date.getTime() + (14 * 24 * 60 * 60 * 1000))
    const expires = "; expires=" + date.toUTCString()

    document.cookie = cookieSettingName + "=" + JSON.stringify(setting) + expires + "; path=/"
  }

  allSwitches.forEach(element => {
    // record cookie setting
    element.addEventListener('change', () => {
      updateCookie()
      toggleCookiePref(true)
    })

    // extra keyboard support
    element.addEventListener('keydown', event => {
      if (event.key === "Enter") {
        element.click()
      }
    })
  })

  // record cookie setting (close banner with button)
  document.querySelector("#close-cookie-banner").addEventListener('click', () => {
    updateCookie()
    toggleCookiePref(true)
    const menubutton = bootstrap.Dropdown.getOrCreateInstance(
      document.querySelector(".cookie-banner .float-dropdown-menubutton")
    )
    menubutton.hide()
  })

  // remove rejected cookie
  document.querySelector(".cookie-banner").addEventListener("hidden.bs.dropdown", () => {
    const setting = Array.from(allSwitches).map(({ id, checked }) => ({id, checked}))
    setting.forEach(rule => {
      if (!rule.checked) {
        document.cookie = rule.id + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
      }
    })
  })

  // keyboard support for remove all cookie
  const removeLink = document.querySelector(".cookie-remove-link")
  removeLink.addEventListener('keydown', event => {
    if (event.key === "Enter") {
      removeLink.click()
    }
  })
})
