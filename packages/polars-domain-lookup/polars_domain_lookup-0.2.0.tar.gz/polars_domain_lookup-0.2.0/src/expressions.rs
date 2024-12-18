#![allow(clippy::unused_unit)]
use serde::Deserialize;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::fs::read_to_string;

#[derive(Deserialize)]
struct TopDomainsFileKwargs {
    top_domains_file: String,
}

#[polars_expr(output_type=Boolean)]
fn is_common_domain(inputs: &[Series], kwargs: TopDomainsFileKwargs) -> PolarsResult<Series> {
    let cisco_umbrella: Vec<String> = get_common_domains(&kwargs.top_domains_file);

    let ca: &StringChunked = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(
        DataType::Boolean, |x| cisco_umbrella.contains(&x.to_string())
    );
    Ok(out.into_series())
}

fn get_common_domains(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        let line_string = line.to_string();

        result.push(line_string);
    }

    result
}
