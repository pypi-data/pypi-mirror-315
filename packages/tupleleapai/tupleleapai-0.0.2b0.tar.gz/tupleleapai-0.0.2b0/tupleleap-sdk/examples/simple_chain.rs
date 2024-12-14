use std::io::{self, Write};
use tupleleap_sdk::llm::{TupleleapAI, TupleleapAIModel};
use tupleleap_sdk::{
    chain::{Chain, LLMChainBuilder},
    prompt::HumanMessagePromptTemplate,
    prompt_args, template_jinja2,
};
// Include io Library for terminal input

#[tokio::main]
async fn main() {
    let prompt = HumanMessagePromptTemplate::new(template_jinja2!(
        "Give me a creative name for a store that sells: {{producto}}",
        "producto"
    ));

    let llm = TupleleapAI::default().with_model(TupleleapAIModel::Gpt35);
    let chain = LLMChainBuilder::new()
        .prompt(prompt)
        .llm(llm)
        .build()
        .unwrap();

    print!("Please enter a product: ");
    io::stdout().flush().unwrap(); // Display prompt to terminal

    let mut product = String::new();
    io::stdin().read_line(&mut product).unwrap(); // Get product from terminal input

    let product = product.trim();

    let output = chain
        .invoke(prompt_args!["producto" => product]) // Use product input here
        .await
        .unwrap();

    println!("Output: {}", output);
}
