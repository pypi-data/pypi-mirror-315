use url::Origin::Tuple;
use tupleleap_sdk::{language_models::llm::LLM, llm::openai::TupleleapAIConfig};
use tupleleap_sdk::llm::TupleleapAI;

#[tokio::main]
async fn main() {
    //OpenAI Example
    let open_ai = TupleleapAI::default();
    let response = open_ai.invoke("hola").await.unwrap();
    println!("{}", response);

    //or we can set config as
    let open_ai = TupleleapAI::default().with_config(
        TupleleapAIConfig::default()
            .with_api_base("xxx") //if you want to specify base url
            .with_api_key("<you_api_key>"), //if you want to set you open ai key,
    );

    let response = open_ai.invoke("hola").await.unwrap();
    println!("{}", response);
}
