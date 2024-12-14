use futures_util::StreamExt;
use pyo3::prelude::*;
use pyo3::{prelude::*, wrap_pyfunction};
use std::fs::File;
use std::io::{Cursor, Read};
use tupleleap_sdk::document_loaders::lo_loader::LoPdfLoader;
use tupleleap_sdk::document_loaders::Loader;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

// #[pyfunction]
// pub fn sum_as_async(py: Python, a: usize, b: usize) -> PyResult<String> {
//     pyo3_async_runtimes::tokio::future_into_py(py, async {
//         tokio::time::sleep(std::time::Duration::from_secs(1)).await;
//         sum_as_string(a, b)
//     })
// }

#[pyfunction]
fn sum_as_string_async(py: Python, a: usize, b: usize) -> PyResult<Bound<PyAny>> {
    pyo3_async_runtimes::tokio::future_into_py(py, async move {
        tokio::time::sleep(std::time::Duration::from_secs(a.clone() as u64)).await;
        sum_as_string(a, b)
    })
}

#[pyfunction]
/// This is an async python function to parse pdf
fn pdf_parse_async(py: Python, path: String) -> PyResult<Bound<PyAny>> {
    pyo3_async_runtimes::tokio::future_into_py(py, async move { pdf_parse(&path).await })
}

/// This is the rust async function to parse PDF
pub async fn pdf_parse(path: &str) -> PyResult<Vec<String>> {
    let mut file = File::open(path).unwrap();
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).unwrap();
    let reader = Cursor::new(buffer);

    let loader = LoPdfLoader::new(reader).expect("Failed to create PdfLoader");

    let mut docs = loader
        .load()
        .await
        .unwrap()
        .map(|d| d.unwrap())
        .collect::<Vec<_>>()
        .await;
    let pages: Vec<String> = docs.drain(..).map(|doc| doc.page_content).collect();
    Ok(pages)
}

/// A Python module implemented in Rust.
#[pymodule]
fn tupleleap_python_sdk(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string_async, m)?)?;
    m.add_function(wrap_pyfunction!(pdf_parse_async, m)?)?;
    Ok(())
}
