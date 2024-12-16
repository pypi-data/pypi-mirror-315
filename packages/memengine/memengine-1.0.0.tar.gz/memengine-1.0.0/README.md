# MemEngine

MemEngine is a unified and modularied library for developing advanced memory of LLM-based agents.

## Introduction

Many research methods have been proposed to improve the memory capability of LLM-based agents, however, they are implemented under different pipelines without a unified framework. It is difficult for developers to try different methods for experiments due to their inconsistencies. Moreover, many basic functions in different methods (such as retrieval) are duplicated. Researchers often need to repeatedly implement them when developing advanced methods, which reduces their research efficiency. Besides, many academic methods are tightly coupled within agents that are non-pluggable, making them difficult to apply across different agents. Therefore, we develop the MemEngine to solve the above problems.

<img src="assets/framework.png">

## Features

- **Unified and Modularized Memory Framework.** We propose a unified memory framework with three hierarchical levels, in order to implement and organize existing research models under a general structure. All these three levels are modularized inside our framework, where higher-level modules can reuse lower-level modules, thereby improving implementation efficiency and consistency. Besides, we provide a configuration module to easily modify hyper-parameters and prompts in different levels, and implement a utility module to better save and demonstrate memory contents.
- **Abundant Research Memory Implement.** Based on our unified and modularized memory framework, we implement abundant memory models in recent research papers, most of which are widely applied in various applications.
  All of these models can be easily switched and tried under our framework, with different configurations and hyper-parameters that can be adjusted for better application across different agents.

- **Convenient and Extensible Memory Development.** Based on our modularized memory operations and memory functions, researchers can conveniently develop their own advanced memory models. They can also extend existing operations and functions to develop their own modules. For better support researchers' development, we provide detailed instructions and examples in our document to guide the customization.

- **User-friendly and Pluggable Memory Usage.** We provide several deployment manners for our library to empower agents powerful memory capabilities. We also provide various modes for memory usage, including default, configurable, and automatic modes, in order to make it more user-friendly. Moreover, our memory modules are pluggable and can be utilized across different agent frameworks.

## Installation

There are several ways to install MemEngine.


### I. Install from source

```shell
conda create -n memengine_env python=3.9
git clone https://github.com/nuster1128/MemEngine.git
cd MemEngine
pip install -e .
```

### II. Install from pip

```
conda create -n memengine_env python=3.9
pip install memengine
```

### III. Install from conda

```
conda create -n memengine_env python=3.9
conda install memengine
```

## Deployment

There are two primary ways to use our library.

### I. Local Deployment

One can install our library conveniently in their python environment. Then, they can create a memory module for their agents, and using unified interfaces to execute memory operations inside programs. An example is shown as follows:

```python
from langchain.prompts import PromptTemplate
from memengine.config.Config import MemoryConfig
from memengine.memory.FUMemory import FUMemory
......

class DialogueAgent():
    def __init__(self, role, another_role):
        self.llm = LLM()

        self.role = role
        self.another_role = another_role
        self.memory = FUMemory(MemoryConfig(DialogueAgentMemoryConfig))
    
    def response(self, observation):
        prompt = PromptTemplate(
                input_variables=['role', 'memory_context', 'observation'],
                template= DialogueAgentPrompt,
            ).format(role = self.role, memory_context = self.memory.recall(observation), observation = observation)
        res = self.llm.fast_run(prompt)
        self.memory.store('%s: %s\n%s: %s' % (self.another_role, observation, self.role, res))
        return res
```

More details can be found in [Quick Start](#Quick Start).

### II. Remote Deployment

One can also install our library on computer servers, and install `uvicorn` and `fastapi` as follows:

```
pip install uvicorn fastapi
```

Then, lunch the service through a port with the following command:

```bash
uvicorn server_start:memengine_server --reload --port [YOUR PORT]
```

Here, `[YOUR PORT]` is the port you provided, such as `8426`.

Then, they can start a client to conduct memory operations by invoking requests of HTTP protocol remotely, on lightweight devices. An example is shown as follows:

```python
from memengine.utils.Client import Client
from langchain.prompts import PromptTemplate
from memengine.config.Config import MemoryConfig
from memengine.memory.FUMemory import FUMemory
......
ServerAddress = 'http://127.0.0.1:[YOUR PORT]'

class DialogueAgent():
    def __init__(self, role, another_role):
        self.llm = LLM()

        self.role = role
        self.another_role = another_role
	    memory = Client(ServerAddress)
	    memory.initilize_memory('FUMemory', DialogueAgentMemoryConfig)
    
    def response(self, observation):
        prompt = PromptTemplate(
                input_variables=['role', 'memory_context', 'observation'],
                template= DialogueAgentPrompt,
            ).format(role = self.role, memory_context = self.memory.recall(observation), observation = observation)
        res = self.llm.fast_run(prompt)
        self.memory.store('%s: %s\n%s: %s' % (self.another_role, observation, self.role, res))
        return res
```

You can also refer a complete example in `run_client_sample.py`.


## Quick Start

We provide several manners to use MemEngine. We take local deployment as examples.


### Using Stand-alone memory

You can just run our sample `run_memory_samples.py` for the quick start.

```shell
python run_memory_samples.py
```

### Using memory in LLM-based agents

We provide two example usage of applying MemEngine inside agents.

#### I. LLM-based Agents for HotPotQA

You need to install some dependencies as follows:

```bash
pip install libzim beautifulsoup4
```

Then, download the wiki dump `wikipedia_en_all_nopic_2024-06.zim` and the data `hotpot_dev_fullwiki_v1.json` in your own path. After that, change the path and API keys in `cd run_agent_samples/run_hotpotqa.py`. And you can run the program with the command:

```bash
cd run_agent_samples
python run_hotpotqa.py
```

#### II. LLM-based Agents for Dialogue

You need to change the API keys in `cd run_agent_samples/run_dialogue.py`. And you can run the program with the command:

```
cd run_agent_samples
python run_dialogue.py
```

## Customize New Memory

Our library provides a great support to customize advanced memory models for developers. There are major three aspects to customize new methods.

### I. Customize Memory Functions

Researchers may need to implement new functions in their method. For example, they may extend *LLMJudge* to design a *BiasJudge* for poisoning detection. Here, we provide an example of *RandomJudge*:

```python
from memengine.function import BaseJudge

class MyBiasJudge(BaseJudge):
    def __init__(self, config):
        super().__init__(config)

    def __call__(self, text):
        return random.random()/self.config.scale
```

### II. Customize Memory Operations

To implement a new method, the memory operation is most significant part to customize, containing major pipelines of the detailed process. Here is an example:

```python
......

class MyMemoryRecall(BaseRecall):
    def __init__(self, config, **kwargs):
        super().__init__(config)

        self.storage = kwargs['storage']
        self.insight = kwargs['insight']
        self.truncation = LMTruncation(self.config.truncation)
        self.utilization = ConcateUtilization(self.config.utilization)
        self.text_retrieval = TextRetrieval(self.config.text_retrieval)
        self.bias_retrieval = ValueRetrieval(self.config.bias_retrieval)
    
    def reset(self):
        self.__reset_objects__([self.truncation, self.utilization, self.text_retrieval, self.bias_retrieval])
    
    @__recall_convert_str_to_observation__
    def __call__(self, query):
        if self.storage.is_empty():
            return self.config.empty_memory
        text = query['text']
        
        relevance_scores, _ = self.text_retrieval(text, topk=False, with_score = True, sort = False)
        bias, _ = self.bias_retrieval(None, topk=False, with_score = True, sort = False)
        final_scores = relevance_scores + bias
        scores, ranking_ids = torch.sort(final_scores, descending=True)

        if hasattr(self.config, 'topk'):
            scores, ranking_ids = scores[:self.config.topk], ranking_ids[:self.config.topk]

        memory_context = self.utilization({
                    'Insight': self.insight['global_insight'],
                    'Memory': [self.storage.get_memory_text_by_mid(mid) for mid in ranking_ids]
                })

        return self.truncation(memory_context)
```

### III. Customize Memory Methods

By utilizing the newly customized memory operations and the existing ones, research can formulate their methods with various combinations in final. Here is an example:

```python
......

class MyMemory(ExplicitMemory):
    def __init__(self, config) -> None:
        super().__init__(config)
        
        self.storage = LinearStorage(self.config.args.storage)
        self.insight = {'global_insight': '[None]'}

        self.recall_op = MyMemoryRecall(
            self.config.args.recall,
            storage = self.storage,
            insight = self.insight
        )
        self.store_op = MyMemoryStore(
            self.config.args.store,
            storage = self.storage,
            text_retrieval = self.recall_op.text_retrieval,
            bias_retrieval = self.recall_op.bias_retrieval
        )
        self.optimize_op = RFOptimize(self.config.args.optimize, insight = self.insight)

        self.auto_display = ScreenDisplay(self.config.args.display, register_dict = {
            'Memory Storage': self.storage,
            'Insight': self.insight
        })

    def reset(self):
        self.__reset_objects__([self.storage, self.store_op, self.recall_op])
        self.insight = {'global_insight': '[None]'}

    def store(self, observation) -> None:
        self.store_op(observation)
    
    def recall(self, observation) -> object:
        return self.recall_op(observation)

    ......
```

The full example can be found in `run_custom_samples.py`.

## Acknowledgement

