fews-3di
==========================================

Program to start `3Di <https://3diwatermanagement.com/>`_ simulations from
FEWS.


Installation and usage
----------------------

We can be installed using python 3.6+ with::

  $ pip install fews-3di

The script is called ``run-fews-3di``, you can pass ``--help`` to get usage
instructions and ``--verbose`` to get more verbose output in case of problems.

``run-fews-3di`` looks for a ``run_info.xml`` in the current directory by
default, but you can pass a different file in a different location with
``--settings``::

  $ run-fews-3di
  $ run-fews-3di --help
  $ run-fews-3di --settings /some/directory/run_info.xml


Configuration and input/output files
------------------------------------

The expected information in run_info.xml is::

  <?xml version="1.0" encoding="UTF-8"?>
  <Run xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns="http://www.wldelft.nl/fews/PI"
       xsi:schemaLocation="http://www.wldelft.nl/fews/PI
                           http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_run.xsd"
                           version="1.5">
      <startDateTime date="2020-01-26" time="10:00:00"/>
      <endDateTime date="2020-01-30" time="12:00:00"/>
      <properties>
          <string key="api_token" value="aBCd1234.5678tOkeNabcde"/>
          <string key="organisation" value="12345678abcd"/>
          <string key="modelrevision" value="abcd123456787"/>
          <string key="simulationname" value="Simulation name"/>
          <string key="save_state" value="True"/>
          <string key="fews_state_management" value="True"/>
          <string key="use_last_available_state" value="False" />
          <string key="save_state_time" value="1400"/>
          <string key="saved_state_expiry_days" value="5"/>
          <string key="rain_type" value="radar"/>
          <string key="rain_input" value="730d6675-35dd-4a35-aa9b-bfb8155f9ca7"/>
          <string key="rain_radar_multiplier" value="0.8"/>
          <string key="fews_pre_processing" value="True"/>
          <string key="lizard_results_scenario_name" value="Testsimulatie"/>
          <string key="lizard_results_scenario_uuid" value=""/>
          <string key="initial_waterlevel" value=""/>
          <string key="api_host" value=""/>
          <string key="use_lizard_timeseries_as_boundary" value=""/>
          <string key="boundary_file" value="boundary_file.json"/>
          <string key="simulation_template" value="default"/>
      </properties>
  </Run>



**Note:** ``saved_state_expiry_days`` used to be spelled as
``save_state_expiry_days``, without a "d". The example radar uuid is the Dutch
rainfall radar (NRR).

**save_state:** This option enables using and saving state files. To use a warm
state provide a text file with id in the states folder using the name
``states/3di-saved-state-id.txt``.  A cold state is supplied in a similar way
with the name: ``states/3di-cold-state-id.txt``. If this option is enabled, after
the simulation the id of the saved state at is updated in same file
``states/3di-saved-state-id.txt``.

**fews_state_management:** Can be set to `False` to overrule the filebased state
management for FEWS. Instead only stores states in the 3Di database, which can be picked
up with the option `use_last_available_state`. Default `True`.

**use_last_available_state:** To overpass the state management system and
directly take the last available state in the 3Di database the option:
``use_last_available_state`` can be set to `True`.

**save_state_time:** This parameter defines the time in the simulation
(in seconds) when the state should be saved. If left empty the end of
the simulation is used.

**saved_state_expiry_days:** The expiry time can be set to store states
for a relevant period to enable hindcasting and at the same time prevent
the usage of too much storage space.

**rain_type:** multipe rain-types can be used in the configuration:

- ``constant``

- ``radar``

- ``custom``

**rain_input:** according to the chosen rain-type, a rain input must be given
 in the configuration:

- ``constant`` --> ``integer [m/s]``

- ``radar`` --> ``lizard uuid``

- ``custom`` --> two options: ``rain_csv`` or ``rain_netcdf``. These files
  must be stored in the input directory as ``input/rain.csv`` and
  ``input/precipitation.nc``

**rain_radar_multiplier:** can be used to multiply the rain_input ``radar``
 with a constant value. This can be used to correct the radar input. The
 default value is 1.0.

**fews_pre_processing:** can be ``True`` or ``False``. Must be True if the
 results are needed in fews: additional pre_processing of the results is
 needed.

**initial_waterlevel:** can be ``min``, ``max``, or ``mean``. When specified
 the initial waterlevel raster is taken into account. If left empty no initial
 waterlevel is used in the simulation.

**initial_waterlevel:** if you want to use the initial waterlevel raster as
 defined in the settings (leave empty if no initial waterlevel is predefined):

- ``min``

- ``mean``

- ``max``

**api_host:** (optional) api_host address can be added here. If not provided
the default api_host address ("https://api.3di.live/v3.0") will be used.

**use_lizard_timeseries_as_boundary:** (optional) can be ``True`` or ``False``.
Must be True if the boundary conditions of the simulation has to be updated by
the boundary_file.json

**boundary_file:** (optional) the name of the boundary json file that will be
updated to the simulation if ``use_lizard_timeseries_as_boundary`` is ``True``.
No checks are done for the content of the file.

**simulation_template:** (optional) the name of the simulation template to be
used for the simulation. If not provided defaults to ``default``, the
simulation template generated at model creation.

Several input files are needed, they should be in the ``input`` directory
**relative** to the ``run_info.xml``:

- ``run_info.xml``

- ``input/lateral.csv``

- ``input/precipitation.nc``

- ``input/evaporation.nc``

- ``input/boundary_file.json``

- ``input/ow.nc``

- ``model/gridadmin.h5``

Output is stored in the ``output`` directory relative to the ``run_info.xml``:

- ``output/simulation.log`` (unavailable, but included in the zip)

- ``output/flow_summary.log`` (idem)

- ``output/log_files_sim_ID.zip``

- ``output/results_3di.nc``

- ``output/dischages.csv``

- ``output/ow.nc``


Development
-----------

Development happens on github. See ``DEVELOPMENT.rst`` for more information.
