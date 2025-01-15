WITH FIRST_QUERY AS (SELECT DISTINCT
    proc.pid,
    proc.path,
    proc.cmdline,
    proc.cwd,
    mmap.path AS mmap_path
FROM process_memory_map AS mmap
LEFT JOIN processes AS proc USING(pid)
)

SELECT * FROM FIRST_QUERY
JOIN yara ON yara.path = FIRST_QUERY.mmap_path

WHERE sigrule = 'rule openssl_3 {
strings:
$re1 = /OpenSSL\s3.[0-6]{1}.[0-9]{1}[a-z]{,1}/
condition:
$re1
}
'
AND yara.count > 0
