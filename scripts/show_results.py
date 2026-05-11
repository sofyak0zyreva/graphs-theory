import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Загрузка данных
df = pd.read_csv('/Users/sofyakozyreva/graphs-theory/scripts/benchmark/results/bfs_results.csv')

# Настройка стиля
sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 8))

# Построение графика
# Сделаем 'nodes' категориальным признаком для корректного отображения групп
df['nodes'] = df['nodes'].astype(str)

ax = sns.barplot(
    data=df,
    x='graph',
    y='mean',
    hue='nodes',
    palette='viridis'
)

# Установка логарифмической шкалы
ax.set_yscale("log")

# Добавление подписей mean над столбиками
for container in ax.containers:
    # Для логарифмической шкалы нужно аккуратно располагать текст,
    # чтобы он не наезжал на границы
    labels = [f'{val:.2f}' if val > 0 else '' for val in container.datavalues]
    ax.bar_label(container, labels=labels, padding=3, fontsize=9, rotation=45)

# Настройка осей и легенды
plt.title('BFS Performance by Graph and Node Count', fontsize=16)
plt.xlabel('Graph Name', fontsize=12)
plt.ylabel('Mean Time (log scale)', fontsize=12)
plt.xticks(rotation=15, ha='right')
plt.legend(title='Nodes', loc='upper left')

plt.tight_layout()
plt.show()
