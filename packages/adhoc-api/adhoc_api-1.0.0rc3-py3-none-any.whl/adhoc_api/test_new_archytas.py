from adhoc_api.tool import view_filesystem
from archytas.react import ReActAgent, FailedTaskError
from easyrepl import REPL
import pdb
from archytas.tool_utils import get_tool_prompt_description
def main():
    tools = [view_filesystem]
    agent = ReActAgent(model='gpt-4o', tools=tools, verbose=True)
    print(agent.prompt)
    pdb.set_trace()
    for query in REPL(history_file='.chat'):
        try:
            answer = agent.react(query)
            print(answer)
        except FailedTaskError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            agent.add_context(f'User issued KeyboardInterrupt')
            print("KeyboardInterrupt")



if __name__ == "__main__":
    main()