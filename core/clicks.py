import pyautogui
from core.state import state

def click_call():
    c = state["coords"]["call"]; pyautogui.click(c["x"], c["y"])

def click_put():
    c = state["coords"]["put"]; pyautogui.click(c["x"], c["y"])

def click_new():
    c = state["coords"]["new"]; pyautogui.click(c["x"], c["y"])
