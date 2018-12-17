from berlekamp_massey import simple_bm, print_int_polynome, int_to_bin
import argparse

VSRSION = "1.01"


def get_args():
    parser = argparse.ArgumentParser(description="一个基于 BM 算法的序列生成器", epilog="henry@hejunlin.cn")
    parser.add_argument("-d", "--debug", dest="debug", type=int, default=None, choices=[1, 2, 3], help="调试等级，用于控制输出信息。1 - 基础输出，包含推导更新多项式的输出。2 - 丰富输出，包含推导更新多项式的更多信息输出。3 - 作业级别的输出，运行，复制，提交作业即可。")
    parser.add_argument("-l", "--language", dest="language", type=str, choices=["ch", "en"], help="在作业输出模式下的语言控制。")
    parser.add_argument("-v", "--version", help=VSRSION)
    parser.add_argument("flow", type=str, help="序列")
    arguments = parser.parse_args()
    return arguments


def main():
    arguments = get_args()
    flow = input_proc(arguments.flow)
    [fx, l] = simple_bm(flow, debug=arguments.debug)
    print("输入序列为：" + arguments.flow + "\n可以生成此序列的最优为 " + str(l) + " 级线性反馈移位寄存器\n该寄存器的连接多项式为：", end="")
    print_int_polynome(int_to_bin(fx), with_fx=0)


def input_proc(input):
    '''
    处理两种输入："101010101101",101010101101，可以判断输入是否正确
    '''
    to_str = str(input)
    to_list = list(to_str)
    to_bin_list = []
    for i in to_list:
        try:
            i = int(i)
        except Exception as ex:
            print(ex)
            raise TypeError
        if i in [1, 0]:
            to_bin_list.append(i)
        else:
            raise TypeError
    return to_bin_list


if __name__ == "__main__":
    main()