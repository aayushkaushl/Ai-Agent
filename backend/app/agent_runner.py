import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory


load_dotenv()


# Initialize LLM and tools lazily; protect against re-init on every request
_llm = None
_agent = None
_memory = None
_tools = None




def _init_agent():
global _llm, _agent, _memory, _tools
if _agent is not None:
return _agent, _memory


_llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"), temperature=float(os.getenv("TEMPERATURE", "0")))


wrapper = GoogleSerperAPIWrapper()
google_search = GoogleSerperRun(api_wrapper=wrapper)
wiki_tool = WikipediaAPIWrapper()
python_tool = PythonREPLTool()


_tools = [
Tool(name="Google Search", func=google_search.run, description="Search Google for current events or general information"),
Tool(name="Wikipedia", func=wiki_tool.run, description="Search Wikipedia for factual information"),
Tool(name="Python REPL", func=python_tool.run, description="Execute Python code for math or data analysis"),
]


_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


_agent = initialize_agent(
_tools,
_llm,
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
verbose=True,
memory=_memory,
max_iterations=int(os.getenv("MAX_ITERATIONS", "2")),
)
return _agent, _memory




def run_agent_with_logs(query: str):
agent, memory = _init_agent()
log_stream = io.StringIO()
from contextlib import redirect_stdout
with redirect_stdout(log_stream):
result = agent.invoke({
"input": query,
"chat_history": memory.chat_memory.messages
})
logs = log_stream.getvalue()
answer = result.get("output") if isinstance(result, dict) else str(result)


# Extract last tool used
matches = re.findall(r"Action:\s*([^\n]+)", logs)
used_tool = matches[-1] if matches else None


return answer, used_tool, logs