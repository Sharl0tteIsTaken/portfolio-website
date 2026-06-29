/**
 * Note: This is duplicated from `scripts/color-scheme.js`.
 */

const cookieName = "scheme"
const allowTheme = ["light", "dark", "auto"]

const getCookie = (cookieKey) => {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookieKey + "="))
    ?.split("=")[1] ?? null
}

const getTheme = () => {
  const prefer = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  const theme = getCookie(cookieName) ?? prefer
  return allowTheme.includes(theme) ? theme : prefer
}

const setTheme = theme => {
  document.documentElement.setAttribute('data-bs-theme', theme)
}

setTheme(getTheme())
