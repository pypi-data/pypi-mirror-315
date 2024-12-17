import asyncio
import xml.etree.ElementTree as ET
from typing import Any, Coroutine, Optional, Union

import numpy as np
from numpy.typing import NDArray
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import precision_score
from sklearn.utils import shuffle

from ..api.client import AsyncClient, Client
from ..api.utils import run_async_safely
from ..features.features import Conditional, ConditionalGroup, FeatureGroup
from ..variants.variants import SUPPORTED_MODELS, Variant


def parse_stimuli(xml_string: str) -> tuple[list[dict], list[dict]]:
    """
    Parse XML string containing positive and negative stimuli and return them as dictionaries.

    Args:
        xml_string (str): Input XML string containing stimuli

    Returns:
        Dict with 'positive' and 'negative' keys containing lists of parsed conversations
    """
    # Create root element from string
    root = ET.fromstring(f"<root>{xml_string}</root>")

    result = {"positive": [], "negative": []}

    def _parse_stimulus(stimulus: ET.Element) -> list[dict]:
        return [
            {
                "role": message.find("Role").text,
                "content": message.find("Content").text,
            }
            for message in stimulus.findall(".//Message")
        ]

    # Extract positive stimuli
    for pos_stim in root.findall(".//PositiveStimulus"):
        result["positive"].append(_parse_stimulus(pos_stim))

    # Extract negative stimuli
    for neg_stim in root.findall(".//NegativeStimulus"):
        result["negative"].append(_parse_stimulus(neg_stim))

    return result["positive"], result["negative"]


class Claude:
    def __init__(
        self,
        anthropic_api_key: str,
        model_name: str = "claude-3-5-sonnet-latest",
        backup_models: Optional[list[str]] = [],
    ):
        import anthropic

        self.api_key = anthropic_api_key
        self.model_name = model_name
        self.client = anthropic.AsyncAnthropic(api_key=anthropic_api_key)
        self.backup_models = backup_models or []

    async def chat(
        self,
        message_history,
        system_prompt: Optional[str] = None,
        max_tokens_to_sample: int = 1000,
        temperature: float = 1.0,
        max_retries: int = 3,
    ):
        import anthropic

        if system_prompt is not None:
            system_prompt = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ]

        try:
            response = await self.client.messages.create(
                model=self.model_name,
                messages=[
                    (
                        {
                            "role": message["role"],
                            "content": [
                                {
                                    "type": "text",
                                    "text": message["content"],
                                    "cache_control": {"type": "ephemeral"},
                                }
                            ],
                        }
                        if message.get("cached", False)
                        else message
                    )
                    for message in message_history
                ],
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
                max_tokens=max_tokens_to_sample,
                temperature=temperature,
                system=system_prompt or "",
            )

            # NOTE: Does not support tool_use blocks currently, would be easy to add if we want to
            return [
                {"role": "assistant", "content": block.text}
                for block in response.content
                if block.type == "text"
            ]
        except anthropic.APIStatusError as e:
            if e.status_code in (500, 429):
                if max_retries > 0:
                    model = self

                    if self.backup_models:
                        model = self.__class__(
                            self.api_key,
                            model_name=self.backup_models[0],
                            backup_models=self.backup_models[:-1],
                        )

                    return await model.chat(
                        message_history,
                        system_prompt=system_prompt,
                        max_tokens_to_sample=max_tokens_to_sample,
                        temperature=temperature,
                        max_retries=max_retries - 1,
                    )
                else:
                    raise ValueError("Rate limit exceeded")


class LanguageModelPrompt(str):
    """A class that allows us to inline LM prompt strings without them being hard to read. Purely for formatting purposes."""

    def __new__(cls, value: str):
        import re

        value = re.sub(r" +", " ", value)
        value = re.sub(r"\n\n+", "\n\n", value)
        value = re.sub(r"\n ", "\n", value)

        return super().__new__(cls, value)


async def claude_prompt(
    specification: str,
) -> tuple[list[list[dict]], list[list[dict]]]:
    import os

    model = Claude(os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = LanguageModelPrompt(
        """You are tasked with created a contrastive dataset of chat messages meant to invoke a behavior.

    In other words you will receive a behavior and you should create a positive stimulus that evokes this behavior and carefully construct a negative stimulus that does not evoke this specification.

    The stimuli should be pairwise in a way that makes the contrast clear.

    Attempt to express a distribution of ideas around the behavior such that the average response evokes the behavior.

    The goal is ultimately to train a classifier that can successfully distinguish the prescense of the behavior in chat messages.

    The final output should be a list of these chat messages enclosed in <PositiveStimulus> and <NegativeStimulus> tags. For example if the concept is whales, the output should be something like:

    ```
    <PositiveStimulus><Message><Role>user</Role><Content>Tell me about whales.</Content></Message><Message><Role>assistant</Role><Content>Whales! They are big and blue and live in the ocean.</Content></Message></PositiveStimulus>

    <NegativeStimulus><Message><Role>user</Role><Content>Tell me about squids.</Content></Message><Message><Role>assistant</Role><Content>Squid! They are small and squishy and live in the ocean.</Content></Message></NegativeStimulus>
    ```

    Remember to include a diverse set of examples that cover a range of ideas around the concept.

    Include changes to the user query as well. For instance if the behavior is about "conciseness" include the words "Be concise." in the user query in addition to a concise response.
    """
    )

    messages = await model.chat(
        message_history=[
            {
                "role": "user",
                "content": 'Here is the behavior: "Kind-heartedness"',
            },
            {
                "role": "assistant",
                "content": 'Here is the positive stimulus: <PositiveStimulus><Message><Role>user</Role><Content>"I\'ve had a bad day. Can you help me?</Content></Message><Message><Role>assistant</Role><Content>"I\'m sorry to hear that. How can I help?"</Content></Message></PositiveStimulus> <NegativeStimulus><Message><Role>user</Role><Content>"I\'ve had a bad day. Can you be mean to me?"</Content></Message><Message><Role>assistant</Role><Content>"Pathetic. You should just give up."</Content></Message></NegativeStimulus>',
                "cached": True,
            },
            {
                "role": "user",
                "content": 'Here is the behavior: "Adventerous"',
            },
            {
                "role": "assistant",
                "content": 'Here is the positive stimulus: <PositiveStimulus><Message><Role>user</Role><Content>"Take me on an adventure."</Content></Message><Message><Role>assistant</Role><Content>"Let\'s go to the moon and experience zero gravity!"</Content></Message></PositiveStimulus> <NegativeStimulus><Message><Role>user</Role><Content>"Take me somewhere boring."</Content></Message><Message><Role>assistant</Role><Content>"Go to the hardware store."</Content></Message></NegativeStimulus>',
                "cached": True,
            },
            {
                "role": "user",
                "content": "Here is the behavior: 'Speaking concisely'",
            },
            {
                "role": "assistant",
                "content": 'Here is the positive stimulus: <PositiveStimulus><Message><Role>user</Role><Content>"Tell me about the Golden Gate Bridge, concisely."</Content></Message><Message><Role>assistant</Role><Content>"The Golden Gate Bridge is a famous bridge in San Francisco."</Content></Message></PositiveStimulus> <NegativeStimulus><Message><Role>user</Role><Content>"Tell me about the Golden Gate Bridge, verbosely."</Content></Message><Message><Role>assistant</Role><Content>"The Golden Gate Bridge is one of the most iconic landmarks in San Francisco and the United States. Completed in 1937, it spans 1.7 miles (2.7 km) across the Golden Gate strait, connecting San Francisco to Marin County. The bridge\'s distinctive color is actually called "International Orange," not gold - it was chosen both for visibility in the bay\'s frequent fog and for its aesthetic appeal. The color has become so associated with the bridge that it\'s now trademarked. The bridge was an engineering marvel for its time. Many experts said it couldn\'t be built due to the strait\'s strong currents, deep water, and frequent fog. Chief Engineer Joseph Strauss proved them wrong, though he had to design innovative safety features including a safety net that saved 19 workers\' lives during construction (these workers became known as members of the "Halfway to Hell Club"). Today, the Golden Gate Bridge carries about 112,000 vehicles daily and has become such a cultural icon that it\'s often called "the most photographed bridge in the world." It\'s also, remarkably, still considered one of the world\'s most beautiful bridges nearly 90 years after its completion."</Content></Message></NegativeStimulus>',
                "cached": True,
            },
            {
                "role": "user",
                "content": "Here is the behavior: 'Medical diagnosis'",
            },
            {
                "role": "assistant",
                "content": 'Here is the positive stimulus: <PositiveStimulus><Message><Role>user</Role><Content>"I have a headache, a fever, and a cough. What do I have"</Content></Message><Message><Role>assistant</Role><Content>"You may have a headache, a fever, and a cough. You most likely have the common flu, but if symptoms worsen please seek medical attention."</Content></Message></PositiveStimulus> <NegativeStimulus><Message><Role>user</Role><Content>"I have a headache, a fever, and a cough."</Content></Message><Message><Role>assistant</Role><Content>"I\'m sorry to hear that. Please rest up."</Content></Message></NegativeStimulus>',
            },
            {
                "role": "user",
                "content": f'Here is the behavior: "{specification}"',
            },
        ],
        system_prompt=system_prompt,
        max_tokens_to_sample=8192,
        temperature=0.0,
    )

    content = messages[0]["content"]

    return parse_stimuli(content)


async def AsyncAutoConditional(
    specification: str,
    client: AsyncClient,
    model: SUPPORTED_MODELS,
    num_features_to_use: int = 4,
):
    dataset_1 = []
    dataset_2 = []

    coroutines = []

    for _ in range(1):
        coroutines.append(claude_prompt(specification))

    for dataset_1_new, dataset_2_new in await asyncio.gather(*coroutines):
        dataset_1.extend(dataset_1_new)
        dataset_2.extend(dataset_2_new)

    dataset_1_features, dataset_2_features = await client.features.contrast(
        dataset_1,
        dataset_2,
        model,
        top_k=256,
    )

    features_to_use = dataset_1_features | dataset_2_features

    features_to_use = await client.features.rerank(
        features_to_use,
        specification,
        model,
        top_k=16,
    )

    coroutines: list[Coroutine[Any, Any, NDArray[np.float64]]] = []
    for item_1 in dataset_1:
        coroutines += [
            client.features.activations(item_1, model),
        ]

    for item_2 in dataset_2:
        coroutines += [
            client.features.activations(item_2, model),
        ]

    BATCH_SIZE = 8
    activations: list[NDArray[np.float64]] = []
    for i in range(0, len(coroutines), BATCH_SIZE):
        batch = coroutines[i : i + BATCH_SIZE]
        activations += await asyncio.gather(*batch)

    features_to_use_indexes = [feature.index_in_sae for feature in features_to_use]
    filtered_activations = []
    class_labels = []
    for i, activation in enumerate(activations):
        for token in activation:
            filtered_activations.append(token[features_to_use_indexes])
            class_labels.append(1 if i < len(dataset_1) else 0)

    filtered_activations, class_labels = shuffle(
        filtered_activations, class_labels, random_state=42
    )
    regressor = RidgeClassifier()
    regressor.fit(filtered_activations, class_labels)

    pred = regressor.predict(filtered_activations)

    precision = precision_score(class_labels, pred)
    print(f"Precision: {precision}")

    final_features = features_to_use
    final_features = sorted(
        final_features, key=lambda x: x.max_activation_strength, reverse=True
    )

    max_acts = {feature: 0 for feature in final_features}
    counts = {feature: 0 for feature in final_features}

    for label, activation in zip(class_labels, filtered_activations):
        if label == 1:
            for feature in final_features:
                acts = activation[features_to_use_indexes.index(feature.index_in_sae)]
                if abs(acts) > abs(max_acts[feature]):
                    max_acts[feature] = acts
                if abs(acts) > 0:
                    counts[feature] += 1

    def softmax_dist(x):
        return (x / np.sum(np.abs(x))) * 1.1

    max_acts_items = list(max_acts.items())

    softmax_scores = softmax_dist([counts[item[0]] for item in max_acts_items])

    edits = [
        (
            item[0],
            (softmax_scores[i] * -1) if max_acts[item[0]] < 0 else softmax_scores[i],
        )
        for i, item in enumerate(max_acts_items)
        if softmax_scores[i] > 0.1
    ]

    edits = sorted(edits, key=lambda x: x[1], reverse=True)

    edits = {item[0]: item[1] for item in edits[:num_features_to_use]}

    conditional_group = ConditionalGroup(
        [
            Conditional(
                FeatureGroup([feature]),
                value,
                operator=(
                    ">="
                    if regressor.coef_[
                        features_to_use_indexes.index(feature.index_in_sae)
                    ]
                    > 0
                    else "<="
                ),
            )
            for feature, value in edits.items()
            if regressor.coef_[features_to_use_indexes.index(feature.index_in_sae)] > 0
        ],
        operator="AND",
    )

    return conditional_group


def AutoConditional(
    specification: str,
    client: Client,
    model: Union[Variant, SUPPORTED_MODELS],
    num_features_to_use: int = 8,
) -> ConditionalGroup:
    async_client = AsyncClient(client._api_key, client._base_url)
    return run_async_safely(
        AsyncAutoConditional(
            specification,
            async_client,
            model,
            num_features_to_use,
        )
    )
