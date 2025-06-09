import random
import json
from pathlib import Path


class HiraganaQuiz:
    def __init__(self):
        # 基础五十音图数据（平假名、片假名和罗马音）
        self.basic_kana = {
            'あ行': {'hiragana': ['あ', 'い', 'う', 'え', 'お'],
                   'katakana': ['ア', 'イ', 'ウ', 'エ', 'オ'],
                   'romaji': ['a', 'i', 'u', 'e', 'o']},
            'か行': {'hiragana': ['か', 'き', 'く', 'け', 'こ'],
                   'katakana': ['カ', 'キ', 'ク', 'ケ', 'コ'],
                   'romaji': ['ka', 'ki', 'ku', 'ke', 'ko']},
            'が行': {'hiragana': ['が', 'ぎ', 'ぐ', 'げ', 'ご'],
                   'katakana': ['ガ', 'ギ', 'グ', 'ゲ', 'ゴ'],
                   'romaji': ['ga', 'gi', 'gu', 'ge', 'go']},
            'さ行': {'hiragana': ['さ', 'し', 'す', 'せ', 'そ'],
                   'katakana': ['サ', 'シ', 'ス', 'セ', 'ソ'],
                   'romaji': ['sa', 'shi', 'su', 'se', 'so']},
            'ざ行': {'hiragana': ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'],
                   'katakana': ['ザ', 'ジ', 'ズ', 'ゼ', 'ゾ'],
                   'romaji': ['za', 'ji', 'zu', 'ze', 'zo']},
            'た行': {'hiragana': ['た', 'ち', 'つ', 'て', 'と'],
                   'katakana': ['タ', 'チ', 'ツ', 'テ', 'ト'],
                   'romaji': ['ta', 'chi', 'tsu', 'te', 'to']},
            'だ行': {'hiragana': ['だ', 'ぢ', 'づ', 'で', 'ど'],
                   'katakana': ['ダ', 'ヂ', 'ヅ', 'デ', 'ド'],
                   'romaji': ['da', 'ji', 'zu', 'de', 'do']},
            'な行': {'hiragana': ['な', 'に', 'ぬ', 'ね', 'の'],
                   'katakana': ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'],
                   'romaji': ['na', 'ni', 'nu', 'ne', 'no']},
            'は行': {'hiragana': ['は', 'ひ', 'ふ', 'へ', 'ほ'],
                   'katakana': ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'],
                   'romaji': ['ha', 'hi', 'fu', 'he', 'ho']},
            'ば行': {'hiragana': ['ば', 'び', 'ぶ', 'べ', 'ぼ'],
                   'katakana': ['バ', 'ビ', 'ブ', 'ベ', 'ボ'],
                   'romaji': ['ba', 'bi', 'bu', 'be', 'bo']},
            'ぱ行': {'hiragana': ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'],
                   'katakana': ['パ', 'ピ', 'プ', 'ペ', 'ポ'],
                   'romaji': ['pa', 'pi', 'pu', 'pe', 'po']},
            'ま行': {'hiragana': ['ま', 'み', 'む', 'め', 'も'],
                   'katakana': ['マ', 'ミ', 'ム', 'メ', 'モ'],
                   'romaji': ['ma', 'mi', 'mu', 'me', 'mo']},
            'や行': {'hiragana': ['や', 'ゆ', 'よ'],
                   'katakana': ['ヤ', 'ユ', 'ヨ'],
                   'romaji': ['ya', 'yu', 'yo']},
            'ら行': {'hiragana': ['ら', 'り', 'る', 'れ', 'ろ'],
                   'katakana': ['ラ', 'リ', 'ル', 'レ', 'ロ'],
                   'romaji': ['ra', 'ri', 'ru', 're', 'ro']},
            'わ行': {'hiragana': ['わ', 'を', 'ん'],
                   'katakana': ['ワ', 'ヲ', 'ン'],
                   'romaji': ['wa', 'wo', 'n']}
        }

        # 拗音数据
        self.youon_kana = {
            'きゃきゅきょ': {'hiragana': ['きゃ', 'きゅ', 'きょ'],
                       'katakana': ['キャ', 'キュ', 'キョ'],
                       'romaji': ['kya', 'kyu', 'kyo']},
            'ぎゃぎゅぎょ': {'hiragana': ['ぎゃ', 'ぎゅ', 'ぎょ'],
                       'katakana': ['ギャ', 'ギュ', 'ギョ'],
                       'romaji': ['gya', 'gyu', 'gyo']},
            'しゃしゅしょ': {'hiragana': ['しゃ', 'しゅ', 'しょ'],
                       'katakana': ['シャ', 'シュ', 'ショ'],
                       'romaji': ['sha', 'shu', 'sho']},
            'じゃじゅじょ': {'hiragana': ['じゃ', 'じゅ', 'じょ'],
                       'katakana': ['ジャ', 'ジュ', 'ジョ'],
                       'romaji': ['ja', 'ju', 'jo']},
            'ちゃちゅちょ': {'hiragana': ['ちゃ', 'ちゅ', 'ちょ'],
                       'katakana': ['チャ', 'チュ', 'チョ'],
                       'romaji': ['cha', 'chu', 'cho']},
            'ぢゃぢゅぢょ': {'hiragana': ['ぢゃ', 'ぢゅ', 'ぢょ'],
                       'katakana': ['ヂャ', 'ヂュ', 'ヂョ'],
                       'romaji': ['ja', 'ju', 'jo']},
            'にゃにゅにょ': {'hiragana': ['にゃ', 'にゅ', 'にょ'],
                       'katakana': ['ニャ', 'ニュ', 'ニョ'],
                       'romaji': ['nya', 'nyu', 'nyo']},
            'ひゃひゅひょ': {'hiragana': ['ひゃ', 'ひゅ', 'ひょ'],
                       'katakana': ['ヒャ', 'ヒュ', 'ヒョ'],
                       'romaji': ['hya', 'hyu', 'hyo']},
            'びゃびゅびょ': {'hiragana': ['びゃ', 'びゅ', 'びょ'],
                       'katakana': ['ビャ', 'ビュ', 'ビョ'],
                       'romaji': ['bya', 'byu', 'byo']},
            'ぴゃぴゅぴょ': {'hiragana': ['ぴゃ', 'ぴゅ', 'ぴょ'],
                       'katakana': ['ピャ', 'ピュ', 'ピョ'],
                       'romaji': ['pya', 'pyu', 'pyo']},
            'みゃみゅみょ': {'hiragana': ['みゃ', 'みゅ', 'みょ'],
                       'katakana': ['ミャ', 'ミュ', 'ミョ'],
                       'romaji': ['mya', 'myu', 'myo']},
            'りゃりゅりょ': {'hiragana': ['りゃ', 'りゅ', 'りょ'],
                       'katakana': ['リャ', 'リュ', 'リョ'],
                       'romaji': ['rya', 'ryu', 'ryo']}
        }

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

    def generate_quiz_items(self, num_questions=5, mode='hira_to_roma', chars_per_question=2, char_type='all'):
        """生成一批测验题目，每个题目包含多个字符"""
        items = []
        for _ in range(num_questions):
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
                row_name = random.choice(list(self.basic_kana.keys()))
                row_data = self.basic_kana[row_name]
            elif char_type == 'youon':
                # 只使用拗音
                row_name = random.choice(list(self.youon_kana.keys()))
                row_data = self.youon_kana[row_name]
            else:  # all
                # 随机选择基础五十音或拗音
                if random.random() < 0.7:  # 70%概率选择基础五十音
                    row_name = random.choice(list(self.basic_kana.keys()))
                    row_data = self.basic_kana[row_name]
                else:  # 30%概率选择拗音
                    row_name = random.choice(list(self.youon_kana.keys()))
                    row_data = self.youon_kana[row_name]

            # 随机选择位置
            index = random.randint(0, len(row_data[source_type]) - 1)

            selected_chars.append(row_data[source_type][index])
            answers.append(row_data[target_type][index])

        # 构建问题和答案
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

    def run_batch_quiz(self, num_questions=5, mode='hira_to_roma', chars_per_question=2, char_type='all'):
        """运行批量测验"""
        print(f"=== {self.modes[mode]}批量练习（每题{chars_per_question}个字符，{self.char_types[char_type]}）===")

        # 生成题目
        quiz_items = self.generate_quiz_items(num_questions, mode, chars_per_question, char_type)

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
        for i, (item, user_answer) in enumerate(zip(quiz_items, user_answers), 1):
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
                'mode': mode,
                'char_type': char_type,
                'timestamp': str(Path('').cwd().stat().st_mtime)
            })

        # 保存结果
        self.save_results()

        # 显示成绩
        print(f"\n=== 测验完成 ===")
        print(f"得分：{score}/{num_questions}")
        print(f"正确率：{score/num_questions*100:.1f}%")

        # 显示历史统计
        if self.results:
            mode_results = [r for r in self.results if r['mode'] == mode and r['char_type'] == char_type]
            if mode_results:
                correct_count = sum(1 for r in mode_results if r['is_correct'])
                total_tries = len(mode_results)
                print(
                    f"\n{self.modes[mode]}({self.char_types[char_type]})历史正确率：{correct_count/total_tries*100:.1f}% ({correct_count}/{total_tries})")


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

    # 开始批量测验
    quiz.run_batch_quiz(num_questions, mode, chars_per_question, char_type)
