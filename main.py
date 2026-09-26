def read_input(file_path):
    a = []
    b = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            parts = [float(x) for x in line_str.split()]
            a.append(parts[:-1])
            b.append(parts[-1])

    return a, b


def solve_gauss_with_pivoting(a, b, eps=1e-12):
    n = len(b)

    for k in range(n - 1):
        #поиск строки m с максимальным по модулю элементом в столбце k
        m = k
        max_val = abs(a[k][k])
        for i in range(k + 1, n):
            if abs(a[i][k]) > max_val:
                max_val = abs(a[i][k])
                m = i

        #если близок к 0
        if max_val < eps:
            raise ValueError(
                "Система не имеет однозначного решения (главный элемент близок к нулю)."
            )

        #меняем строки k и m
        if m != k:
            b[k], b[m] = b[m], b[k]
            for j in range(k, n):
                a[k][j], a[m][j] = a[m][j], a[k][j]

        #зануление
        for i in range(k + 1, n):
            t_ik = a[i][k] / a[k][k]

            b[i] -= t_ik * b[k]

            for j in range(k + 1, n):
                a[i][j] -= t_ik * a[k][j]

    #проверка последнего элемента перед обратным ходом
    if abs(a[n - 1][n - 1]) < eps:
        raise ValueError("Система не имеет однозначного решения.")

    #обратный ход
    x = [0.0] * n

    #первый элемент (на самом деле последний)
    x[n - 1] = b[n - 1] / a[n - 1][n - 1]

    for k in range(n - 2, -1, -1):
        s = 0.0
        for j in range(k + 1, n):
            s += a[k][j] * x[j]
        x[k] = (b[k] - s) / a[k][k]

    return x


def main():
    input_filename = "input.txt"

    try:
        a, b = read_input(input_filename)
        n = len(b)
        print(f"Загружена система размерности: {n}x{n}\n")

        x = solve_gauss_with_pivoting(a, b)

        print("Решение системы (x_1, x_2, ..., x_n):")
        for i, val in enumerate(x, 1):
            print(f"x_{i} = {val:.8f}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден.")
    except Exception as e:
        print(f"Ошибка при вычислениях: {e}")


if __name__ == "__main__":
    main()