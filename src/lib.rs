#![allow(unused)]
use pyo3::prelude::*;

#[pyfunction]
fn calc_sim(z:f64,mass:f64,m_dot:f64,v:f64,c0:f64,ft:f64,area:f64,theta:f64,x_pos:f64,y_pos:f64,t:f64) -> PyResult<Vec<f64>> {
    let dt = 0.1;
    
    //gravity equation
    let distance = z+6371000.0;
    let g_t = (6.674e-11*5.972e24)/f64::powf(distance,2.0);
    
    //mass update
    let m = mass - m_dot;
    
    //Model the atmosphere
    pub const EULER: f64 = 2.71828182845904523536028747135266250;
	let mut t_m: f64 = 300.0; // Initialize thermodynamic temperature
    let mut p: f64 = 0.0; // Initialize Pressure
    let z_km = z/1000.0;
    let z_check = z_km as i64;
    let z_4 = f64::powf(z_km,4.0);
    let z_3 = f64::powf(z_km,3.0);
    let z_2 = f64::powf(z_km,2.0);
    let m_0: f64 = 28.9644; //kg/kmol
    let r_star: f64 = 0.0083144621; //kg(km/s)2/kmol-K 
    let mut rho = p * m_0 / (r_star * t_m); //initialize density
    
    if (z_check >= 0) && (z_check < 11) {
        t_m = 288.15 - 6.5 * z_km; 
        p *= f64::powf(288.15/t_m,34.1632/-6.5);
    } else if (z_check >= 11) && (z_check < 20) {
        t_m = 216.65;
        p = 22632.06 * f64::powf(EULER,-34.1632*(z_km-11.0)/t_m);
    } else if (z_check >= 20) && (z_check < 32) {
        t_m = 196.65 + z_km;
        let b = 216.65/(196.65 + z_km);
        p = 5474.889 * f64::powf(b,34.1632);
        drop(b);
    } else if (z_check >= 32) && (z_check < 47) {
        t_m = 139.05 + 2.8 * z_km;
        let bb = 228.65 / (228.65 + 2.8 * (z_km-32.0));
        p = 868.0187 * f64::powf(bb,34.1632/2.8);
        drop(bb);
    } else if (z_check >= 47) && (z_check < 51) {
        t_m = 270.65;
        p = 110.9063 * f64::powf(EULER,-34.1632*(z_km-47.0)/270.65);
    } else if (z_check >= 51) && (z_check < 71) {
        t_m = 413.45 - 2.8 * z_km;
        let c = 270.65 / (270.65 - 2.8 * (z_km-51.0));
        p = 66.93887 * f64::powf(c,34.1632/-2.8);
        drop(c);
    } else if (z_check >= 71) && (z < 84.852) {
        t_m = 356.65 - 2.0 *z_km;
        let cc = 214.65 / (214.65-2.0 * (z_km-71.0));
        p = 3.956420 * f64::powf(cc,34.1632/-2.0);
        drop(cc);
    } else if (z_check >= 86) && (z_check < 91) {
        t_m = 186.8673;
        p = (2.159582e-6*z_3) + (-4.836957e-4*z_2) + (-0.1425192*z_km) + 13.47530;
        rho =  (-3.322622e-6*z_3) + (9.111460*z_2) + (-0.2609971*z_km) + 5.944694;
    } else if (z_check >= 91) && (z_check < 110) {
        let sqr = 1.0 - f64::powf(z_km-91.0/-19.9429, 2.0);
        t_m = 263.1905 - 76.3232 * sqr.sqrt();
        if z_check >= 100 {
            p = (6.693926e-5*z_3) + (-0.01945388*z_2) + (1.719080*z_km) - 47.75030;
            rho = (-1.240774e-5*z_4) + (0.005162063*z_3) + (-0.8048342*z_2) + (55.55996*z_km) - 1443.338;}
        else {
            p = (3.304895e-5*z_3) + (-0.009062730*z_2) + (0.6516698*z_km) - 11.03037;
            rho = (2.873405e-5*z_3) + (-0.008492037*z_2) + (0.6541179*z_km) - 23.62010; 
        }
    } else if (z_check >= 110) && (z_check < 120) {
        t_m = 240.0 + 12.0 * (z_km-110.0);
        p = (-6.539316e-5*z_3) + (0.02485568*z_2) + (-3.223620*z_km) + 135.9355;
        rho = (-8.854164e-5*z_3) + (0.03373254*z_2) + (-4.390837*z_km)+ 176.5294; 
    } else if (z_check >= 120) && (z_check < 1000) {
        let epsilon = (z_km-120.0) * (6356.766+120.0)/(6356.766+z_km);
        t_m = 1000.0 - 640.0 * f64::powf(EULER,-0.01875*epsilon);
        p = 0.0;
        if z_check < 150 {
            let r_pow = (3.661771e-7*z_4) + (-2.154344e-4*z_3) + (0.04809214*z_2) + (-4.884744*z_km) + 172.3597;
            rho = f64::powf(EULER,r_pow)
        } 
        else {rho = 2.0763e-9;}
    drop(z_km);
    }
    
    //Drag Coefficient Calculations
    let speed_sound = (1.4*287.0*t_m).sqrt();
    let mut mach = v/speed_sound;
    let mut cd: f64;
    if mach < 1.0 {
        cd = c0/(1.0-f64::powf(mach,2.0)).sqrt();
    } else if mach == 1.0 {
        mach = 0.999999;
        cd = c0/(1.0-f64::powf(mach,2.0)).sqrt();
    } else {
        cd = c0/(f64::powf(mach,2.0)-1.0).sqrt();
    }
    
    //Update thrust
    let thrust = 560000.0/m;
    
    //Drag force
    let mut drag = 0.5 * rho * f64::powf(v,2.0) * cd * area;
    if v < 0.1 {
        drag *= -1.0;
    }
    //euler-cromer
    let v_t = v + (thrust - drag - g_t)*dt;
    let z_t = (z + v_t)*dt;
    
    //3D
    let v_x = v * theta.cos();
    let v_y = v * theta.sin();
    let x = x_pos + (v_x*t);
    let y = y_pos + (v_y*t - (0.5*g_t*f64::powf(t,2.0)));
    
    let values = vec![z_t,m,v_t,thrust,x,y];
    return Ok(values);
}

#[pymodule]
fn atmos_model(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calc_sim, m)?)?;
    Ok(())
    }
    

