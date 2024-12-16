#[path = "events.rs"]
pub mod events;

use events::Time;

use crate::scheduler::events::CourseType;
use crate::scheduler::events::Day;
use crate::scheduler::events::ScheduleCell;
use std::collections::HashMap;
use std::collections::HashSet;

pub fn generate_schedule_table<'a>(
    schedule: &Vec<events::EventCombination<'a>>,
) -> Vec<Vec<ScheduleCell<'a>>> {
    // Time slots based on the Event's from and to times
    let mut time_slots: Vec<(Time, Time)> = Vec::new();

    for hour in 8..=19 {
        let start_time = Time { hour, minute: 0 };
        let end_time = Time { hour, minute: 50 };
        time_slots.push((start_time, end_time));
    }

    // Determine unique days in the schedule
    let mut unique_days: Vec<Day> = schedule
        .iter()
        .flat_map(|combo| {
            let mut days = Vec::new();
            if let Some(lecture) = combo.lecture {
                days.push(lecture.day);
            }
            if let Some(tutorial) = combo.tutorial {
                days.push(tutorial.day);
            }
            days
        })
        .collect::<std::collections::HashSet<_>>()
        .into_iter()
        .collect();

    unique_days.sort();
    // Create header row
    let mut table: Vec<Vec<ScheduleCell<'a>>> = Vec::new();

    // Header row with "Time" and day names
    let mut header_row = vec![ScheduleCell {
        event: None,
        rowspan: 1,
        is_merged: false,
        display_text: Some("Time".to_string()),
    }];
    header_row.extend(unique_days.iter().map(|day| ScheduleCell {
        event: None,
        rowspan: 1,
        is_merged: false,
        display_text: Some(format!("{:?}", day)),
    }));
    table.push(header_row);

    let mut seen_events: HashSet<u16> = HashSet::new();

    // Populate the table with time slots and events
    for (_slot_index, (from, to)) in time_slots.iter().enumerate() {
        let mut row = vec![ScheduleCell {
            event: None,
            rowspan: 1,
            is_merged: false,
            display_text: Some(format!("{} {}", from.to_string(), to.to_string())),
        }];

        // For each unique day, find events in the current time slot
        for &day in &unique_days {
            let cell_event = schedule.iter().find_map(|combo| {
                // Check lecture first
                let lecture_event = combo
                    .lecture
                    .filter(|e| e.day == day && e.from <= *from && e.to >= *to);

                // If no lecture, check tutorial
                let tutorial_event = combo
                    .tutorial
                    .filter(|e| e.day == day && e.from <= *from && e.to >= *to);

                // Prioritize lecture if both exist
                lecture_event.or(tutorial_event)
            });

            let is_merged = match cell_event {
                Some(e) => e.from != *from,
                None => false,
            };

            let rowspan = if !is_merged {
                cell_event.map_or(1, |event| (event.to - event.from) / 50)
            } else {
                1
            };

            // Create cell with event and rowspan
            row.push(ScheduleCell {
                event: cell_event,
                rowspan,
                is_merged: is_merged,
                display_text: cell_event.map(|e| {
                    format!(
                        "{} ({}) - {}\n{}",
                        e.code,
                        match e.r#type {
                            CourseType::Lecture => "Lecture",
                            CourseType::Tutorial => "Tutorial",
                        },
                        e.name,
                        e.location
                    )
                }),
            });

            if let Some(e) = cell_event {
                seen_events.insert(e.id);
            }
        }

        table.push(row);
    }

    table
}

fn satisfies_constraints(lecture: &events::Event, tutorial: &events::Event) -> bool {
    if lecture.pair_group && lecture.group != tutorial.group {
        return false;
    }

    if has_overlap(
        std::option::Option::Some(lecture),
        std::option::Option::Some(tutorial),
    ) {
        return false;
    }

    return true;
}

fn has_overlap(event1: Option<&events::Event>, event2: Option<&events::Event>) -> bool {
    if event1.is_none() || event2.is_none() {
        return false;
    }

    let event1 = event1.unwrap();
    let event2 = event2.unwrap();

    if event1.day != event2.day {
        return false;
    }

    if (event1.from <= event2.from && event2.from < event1.to)
        || (event2.from <= event1.from && event1.from < event2.to)
    {
        return true;
    }

    return false;
}

fn generate(
    course_map: std::collections::HashMap<String, Vec<events::EventCombination<'_>>>,
    course_codes: Vec<String>,
) -> Result<Vec<Vec<events::EventCombination<'_>>>, String> {
    let num_courses = course_codes.len();
    if num_courses == 0 {
        return Err("No courses provided".to_string());
    }

    let mut combinations = Vec::new();

    for code in course_codes {
        match course_map.get(&code) {
            Some(value) => {
                combinations.push(value);
            }
            None => {
                return Err(format!("Course {} not found", code).to_string());
            }
        }
    }

    let mut num_schedules = 1;
    let mut skips = vec![1; num_courses];

    for i in 0..num_courses {
        num_schedules *= combinations[i].len();
        let mut skip = 1;
        for j in i + 1..num_courses {
            skip *= combinations[j].len();
        }
        skips[i] = skip;
    }

    let mut schedules = Vec::new();

    for i in 0..num_schedules {
        let mut schedule = vec![
            events::EventCombination {
                lecture: None,
                tutorial: None,
            };
            num_courses
        ];

        for j in 0..num_courses {
            let idx = i / skips[j] % combinations[j].len();
            schedule[j] = combinations[j][idx];
        }

        schedules.push(schedule);
    }

    for i in (0..(schedules.len())).rev() {
        if !valid_schedule(&schedules[i]) {
            schedules.swap_remove(i);
        }
    }

    return Ok(schedules);
}

fn valid_schedule(schedule: &Vec<events::EventCombination>) -> bool {
    for i in 0..schedule.len() {
        for j in (i + 1)..schedule.len() {
            if has_overlap(schedule[i].lecture, schedule[j].lecture)
                || has_overlap(schedule[i].lecture, schedule[j].tutorial)
                || has_overlap(schedule[i].tutorial, schedule[j].lecture)
                || has_overlap(schedule[i].tutorial, schedule[j].tutorial)
            {
                return false;
            }
        }
    }
    return true;
}

fn create_course_map(
    events: &events::EventList,
) -> HashMap<String, Vec<events::EventCombination<'_>>> {
    let mut course_map = HashMap::new();

    for event in events.courses.iter() {
        let event_combinations = course_map.entry(event.code.clone()).or_insert(Vec::new());

        if event_combinations.len() == 0 {
            match event.r#type {
                events::CourseType::Lecture => {
                    let event_combination = events::EventCombination {
                        lecture: Some(event),
                        tutorial: None,
                    };
                    event_combinations.push(event_combination);
                }
                events::CourseType::Tutorial => {
                    let event_combination = events::EventCombination {
                        lecture: None,
                        tutorial: Some(event),
                    };
                    event_combinations.push(event_combination);
                }
            }
            continue;
        }

        let mut inserted: bool = false;
        let size = event_combinations.len();
        for i in 0..size {
            let event_combination = &event_combinations[i];

            match event.r#type {
                events::CourseType::Lecture => {
                    if event_combination.lecture.is_some() && event_combination.tutorial.is_none() {
                        continue;
                    }

                    if event_combination.lecture.is_some() {
                        if satisfies_constraints(event, event_combination.tutorial.unwrap()) {
                            let new_combination = events::EventCombination {
                                lecture: Some(event),
                                tutorial: event_combination.tutorial,
                            };

                            if !event_combinations.contains(&new_combination) {
                                event_combinations.push(new_combination);
                                inserted = true;
                            }
                        }
                        continue;
                    }

                    if event_combination.tutorial.is_some() {
                        if satisfies_constraints(event, event_combination.tutorial.unwrap()) {
                            event_combinations[i].lecture = Some(event);
                            inserted = true;
                        }
                        continue;
                    }
                }
                events::CourseType::Tutorial => {
                    if event_combination.tutorial.is_some() && event_combination.lecture.is_none() {
                        continue;
                    }

                    if event_combination.tutorial.is_some() {
                        if satisfies_constraints(event_combination.lecture.unwrap(), event) {
                            let new_combination = events::EventCombination {
                                lecture: event_combination.lecture,
                                tutorial: Some(event),
                            };

                            if !event_combinations.contains(&new_combination) {
                                event_combinations.push(new_combination);
                                inserted = true;
                            }
                        }
                        continue;
                    }

                    if event_combination.lecture.is_some() {
                        if satisfies_constraints(event, event_combination.lecture.unwrap()) {
                            event_combinations[i].tutorial = Some(event);
                            inserted = true;
                        }
                        continue;
                    }
                }
            }
        }

        if !inserted {
            match event.r#type {
                events::CourseType::Lecture => {
                    let event_combination = events::EventCombination {
                        lecture: Some(event),
                        tutorial: None,
                    };
                    event_combinations.push(event_combination);
                }
                events::CourseType::Tutorial => {
                    let event_combination = events::EventCombination {
                        lecture: None,
                        tutorial: Some(event),
                    };
                    event_combinations.push(event_combination);
                }
            }
        }
    }
    return course_map;
}

fn rate_schedule(schedule: &Vec<events::EventCombination>) -> i32 {
    let mut days = [false; 7];
    let mut start_times = [events::Time {
        hour: 25,
        minute: 0,
    }; 7];
    let mut end_times = [events::Time { hour: 0, minute: 0 }; 7];

    for i in 0..schedule.len() {
        let lecture = schedule[i].lecture.unwrap();
        let lecture_day = lecture.day as usize;

        days[lecture_day] = true;

        if lecture.from < start_times[lecture_day] {
            start_times[lecture_day] = lecture.from;
        }
        if lecture.to > end_times[lecture_day] {
            end_times[lecture_day] = lecture.to;
        }

        match schedule[i].tutorial {
            Some(tutorial) => {
                let tutorial_day = tutorial.day as usize;
                days[tutorial_day] = true;

                if tutorial.from < start_times[tutorial_day] {
                    start_times[tutorial_day] = tutorial.from;
                }
                if tutorial.to > end_times[tutorial_day] {
                    end_times[tutorial_day] = tutorial.to;
                }
            }
            None => {}
        }
    }

    let mut num_days = 0;
    let mut ranges = 0;
    for i in 0..7 {
        if days[i] {
            num_days += 1;
            ranges += end_times[i] - start_times[i];
        }
    }
    return num_days * 1000 + ranges;
}

pub fn generate_schedules(
    value: &events::EventList,
    course_codes: Vec<String>,
) -> Result<Vec<Vec<events::EventCombination>>, String> {
    let course_map = create_course_map(value);

    let schedules = generate(course_map, course_codes);

    if schedules.is_err() {
        return schedules;
    }

    let mut schedules = schedules.unwrap();
    schedules.sort_by(|a, b| rate_schedule(a).cmp(&rate_schedule(b)));

    return Ok(schedules);
}

pub fn generate_day_map<'a>(
    schedule: &'a Vec<events::EventCombination<'a>>,
) -> HashMap<usize, Vec<&'a events::Event>> {
    let mut day_map: HashMap<usize, Vec<&events::Event>> = HashMap::new();

    for course_combination in schedule {
        if let Some(lecture) = &course_combination.lecture {
            let day = lecture.day as usize;
            day_map.entry(day).or_insert_with(Vec::new).push(lecture);
        }
        if let Some(tutorial) = &course_combination.tutorial {
            let day = tutorial.day as usize;
            day_map.entry(day).or_insert_with(Vec::new).push(tutorial);
        }
    }
    for events in day_map.values_mut() {
        events.sort_by(|a, b| a.from.cmp(&b.from));
    }

    return day_map;
}
