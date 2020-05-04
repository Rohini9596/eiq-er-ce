#!/bin/bash
if [ "$(whoami &2>/dev/null)" != "root" ] && [ "$(id -un &2>/dev/null)" != "root" ]
    then
    path="$(dirname "$(pwd)")"/.rnd
else
    root_path="/root/.rnd"
    path="$(dirname "$(pwd)")"/.rnd
fi
touch $path $root_path
a=$1
echo $a
# Setting tls_hostname as the provided ip address while generating certs

for i in $(find $PWD -type  f -name \*.flags); do # Not recommended, will break on whitespace
    sed  's/tls_hostname=.*/tls_hostname='"$a"':9000/g' $i > "${1}_copy"
    rm -rf $i
    mv "${1}_copy" $i
done
rm -rf $path $root_path
