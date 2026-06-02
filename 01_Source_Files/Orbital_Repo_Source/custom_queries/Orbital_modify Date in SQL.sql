/* Simple query qhere the date field gets updated */

select path,
  directory,
  filename,
  size, 
  date(btime,"unixepoch", "UTC") AS creation_date
from file
where path like"C:\Program Files\Cisco\AMP\%\sfc.exe";
