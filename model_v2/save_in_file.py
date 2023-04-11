
import pandas as pd
import matplotlib.pyplot as plt


class AnalyseData:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def save_data(self):
        s = pd.Series(self.data)

        with pd.ExcelWriter(f"{self.file_name}.xlsx") as writer:
            s.to_excel(writer, sheet_name='Sheet1', startrow=0, index=False, header=False)

    def  plot_data(self, title:str):
        self.title = title
        self.data = pd.read_excel(f"{self.file_name}.xlsx", sheet_name="Sheet1", header=None)

        plt.plot(self.data)

        plt.xlabel("Frames")
        plt.ylabel("Angle - degrees")
        plt.title(self.title)

        plt.show()