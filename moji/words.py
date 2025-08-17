from pathlib import Path
from typing import Union, List
from utils import expand_range_list
import pandas as pd


class WordQuiz:
    def __init__(self, root_path: Union[str, Path]) -> None:
        if isinstance(root_path, str):
            root_path = Path(root_path)

        self.root_path = root_path
        self.modes = ["日译中", "中译日"]
        self.units = [f for f in self.root_path.iterdir() if f.is_file()]

    def gen_question(self, out_dir: Union[str, Path], mode_choice: int, unit_choice: List[int], question_num: int) -> None:
        if isinstance(out_dir, str):
            out_dir = Path(out_dir)

        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)

        if mode_choice > len(self.modes)-1:
            raise ValueError(f"error mode: {mode_choice}")

        unit_paths = [self.root_path / f"ch{num}.csv" for num in unit_choice]
        dataframes = []
        for path in unit_paths:
            if path not in self.units:
                raise FileNotFoundError(f"Missing unit files")
            try:
                df = pd.read_csv(path, encoding="utf-8", engine="python")
                dataframes.append(df)
            except Exception as e:
                print(f"Error reading {path}: {e}")

        combined_df = pd.concat(dataframes, ignore_index=True)
        if question_num == -1:
            question_num = len(combined_df)
        elif question_num > len(combined_df):
            question_num = len(combined_df)
        elif question_num < -1:
            raise ValueError(f"error question num: {question_num}")

        sample_df = combined_df.sample(question_num, random_state=42)
        question_path = out_dir / "quesions.txt"
        answer_path = out_dir / "answer.txt"
        if mode_choice == 0:
            questions_col = sample_df["japan"]
            questions_col.to_csv(question_path.as_posix(), index=False, header=True)

            result_col = sample_df[["japan", "chinese"]]
            result_col.to_csv(answer_path.as_posix(), index=False, header=True)
        elif mode_choice == 1:
            questions_col = sample_df["chinese"]
            questions_col.to_csv(question_path.as_posix(), index=False, header=True)

            result_col = sample_df[["chinese", "japan"]]
            result_col.to_csv(answer_path.as_posix(), index=False, header=True)
        else:
            raise ValueError(f"error mode: {mode_choice}")

        print(f"save questions to {question_path.as_posix()}")
        print(f"save answers to {answer_path.as_posix()}")


if __name__ == "__main__":
    quiz = WordQuiz(r"words")

    print("请选择练习模式: ")
    for i, value in enumerate(quiz.modes):
        print(f"{i}. {value}")

    try:
        mode_choice = int(input())
    except Exception as e:
        raise ValueError(f"Unknown mode: {e}")

    print("你想复习哪些单元: ")
    out_str = " ".join(path.stem for path in quiz.units)
    print(out_str)

    unit_choice = str(input())
    unit_choice = expand_range_list(unit_choice)

    print("想要练习多少题(-1表示全部): ")
    question_num = int(input())

    out_dir = r"results/"
    quiz.gen_question(out_dir, mode_choice, unit_choice, question_num)
