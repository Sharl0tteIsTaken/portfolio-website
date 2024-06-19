import pyautogui


window = pyautogui.getWindowsWithTitle("Demo - Google Chrome") # type: ignore

window[0].resizeTo(1080, 720)





# 720, 480
# 1080, 720

print(window[0])