#!/bin/bash

input_dir=$1
output_dir=$2
scripts_dir=/usr/local/bin/nLogReporter

# if output_dir doesn't exist - then, create it
mkdir -p ${output_dir}

# 1) generalLog and counter.txt
for dir in $(find $input_dir -mindepth 1 -maxdepth 1 -type d); do 
  unzip -p -P fixmeplease ${dir}/*2017*.zip generalLog.txt | iconv -f UTF-16 1>${output_dir}/$(basename ${dir}).generalLog.txt; 
  unzip -p -P fixmeplease ${dir}/*2017*.zip countersForAllTestTypesDeterminations.txt | iconv -f UTF-16 1>${output_dir}/$(basename ${dir}).counters.txt; 
done

# 2) Get an aggregate report for counters
for file in $(find ${output_dir} -type f -name "*counters.txt"); do 
  name=$(basename $file | sed -e "s/.counters.txt//g"); 
  sed -ne "2,$ p" $file | awk -v total=0 -v file_name=${name} '{ total += $2; } END{ print file_name,total; }'; 
done 1>${output_dir}/aggregate_counters.txt

# 3) Hard and soft
for file in $(find ${output_dir} -mindepth 1 -maxdepth 1 -type f -name "*.generalLog.txt"); do 
  sys_name=$(basename $file | sed -e "s/.generalLog.txt//g"); 
  cat $file | python3 ${scripts_dir}/separate_log_into_hard_and_soft.py 1>${output_dir}/${sys_name}.hard.txt 2>${output_dir}/${sys_name}.soft.txt; 
done

# 4) Time diff for lld
for log_file in $(find ${output_dir} -mindepth 1 -maxdepth 1 -type f -name "*hard.txt" -o -name "*soft.txt"); do 
  name=$(basename $log_file | sed -e "s/.txt/_lld.txt/g"); 
  cat $log_file | awk 'BEGIN { FS="\t"; OFS="\t"; }{ print $1,$3,$6 }' | python3 ${scripts_dir}/time_diff_lld.py 1>${output_dir}/${name}; 
done

# 5) Time diff for no_lld
for log_file in $(find ${output_dir} -mindepth 1 -maxdepth 1 -type f -name "*hard.txt" -o -name "*soft.txt"); do 
  name=$(basename $log_file | sed -e "s/.txt/_nolld.txt/g"); 
  cat $log_file | awk 'BEGIN { FS="\t"; OFS="\t"; }{ print $1,$3,$6 }' | python3 ${scripts_dir}/time_diff_no_lld.py 1>${output_dir}/${name};
done

# 6) Time diff for logic
for log_file in $(find ${output_dir} -mindepth 1 -maxdepth 1 -type f -name "*hard.txt" -o -name "*soft.txt"); do 
  name=$(basename $log_file | sed -e "s/.txt/_logic.txt/g"); 
  cat $log_file | awk 'BEGIN { FS="\t"; OFS="\t"; }{ print $1,$3,$6 }' | python3 ${scripts_dir}/time_diff_slip_car_logic.py 1>${output_dir}/${name}; 
done

# 7) All failures
for file in $(find ${output_dir} -mindepth 1 -maxdepth 1 -type f -name "*hard_*" -o -name "*soft_*"); do 
  echo "Processing $(basename $file)" >&2; 
  cat $file | perl -e 'my $token = $ARGV[0]; my( $name, $one, $two ) = ( $token =~ /(\w+)\.(\w+)_(\w+)\./); while( my $line = <STDIN>) { chomp $line; my @info = split( "\t", $line ); print join("\t", ( @info, ($name, $one, $two))), "\n"; }' $(basename $file); 
done 1>${output_dir}/all_failures.txt

