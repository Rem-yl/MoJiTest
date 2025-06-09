import json
import random
from pathlib import Path
from typing import Any, Dict, List

from utils import load_kana_data, load_result_data


class HiraganaQuiz:
    def __init__(self) -> None:
        # 从JSON文件加载五十音图数据
        self.basic_kana, self.youon_kana = load_kana_data()
        self.total_hira: List[str] = []  # 所有的平假名
        self.total_kata: List[str] = []  # 所有的片假名
        self.total_roma: List[str] = []  # 所有的罗马音

        # 结果记录文件
        self.results_file = Path("hiragana_quiz_results.json")
        self.results = load_result_data(self.results_file)

        # 练习模式
        self.modes = {
            "hira_to_roma": "平假名→罗马音",
            "kata_to_roma": "片假名→罗马音",
            "roma_to_hira": "罗马音→平假名",
            "roma_to_kata": "罗马音→片假名",
        }

        # 字符类型
        self.char_types = {"basic": "基础五十音", "youon": "拗音", "all": "全部字符"}

    def save_results(self) -> None:
        """保存答题记录"""
        self.results_file.write_text(
            json.dumps(self.results, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _load_basic_total(self) -> None:
        for _, row_value in self.basic_kana.items():
            for key, value in row_value.items():
                if key.startswith("hira"):
                    self.total_hira.extend(value)
                elif key.startswith("kata"):
                    self.total_kata.extend(value)
                elif key.startswith("roma"):
                    self.total_roma.extend(value)
                else:
                    raise ValueError(f"Unknown key: {key}")

    def _load_youon_total(self) -> None:
        for _, row_value in self.youon_kana.items():
            for key, value in row_value.items():
                if key.startswith("hira"):
                    self.total_hira.extend(value)
                elif key.startswith("kata"):
                    self.total_kata.extend(value)
                elif key.startswith("roma"):
                    self.total_roma.extend(value)
                else:
                    raise ValueError(f"Unknown key: {key}")

    def _generate_quiz_item(
        self, mode: str, num_questions: int, chars_per_question: int
    ) -> List[Dict[str, Any]]:
        total = len(self.total_roma)
        index = [i for i in range(total)]
        random.shuffle(index)
        total_nums = num_questions * chars_per_question
        index = index[:total_nums]

        selected_chars = []
        answers = []

        if mode == "hira_to_roma":
            selected_chars.extend([self.total_hira[i] for i in index])
            answers.extend([self.total_roma[i] for i in index])
            source_type = "平假名"
            target_type = "罗马音"
        elif mode == "kata_to_roma":
            selected_chars.extend([self.total_kata[i] for i in index])
            answers.extend([self.total_roma[i] for i in index])
            source_type = "片假名"
            target_type = "罗马音"
        elif mode == "roma_to_hira":
            selected_chars.extend([self.total_roma[i] for i in index])
            answers.extend([self.total_hira[i] for i in index])
            source_type = "罗马音"
            target_type = "平假名"
        elif mode == "roma_to_kata":
            selected_chars.extend([self.total_roma[i] for i in index])
            answers.extend([self.total_hira[i] for i in index])
            source_type = "罗马音"
            target_type = "片假名"
        else:
            raise ValueError(f"Unknown mode: {mode}")

        items = []
        for i in range(0, total_nums, chars_per_question):
            selected_char = selected_chars[i : i + chars_per_question]
            selected_answer = answers[i : i + chars_per_question]

            question = f"{source_type}「{'、'.join(selected_char)}」的对应{target_type}是什么？（用空格分隔）"
            answer = " ".join(selected_answer)

            item = {
                "type": "multi_char_quiz",
                "question": question,
                "answer": answer,
                "details": {
                    "chars": selected_chars,
                    "answers": answers,
                    "mode": mode,
                },
            }
            items.append(item)

        return items

    def generate_quiz_items(
        self,
        num_questions: int = 5,
        mode: str = "hira_to_roma",
        chars_per_question: int = 2,
        char_type: str = "all",
    ) -> List[Dict[str, Any]]:
        """生成一批测验题目，每个题目包含多个字符"""
        if char_type == "basic":
            self._load_basic_total()
        elif char_type == "youon":
            self._load_youon_total()
        elif char_type == "all":
            self._load_basic_total()
            self._load_youon_total()
        else:
            raise ValueError(f"Unknown char_type: {char_type}")

        items = self._generate_quiz_item(mode, num_questions, chars_per_question)

        return items

    def run_batch_quiz(
        self,
        num_questions: int = 5,
        mode: str = "hira_to_roma",
        chars_per_question: int = 2,
        char_type: str = "all",
    ) -> None:
        """运行批量测验"""
        unique_text = "（字符不重复）"
        print(
            f"=== {self.modes[mode]}批量练习（每题{chars_per_question}个字符，{self.char_types[char_type]}{unique_text}）==="
        )

        # 生成题目
        quiz_items = self.generate_quiz_items(
            num_questions, mode, chars_per_question, char_type
        )

        # 显示所有题目
        print("\n==== 题目 ====")
        for i, item in enumerate(quiz_items, 1):
            print(f"{i}. {item['question']}")

        # 收集答案
        print("\n==== 请输入答案 ====")
        user_answers = []
        for i in range(num_questions):
            answer = input(f"第 {i+1} 题答案：").strip().lower()
            user_answers.append(answer)

        # 核对答案
        print("\n==== 核对答案 ====")
        score = 0
        mistakes = []
        for i, (item, user_answer) in enumerate(zip(quiz_items, user_answers), 1):
            is_correct = user_answer == item["answer"]

            if is_correct:
                print(f"第 {i} 题：✅ 正确！")
                score += 1
            else:
                print(f"第 {i} 题：❌ 错误！正确答案是：{item['answer']}")
                mistakes.append((i, item, user_answer))

            # 记录结果
            self.results.append(
                {
                    "question": item["question"],
                    "user_answer": user_answer,
                    "correct_answer": item["answer"],
                    "is_correct": is_correct,
                    "mode": mode,
                    "char_type": char_type,
                    "timestamp": str(Path("").cwd().stat().st_mtime),
                    "is_review": False,  # 是否为复习题
                }
            )

        # 保存结果
        self.save_results()
        print(f"测验结果保存在: {self.results_file.as_posix()}")

        # 显示成绩
        print("\n=== 测验完成 ===")
        print(f"得分：{score}/{num_questions}")
        print(f"正确率：{score/num_questions*100:.1f}%")


if __name__ == "__main__":
    quiz = HiraganaQuiz()

    # 选择练习模式
    print("请选择练习模式：")
    for i, (key, value) in enumerate(quiz.modes.items(), 1):
        print(f"{i}. {value}")

    try:
        mode_choice = int(input("请输入数字 (1-5): "))
        mode = list(quiz.modes.keys())[mode_choice - 1]
    except Exception as e:
        raise ValueError(f"Unknown mode: {e}")

    # 选择字符类型
    print("\n请选择字符类型: ")
    for i, (key, value) in enumerate(quiz.char_types.items(), 1):
        print(f"{i}. {value}")

    try:
        char_choice = int(input())
        char_type = list(quiz.char_types.keys())[char_choice - 1]
    except Exception as e:
        raise ValueError(f"Unknown char type: {e}")

    # 选择题目数量
    try:
        num_questions = int(input("请输入题目数量 (默认5): ") or "5")
    except Exception as _:
        num_questions = 5
        print("输入无效，使用默认值5")

    # 选择每题字符数量
    try:
        chars_per_question = int(input("请输入每题字符数量 (默认2): ") or "2")
    except Exception as _:
        chars_per_question = 2
        print("输入无效，使用默认值2")

    # 开始批量测验
    quiz.run_batch_quiz(num_questions, mode, chars_per_question, char_type)
