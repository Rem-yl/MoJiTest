import pandas as pd
import argparse
import os


def csv_to_markdown(input_file: str, output_file: str) -> None:
    """将CSV文件转换为Markdown表格并保存"""
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件 {input_file} 不存在")

    try:
        # 读取CSV文件，假设文件有三列：日语、罗马音、中文
        df = pd.read_csv(input_file, encoding='utf-8', header=None, names=['Japanese', 'Romaji', 'Chinese'])

        # 构建Markdown表格
        md_table = "| 日语 | 罗马音 | 中文 |\n| ---- | ---- | ---- |\n"
        for index, row in df.iterrows():
            md_table += f"| {row['Japanese']} | {row['Romaji']} | {row['Chinese']} |\n"

        # 保存Markdown文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_table)

        print(f"✅ 成功将 {input_file} 转换为 Markdown 表格并保存至 {output_file}")

    except pd.errors.EmptyDataError:
        print("错误：CSV文件为空")
    except pd.errors.ParserError:
        print("错误：CSV文件解析失败，请检查文件格式")
    except Exception as e:
        print(f"处理文件时发生错误：{str(e)}")


def main():
    """命令行参数解析主函数"""
    parser = argparse.ArgumentParser(description='将CSV文件转换为Markdown表格')

    # 输入CSV文件路径（必填参数）
    parser.add_argument('-i', '--input', required=True,
                        help='输入CSV文件路径（需包含日语、罗马音、中文三列）')

    # 输出Markdown文件路径（可选，默认生成在当前目录）
    parser.add_argument('-o', '--output', default='vocab_table.md',
                        help='输出Markdown文件路径（默认：vocab_table.md）')

    # 解析命令行参数
    args = parser.parse_args()

    # 执行转换
    csv_to_markdown(args.input, args.output)


if __name__ == "__main__":
    main()
