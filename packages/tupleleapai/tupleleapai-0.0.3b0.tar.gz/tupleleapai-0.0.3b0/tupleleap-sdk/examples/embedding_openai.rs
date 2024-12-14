use tupleleap_sdk::embedding::{embedder_trait::Embedder, openai::TupleleapAiEmbedder};

#[tokio::main]
async fn main() {
    let openai = TupleleapAiEmbedder::default();

    let response = openai.embed_query("What is the sky blue?").await.unwrap();

    println!("{:?}", response);
}
