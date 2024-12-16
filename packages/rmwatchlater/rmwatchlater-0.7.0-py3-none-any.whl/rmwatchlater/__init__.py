import pyautogui as gui
import webbrowser
import time
from mylocale.TR import tr


def main():
    url = "https://www.youtube.com/playlist?list=WL"
    trfile = "rmwatcher/localisation.csv"
    promt = input(
        "Are you logged into your Google Account? ([{yes}]es/[{no}]o)".format(
            yes="y", no="n"
        )
    )
    webbrowser.open(url)
    try:
        if promt == tr(csv_file=trfile, target_key="YES"):
            while True:
                gui.click("rmwatchlater/imgs/menue.png")
        else:
            print("Error")

    except:
        pass


if __name__ == "__main__":
    main()
