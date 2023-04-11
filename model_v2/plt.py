import pandas as pd
import matplotlib.pyplot as plt


def show_data(joint:str):
    data = pd.read_excel(f"/Users/tiagocoutinho/Desktop/Gait_Software/{joint} angles.xlsx", sheet_name="Sheet1", header=None)

    plt.plot(data)

    plt.xlabel("Frames")
    plt.ylabel(f"{joint} (degrees)")
    plt.title(f"{joint} angle")

    plt.show()