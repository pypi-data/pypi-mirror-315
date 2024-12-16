import numpy as np
import matplotlib.pyplot as plt


def train(network, x_train, y_train, loss_func, epochs, batch_size=None, optimizer=None, visualize=False):
    """
    Обучает нейронную сеть на заданных тренировочных данных.

    Параметры:
    network: объект сети, который имеет методы forward и backward для прямого и обратного распространения.
    x_train: ndarray, входные данные для обучения (размерность: [количество образцов, количество признаков]).
    y_train: ndarray, целевые значения (размерность: [количество образцов, количество выходов]).
    loss_func: функция потерь, которая оценивает разницу между предсказаниями сети и целевыми значениями.
    epochs: int, количество эпох для обучения сети.
    batch_size: int или None, размер батча для мини-батч обучения (если None, обучение происходит на всех данных за раз).
    optimizer: объект оптимизатора, который будет использован для обновления весов слоя (может быть None).
    visualize: bool, если True, то активирует визуализацию потерь и точности.
    """

    n_samples = x_train.shape[0]  # Количество обучающих образцов
    accuracy_list = []
    loss_list = []

    for epoch in range(epochs):
        print(f"\nЭпоха {epoch + 1}/{epochs}:")
        epoch_loss = 0
        correct_predictions = 0
        total_batch_loss = 0  # Переменная для накопления потерь за все батчи в эпохе
        total_batches = 0  # Счётчик количества батчей

        if batch_size:  # Если указан размер батча, проводим обучение по батчам
            indices = np.arange(n_samples)  # Индексы всех образцов
            np.random.shuffle(indices)  # Перемешиваем индексы для случайной выборки

            x_train, y_train = x_train[indices], y_train[indices]  # Перемешиваем данные

            for start_idx in range(0, n_samples, batch_size):
                end_idx = start_idx + batch_size
                x_batch = x_train[start_idx:end_idx]  # Получаем текущий батч данных
                y_batch = y_train[start_idx:end_idx]  # Получаем текущий батч целевых значений

                # Обратное распространение и обновление весов для текущего батча
                network.backward(x_batch, y_batch, loss_func)

                for layer in network.layers:
                    if hasattr(layer, 'update_weights'):
                        layer.update_weights(network.learning_rate, optimizer=optimizer)  # Обновление весов слоя

                batch_loss = loss_func(y_batch, network.forward(x_batch)) / y_batch.size
                total_batch_loss += batch_loss
                total_batches += 1
                batch_num = start_idx // batch_size + 1
                if batch_num % batch_size == 0:
                    print(f"  Батч {batch_num}, Потеря: {batch_loss:.4f}")

                predictions = network.forward(x_batch)
                predicted_class = np.argmax(predictions, axis=1)
                true_class = np.argmax(y_batch, axis=1)
                correct_predictions += np.sum(predicted_class == true_class)
            epoch_loss = total_batch_loss / total_batches


        else:  # Обучение без разбивки на батчи
            network.backward(x_train, y_train, loss_func)  # Обратное распространение для всех данных

            for layer in network.layers:  # Обновление весов для всех слоев
                if hasattr(layer, 'update_weights'):
                    layer.update_weights(network.learning_rate, optimizer=optimizer)
            # Вычисляем потери эпоху
            epoch_loss = loss_func(y_train, network.forward(x_train)) / y_train.size

            # Вычисление точности за эпоху
            predictions = network.forward(x_train)
            predicted_class = np.argmax(predictions, axis=1)
            true_class = np.argmax(y_train, axis=1)
            correct_predictions = np.sum(predicted_class == true_class)

        # Записываем значения точности и потерь
        accuracy = correct_predictions / n_samples
        accuracy_list.append(accuracy)
        loss_list.append(epoch_loss)

        # Выводим информацию по эпохе
        print(f"Точность за эпоху: {accuracy * 100:.2f}%")
        print(f"Потери за эпоху: {epoch_loss:.4f}")

    # Если активирована визуализация, передаем данные в визуализацию
    if visualize:
        visualize_training(accuracy_list, loss_list)


def visualize_training(accuracy_list, loss_list):
    """
    Функция для визуализации точности и потерь во время обучения.

    Параметры:
    accuracy_list: список точности на каждой эпохе.
    loss_list: список потерь на каждой эпохе.
    """
    epochs = len(accuracy_list)
    x = np.arange(1, epochs + 1)

    # Визуализация точности
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(x, accuracy_list, label='Точность')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность')
    plt.title('Точность на каждой эпохе')
    plt.grid(True)

    # Визуализация потерь
    plt.subplot(1, 2, 2)
    plt.plot(x, loss_list, label='Потери', color='red')
    plt.xlabel('Эпохи')
    plt.ylabel('Потери')
    plt.title('Потери на каждой эпохе')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
