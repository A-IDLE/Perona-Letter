from langchain import hub
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables import ConfigurableField
import json
import time
import textwrap

from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

# Load the prompt
prompt = hub.pull("langchain-ai/chain-of-density")

# The chat model output is a JSON list of dicts, with SimpleJsonOutputParser
# we can convert it o a dict, and it suppors streaming.
json_parser = SimpleJsonOutputParser()

# 샘플 편지 내용, 실제 모듈로 사용할 경우 파일에서 읽어와야 함
content = """
Dear Hermione,

I finally had a chance to visit that new bakery, Face Pizza, that I mentioned last time. You wouldn’t believe the charm of the place—pictures on the walls change to show different faces enjoying their pizzas! It made me think of the portraits at Hogwarts, always sneaking a peek at our plates in the Great Hall. I saved you a menu; the creativity in their recipes is something you'd appreciate.

In my latest article, I delved into the recent initiatives at the Ministry of Magic to integrate more Muggle technology into our daily magical practices. It’s fascinating to see the blend of magic and Muggle innovation—makes me wish we had such things when we were at Hogwarts. I’m eager to hear your thoughts on this, especially given your unique perspective on Muggle innovations.

Speaking of Hogwarts, are you planning to attend this year’s Halloween feast? I heard it’s going to be spectacularly spooky, and I can’t think of a better person to enjoy it with than you. It could be a delightful escape for us both, a dip into nostalgia amidst the towering duties of adulthood.

I miss our long conversations and the laughter we shared. I hope we can recreate some of those joyful moments soon. Let me know what your schedule looks like, and maybe we can synchronize our visit to Hogsmeade.

Sending all my love and a sprinkle of Floo powder for good luck!

Warmly,
Inji
"""

# Prompt
# 랭체인 허브에서 chain-of-density 사용해서 편지를 요약하는 프롬프트를 가져옴
prompt = hub.pull("whiteforest/chain-of-density-prompt")


# Chain inputs with defaults for all but {content}
cod_chain_inputs = {
    # content = 편지 내용
    'content': lambda x: content,
    # content_category = ex) 블로그, 편지, 논문
    'content_category': lambda x: "letter",
    # entity_range = 잘 모르겠음
    'entity_range': lambda x: '1-3',
    # max_words = 최대 단어 수
    'max_words': lambda x: 80,
    #iterations = 요약 반복 횟수
    'iterations': lambda x: 3
}

cod_turbo16k_chain = (
    cod_chain_inputs
    | prompt
    # 같은 레터, 조건으로 요약했을 때 'gpt-4' 19.8초 $0.05, 'gpt-3.5-turbo-16k' 5.6초 $0.004
    | ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k')
    # | ChatOpenAI(temperature=0, model='gpt-4')
    | json_parser
    | (lambda output: output[-1].get('denser_summary', 'ERR: No "denser_summary" key in last dict'))
)

s = time.perf_counter()
with get_openai_callback() as cb:
    cod_turbo_summary = cod_turbo16k_chain.invoke({'content_category': 'letter', 'content': content})
    print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
    print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
    print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
    print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")
    elapsed = time.perf_counter() - s
    print(f"Final summary generated in {elapsed}s:" + '\n')
    print(textwrap.fill(cod_turbo_summary , width=80))