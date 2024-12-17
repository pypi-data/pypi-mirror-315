use pyo3::prelude::*;

#[pyfunction]
fn run(args: Vec<String>) -> PyResult<()> {
    run_manjoo(&args)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
}

#[pymodule]
fn manjoo_pypi(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run,m)?)?;
    m.add_function(wrap_pyfunction!(main,m)?)?;
    Ok(())
}
#[pyfunction]
fn main() -> PyResult<()> {
    // Collect command-line arguments, excluding the script name
    let args: Vec<String> = std::env::args().skip(1).collect();
    run(args)
}
mod manjoo;
mod tomato;
mod constants;
use manjoo::Manjoo;
use ratatui::{
    backend::TermwizBackend, layout::Alignment, symbols::Marker, widgets::{canvas::Canvas, Block}, Terminal
};
use std::{
    error::Error,
    thread,
    time::{Duration, Instant}
};
use tomato::Tomato;

pub fn run_manjoo(args: &[String]) -> Result<(), Box<dyn Error>> {
    if !args.is_empty() && args[1] == "run"{
        let backend = TermwizBackend::new()?;
    let mut terminal = Terminal::new(backend)?;
    
    let now = Instant::now();
    let mut sleep_duration = 30;
    let mut render_static = true;
    let mut running_manjoo_x: usize = 0;
    let mut running_flag = false;
    let mut has_tomato = false;
    let mut size_global = ratatui::layout::Rect::default();
    let scale = 1;
    let tomato_radius = scale as f64 * 3 as f64;
    
    while now.elapsed() < Duration::from_secs(17) {
        terminal.draw(|f| {
            let size = f.area();
            size_global = size.clone();
            let canvas = Canvas::default()
                .block(
                    Block::default()
                        .borders(ratatui::widgets::Borders::ALL)
                        .title("WheekHigh, RIP MANJOO").title_alignment(Alignment::Center),
                )
                .x_bounds([0.0, (size.width * 2) as f64])
                .y_bounds([0.0, (size.height * 2) as f64])
                .marker(Marker::HalfBlock)
                .paint(|ctx| {
                    let tomato_y = size.height as f64 ;
                    if !has_tomato {
                        ctx.draw(&Tomato {
                            x: size.width as f64 / 2.0,
                            y: tomato_y,
                            radius: tomato_radius,
                        });
                    }
                    if render_static {
                        ctx.draw(&Manjoo {
                            scale,
                            is_static: true,
                            x_position: running_manjoo_x,
                            y_position: tomato_y,
                            running_flag,
                            has_tomato: false,
                        });
                    } else {
                        ctx.draw(&Manjoo {
                            scale,
                            is_static: false,
                            x_position: running_manjoo_x,
                            y_position: tomato_y,
                            running_flag,
                            has_tomato,
                        })
                    }
                });
            f.render_widget(canvas, size);
        })?;
        if render_static {
            render_static = !render_static;
            thread::sleep(Duration::from_secs(2));
        }
        if !render_static {
            running_flag = !running_flag;
            running_manjoo_x += 2;
            if running_manjoo_x > (size_global.width * 2) as usize {
                running_manjoo_x = 0;
            }
            let tomato_x = (size_global.width as f64 / 2.0) as usize - (tomato_radius as usize) * 15;
            if running_manjoo_x >= (tomato_x) {
                sleep_duration = 100;
                has_tomato = true;
            }
        }
        thread::sleep(Duration::from_millis(sleep_duration));
    }

    terminal.show_cursor()?;
    terminal.flush()?;
    }
    else{
        println!("Usage: manjoo run")
    }

    Ok(())
}
