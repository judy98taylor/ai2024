import asyncio
import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness,context_recall,context_precision,answer_relevancy,context_entity_recall,answer_similarity
from ragas.llms.base import LangchainLLMWrapper
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
import nest_asyncio
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

async def get_score(data_samples):
    if data_samples is None:
        return 'no data_samples'
   
    nest_asyncio.apply()
    one_api_key = 'sk-p9GKPwvhmZvYeHN15aC400410f3249C6A4E6Fe559e6a6336' #AIT
    one_api_url = 'http://10.26.9.148:3007/v1'
    model_llm = ChatOpenAI(
        model="ds/deepseek-chat", # only n=1
        # model="sf/Qwen1.5-7B-Chat", # slow!!!! can get answer_relevancy score
        api_key="sk-p9GKPwvhmZvYeHN15aC400410f3249C6A4E6Fe559e6a6336",  #AIT
        base_url="http://10.26.9.148:3007/v1"
    )
    model_embeddings = OpenAIEmbeddings(
        model="bge-m3",
        base_url=one_api_url,
        api_key=one_api_key,
        openai_api_type="open-ai"
    )

    wrapper_llm = LangchainLLMWrapper(model_llm)
    wrapper_embeddings = LangchainEmbeddingsWrapper(model_embeddings)

    # data_samples = {
    #     'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
    #     'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
    #     'contexts' : [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'],
    #     ['The Green Bay Packers...Green Bay, Wisconsin.','The Packers compete...Football Conference']],
    #     'ground_truth': ['The first superbowl was held on January 15, 1967', 'The New England Patriots have won the Super Bowl a record six times']
    # }

    dataset = Dataset.from_dict(data_samples)

    # metrics = [answer_relevancy] 
    metrics=[faithfulness,answer_correctness,context_recall,context_precision,context_entity_recall,answer_similarity,answer_relevancy]

    # run_config_ = RunConfig()
    run_config_ = RunConfig(timeout=600000,thread_timeout=600000,max_retries=1, max_wait=60000,max_workers=600,log_tenacity=True)

    # score = evaluate(dataset,metrics,llm=wrapper_llm,embeddings=wrapper_embeddings,is_async=True,raise_exceptions=False)
    score = evaluate(dataset,
                    metrics,
                    llm=wrapper_llm,
                    embeddings=wrapper_embeddings,
                    is_async=True,
                    run_config=run_config_,
                    raise_exceptions=False)

    score.to_pandas()
    print(score)
    return score

# get_score()