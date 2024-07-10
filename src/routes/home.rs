use anyhow::Result;
use spin_sdk::http::{IntoResponse, Params, Request, Response};
use tera::{Context, Tera};
pub fn handle(req: Request, _: Params) -> Result<impl IntoResponse> {
    let mut tera = Tera::default();
    tera.add_raw_template("base.html", include_str!("../html/base.html"))?;
    tera.add_raw_template("home.html", include_str!("../html/home.html"))?;
    let path = req.uri();
    let current_page = path.trim_matches('/').split('/').last().unwrap_or("").to_string();

    let mut context = Context::new();
    context.insert("url", path);
    context.insert("title", "Kickstart your Spin website");
    context.insert("description", "Home Page");

    context.insert("current_page", &current_page);
    context.insert("content", "This is a lightweight Spin framework to kickstart integrating HTMX for dynamic web applications using WebAssembly hosted on <a href=\"https://www.fermyon.com/cloud\" target=\"_blank\">Fermyon Spin Cloud</a>. Features modular routing, server-side rendering, and HTMX-powered components. Ideal for building interactive, server-driven web experiences with minimal client-side JavaScript.");

    let body = tera.render("home.html", &context)?;

    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/html")
        .body(body)
        .build())
}