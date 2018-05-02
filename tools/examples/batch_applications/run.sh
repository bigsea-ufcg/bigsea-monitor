#!/bin/bash
# Copyright (c) 2017 UFCG-LSD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

python cpu_bound.py $1 $2 $3 $4 $5 $6 $7 $8 &
touch progress.txt

TOTAL_TASKS=$(( $1 * $6 ))
COMPLETED_TASKS=`wc -l progress.txt | awk '{ print $1 }'`

while [ "$COMPLETED_TASKS" -ne "$TOTAL_TASKS" ] 
do
	PROGRESS=`echo "$COMPLETED_TASKS / $TOTAL_TASKS" | bc -l | awk '{printf "%08f\n", $0}'`
	COMPLETED_TASKS=`wc -l progress.txt | awk '{ print $1 }'`
	echo "`date +[%Y-%m-%dT%H:%M:%SZ]`[Progress]: #$PROGRESS" >> $9
	sleep 1
done

echo "`date +[%Y-%m-%dT%H:%M:%SZ]`[Progress]: #1.0" >> $9

rm progress.txt

#sleep 10

#shutdown -h now
