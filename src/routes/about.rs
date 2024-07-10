use anyhow::Result;
use spin_sdk::http::{IntoResponse, Params, Request, Response};
use tera::{Context, Tera};

pub fn handle(req: Request, _: Params) -> Result<impl IntoResponse> {
    let mut tera = Tera::default();
    tera.add_raw_template("base.html", include_str!("../html/base.html"))?;
    tera.add_raw_template("about.html",  include_str!("../html/about.html"))?;

    let mut context = Context::new();
    context.insert("url", &req.header("spin-full-url").map(|v| v.as_str()).unwrap_or_default());
    context.insert("title", "About Us");
    context.insert("description", "About Us page");
    context.insert("current_page", "about");
    context.insert("content", "Every Good Work, Inc.  Custom Software Development.");

    let body = tera.render("about.html", &context)?;

    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/html")
        .body(body)
        .build())
}