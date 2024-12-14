import re
import time
import numpy as np

from matplotlib import pyplot as plt


class LatexPlot:
    def __init__(self):
        self.fig = None
        self.inline_pattern = re.compile(r'\\\([\s\n]+(\\.*?=.*?)\\\)')
        self.block_pattern = re.compile(r'\\\[[\s\n]+(.*?=.*?)[\s\n]+\\]')
        self.chinese_pattern = re.compile(
            r'[\u4e00-\u9fff\uf900-\ufaff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002ceb0-\U0002ebef\U00030000-\U0003134f]')

    def match_latex(self, text: str):
        block_matches = self.block_pattern.findall(text)

        inline_matches = ['$' + m + '$' for m in self.inline_pattern.findall(text) if m != '' and not self.contains_chinese(m)]
        block_matches = ['$' + m + '$' for m in block_matches if not self.contains_chinese(m)]

        return inline_matches, block_matches

    def show_latex(self, inline_latex, block_latex):
        # 创建一个包含两个子图的图像，上下布局
        self.fig, axs = plt.subplots(figsize=(8, len(inline_latex) + len(block_latex) + 2))
        axs.axis('off')

        y_positions = np.linspace(1, 0, len(inline_latex) + len(block_latex) + 2)

        # 绘制inline latex
        for i in range(len(inline_latex) + 1):
            if i == 0:
                axs.text(0.5, y_positions[i], 'inline latex', fontsize=20, ha='center', va='center')
            else:
                axs.text(0.5, y_positions[i], inline_latex[i - 1], fontsize=20, ha='center', va='center')

        for i in range(len(block_latex) + 1):
            if i == 0:
                axs.text(0.5, y_positions[i + len(inline_latex) + 1], 'block latex', fontsize=15, ha='center',
                         va='center')
            else:
                axs.text(0.5, y_positions[i + len(inline_latex) + 1], block_latex[i - len(inline_latex) - 2],
                         fontsize=15,
                         ha='center', va='center')
        # 显示图像
        try:
            plt.show()
        except KeyboardInterrupt:
            print("Ctrl+C pressed, exiting...")
        finally:
            plt.close('all')

    def contains_chinese(self, s):
        return bool(self.chinese_pattern.search(s))


if __name__ == '__main__':
    a = LatexPlot()
    with open(r'C:\Users\s\Desktop\text.md', 'r', encoding='utf-8') as file:
        text = file.read()

    # print(text)
    m1, m2 = a.match_latex(text)
    a.show_latex(m1, m2)
    print("test")

    while True:
        time.sleep(1)
        print("sleep")
