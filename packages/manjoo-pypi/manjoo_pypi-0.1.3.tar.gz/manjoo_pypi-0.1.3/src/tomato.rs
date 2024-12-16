use ratatui::{
    style::Color,
    widgets::canvas::{Painter, Shape},
};

pub struct Tomato {
    pub x: f64,
    pub y: f64,
    pub radius: f64,
}

impl Shape for Tomato {
    fn draw(&self, painter: &mut Painter) {
        let mut x = 0;
        let mut y = self.radius as i32;
        let mut d = 3 - 2 * y;

        let draw_circle_points = |painter: &mut Painter, cx: f64, cy: f64, x: i32, y: i32| {
            let points = [
                (cx + x as f64, cy + y as f64),
                (cx - x as f64, cy + y as f64),
                (cx + x as f64, cy - y as f64),
                (cx - x as f64, cy - y as f64),
                (cx + y as f64, cy + x as f64),
                (cx - y as f64, cy + x as f64),
                (cx + y as f64, cy - x as f64),
                (cx - y as f64, cy - x as f64),
            ];

            for &(px, py) in &points {
                painter.paint(px as usize, py as usize, Color::Red);
            }
        };

        while x <= y {
            draw_circle_points(painter, self.x, self.y, x, y);
            if d < 0 {
                d = d + 4 * x + 6;
            } else {
                d = d + 4 * (x - y) + 10;
                y -= 1;
            }
            x += 1;
        }

        let mut stack = vec![(self.x as i32, self.y as i32)];
        let mut visited = std::collections::HashSet::new();

        while let Some((cx, cy)) = stack.pop() {
            if visited.contains(&(cx, cy)) {
                continue;
            }
            visited.insert((cx, cy));

            if (cx as f64 - self.x).powi(2) + (cy as f64 - self.y).powi(2) <= self.radius.powi(2) {
                painter.paint(cx as usize, cy as usize, Color::Red);

                stack.push((cx + 1, cy));
                stack.push((cx - 1, cy));
                stack.push((cx, cy + 1));
                stack.push((cx, cy - 1));
            }
        }
		let stem_height = self.radius/1.5;
        for i in 0..stem_height as i32 {
            painter.paint(self.x as usize, (self.y - self.radius - i as f64) as usize, Color::Green);
        }
		
    }
}