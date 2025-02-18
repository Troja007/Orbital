SELECT 
p.pid, p.name, p.path, p.cmdline, p.state, h.sha256 
FROM processes p 
INNER JOIN hash h 
ON p.path=h.path;