import pandas as pd


def mergeData(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Fusiona df1 y df2 usando 'User ID' y 'Person ID',
    y guarda el resultado como CSV.

    Args:
        df1 (pd.DataFrame): DataFrame con 'User ID'.
        df2 (pd.DataFrame): DataFrame con 'Person ID' y datos de salud.

    Raises:
        KeyError: Si faltan columnas clave.
    """
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


def identifyOutliers(df: pd.DataFrame, column: pd.Series):
    """
    Identifica y muestra los valores atípicos (outliers) de una columna
    numérica usando el método del rango intercuartílico (IQR).

    Parámetros:
    -----------
    column : pd.Series
        Serie de pandas que contiene los datos numéricos a analizar.

    Salidas:
    --------
    Imprime el número de outliers encontrados y una
    lista de los valores atípicos.
    """
    # Calcular cuartiles
    q1 = column.quantile(0.25)
    q3 = column.quantile(0.75)

    # Rango intercuartílico
    ric = q3 - q1

    # Límites para detectar outliers
    high = q3 + 1.5 * ric
    low = q1 - 1.5 * ric

    # Filtrar outliers
    outliers = df[(column > high) | (column < low)]

    print(f"Número de outliers en {column.name}: {len(outliers)}")
    print(f"Outliers en {column.name}: {outliers[column.name].tolist()}")


def calculateRoutineLevel(row: pd.Series) -> str:
    """
    Calcula el nivel de rutina diaria ('Low', 'Medium', 'High')
    según indicadores de salud y hábitos, ajustando por edad y género.

    Parámetros:
    -----------
    row : pd.Series
        Fila del DataFrame con información de salud y estilo de vida.

    Retorna:
    --------
    str
        Nivel de rutina: 'Low', 'Medium' o 'High'.
    """
    score = 0

    # Tolerancia para ajustar la rutina según edad y género
    ageFactor = 0
    genderFactor = 0

    if row['Age'] < 30:
        ageFactor += 1.0
    elif row['Age'] < 60:
        ageFactor += 0.8
    else:
        ageFactor += 0.6

    if row['Gender'].lower() == 'm' or row['Gender'].lower() == 'hombre':
        genderFactor = 1.0
    else:
        genderFactor = 0.95

    tolerance = (ageFactor + genderFactor) / 2

    # Indicador de la rutina

    # Sleep Quality
    if row['Sleep Quality'] > 7:
        score += 2
    elif row['Sleep Quality'] >= 4:
        score += 1
    else:
        score += 0.5

    # Bedtime

    # Usar solo la hora, de 'Bedtime'
    hour = pd.to_datetime(row['Bedtime'], format='%H:%M').hour
    bedtime = hour if hour > 6 else hour + 24

    if 21 <= bedtime < 23:
        score += 2
    elif 23 <= bedtime < 25:
        score += 1
    elif 25 <= bedtime < 27:
        score -= 0.5
    else:
        score -= 1  # muy tarde → desorden de sueño

    # Daily Steps
    if row['Daily Steps'] >= 10000:
        score += 2
    elif 5000 <= row['Daily Steps'] < 10000:
        score += 1
    else:
        score -= 0.5

    # Calories Burned
    if row['Calories Burned'] >= 2500:
        score += 2
    elif 1800 <= row['Calories Burned'] < 2500:
        score += 1
    else:
        score -= 0.5

    # Physical Activity Level
    pal = row['Physical Activity Level'].lower().strip()
    if pal in ['high', 'alto']:
        score += 2
    elif pal in ['medium', 'medio']:
        score += 1
    else:
        score -= 0.5

    # Dietary Habits
    dh = row['Dietary Habits'].lower().strip()
    if dh in ['healthy', 'saludables']:
        score += 2
    elif dh in ['medium', 'moderados']:
        score += 1
    else:
        score -= 0.5

    # Sleep Disorders y Medication Usage
    sd = row['Sleep Disorders'].lower().strip()
    mu = row['Medication Usage'].lower().strip()
    if sd in ['yes', 'sí'] and mu in ['yes', 'sí']:
        score -= 2
    elif sd in ['yes', 'sí'] or mu in ['yes', 'sí']:
        score -= 1

    # Sleep Duration
    if 7 <= row['Sleep Duration'] <= 9:
        score += 2
    elif 5 <= row['Sleep Duration'] < 7:
        score += 1
    elif 9 < row['Sleep Duration'] <= 10:
        score += 0.5
    else:
        score -= 1  # sueño insuficiente o excesivo

    # Stress Level
    if row['Stress Level'] <= 3:
        score += 2
    elif 4 <= row['Stress Level'] <= 6:
        score += 0.5
    elif 7 <= row['Stress Level'] <= 8:
        score -= 1
    else:
        score -= 2  # estrés no tan normal

    # BMI Category
    bmi = row['BMI Category'].lower().strip()
    if bmi in ['normal', 'normal weight', 'peso normal']:
        score += 2
    elif bmi in ['overweight', 'sobrepeso']:
        score += 0.5
    elif bmi in ['obese', 'obesidad']:
        score -= 1

    # Heart Rate
    if 60 <= row['Heart Rate'] <= 80:
        score += 2
    elif 81 <= row['Heart Rate'] <= 90:
        score += 0.5
    elif row['Heart Rate'] < 60:
        score += 1
    else:
        score -= 1  # alta frecuencia → puede indicar estrés o bajo fitness

    # Blood Pressure
    if row['BP_Systolic'] < 120 and row['BP_Diastolic'] < 80:
        score += 2
    elif 120 <= row['BP_Systolic'] < 130 and row['BP_Diastolic'] < 80:
        score += 1
    elif 130 <= row['BP_Systolic'] < 140 or 80 <= row['BP_Diastolic'] < 90:
        score += 0
    else:
        score -= 1  # hipertensión → riesgo y afectación de rutina

    # Aplicar tolerancia
    score *= tolerance

    # Clasificación final
    if score >= 14:
        return 'High'
    elif score >= 6:
        return 'Medium'
    else:
        return 'Low'


if __name__ == "__main__":
    try:
        df1 = pd.read_csv('../data/Health_Sleep_Statistics.csv')
        df2 = pd.read_csv('../data/Sleep_health_and_lifestyle_dataset.csv')
        mergeData(df1, df2)
    except Exception as e:
        print(f"Error cargando datos | {e}")
