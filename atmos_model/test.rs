fn main() {
    pub const EULER: f64 = 2.71828182845904523536028747135266250;
    
	let mut t_m: f64 = 300.0; // Initialize thermodynamic temperature
    let mut p: f64 = 101325.0; // Initialize Pressure
    let z: f64 = 20.10;
    let z_check = z as i64;
    let z_3 = f64::powf(z,3.0);
    let z_2 = f64::powf(z,2.0);
    
    if (z_check >= 0) && (z_check < 11) {
        t_m = 288.15 - 6.5 * z; 
        p *= f64::powf(288.15/t_m,34.1632/-6.5);
    } else if (z_check >= 11) && (z_check < 20) {
        t_m = 216.65;
        p = 22632.06 * f64::powf(EULER,-34.1632*(z-11.0)/t_m);
    } else if (z_check >= 20) && (z_check < 32) {
        t_m = 196.65 + z;
        let b = 216.65/(196.65 + z);
        p = 5474.889 * f64::powf(b,34.1632);
        drop(b);
    } else if (z_check >= 32) && (z_check < 47) {
        t_m = 139.05 + 2.8 * z;
        let bb = 228.65 / (228.65 + 2.8 * (z-32.0));
        p = 868.0187 * f64::powf(bb,34.1632/2.8);
        drop(bb);
    } else if (z_check >= 47) && (z_check < 51) {
        t_m = 270.65;
        p = 110.9063 * f64::powf(EULER,-34.1632*(z-47.0)/270.65);
    } else if (z_check >= 51) && (z_check < 71) {
        t_m = 413.45 - 2.8 * z;
        let c = 270.65 / (270.65 - 2.8 * (z-51.0));
        p = 66.93887 * f64::powf(c,34.1632/-2.8);
        drop(c);
    } else if (z_check >= 71) && (z < 84.852) {
        t_m = 356.65 - 2.0 * z;
        let cc = 214.65 / (214.65-2.0 * (z-71.0));
        p = 3.956420 * f64::powf(cc,34.1632/-2.0);
        drop(cc);
    } else if (z_check >= 86) && (z_check < 91) {
        t_m = 186.8673;
        p = (2.159582e-6*z_3) + (-4.836957e-4*z_2) + (-0.1425192*z) + 13.47530;
    } else if (z_check >= 91) && (z_check < 110) {
        let sqr = 1.0 - f64::powf(z-91.0/-19.9429, 2.0);
        t_m = 263.1905 - 76.3232 * sqr.sqrt();
        if z_check >= 100 {p = (6.693926e-5*z_3) + (-0.01945388*z_2) + (1.719080*z) - 47.75030;}
        else {p = (3.304895e-5*z_3) + (-0.009062730*z_2) + (0.6516698*z) - 11.03037;}
    } else if (z_check >= 110) && (z_check < 120) {
        t_m = 240.0 + 12.0 * (z-110.0);
        p = (-6.539316e-5*z_3) + (0.02485568*z_2) + (-3.223620*z) + 135.9355;
    } else if (z_check >= 120) && (z_check < 1000) {
        let epsilon = (z-120.0) * (6356.766+120.0)/(6356.766+z);
        t_m = 1000.0 - 640.0 * f64::powf(EULER,-0.01875*epsilon);
        p = 0.0;
    }

    println!("{} and {}",p,t_m);
}
