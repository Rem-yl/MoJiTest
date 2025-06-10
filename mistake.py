import json
from pathlib import Path
from typing import Any, Dict, List, Set


class MistakeReviewer:
    def __init__(
        self, json_file: str, reviewed_file: str = "reviewed_mistakes.json"
    ) -> None:
        self.json_file = Path(json_file)
        self.reviewed_file = Path(reviewed_file)
        self.reviewed = self.load_reviewed()  # 先初始化 self.reviewed
        self.mistakes = self.load_mistakes()  # 再调用依赖 self.reviewed 的方法

    def load_mistakes(self) -> List[Any]:
        """加载未复习的错题数据"""
        try:
            with open(self.json_file, "r", encoding="utf-8") as f:
                all_mistakes = json.load(f)
                # 过滤已复习的题目和正确题目
                return [
                    item
                    for item in all_mistakes
                    if not item["is_correct"] and item["question"] not in self.reviewed
                ]
        except FileNotFoundError:
            print("错误：未找到错题文件")
            return []
        except json.JSONDecodeError:
            print("错误：JSON文件格式不正确")
            return []

    def load_reviewed(self) -> Set[str]:
        """加载已复习的题目记录"""
        if self.reviewed_file.exists():
            try:
                with open(self.reviewed_file, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception as _:
                return set()
        return set()

    def save_reviewed(self, question: str) -> None:
        """保存已复习的题目"""
        reviewed = self.reviewed.copy()
        reviewed.add(question)
        with open(self.reviewed_file, "w", encoding="utf-8") as f:
            json.dump(list(reviewed), f, ensure_ascii=False, indent=2)

    def display_mistakes(self) -> None:
        """显示所有未复习的错题详情"""
        if not self.mistakes:
            print("没有未复习的错题记录")
            return

        print(f"\n=== 共有 {len(self.mistakes)} 道未复习错题 ===")
        for idx, mistake in enumerate(self.mistakes, 1):
            print(f"\n第 {idx} 题")
            print(f"题目: {mistake['question']}")
            print(f"你的答案: {mistake['user_answer']}")
            print(f"正确答案: {mistake['correct_answer']}")
            print(f"模式: {mistake['mode']} - {mistake['char_type']}")
            print("-" * 40)

    def generate_review_questions(self) -> List[Dict[str, str]]:
        """生成未复习的复习题目"""
        return [
            {
                "question": mistake["question"],
                "answer": mistake["correct_answer"].split(),
            }
            for mistake in self.mistakes
        ]

    def run_review_quiz(self) -> None:
        """运行复习测验并标记已掌握的题目"""
        review_questions = self.generate_review_questions()
        if not review_questions:
            print("没有可复习的未掌握题目")
            return

        print("\n=== 开始复习测验 ===")
        score = 0
        total = len(review_questions)

        for i, question_data in enumerate(review_questions, 1):
            print(f"\n第 {i}/{total} 题")
            print(question_data["question"])
            user_answer = input("请输入答案：").strip().lower()

            user_answer_list = user_answer.split()
            correct_answer_list = [ans.lower() for ans in question_data["answer"]]
            is_correct = user_answer_list == correct_answer_list

            if is_correct:
                print("✅ 正确！该题已标记为已掌握")
                score += 1
                self.save_reviewed(question_data["question"])  # 标记为已复习
            else:
                print(f"❌ 错误！正确答案：{' '.join(correct_answer_list)}")

        print("\n=== 复习完成 ===")
        print(f"得分：{score}/{total}")
        print(f"正确率：{score/total*100:.1f}%")
        print(f"已掌握题目数量：{score}")
        print(f"剩余未掌握题目数量：{total - score}")


if __name__ == "__main__":
    # 替换为你的JSON文件路径
    json_file = "hiragana_quiz_results.json"
    reviewer = MistakeReviewer(json_file)

    # 显示未复习的错题
    reviewer.display_mistakes()

    # 运行复习测验
    review_choice = input("\n是否开始复习测验？(y/n): ").strip().lower()
    if review_choice == "y":
        reviewer.run_review_quiz()
        print("\n下次复习将自动跳过已掌握的题目")
