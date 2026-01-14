select build_platform, build_distro, pid, version, uuid, instance_id, config_hash, config_valid, extensions, datetime(start_time, "unixepoch", "UTC") AS STARTUPTIME, watcher
from osquery_info;