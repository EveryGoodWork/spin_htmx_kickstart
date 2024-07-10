use anyhow::Result;
use spin_sdk::http::{IntoResponse, Request, Router};
use spin_sdk::http_component;

mod routes;
mod htmx;

#[http_component]
fn handle_htmx_template(req: Request) -> Result<impl IntoResponse> {
    println!("Handling request to {:?}", req.uri());

    let mut router = Router::new();
    router.get("/", routes::home::handle);
    router.get("/about", routes::about::handle);
    router.get("/examples", routes::examples::handle);
    router.get("/htmx/server_time", htmx::server_time::handle);
    Ok(router.handle(req))
}