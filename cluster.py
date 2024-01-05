import pandas as pd
from sklearn.cluster import KMeans

# Загрузка временных фреймов
data = pd.read_csv('data.csv')  # Замените 'data.csv' на путь к вашему файлу с временными фреймами

# Подготовка данных для кластеризации
X = data[['time']].values  # Замените 'time' на название столбца с временными данными
# Нормализация данных
X = (X - X.min()) / (X.max() - X.min())

# Кластеризация временных фреймов
kmeans = KMeans(n_clusters=7)  # Задайте количество кластеров в соответствии с требуемыми временными фреймами
kmeans.fit(X)

# Получение меток кластеров для каждого временного фрейма
cluster_labels = kmeans.labels_

# Вывод результатов
for i, cluster_label in enumerate(cluster_labels):
    print(f"Временной фрейм {i+1} относится к кластеру {cluster_label}")