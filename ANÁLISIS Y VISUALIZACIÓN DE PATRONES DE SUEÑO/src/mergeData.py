import pandas as pd

#Con este código unimos las dos bases de datos
def mergeData(df1: pd.DataFrame, df2: pd.DataFrame):
    try:
        if 'User ID' not in df1.columns or 'Person ID' not in df2.columns:
            raise KeyError("Columnas clave no encontradas en los DataFrames.")

        df = df1.merge(
            df2[['Person ID',
                 'Occupation',
                 'Sleep Duration',
                 'Stress Level',
                 'BMI Category',
                 'Blood Pressure',
                 'Heart Rate',
                 'Sleep Disorder']],
            left_on=['User ID'],
            right_on=['Person ID'],
            how='left'
        ).drop(columns=['Wake-up Time', 'Person ID'])

        df.to_csv('../data/Merged_Statistics_and_lifestyle.csv',
                  index=False,
                  encoding='utf-8')
    except Exception as e:
        print(f"Error juntando datos | {e}")


if __name__ == "__main__":
    try:
        df1 = pd.read_csv('../data/Health_Sleep_Statistics.csv')
        df2 = pd.read_csv('../data/Sleep_health_and_lifestyle_dataset.csv')
        mergeData(df1, df2)
    except Exception as e:
        print(f"Error cargando datos | {e}")
