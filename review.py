import random
import json
from pathlib import Path


def load_kana_data():
    try:
        with open('hiragana_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('basic_kana', {}), data.get('youon_kana', {})
    except Exception as e:
        print(f"无法加载五十音图数据: {e}")
        print("使用空数据继续运行...")
        return {}, {}


class ReviewQuiz:
    def __init__(self, basic_kana, youon_kana, results_file):
        self.basic_kana = basic_kana
        self.youon_kana = youon_kana
        self.results_file = results_file
        self.results = self.load_results()

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

    def get_results(self):
        """获取最新结果"""
        return self.results

    def run_review_quiz(self, mistakes, original_mode, original_char_type):
        """运行错题复习测验"""
        print(f"\n=== 开始错题巩固练习（{len(mistakes)}题）===")

        # 从错题中提取所有涉及的字符
        mistake_chars = []
        for _, item, _ in mistakes:
            mistake_chars.extend(item['details']['chars'])

        # 生成复习题目
        review_items = self.generate_review_items(mistake_chars, original_mode, original_char_type)

        if not review_items:
            print("无法生成错题巩固练习题目")
            return

        # 显示所有复习题目
        print("\n==== 复习题目 ====")
        for i, item in enumerate(review_items, 1):
            print(f"{i}. {item['question']}")

        # 收集答案
        print("\n==== 请输入答案 ====")
        user_answers = []
        for i in range(len(review_items)):
            answer = input(f"第 {i+1} 题答案：").strip().lower()
            user_answers.append(answer)

        # 核对答案
        print("\n==== 核对答案 ====")
        score = 0
        new_mistakes = []
        for i, (item, user_answer) in enumerate(zip(review_items, user_answers), 1):
            is_correct = user_answer == item['answer']

            if is_correct:
                print(f"第 {i} 题：✅ 正确！")
                score += 1
            else:
                print(f"第 {i} 题：❌ 错误！正确答案是：{item['answer']}")
                new_mistakes.append((i, item, user_answer))

            # 记录结果
            self.results.append({
                'question': item['question'],
                'user_answer': user_answer,
                'correct_answer': item['answer'],
                'is_correct': is_correct,
                'mode': original_mode,
                'char_type': original_char_type,
                'timestamp': str(Path('').cwd().stat().st_mtime),
                'is_review': True,  # 标记为复习题
                'original_mistake': True if i <= len(mistakes) else False  # 是否是原题的复习
            })

        # 保存结果
        self.save_results()

        # 显示成绩
        print(f"\n=== 巩固练习完成 ===")
        print(f"得分：{score}/{len(review_items)}")
        print(f"正确率：{score/len(review_items)*100:.1f}%")

        # 如果还有错题，询问是否进行薄弱环节强化
        if new_mistakes:
            try:
                weak_choice = input("\n是否针对仍未掌握的字符进行强化练习？(y/n，默认n): ").strip().lower()
                if weak_choice == 'y':
                    self.run_weak_point_quiz(new_mistakes, original_mode, original_char_type)
            except Exception as e:
                print(f"错误: {e}")
                print("跳过强化练习")

    def generate_review_items(self, mistake_chars, mode, char_type):
        """为错题中的字符生成复习题目"""
        items = []

        # 为每个错题生成一个题目
        for char in mistake_chars:
            # 确定字符所在的行
            row_name = None
            row_data = None

            # 先在基础五十音中查找
            for key, data in self.basic_kana.items():
                if char in data['hiragana'] or char in data['katakana'] or char in data['romaji']:
                    row_name = key
                    row_data = data
                    break

            # 如果不在基础五十音中，在拗音中查找
            if not row_data:
                for key, data in self.youon_kana.items():
                    if char in data['hiragana'] or char in data['katakana'] or char in data['romaji']:
                        row_name = key
                        row_data = data
                        break

            # 如果找到了字符所在的行，生成题目
            if row_data:
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

                # 找到字符在该行中的索引
                index = -1
                if char in row_data[source_type]:
                    index = row_data[source_type].index(char)
                elif char in row_data[target_type]:
                    index = row_data[target_type].index(char)

                # 如果找到了索引，生成题目
                if index != -1:
                    question = f"{source_name}「{char}」的对应{target_type}是什么？"
                    answer = row_data[target_type][index]

                    items.append({
                        'question': question,
                        'answer': answer,
                        'details': {
                            'chars': [char],
                            'answers': [answer],
                            'mode': mode,
                            'char_type': char_type,
                            'row_name': row_name
                        }
                    })

        # 如果生成的题目太少，补充一些随机题目
        if len(items) < len(mistake_chars) // 2:
            for _ in range(len(mistake_chars) - len(items)):
                item = self.generate_random_quiz_item(mode, char_type)
                if item:
                    items.append(item)

        return items

    def generate_random_quiz_item(self, mode, char_type):
        """生成随机题目"""
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
        if char_type == 'basic':
            # 只使用基础五十音
            if not self.basic_kana:
                return None
            row_name = random.choice(list(self.basic_kana.keys()))
            row_data = self.basic_kana[row_name]
        elif char_type == 'youon':
            # 只使用拗音
            if not self.youon_kana:
                return None
            row_name = random.choice(list(self.youon_kana.keys()))
            row_data = self.youon_kana[row_name]
        else:  # all
            # 随机选择基础五十音或拗音
            if not self.basic_kana and not self.youon_kana:
                return None
            if (self.basic_kana and not self.youon_kana) or (self.basic_kana and random.random() < 0.7):
                row_name = random.choice(list(self.basic_kana.keys()))
                row_data = self.basic_kana[row_name]
            else:
                row_name = random.choice(list(self.youon_kana.keys()))
                row_data = self.youon_kana[row_name]

        # 随机选择位置
        index = random.randint(0, len(row_data[source_type]) - 1)

        char = row_data[source_type][index]
        answer = row_data[target_type][index]

        question = f"{source_name}「{char}」的对应{target_type}是什么？"

        return {
            'question': question,
            'answer': answer,
            'details': {
                'chars': [char],
                'answers': [answer],
                'mode': mode,
                'char_type': char_type,
                'row_name': row_name
            }
        }

    def run_weak_point_quiz(self, mistakes, original_mode, original_char_type):
        """针对薄弱字符运行强化练习"""
        print(f"\n=== 开始薄弱环节强化练习 ===")

        # 分析错题，找出最薄弱的字符
        weak_chars = {}
        for _, item, _ in mistakes:
            chars = item['details']['chars']
            for char in chars:
                if char in weak_chars:
                    weak_chars[char] += 1
                else:
                    weak_chars[char] = 1

        # 按错误次数排序
        sorted_weak_chars = sorted(weak_chars.items(), key=lambda x: x[1], reverse=True)

        # 选择错误最多的前5个字符进行强化
        chars_to_practice = [char for char, _ in sorted_weak_chars[:5]]

        if not chars_to_practice:
            print("没有需要强化的字符")
            return

        print(f"\n需要强化练习的字符：{', '.join(chars_to_practice)}")

        # 为每个薄弱字符生成3个题目
        need_items = []  # 缩进修正：与上方代码对齐（4个空格）
        for char in chars_to_practice:
            for _ in range(3):
                item = self.generate_quiz_item_for_char(char, original_mode)
                if item:
                    need_items.append(item)

        if not need_items:
            print("无法生成强化练习题目")
            return

        # 打乱题目顺序
        random.shuffle(need_items)

        # 显示所有强化题目
        print(f"\n==== 强化练习题目（共{len(need_items)}题） ====")
        for i, item in enumerate(need_items, 1):
            print(f"{i}. {item['question']}")

        # 收集答案
        print("\n==== 请输入答案 ====")
        user_answers = []
        for i in range(len(need_items)):
            answer = input(f"第 {i+1} 题答案：").strip().lower()
            user_answers.append(answer)

        # 核对答案
        print("\n==== 核对答案 ====")
        score = 0
        for i, (item, user_answer) in enumerate(zip(need_items, user_answers), 1):
            is_correct = user_answer == item['answer']

            if is_correct:
                print(f"第 {i} 题：✅ 正确！")
                score += 1
            else:
                print(f"第 {i} 题：❌ 错误！正确答案是：{item['answer']}")

            # 记录结果
            self.results.append({
                'question': item['question'],
                'user_answer': user_answer,
                'correct_answer': item['answer'],
                'is_correct': is_correct,
                'mode': original_mode,
                'char_type': original_char_type,
                'timestamp': str(Path('').cwd().stat().st_mtime),
                'is_review': True,  # 标记为复习题
                'is_weak_point': True  # 标记为薄弱环节强化
            })

        # 保存结果
        self.save_results()

        # 显示成绩
        print(f"\n=== 强化练习完成 ===")
        print(f"得分：{score}/{len(need_items)}")
        print(f"正确率：{score/len(need_items)*100:.1f}%")

        # 显示进步情况
        if score == len(need_items):
            print("\n🎉 恭喜！所有薄弱字符都已掌握！")
        else:
            print("\n继续加油！建议针对仍未掌握的字符进行更多练习。")

    def generate_quiz_item_for_char(self, char, mode):
        """为特定字符生成题目"""
        # 确定字符所在的行
        row_name = None
        row_data = None

        # 先在基础五十音中查找
        for key, data in self.basic_kana.items():
            if char in data['hiragana'] or char in data['katakana'] or char in data['romaji']:
                row_name = key
                row_data = data
                break

        # 如果不在基础五十音中，在拗音中查找
        if not row_data:
            for key, data in self.youon_kana.items():
                if char in data['hiragana'] or char in data['katakana'] or char in data['romaji']:
                    row_name = key
                    row_data = data
                    break

        # 如果找到了字符所在的行，生成题目
        if row_data:
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

            # 找到字符在该行中的索引
            index = -1
            if char in row_data[source_type]:
                index = row_data[source_type].index(char)
            elif char in row_data[target_type]:
                index = row_data[target_type].index(char)

            # 如果找到了索引，生成题目
            if index != -1:
                question = f"{source_name}「{char}」的对应{target_type}是什么？"
                answer = row_data[target_type][index]

                return {
                    'question': question,
                    'answer': answer,
                    'details': {
                        'chars': [char],
                        'answers': [answer],
                        'mode': mode,
                        'row_name': row_name
                    }
                }

        return None


if __name__ == "__main__":
    basic_kana, youon_kana = load_kana_data()
    results_file = Path('hiragana_quiz_results.json')
    reviewer = ReviewQuiz(basic_kana, youon_kana, results_file)
