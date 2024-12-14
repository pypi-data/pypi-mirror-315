use tupleleap_sdk::{
    chain::{Chain, StuffDocumentBuilder},
    llm::openai::TupleleapAI,
    prompt_args,
    schemas::Document,
};

#[tokio::main]
async fn main() {
    let llm = TupleleapAI::default();

    let chain = StuffDocumentBuilder::new()
        .llm(llm)
        // .prompt() you can add a custom prompt if you want
        .build()
        .unwrap();
    let input = prompt_args! {
        "input_documents"=>vec![
            Document::new(format!(
                "\nQuestion: {}\nAnswer: {}\n",
                "Which is the favorite text editor of luis", "Nvim"
            )),
            Document::new(format!(
                "\nQuestion: {}\nAnswer: {}\n",
                "How old is Luis", "24"
            )),
        ],
        "question"=>"How old is luis and whats his favorite text editor"
    };

    let output = chain.invoke(input).await.unwrap();

    println!("{}", output);
}
