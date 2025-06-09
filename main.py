import random
import json
from pathlib import Path
from mistake import MistakeAnalyzer
from review import ReviewQuiz


class HiraganaQuiz:
    def __init__(self):
        # 从JSON文件加载五十音图数据
        self.basic_kana, self.youon_kana = self.load_kana_data()

        # 结果记录文件
        self.results_file = Path('hiragana_quiz_results.json')
        self.results = self.load_results()

        # 练习模式
        self.modes = {
            'hira_to_roma': '平假名→罗马音',
            'kata_to_roma': '片假名→罗马音',
            'roma_to_hira': '罗马音→平假名',
            'roma_to_kata': '罗马音→片假名',
            'mix': '混合模式'
        }

        # 字符类型
        self.char_types = {
            'basic': '基础五十音',
            'youon': '拗音',
            'all': '全部字符'
        }

        # 错题分析器
        self.analyzer = MistakeAnalyzer(self.basic_kana, self.youon_kana)

        # 复习测验器
        self.review_quiz = ReviewQuiz(self.basic_kana, self.youon_kana, self.results_file)

    def load_kana_data(self):
        """从JSON文件加载五十音图数据"""
        try:
            with open('hiragana_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('basic_kana', {}), data.get('youon_kana', {})
        except Exception as e:
            print(f"无法加载五十音图数据: {e}")
            print("使用空数据继续运行...")
            return {}, {}

    def load_results(self):
        """加载历史答题记录"""
        if self.results_file.exists():
            try:
                return json.loads(self.results_file.read_text(encoding='utf-8'))
            except:
                print("无法加载历史记录，将创建新记录")
        return []

    def save_results(self):
        """保存答题记录"""
        self.results_file.write_text(json.dumps(self.results, ensure_ascii=False, indent=2), encoding='utf-8')

    def generate_quiz_items(self, num_questions=5, mode='hira_to_roma', chars_per_question=2, char_type='all', unique_chars=True):
        """生成一批测验题目，每个题目包含多个字符"""
        # 已使用的字符集合（根据模式决定使用哪种字符类型）
        used_chars = set()

        # 根据模式确定需要跟踪的字符类型
        if mode.startswith('hira'):
            track_type = 'hiragana'
        elif mode.startswith('kata'):
            track_type = 'katakana'
        else:  # roma_to_*
            track_type = 'romaji'

        items = []
        for _ in range(num_questions):
            # 尝试生成不重复的题目
            max_attempts = 100
            for _ in range(max_attempts):
                item = self.generate_quiz_item(mode, chars_per_question, char_type)

                # 检查是否有重复字符
                has_duplicate = False
                for char in item['details']['chars']:
                    if char in used_chars:
                        has_duplicate = True
                        break

                # 如果没有重复或者不要求唯一，则添加该题目
                if not has_duplicate or not unique_chars:
                    # 添加新字符到已使用集合
                    if unique_chars:
                        for char in item['details']['chars']:
                            used_chars.add(char)
                    items.append(item)
                    break
            else:
                # 如果尝试多次仍无法生成唯一字符，使用当前可能有重复的题目
                items.append(self.generate_quiz_item(mode, chars_per_question, char_type))

        return items

    def generate_quiz_item(self, mode='hira_to_roma', chars_per_question=2, char_type='all'):
        """生成单个测验题目，包含多个字符"""
        # 确保每个题目至少有1个字符
        chars_per_question = max(1, chars_per_question)

        if mode == 'mix':
            # 混合模式：随机选择一种练习类型
            mode = random.choice(['hira_to_roma', 'kata_to_roma', 'roma_to_hira', 'roma_to_kata'])

        # 根据模式确定字符类型和目标类型
        if mode.startswith('hira'):
            source_type = 'hiragana'
            target_type = 'romaji'
            source_name = '平假名'
        elif mode.startswith('kata'):
            source_type = 'katakana'
            target_type = 'romaji'
            source_name = '片假名'
        elif mode.startswith('roma') and mode.endswith('hira'):
            source_type = 'romaji'
            target_type = 'hiragana'
            source_name = '罗马音'
        else:  # roma_to_kata
            source_type = 'romaji'
            target_type = 'katakana'
            source_name = '罗马音'

        # 随机选择字符
        selected_chars = []
        answers = []

        for _ in range(chars_per_question):
            # 根据字符类型选择数据源
            if char_type == 'basic':
                # 只使用基础五十音
                if not self.basic_kana:
                    continue
                row_name = random.choice(list(self.basic_kana.keys()))
                row_data = self.basic_kana[row_name]
            elif char_type == 'youon':
                # 只使用拗音
                if not self.youon_kana:
                    continue
                row_name = random.choice(list(self.youon_kana.keys()))
                row_data = self.youon_kana[row_name]
            else:  # all
                # 随机选择基础五十音或拗音
                if not self.basic_kana and not self.youon_kana:
                    continue
                if (self.basic_kana and not self.youon_kana) or (self.basic_kana and random.random() < 0.7):
                    row_name = random.choice(list(self.basic_kana.keys()))
                    row_data = self.basic_kana[row_name]
                else:
                    row_name = random.choice(list(self.youon_kana.keys()))
                    row_data = self.youon_kana[row_name]

            # 随机选择位置
            index = random.randint(0, len(row_data[source_type]) - 1)

            selected_chars.append(row_data[source_type][index])
            answers.append(row_data[target_type][index])

        # 构建问题和答案
        if not selected_chars:
            return self.generate_quiz_item(mode, chars_per_question, char_type)

        question = f"{source_name}「{'、'.join(selected_chars)}」的对应{target_type}是什么？（用空格分隔）"
        answer = " ".join(answers)

        return {
            'type': 'multi_char_quiz',
            'question': question,
            'answer': answer,
            'details': {
                'chars': selected_chars,
                'answers': answers,
                'mode': mode,
                'char_type': char_type,
                'row_name': row_name
            }
        }

    def run_batch_quiz(self, num_questions=5, mode='hira_to_roma', chars_per_question=2, char_type='all', unique_chars=True):
        """运行批量测验"""
        unique_text = "（字符不重复）" if unique_chars else ""
        print(f"=== {self.modes[mode]}批量练习（每题{chars_per_question}个字符，{self.char_types[char_type]}{unique_text}）===")

        # 生成题目
        quiz_items = self.generate_quiz_items(num_questions, mode, chars_per_question, char_type, unique_chars)

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
            is_correct = user_answer == item['answer']

            if is_correct:
                print(f"第 {i} 题：✅ 正确！")
                score += 1
            else:
                print(f"第 {i} 题：❌ 错误！正确答案是：{item['answer']}")
                mistakes.append((i, item, user_answer))

            # 记录结果
            self.results.append({
                'question': item['question'],
                'user_answer': user_answer,
                'correct_answer': item['answer'],
                'is_correct': is_correct,
                'mode': mode,
                'char_type': char_type,
                'timestamp': str(Path('').cwd().stat().st_mtime),
                'is_review': False  # 是否为复习题
            })

        # 保存结果
        self.save_results()

        # 显示成绩
        print(f"\n=== 测验完成 ===")
        print(f"得分：{score}/{num_questions}")
        print(f"正确率：{score/num_questions*100:.1f}%")

        # 显示历史统计
        self.analyzer.analyze_history(self.results, mode, char_type)

        # 如果有错题，询问是否进行巩固练习
        if mistakes:
            try:
                review_choice = input("\n是否针对错题进行巩固练习？(y/n，默认n): ").strip().lower()
                if review_choice == 'y':
                    self.review_quiz.run_review_quiz(mistakes, mode, char_type)

                    # 更新结果
                    self.results = self.review_quiz.get_results()

                    # 分析薄弱环节
                    self.analyzer.analyze_weak_points(mistakes)
            except Exception as e:
                print(f"错误: {e}")
                print("跳过巩固练习")


if __name__ == "__main__":
    quiz = HiraganaQuiz()

    # 选择练习模式
    print("请选择练习模式：")
    for i, (key, value) in enumerate(quiz.modes.items(), 1):
        print(f"{i}. {value}")

    try:
        mode_choice = int(input("请输入数字 (1-5): "))
        mode = list(quiz.modes.keys())[mode_choice - 1]
    except:
        mode = 'mix'
        print("输入无效，使用默认模式：混合模式")

    # 选择字符类型
    print("\n请选择字符类型：")
    for i, (key, value) in enumerate(quiz.char_types.items(), 1):
        print(f"{i}. {value}")

    try:
        char_choice = int(input("请输入数字 (1-3): "))
        char_type = list(quiz.char_types.keys())[char_choice - 1]
    except:
        char_type = 'all'
        print("输入无效，使用默认类型：全部字符")

    # 选择题目数量
    try:
        num_questions = int(input("请输入题目数量 (默认5): ") or "5")
    except:
        num_questions = 5
        print("输入无效，使用默认值5")

    # 选择每题字符数量
    try:
        chars_per_question = int(input("请输入每题字符数量 (默认2): ") or "2")
    except:
        chars_per_question = 2
        print("输入无效，使用默认值2")

    # 选择是否使用不重复字符
    try:
        unique_choice = input("是否使用不重复字符？(y/n，默认y): ").strip().lower()
        unique_chars = unique_choice != 'n'
    except:
        unique_chars = True
        print("输入无效，使用默认设置：不重复字符")

    # 开始批量测验
    quiz.run_batch_quiz(num_questions, mode, chars_per_question, char_type, unique_chars)
