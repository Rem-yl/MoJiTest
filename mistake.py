import json
from collections import defaultdict


class MistakeAnalyzer:
    def __init__(self, basic_kana, youon_kana):
        self.basic_kana = basic_kana
        self.youon_kana = youon_kana

    def analyze_history(self, results, current_mode, current_char_type):
        """分析历史记录，显示统计信息"""
        if not results:
            print("\n暂无历史记录")
            return

        # 筛选当前模式和字符类型的记录
        mode_results = []
        for r in results:
            if 'mode' in r and 'char_type' in r:
                if r['mode'] == current_mode and r['char_type'] == current_char_type:
                    mode_results.append(r)
            elif 'mode' in r and r['mode'] == current_mode:
                # 旧记录没有char_type字段，默认为'all'
                if current_char_type == 'all':
                    mode_results.append(r)

        if mode_results:
            correct_count = sum(1 for r in mode_results if r['is_correct'])
            total_tries = len(mode_results)
            print(f"\n{self.get_mode_name(current_mode)}({self.get_char_type_name(current_char_type)})历史正确率：{correct_count/total_tries*100:.1f}% ({correct_count}/{total_tries})")

            # 显示最近5次练习的趋势
            recent_tries = []
            current_try = []
            last_timestamp = None

            for r in reversed(mode_results):
                timestamp = r['timestamp']
                if last_timestamp and abs(float(timestamp) - float(last_timestamp)) > 3600:  # 假设超过1小时算新的一次练习
                    if current_try:
                        recent_tries.append(current_try)
                        current_try = []
                current_try.append(r)
                last_timestamp = timestamp

            if current_try:
                recent_tries.append(current_try)

            recent_tries = recent_tries[:5]  # 取最近5次
            if len(recent_tries) > 1:
                print("\n最近练习趋势：")
                for i, tries in enumerate(reversed(recent_tries), 1):
                    correct = sum(1 for t in tries if t['is_correct'])
                    total = len(tries)
                    print(f"练习 {i}: {correct}/{total} ({correct/total*100:.1f}%)")

    def analyze_weak_points(self, mistakes):
        """分析错题，找出薄弱字符"""
        if not mistakes:
            print("\n🎉 恭喜！没有错题，继续保持！")
            return

        weak_chars = defaultdict(int)

        for _, item, _ in mistakes:
            chars = item['details']['chars']
            for char in chars:
                weak_chars[char] += 1

        # 按错误次数排序
        sorted_weak_chars = sorted(weak_chars.items(), key=lambda x: x[1], reverse=True)

        print("\n=== 薄弱字符分析 ===")
        print("错误率最高的字符：")
        for i, (char, count) in enumerate(sorted_weak_chars[:5], 1):
            print(f"{i}. {char}: {count}次错误")

        # 分析错误最多的行
        weak_rows = defaultdict(int)
        for _, item, _ in mistakes:
            row_name = item['details']['row_name']
            weak_rows[row_name] += 1

        if weak_rows:
            sorted_weak_rows = sorted(weak_rows.items(), key=lambda x: x[1], reverse=True)
            print("\n错误率最高的行：")
            for i, (row, count) in enumerate(sorted_weak_rows[:3], 1):
                print(f"{i}. {row}: {count}次错误")

    def get_mode_name(self, mode):
        """获取模式的中文名"""
        mode_names = {
            'hira_to_roma': '平假名→罗马音',
            'kata_to_roma': '片假名→罗马音',
            'roma_to_hira': '罗马音→平假名',
            'roma_to_kata': '罗马音→片假名',
            'mix': '混合模式'
        }
        return mode_names.get(mode, mode)

    def get_char_type_name(self, char_type):
        """获取字符类型的中文名"""
        char_type_names = {
            'basic': '基础五十音',
            'youon': '拗音',
            'all': '全部字符'
        }
        return char_type_names.get(char_type, char_type)
