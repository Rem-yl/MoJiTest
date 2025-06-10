import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, cast


def load_kana_data() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """从JSON文件加载五十音图数据"""
    try:
        with open("hiragana_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("basic_kana", {}), data.get("youon_kana", {})
    except Exception as e:
        print(f"无法加载五十音图数据: {e}")
        print("使用空数据继续运行...")
        return {}, {}


def load_result_data(path: Union[Path, str]) -> List[Any]:
    """加载错题本"""
    if isinstance(path, str):
        path = Path(path)

    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return cast(List[Any], data)  # 显式类型断言
        except Exception:
            print("无法加载历史记录，将创建新记录")

    return []
