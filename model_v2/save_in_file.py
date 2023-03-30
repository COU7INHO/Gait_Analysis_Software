import pandas as pd


def save_data(data, file_name:str, save=False):
    if save == True:
        s = pd.Series(data)

        with pd.ExcelWriter(f"{file_name}.xlsx") as writer:
            s.to_excel(writer, sheet_name='Sheet1', startrow=0, index=False)
