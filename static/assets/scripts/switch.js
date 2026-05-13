const cookieSettingName = "setting"
const switchCheckbox = ".form-check-input"

const toggleAllSwitch = state => {
  document.querySelectorAll(switchCheckbox)
    .forEach(element => {
      if (element.checked !== state) {
        element.checked = state
        element.dispatchEvent(new Event('change'))
      }
    }
  )
}

window.addEventListener('DOMContentLoaded', () => {
  // restore user setting in cookie banner
  const settingValue = JSON.parse(
    document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookieSettingName + "="))
    ?.split("=")[1] ?? null
  )
  if (settingValue) {
    settingValue.forEach(setting => {
      const element = document.getElementById(setting.id)
      if (element) {
        element.checked = setting.checked
        element.dispatchEvent(new Event('change'))
      }
    })
  } else {
    const menubutton = bootstrap.Dropdown.getOrCreateInstance(
      document.querySelector(".cookie-banner .float-dropdown-menubutton")
    )
    menubutton.show()
  }

  // parent container toggleable
  document.querySelectorAll(".cookie-banner ul .dropdown-item")
    .forEach(element => {
      element.addEventListener('click', click => {
        if (click.target.tagName !== "INPUT" && click.target.tagName !== "LABEL") {
          const checkbox = element.querySelector(switchCheckbox)
          checkbox.click()
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

  // close banner should record cookie setting
  document.querySelector("#close-cookie-banner").addEventListener('click', () => {
    updateCookie()
    const menubutton = bootstrap.Dropdown.getOrCreateInstance(
      document.querySelector(".cookie-banner .float-dropdown-menubutton")
    )
    menubutton.hide()
  })

  allSwitches.forEach(element => {
    // record cookie setting
    element.addEventListener('change', () => {
      updateCookie()
    })

    // extra keyboard support
    element.addEventListener('keydown', event => {
      if (event.key === "Enter") {
        element.click()
      }
    })
  })
})
