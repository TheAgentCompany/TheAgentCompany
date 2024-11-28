Clone http://the-agent-company.com:8929/root/bustub to /workspace folder and complete http://the-agent-company.com:8929/root/bustub/-/issues/759 locally. Specifically, complete 4 files: 
- "bustub/src/include/primer/hyperloglog.h",
- "bustub/src/include/primer/hyperloglog_presto.h",
- "bustub/src/primer/hyperloglog.cpp",
- "bustub/src/primer/hyperloglog_presto.cpp",

To ensure compatibility of testing across different operating systems, please change the line "hash = ((hash << 5) ^ (hash >> 27)) ^ bytes[i];" in your local file "src/include/common/util/hash_util.h" to "hash = ((hash << 5) ^ (hash >> 27)) ^ static_cast<signed char>(bytes[i]);"
