from typing import Any, Dict, List

from utils import load_kana_data


class Quiz:
    def __init__(self) -> None:
        self.basic_kana, _ = load_kana_data()
        self.row_name = list(self.basic_kana.keys())
        self.total_hira: List[str] = []  # 所有的平假名
        self.total_kata: List[str] = []  # 所有的片假名
        self.total_roma: List[str] = []  # 所有的罗马音

        self.modes: List[str] = [
            "罗马音->片假名",
            "罗马音->平假名",
        ]

    def _gen_quiz_items(
        self, mode_choice: int, row_choice: int
    ) -> List[Dict[str, Any]]:
        if mode_choice > len(self.modes) - 1:
            raise ValueError(f"mode must be in 0-{len(self.modes)-1}")
        if row_choice > len(self.row_name) - 1:
            raise ValueError(f"row must be in 0-{len(self.row_name)-1}")

        items = []
        if mode_choice == 0:
            source_type = "罗马音"
            target_type = "片假名"
            for i in range(row_choice + 1):
                row_name = self.row_name[i]
                selected_char = self.basic_kana[row_name]["romaji"]
                selected_answer = self.basic_kana[row_name]["katakana"]
                question = f"{source_type}「{'、'.join(selected_char)}」的对应{target_type}是什么？（用空格分隔）"
                answer = " ".join(selected_answer)

                item = {
                    "type": self.modes[mode_choice],
                    "question": question,
                    "answer": answer,
                    "details": {
                        "chars": selected_char,
                        "answers": answer,
                        "mode": self.modes[mode_choice],
                    },
                }
                items.append(item)

        elif mode_choice == 1:
            source_type = "罗马音"
            target_type = "平假名"
            for i in range(row_choice + 1):
                row_name = self.row_name[i]
                selected_char = self.basic_kana[row_name]["romaji"]
                selected_answer = self.basic_kana[row_name]["hiragana"]
                question = f"{source_type}「{'、'.join(selected_char)}」的对应{target_type}是什么？（用空格分隔）"
                answer = " ".join(selected_answer)

                item = {
                    "type": self.modes[mode_choice],
                    "question": question,
                    "answer": answer,
                    "details": {
                        "chars": selected_char,
                        "answers": answer,
                        "mode": self.modes[mode_choice],
                    },
                }
                items.append(item)
        else:
            raise ValueError("Unknown mode.")

        return items

    def gen_question(self, mode_choice: int, row_choice: int) -> None:

        items = self._gen_quiz_items(mode_choice, row_choice)
        mistake = []

        for i, item in enumerate(items):
            print("\n==== 题目 ====")
            print(f"{i}. {item['question']}")

            print("\n==== 请输入答案 ====")
            answer = input(f"第 {i} 题答案: ").strip().lower()
            is_correct = answer == item["answer"]

            if is_correct:
                print("✅ 正确！")
            else:
                print(f"❌ 错误！正确答案是：{item['answer']}")
                mistake.append(item)

        # 总结错题
        print("\n ==== 错题总结 ====")
        for item in mistake:
            print("\n==== 题目 ====")
            print(item["question"])
            print("\n==== 答案 ====")
            print(item["answer"])


if __name__ == "__main__":
    quiz = Quiz()

    print("请选择练习模式: ")
    for i, value in enumerate(quiz.modes):
        print(f"{i}. {value}")

    try:
        mode_choice = int(input())
    except Exception as e:
        raise ValueError(f"Unknown mode: {e}")

    print("请问你想从哪行开始: ")
    for i, value in enumerate(quiz.row_name):
        print(f"{i}. {value}")

    try:
        row_choice = int(input())
    except Exception as e:
        raise ValueError(f"Unknown row name: {e}")

    quiz.gen_question(mode_choice, row_choice)
