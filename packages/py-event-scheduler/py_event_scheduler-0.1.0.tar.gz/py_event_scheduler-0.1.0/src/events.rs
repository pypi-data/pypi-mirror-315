use core::ops;
use pyo3::types::PyAnyMethods;
use pyo3::types::PyDict;
use pyo3::Py;
use pyo3::PyAny;
use pyo3::ToPyObject;
use serde::ser::SerializeMap;
use serde::{Deserialize, Deserializer, Serialize};
use std::cmp::Ordering;
use std::collections::HashMap;
use std::fmt::Display;
use std::fmt::Formatter;
use std::str::FromStr;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum CourseType {
    Lecture,
    Tutorial,
}

impl ToString for CourseType {
    fn to_string(&self) -> String {
        match self {
            CourseType::Lecture => "Lecture".to_string(),
            CourseType::Tutorial => "Tutorial".to_string(),
        }
    }
}

#[derive(Serialize, Clone, Debug, Copy)]
pub struct Time {
    pub hour: i32,
    pub minute: i32,
}

impl ToString for Time {
    fn to_string(&self) -> String {
        if self.minute.to_string().len() == 1 {
            return self.hour.to_string() + ":" + "0" + &self.minute.to_string();
        } else {
            return self.hour.to_string() + ":" + &self.minute.to_string();
        }
    }
}

impl ops::Sub<Time> for Time {
    type Output = i32;

    fn sub(self, other: Time) -> Self::Output {
        (self.hour * 60 + self.minute) - (other.hour * 60 + other.minute)
    }
}

impl PartialOrd for Time {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match self.hour.cmp(&other.hour) {
            Ordering::Equal => self.minute.cmp(&other.minute).into(),
            other => Some(other),
        }
    }
}

impl PartialEq for Time {
    fn eq(&self, other: &Self) -> bool {
        self.hour == other.hour && self.minute == other.minute
    }
}

impl Eq for Time {}

impl Ord for Time {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

impl FromStr for Time {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split(":").collect();
        if parts.len() != 3 {
            return Err(format!("Invalid time format: {}", s));
        }

        let hour = parts[0].parse::<i32>().map_err(|_| "Invalid hour")?;
        let minute = parts[1].parse::<i32>().map_err(|_| "Invalid minute")?;

        Ok(Time { hour, minute })
    }
}

impl<'de> Deserialize<'de> for Time {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        Time::from_str(&s).map_err(serde::de::Error::custom)
    }
}

#[derive(Serialize, Deserialize, Clone, Debug, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Day {
    Sunday,
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
}

impl ToString for Day {
    fn to_string(&self) -> String {
        match self {
            Day::Sunday => "Sunday".to_string(),
            Day::Monday => "Monday".to_string(),
            Day::Tuesday => "Tuesday".to_string(),
            Day::Wednesday => "Wednesday".to_string(),
            Day::Thursday => "Thursday".to_string(),
            Day::Friday => "Friday".to_string(),
            Day::Saturday => "Saturday".to_string(),
        }
    }
}

#[derive(Serialize, Deserialize, Clone, Debug)]

pub struct Event {
    pub id: u16,
    pub code: String,
    pub name: String,
    pub group: u8,
    pub r#type: CourseType,
    pub day: Day,
    pub from: Time,
    pub to: Time,
    pub class_size: u16,
    pub enrolled: i32,
    pub waiting: i32,
    pub status: bool,
    pub location: String,
    pub date: String,
    pub credits: u8,
    pub pair_group: bool,
    pub requires_tutorial: bool,
}

impl ToPyObject for Event {
    fn to_object(&self, py: pyo3::Python<'_>) -> Py<PyAny> {
        let dict = PyDict::new_bound(py);

        dict.set_item("id", self.id).unwrap();
        dict.set_item("code", &self.code).unwrap();
        dict.set_item("name", &self.name).unwrap();
        dict.set_item("group", self.group).unwrap();
        dict.set_item("type", self.r#type.to_string()).unwrap();
        dict.set_item("day", self.day.to_string()).unwrap();
        dict.set_item("from", self.from.to_string()).unwrap();
        dict.set_item("to", self.to.to_string()).unwrap();
        dict.set_item("class_size", self.class_size).unwrap();
        dict.set_item("enrolled", self.enrolled).unwrap();
        dict.set_item("waiting", self.waiting).unwrap();
        dict.set_item("status", self.status).unwrap();
        dict.set_item("location", &self.location).unwrap();
        dict.set_item("date", &self.date).unwrap();
        dict.set_item("credits", self.credits).unwrap();
        dict.set_item("pair_group", self.pair_group).unwrap();
        dict.set_item("requires_tutorial", self.requires_tutorial)
            .unwrap();

        dict.to_object(py)
    }
}

#[derive(Clone)]
pub struct ScheduleCell<'a> {
    pub event: Option<&'a Event>,
    pub rowspan: i32,
    pub is_merged: bool,
    pub display_text: Option<String>,
}

impl ToPyObject for ScheduleCell<'_> {
    fn to_object(&self, py: pyo3::Python<'_>) -> Py<PyAny> {
        let dict = PyDict::new_bound(py);
        dict.set_item("event", self.event.to_object(py)).unwrap();
        dict.set_item("rowspan", self.rowspan).unwrap();
        dict.set_item("is_merged", self.is_merged).unwrap();
        dict.set_item("display_text", &self.display_text).unwrap();

        dict.to_object(py)
    }
}

impl PartialEq for Event {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}
#[derive(Debug, Clone, Copy)]
pub struct EventCombination<'a> {
    pub lecture: Option<&'a Event>,
    pub tutorial: Option<&'a Event>,
}

impl<'a> PartialEq for EventCombination<'a> {
    fn eq(&self, other: &Self) -> bool {
        self.lecture == other.lecture && self.tutorial == other.tutorial
    }
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct EventList {
    pub courses: Vec<Event>,
}

#[derive(Clone, Debug)]
pub struct DaySchedule<'a> {
    map: HashMap<usize, Vec<&'a Event>>,
}

impl Serialize for DaySchedule<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut map = serializer.serialize_map(Some(self.map.len()))?;
        for (k, v) in &self.map {
            map.serialize_entry(&k, &v)?;
        }
        map.end()
    }
}

impl Display for DaySchedule<'_> {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        write!(f, "{:?}", self.map)
    }
}
