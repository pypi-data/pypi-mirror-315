import argparse
import os
import qianfan

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from .latex_plot import LatexPlot
from .utils import load_config, restricted_float, check_file


class ChatSystem:
    def __init__(self, args):
        self.config = load_config(args.llm)
        self.llm = args.llm
        if self.llm == 'Wenxinyiyan':
            os.environ["QIANFAN_ACCESS_KEY"] = self.config[
                'access_key'] if args.access_key is not None else args.access_key
            os.environ["QIANFAN_SECRET_KEY"] = self.config[
                'secret_key'] if args.secret_key is not None else args.secret_key
            self.client = qianfan.ChatCompletion()
        else:
            self.client = OpenAI(
                api_key=self.config['api_key'] if not args.key else args.key,
                base_url=self.config['base_url'] if not args.base_url else args.base_url,
            )
        if self.llm == 'Wenxinyiyan':
            self.history = [
                {
                    "role": "user",
                    "content": "default"
                }
            ]
        else:
            self.history = [
                {"role": "user",
                 "content": "default"}
            ]
        self.history_path = args.history_path
        check_file(self.history_path)
        self.history_input = FileHistory(self.history_path) if not args.no_history else None
        self.bindings = KeyBindings()
        self.session: PromptSession = PromptSession("llm>", history=self.history_input, key_bindings=self.bindings)
        self.console: Console = Console()
        self.is_stream = args.stream
        self.temperature = args.temperature
        self.model = self.config['model'] if not args.model else args.model
        self.show_latex = args.show_latex
        self.latex_plot = LatexPlot()
        self.no_memory = args.no_memory

    def get_llm_reply(self, query):
        self.history.append({
            "role": "user",
            "content": query
        })
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=self.temperature,
            stream=self.is_stream
        )

        if self.is_stream:
            # 采取流式输出
            collect_messages = []
            with Live(Markdown(''.join([m.content for m in collect_messages])), refresh_per_second=2,
                      vertical_overflow='ellipsis') as live:
                for idx, chunk in enumerate(completion):
                    chunk_message = chunk.choices[0].delta
                    if not chunk_message.content:
                        continue

                    collect_messages.append(chunk_message)
                    live.update(Markdown(''.join([m.content for m in collect_messages])))
            if self.show_latex:
                inline_match, block_match = self.latex_plot.match_latex(''.join([m.content for m in collect_messages]))
                if inline_match or block_match:
                    self.latex_plot.show_latex(inline_match, block_match)

        else:
            # 不采取流式输出
            result = completion.choices[0].message.content
            self.console.print(Markdown(result))

            if self.show_latex:
                inline_match, block_match = self.latex_plot.match_latex(result)
                if inline_match or block_match:
                    self.latex_plot.show_latex(inline_match, block_match)
        self.console.print('\n')

        if self.no_memory:
            del self.history[-2:]

    def get_wenixnyiyan_reply(self, query):
        self.history.append(
            {"role": "user",
             "content": query}
        )

        resp = self.client.do(
            model=self.model,
            messages=self.history,
            stream=self.is_stream
        )

        if self.is_stream:
            collect_messages = []
            with Live(Markdown(''.join([m.content for m in collect_messages])), refresh_per_second=2,
                      vertical_overflow='ellipsis') as live:
                for r in resp:
                    collect_messages.append(r['body']['result'])
                    live.update(Markdown(''.join([m for m in collect_messages])))
            if self.show_latex:
                inline_match, block_match = self.latex_plot.match_latex(''.join([m for m in collect_messages]))
                if inline_match or block_match:
                    self.latex_plot.show_latex(inline_match, block_match)
        else:
            result = resp['body']['result']
            self.console.print(Markdown(result))
            if self.show_latex:
                inline_match, block_match = self.latex_plot.match_latex(result)
                if inline_match or block_match:
                    self.latex_plot.show_latex(inline_match, block_match)
        self.console.print('\n')
        # 由于文心一言的上下文关联性极强，不能连续问两个不相关问题，所以在这里清理history
        if self.no_memory:
            del self.history[-2:]

    def run(self):
        while True:
            try:
                # 获取用户输入
                user_input = self.session.prompt()

                if user_input.lower() in ["exit", "quit", "q"]:
                    break

                @self.bindings.add(Keys.ControlC)
                def _(event):
                    event.app.exit()

                self.console.print("\nLLM is generating answer:\n", style="bright_green blink underline")
                if self.llm == 'Wenxinyiyan':
                    self.get_wenixnyiyan_reply(user_input)
                else:
                    self.get_llm_reply(user_input)

            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def print_config(self):
        print(self.client)
        print(self.model)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-stream', '-s', help='如果指定，将采取流式输出模式', action='store_true')
    parser.add_argument('-no_history', '-nh', help='如果指定，将不读取历史输入', action='store_true')
    parser.add_argument('-show_latex', '-sl', help='如果指定，将解析latex公式以图片形式展示', action='store_true')
    parser.add_argument('-no_memory', '-nm', help='如果指定，对话将不会保留记忆', action='store_true')

    parser.add_argument('-key', '-k', help="指定api_key", default=None, type=str)
    parser.add_argument('-base_url', '-url', '-u', help="指定url", default=None, type=str)
    parser.add_argument('-model', '-m', help="指定使用的模型", default=None, type=str)
    parser.add_argument('-llm', choices=['Kimi', 'ZhiPu', 'Wenxinyiyan'],
                        help="指定预置的的LLM来源，当使用其他来源时，请不要使用本参数",
                        default='ZhiPu')
    parser.add_argument('-access_key', '-ak', help='指定文心一言access_key', default=None)
    parser.add_argument('-secret_key', '-sk', help='指定问你下你一言secret_key', default=None)
    parser.add_argument('-temperature', '-t', help='指定temperature参数', default=0.6, type=restricted_float)
    parser.add_argument('-history_path', '-hp', help='指定历史输入的地址', default='history.txt')

    args = parser.parse_args()
    chat = ChatSystem(args)
    chat.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-stream', '-s', help='如果指定，将采取流式输出模式', action='store_true')
    parser.add_argument('-no_history', '-nh', help='如果指定，将不读取历史输入', action='store_true')
    parser.add_argument('-show_latex', '-sl', help='如果指定，将解析latex公式以图片形式展示', action='store_true')
    parser.add_argument('-no_memory', '-nm', help='如果指定，对话将不会保留记忆', action='store_true')

    parser.add_argument('-key', '-k', help="指定api_key", default=None, type=str)
    parser.add_argument('-base_url', '-url', '-u', help="指定url", default=None, type=str)
    parser.add_argument('-model', '-m', help="指定使用的模型", default=None, type=str)
    parser.add_argument('-llm', choices=['Kimi', 'ZhiPu', 'Wenxinyiyan'],
                        help="指定预置的的LLM来源，当使用其他来源时，请不要使用本参数",
                        default='ZhiPu')
    parser.add_argument('-access_key', '-ak', help='指定文心一言access_key', default=None)
    parser.add_argument('-secret_key', '-sk', help='指定问你下你一言secret_key', default=None)
    parser.add_argument('-temperature', '-t', help='指定temperature参数', default=0.6, type=restricted_float)
    parser.add_argument('-history_path', '-hp', help='指定历史输入的地址', default='history.txt')

    args = parser.parse_args()
    chat = ChatSystem(args)
    chat.run()
