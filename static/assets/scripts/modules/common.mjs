const banners = [".cookie-banner", ".theme-banner"]

const cookieNameSetting = "setting"
const cookieNameLanguage = "language"
const cookieNameEndpoint = "endpoint"
const cookieNameScheme = "scheme"

const cookieUptime = 14 * 24 * 60 * 60 * 1000
const cookieExpire = "Thu, 01 Jan 1970 00:00:00 UTC"

const cookieMap = {
  get [cookieNameLanguage]() {
    return document.documentElement.getAttribute("lang")
  },
  get [cookieNameEndpoint]() {
    return window.location.pathname
  },
  get [cookieNameScheme]() {
    return document.documentElement.getAttribute("data-bs-theme")
  },
}

const setCookie = (cookieKey, cookieVar = "", remove = false) => {
  const date = new Date()
  date.setTime(date.getTime() + cookieUptime)
  const expires = remove ? cookieExpire : date.toUTCString()

  // intentionally unencoded for transparency
  document.cookie = cookieKey + "=" + cookieVar + "; expires=" + expires + "; path=/"
}

const getCookie = (cookieKey) => {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookieKey + "="))
    ?.split("=")[1] ?? null
}

export { banners, cookieMap, cookieNameSetting, setCookie, getCookie }
