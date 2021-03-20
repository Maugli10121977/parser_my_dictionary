#!/bin/bash

arr=`termux-dialog checkbox -v "termux-toast,termux-tts-speak" -t "Выполнение действий:   "`

for i in "${arr[*]}"; do
  val=`echo $i | jq ".values"`
  echo $val > .result_termux_query.txt
done
