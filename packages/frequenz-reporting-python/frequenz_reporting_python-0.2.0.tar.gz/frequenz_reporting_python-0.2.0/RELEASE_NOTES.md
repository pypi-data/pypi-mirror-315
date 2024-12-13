# Reporting Highlevel Interface Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

* Upgraded reporting client to v0.9.0
* Change from resolution to resampling_period

## New Features

* Add Readme information
* Added functionality to extract state durations and filter alerts.
* Energy metrics updated to METRIC_AC_ACTIVE_ENERGY_CONSUMED and METRIC_AC_ACTIVE_ENERGY_DELIVERED for independent tracking of consumption and production.

## Bug Fixes

* Change 0.0 to nan if there is no data available
* Enforce keyword arguments in cumulative_energy function
