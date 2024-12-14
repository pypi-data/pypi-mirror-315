use tupleleap_sdk::{
    language_models::llm::LLM,
    llm::openai::{AzureConfig, TupleleapAI},
};

#[tokio::main]
async fn main() {
    let azure_config = AzureConfig::default()
        .with_api_key("REPLACE_ME_WITH_YOUR_API_KEY")
        .with_api_base("https://REPLACE_ME.openai.azure.com")
        .with_api_version("2024-02-15-preview")
        .with_deployment_id("chatGPT_GPT35-turbo-0301");

    let open_ai = TupleleapAI::new(azure_config);
    let response = open_ai.invoke("Why is the sky blue?").await.unwrap();
    println!("{}", response);
}
