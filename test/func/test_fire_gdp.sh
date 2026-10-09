test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle src test/unit
assert_no_stdout

run test_plot_runs python src/plot_fire_gdp.py \
    --co2_file test/data/co2.csv \
    --gdp_file test/data/gdp.csv \
    --countries Brazil Chile \
    --out fire_gdp.png
assert_exit_code 0
assert_equal fire_gdp.png $( ls fire_gdp.png )
rm -f fire_gdp.png

run test_missing_file python src/plot_fire_gdp.py \
    --co2_file no_such_file.csv \
    --gdp_file test/data/gdp.csv \
    --out fire_gdp.png
assert_exit_code 1
assert_in_stderr "Could not find"
