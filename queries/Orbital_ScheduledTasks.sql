SELECT st.name, st.action, st.path, st.enabled, st.state,
date(st.last_run_time,"unixepoch", "UTC") AS "Last Run",
date(st.next_run_time,"unixepoch", "UTC") AS "Next Run",
st.last_run_code
FROM scheduled_tasks st
WHERE st.path NOT LIKE "\Microsoft\Windows%"
AND name like "%fileless%";
