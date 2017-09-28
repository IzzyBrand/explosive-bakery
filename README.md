# explosive-bakery
Herein lies the software and test data generated by **NASA (North American Steve Association)** and **BRO (Brown Rocketry Organization)**.

## Recording thrust data
initialize a launch with **python set_options.py -n [test-name]** - this creates a json file with the rocket's data.
run **python newlaunch.py -n [test-name]** or **python newlaunch.py -j [json-file.json]** to start log test data from your Arduino based thrust test stand.

## Analyzing thrust data
run **python analyze.py -j [filename]** to run our analysis tool. run with the **-r** flag to reselect the thrust curve's endpoints.

## The thrust test stand
*coming soon*
