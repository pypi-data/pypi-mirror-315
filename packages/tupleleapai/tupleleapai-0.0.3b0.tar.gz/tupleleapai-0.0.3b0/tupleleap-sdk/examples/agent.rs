use std::sync::Arc;

use tupleleap_sdk::{
    agent::{AgentExecutor, ConversationalAgentBuilder},
    chain::{options::ChainCallOptions, Chain},
    llm::openai::{TupleleapAI, TupleleapAIModel},
    memory::SimpleMemory,
    prompt_args,
    tools::CommandExecutor,
};

#[tokio::main]
async fn main() {
    let llm = TupleleapAI::default().with_model(TupleleapAIModel::Gpt4Turbo);
    let memory = SimpleMemory::new();
    let command_executor = CommandExecutor::default();
    let agent = ConversationalAgentBuilder::new()
        .tools(&[Arc::new(command_executor)])
        .options(ChainCallOptions::new().with_max_tokens(1000))
        .build(llm)
        .unwrap();

    let executor = AgentExecutor::from_agent(agent).with_memory(memory.into());

    let input_variables = prompt_args! {
        "input" => "What is the name of the current dir",
    };

    match executor.invoke(input_variables).await {
        Ok(result) => {
            println!("Result: {:?}", result);
        }
        Err(e) => panic!("Error invoking LLMChain: {:?}", e),
    }
}
