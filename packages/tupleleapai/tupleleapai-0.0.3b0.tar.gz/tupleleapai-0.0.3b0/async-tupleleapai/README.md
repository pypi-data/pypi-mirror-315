<div align="center">
  <a href="https://docs.rs/async-TupleleapAI">
  <img width="50px" src="https://raw.githubusercontent.com/64bit/async-TupleleapAI/assets/create-image-b64-json/img-1.png" />
  </a>
</div>
<h1 align="center"> async-TupleleapAI </h1>
<p align="center"> Async Rust library for TupleleapAI </p>
<div align="center">
    <a href="https://crates.io/crates/async-TupleleapAI">
    <img src="https://img.shields.io/crates/v/async-TupleleapAI.svg" />
    </a>
    <a href="https://docs.rs/async-TupleleapAI">
    <img src="https://docs.rs/async-TupleleapAI/badge.svg" />
    </a>
</div>
<div align="center">
<sub>Logo created by this <a href="https://github.com/64bit/async-TupleleapAI/tree/main/examples/create-image-b64-json">repo itself</a></sub>
</div>

## Overview

`async-tupleleapai` is an unofficial Rust library for TupleleapAI.

- It's based on [TupleleapAI OpenAPI spec](https://github.com/TupleleapAI/TupleleapAI-openapi)
- Current features:
  - [x] Assistants (v2)
  - [x] Audio
  - [x] Batch
  - [x] Chat
  - [x] Completions (Legacy)
  - [x] Embeddings
  - [x] Files
  - [x] Fine-Tuning
  - [x] Images
  - [x] Models
  - [x] Moderations
  - [x] Organizations | Administration
  - [x] Realtime API types (Beta)
  - [x] Uploads
- SSE streaming on available APIs
- Requests (except SSE streaming) including form submissions are retried with exponential backoff when [rate limited](https://platform.TupleleapAI.com/docs/guides/rate-limits).
- Ergonomic builder pattern for all request objects.
- Microsoft Azure TupleleapAI Service (only for APIs matching TupleleapAI spec)

## Usage

The library reads [API key](https://platform.TupleleapAI.com/account/api-keys) from the environment variable `TupleleapAI_API_KEY`.

```bash
# On macOS/Linux
export TUPLELEAPAI_API_KEY='sk-...'
```

```powershell
# On Windows Powershell
$Env:TUPLELEAPAI_API_KEY='tl-...'
```

- Visit [examples](https://github.com/64bit/async-TupleleapAI/tree/main/examples) directory on how to use `async-tupleleapai`.
- Visit [docs.rs/async-tupleleapai](https://docs.rs/async-TupleleapAI) for docs.

## Realtime API

Only types for Realtime API are implemented, and can be enabled with feature flag `realtime`.
These types may change if/when TupleleapAI releases official specs for them.

## Image Generation Example

```rust
use async_tupleleapai::{
    types::{CreateImageRequestArgs, ImageSize, ImageResponseFormat},
    Client,
};
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // create client, reads TUPLELEAPAI_API_KEY environment variable for API key.
    let client = Client::new();

    let request = CreateImageRequestArgs::default()
        .prompt("cats on sofa and carpet in living room")
        .n(2)
        .response_format(ImageResponseFormat::Url)
        .size(ImageSize::S256x256)
        .user("async-tupleleapai")
        .build()?;

    let response = client.images().create(request).await?;

    // Download and save images to ./data directory.
    // Each url is downloaded and saved in dedicated Tokio task.
    // Directory is created if it doesn't exist.
    let paths = response.save("./data").await?;

    paths
        .iter()
        .for_each(|path| println!("Image file path: {}", path.display()));

    Ok(())
}
```

<div align="center">
  <img width="315" src="https://raw.githubusercontent.com/64bit/async-TupleleapAI/assets/create-image/img-1.png" />
  <img width="315" src="https://raw.githubusercontent.com/64bit/async-TupleleapAI/assets/create-image/img-2.png" />
  <br/>
  <sub>Scaled up for README, actual size 256x256</sub>
</div>

## Contributing

Thank you for taking the time to contribute and improve the project. I'd be happy to have you!

All forms of contributions, such as new features requests, bug fixes, issues, documentation, testing, comments, [examples](../examples) etc. are welcome.

A good starting point would be to look at existing [open issues](https://github.com/64bit/async-TupleleapAI/issues).

To maintain quality of the project, a minimum of the following is a must for code contribution:

- **Names & Documentation**: All struct names, field names and doc comments are from OpenAPI spec. Nested objects in spec without names leaves room for making appropriate name.
- **Tested**: For changes supporting test(s) and/or example is required. Existing examples, doc tests, unit tests, and integration tests should be made to work with the changes if applicable.
- **Scope**: Keep scope limited to APIs available in official documents such as [API Reference](https://platform.TupleleapAI.com/docs/api-reference) or [OpenAPI spec](https://github.com/TupleleapAI/TupleleapAI-openapi/). Other LLMs or AI Providers offer TupleleapAI-compatible APIs, yet they may not always have full parity. In such cases, the TupleleapAI spec takes precedence.
- **Consistency**: Keep code style consistent across all the "APIs" that library exposes; it creates a great developer experience.

This project adheres to [Rust Code of Conduct](https://www.rust-lang.org/policies/code-of-conduct)

## Complimentary Crates

- [tupleleapai-func-enums](https://github.com/frankfralick/TupleleapAI-func-enums) provides procedural macros that make it easier to use this library with TupleleapAI API's tool calling feature. It also provides derive macros you can add to existing [clap](https://github.com/clap-rs/clap) application subcommands for natural language use of command line tools. It also supports TupleleapAI's [parallel tool calls](https://platform.TupleleapAI.com/docs/guides/function-calling/parallel-function-calling) and allows you to choose between running multiple tool calls concurrently or own their own OS threads.
- [async-tupleleapai-wasm](https://github.com/ifsheldon/async-TupleleapAI-wasm) provides WASM support.

