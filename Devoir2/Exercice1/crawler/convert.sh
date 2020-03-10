#!/bin/sh

sed '1d;$d' data.json | sed '/\[\]/d' | sed 's/},/}/' | sort > scala_readable.json
