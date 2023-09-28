import argparse
import random
from fractions import Fraction
import re

ture = 0

# 定义运算符和运算符的权重
operators = ['+', '-', '*', '/']  # 使用 * 代替 ×，/ 代替 ÷
operator_weights = [2, 2, 1, 1]

# 命令行参数解析
parser = argparse.ArgumentParser(description='Generate elementary school arithmetic problems.')
parser.add_argument('-n', type=int, required=True, help='Number of problems to generate')
parser.add_argument('-r', type=int, required=True, help='Range of numbers (0 to r)')
args = parser.parse_args()


# 生成算术表达式
def generate_expression(min_num, max_num, max_depth):
    if max_depth == 0:
        return str(random.randint(min_num, max_num))

    operator = random.choices(operators, weights=operator_weights)[0]

    if operator in ['+', '-', '*', '/']:
        # 对于加、减、乘、除运算，生成两个子表达式并组合它们
        left_expr = generate_expression(min_num, max_num, max_depth - 1)
        right_expr = generate_expression(min_num, max_num, max_depth - 1)

        try:
            eval(right_expr)
            eval(left_expr)
        except ZeroDivisionError:
            print("除数为零异常发生，重新生成题目。")
            global ture
            ture = 1
            return

        if operator == '-':
            if eval(left_expr) < eval(right_expr):
                translation = left_expr
                left_expr = right_expr
                right_expr = translation

    else:
        print("2b")
        # 对于自定义运算（如除法确保结果是真分数），生成一个子表达式
        right_expr = generate_expression(min_num + 1, max_num, max_depth - 1)
        left_expr = generate_expression(min_num, max_num, max_depth - 1)

    # 检查左表达式是否包含括号，如果是则不执行 int() 转换
    if not re.search(r'\(.*\)', left_expr):
        left_expr = int(left_expr)

    return f'({left_expr} {operator} {right_expr})'


# 生成题目和答案
problems = []
answers = []
for i in range(args.n):
    ture = 0
    expression = generate_expression(0, args.r, 2)
    if ture == 1:
        i = i-1
        break
    try:
        # 使用 eval() 计算表达式并将结果转换为真分数
        improper_fraction = Fraction(eval(expression)).limit_denominator()
        # 使用 divmod 将假分数转化为带分数
        whole_part, remainder = divmod(improper_fraction.numerator, improper_fraction.denominator)
        fraction = Fraction(eval(expression)).limit_denominator() - Fraction(whole_part)  # 得到分数部分
        # 将带分数格式化为字符串形式
        # 判断是否为整数，如果是整数就保持不变，否则转化为带分数形式
        if remainder == 0:
            result = str(whole_part)  # 整数部分
        else:
            if whole_part == 0:
                result = fraction
            else:
                result = f'{whole_part}\'{fraction}'
    except ZeroDivisionError:
        print("除数为零异常发生，跳过此题目。")  # 注意修改
        continue  # 避免除以零的情况
    problems.append(expression)
    answers.append(result)

# 保存题目和答案到文件
with open('Exercises.txt', 'w') as exercises_file:
    for i, problem in enumerate(problems, start=1):
        exercises_file.write(f'四则运算题目{i}: {problem}\n')

with open('Answers.txt', 'w') as answers_file:
    for answer in answers:
        answers_file.write(str(answer) + '\n')

print(f'Generated {args.n} problems in Exercises.txt and Answers.txt.')
