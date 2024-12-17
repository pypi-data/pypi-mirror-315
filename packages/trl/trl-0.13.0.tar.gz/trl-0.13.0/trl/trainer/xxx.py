from trl import PPOConfig, PPOTrainer
from trl.trainer.utils import SIMPLE_CHAT_TEMPLATE
import tempfile
import unittest

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer
from transformers.testing_utils import require_peft


# Set up the models and tokenizer using the test model
model_id = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
model = AutoModelForCausalLM.from_pretrained(model_id)
ref_model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="left")
tokenizer.add_special_tokens({"pad_token": "[PAD]"})

if tokenizer.chat_template is None:
    tokenizer.chat_template = SIMPLE_CHAT_TEMPLATE

# Add reward and value models as in ppo.py
value_model = AutoModelForSequenceClassification.from_pretrained(
    model_id, trust_remote_code=True, num_labels=1
)
reward_model = AutoModelForSequenceClassification.from_pretrained(
    model_id, trust_remote_code=True, num_labels=1
)

# Load dataset
raw_dataset = load_dataset("trl-internal-testing/zen", "standard_prompt_only")
raw_dataset= raw_dataset.map(lambda x : tokenizer(x["prompt"]))

with tempfile.TemporaryDirectory() as tmp_dir:
    # Capture initial weights
    initial_critic_weights = {}
    initial_policy_weights = {}
    for name, param in value_model.named_parameters():
        initial_critic_weights[name] = param.clone().detach()
    for name, param in model.named_parameters():
        initial_policy_weights[name] = param.clone().detach()

    # Configure training args similar to example script
    training_args = PPOConfig(
        output_dir=tmp_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=1,
        learning_rate=3e-6,
        total_episodes=10,
        save_strategy="no",
        report_to="none",
        missing_eos_penalty=1.0,
        vf_coef=1.0,  # Increase value function coefficient
        num_ppo_epochs=4,  # Increase number of PPO epochs
    )

    # Create trainer
    trainer = PPOTrainer(
        args=training_args,
        processing_class=tokenizer,
        model=model,
        ref_model=ref_model,
        reward_model=reward_model,
        value_model=value_model,
        train_dataset=raw_dataset["train"],
        eval_dataset=raw_dataset["test"],
    )

    # Train
    trainer.train()