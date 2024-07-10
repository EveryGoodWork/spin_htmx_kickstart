use anyhow::Result;
use spin_sdk::http::{IntoResponse, Params, Request, Response};
use tera::{Context, Tera};
use chrono::{DateTime, Utc};

pub fn handle(_: Request, _: Params) -> Result<impl IntoResponse> {
    let mut tera = Tera::default();
    tera.add_raw_template("server_time.html", include_str!("../html/server_time.html"))?;
    let utc_now: DateTime<Utc> = Utc::now();
    let utc_time = utc_now.format("%Y/%m/%d %H:%M:%S UTC").to_string();

    let mut context = Context::new();
    context.insert("utc_time", &utc_time);

    let body = tera.render("server_time.html", &context)?;

    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/html")
        .body(body)
        .build())
}