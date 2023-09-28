# 调用库
import argparse
import random
from fractions import Fraction
import re

# 全局变量
ture = 0

# 定义四则运算符号和运算符号的权重
operators = ['+', '-', '*', '/']  # 使用 * 代替 ×，/ 代替 ÷
operator_weights = [2, 2, 1, 1]


# 函数定义
# 1、生成算术表达式
def generate_expression(min_num, max_num, max_depth):
    # 递归到第0层的时候，生成一个数字，并以字符串的形式传回去
    if max_depth == 0:
        return str(random.randint(min_num, max_num))

    # 引用全局变量ture
    global ture
    operator = random.choices(operators, weights=operator_weights)[0]

    # 对于加、减、乘、除运算，生成两个子表达式并组合它们
    left_expr = generate_expression(min_num, max_num, max_depth - 1)
    right_expr = generate_expression(min_num, max_num, max_depth - 1)
    if ture == 1:
        return
    if operator == '/':
        try:
            x = f'({left_expr} {operator} {right_expr})'
            eval(x)
        except ZeroDivisionError:
            print("出错，重新生成题目。")
            ture = 1
            return

    if operator == '-':
        if eval(left_expr) < eval(right_expr):
            translation = left_expr
            left_expr = right_expr
            right_expr = translation

    # 检查左表达式是否包含括号，如果是则不执行 int() 转换
    if not re.search(r'\(.*\)', left_expr):
        left_expr = int(left_expr)

    return f'({left_expr} {operator} {right_expr})'


# 2、从题目文件中读取题目数据
def read_problems(filename):
    with open(filename, 'r') as file:
        return [line.strip().split('. ')[1] for line in file.readlines() if line.strip()]


# 3、从答案文件中读取答案数据
def read_answers(filename):
    with open(filename, 'r') as file:
        return [line.strip().split('. ')[1] for line in file.readlines() if line.strip()]


# 4、对比答案是否正确            (改：problems, answers--》problems_check, answers_check)
def check_answers(problems_check, answers_check):
    correct_indices_check = []  # 存储正确答案的索引
    wrong_indices_check = []    # 存储错误答案的索引

    for j, (problem_c, answer_c) in enumerate(zip(problems_check, answers_check), start=1):
        # 假设答案文件中每行只包含一个答案
        problem_c = problem_c.strip()
        answer_c = answer_c.strip()
        print("正确的计算结果：", Fraction(eval(problem_c)).limit_denominator())

        # 在这里进行答案判定，根据题目和答案的格式来编写具体判定逻辑
        # 这里简单地假设如果题目和答案一致，则判定为正确，否则为错误
        # 由于符号过长，引入变量，简化式子
        pc = Fraction(eval(problem_c)).limit_denominator()
        ac = Fraction(eval(process_answer(answer_c))).limit_denominator()
        if pc == ac:
            correct_indices_check.append(j)
        else:
            wrong_indices_check.append(j)

    return correct_indices_check, wrong_indices_check


# 5、将结果写入Grade.txt文件
def write_grade(correct_count2, correct_indices2, wrong_count2, wrong_indices2):
    with open('Grade.txt', 'w') as file:
        file.write(f'Correct: {correct_count2} ({", ".join(map(str, correct_indices2))})\n')
        file.write(f'Wrong: {wrong_count2} ({", ".join(map(str, wrong_indices2))})\n')


# 6、假设答案字符串包含整数、分数和带分数的部分
def process_answer(answer_in):

    # 遍历答案的各个部分并识别其类型
    if "'" in answer_in:
        # 处理带分数部分
        mixed_parts = answer_in.split("'")
        mixed_whole_part = int(mixed_parts[0])
        mixed_fraction_str = mixed_parts[1]
        mixed_fraction_numerator, mixed_fraction_denominator = map(int, mixed_fraction_str.split('/'))
        mixed_fraction_numerator = mixed_whole_part * mixed_fraction_denominator + mixed_fraction_numerator
        return f'{mixed_fraction_numerator}/{mixed_fraction_denominator}'
    elif '/' in answer_in:
        # 处理分数部分
        fraction_numerator, fraction_denominator = map(int, answer_in.split('/'))
        return f'{fraction_numerator}/{fraction_denominator}'
    else:
        # 处理整数部分
        integer_part = int(answer_in)
        return f'{integer_part}'


# 主程序
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random numbers and check two txt files.")
    parser.add_argument("--generate", action="store_true", help="Generate random numbers.")
    parser.add_argument("--check", action="store_true", help="Check two txt files.")
    parser.add_argument("-n", type=int, help="Number of random numbers to generate.")
    parser.add_argument("-r", type=int, help="Range for random numbers.")
    parser.add_argument("-e", type=str, help="First txt file for checking.")
    parser.add_argument("-a", type=str, help="Second txt file for checking.")
    args = parser.parse_args()

    # parser.add_argument("--filename", type=str, default="random_numbers.txt",
    # help="Specify the filename for writing (default: random_numbers.txt)")

    # parser = argparse.ArgumentParser(description="Generate random numbers and write to a txt file.")
    # parser.add_argument("--generate", action="store_true", help="Generate random numbers.")
    # parser.add_argument("--check", type=str, help="Write numbers to a txt file.")
    # parser.add_argument("--filename", type=str, default="random_numbers.txt",
    #                     help="Specify the filename for writing (default: random_numbers.txt)")
    # parser = argparse.ArgumentParser(description='Check and grade exercise answers.')
    # parser.add_argument('-e', type=str, required=True, help='Exercise file (Exercises.txt)')
    # parser.add_argument('-a', type=str, required=True, help='Answer file (Answers.txt)')
    #
    # # 命令行参数解析
    # parser = argparse.ArgumentParser(description='Generate elementary school arithmetic problems.')
    # parser.add_argument('-n', type=int, required=True, help='Number of problems to generate')
    # parser.add_argument('-r', type=int, required=True, help='Range of numbers (0 to r)')

    if (args.n or args.r) and (args.e is None and args.a is None):
        if args.n is None or args.r is None:
            print("生成题目格式错误，请输入正确格式：main.exe -n 10 -r 10")
        else:
            # 生成题目和答案
            problems = []
            answers = []
            for i in range(args.n):
                expression = generate_expression(0, args.r, 2)
                while ture == 1 or (expression in problems):
                    ture = 0
                    expression = generate_expression(0, args.r, 2)
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

                problems.append(expression)
                answers.append(result)

            # 保存题目和答案到文件
            with open('Exercises.txt', 'w') as exercises_file:
                for i, problem in enumerate(problems, start=1):
                    exercises_file.write(f'{i}. {problem}\n')

            with open('Answers.txt', 'w') as answers_file:
                for i, answer in enumerate(answers, start=1):
                    answers_file.write(f'{i}. {answer}\n')

            print(f'Generated {args.n} problems in Exercises.txt and Answers.txt.')
    # 检查部分
    elif (args.e or args.a) and (args.n is None and args.r is None):
        if args.e is None or args.a is None:
            print("生成题目格式错误，请输入正确格式：main.exe -e <题目文件路径> -a <答案文件路劲>")
        else:
            # 读取题目和答案数据
            problems = read_problems(args.e)
            answers = read_answers(args.a)

            # 判定答案
            correct_indices, wrong_indices = check_answers(problems, answers)

            # 统计结果
            correct_count = len(correct_indices)
            wrong_count = len(wrong_indices)

            # 将结果写入Grade.txt文件
            write_grade(correct_count, correct_indices, wrong_count, wrong_indices)

            print(f'Correct: {correct_count} ({", ".join(map(str, correct_indices))})')
            print(f'Wrong: {wrong_count} ({", ".join(map(str, wrong_indices))})')

    else:
        print("输入格式错误")
        print("生成题目的正确格式：main.exe -n 10 -r 10")
        print("核对答案的正确格式：main.exe -e <题目文件路径> -a <答案文件路劲>")
