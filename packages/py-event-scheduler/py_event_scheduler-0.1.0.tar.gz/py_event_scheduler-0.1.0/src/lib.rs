mod scheduler;
use pyo3::exceptions::PyException;
use pyo3::exceptions::PyFileNotFoundError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use scheduler::generate_schedule_table;
use std::fs;

#[pyfunction]
fn rust_generate_schedule_table(
    py: Python<'_>,
    courses_path: String,
    course_codes: Vec<String>,
) -> PyResult<pyo3::Bound<'_, PyList>> {
    let json_string = fs::read_to_string(courses_path)
        .map_err(|_| PyFileNotFoundError::new_err("File not found"))?;

    let event_list =
        serde_json::from_str(&json_string).map_err(|_| PyException::new_err("Invalid JSON"))?;

    let schedules = scheduler::generate_schedules(&event_list, course_codes)
        .map_err(|e| PyException::new_err(e.to_string()))?;

    let table = schedules
        .iter()
        .map(|schedule| generate_schedule_table(schedule));

    let list = PyList::new_bound(py, table);

    return Ok(list);
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_event_scheduler(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_generate_schedule_table, m)?)?;
    Ok(())
}
