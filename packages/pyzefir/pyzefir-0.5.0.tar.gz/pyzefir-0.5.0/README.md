# PyZefir

Pyzefir is used to build and configure a specific class of mathematical optimization models that represent a given 
energy system. This System is clearly defined by identifying sources, transmission infrastructure and energy customers. 
The processes provided in the model are the acquisition, transfer and processing of various types of energy to meet 
the needs of consumers.

In the model, we distinguish between the supply side (energy sources) and the demand side (energy consumers). 
The key relationship that must occur in the model is the balance relation, which assumes that in each analyzed hour the 
volume of energy supplied to customers is equal to their energy demand.

The tool aims to find the solution of the optimization by determining how – with the given scenario 
assumptions – the technological structure of the given energy system will change over the next years. 
Subjects to optimize are the total cost of maintenance (operating costs), modernization (investment costs) 
and operation (variable costs) of a given energy system.

The elements of the energy system represented in the tool are energy carriers, energy sources, energy storage facilities, 
transmission infrastructure elements and energy consumers.

# Pyzefir module

Install repository from global pip index
```bash
pip install pyzefir
```

## Make setup
Check if make is already installed
```bash
make --version
```

If not, install make
```bash
sudo apt install make
```

## Make stages

Install virtual environment and all dependencies
```bash
make install
```
If you are developing pyZefir it is recommended to use editable mode.
```bash
make install EDITABLE=yes
```
which  allows you to install a package in such a way that any changes made to
the source code are immediately reflected in the installed package without the
need to reinstall it.

Run linters check (black, pylama)
```bash
make lint
```
Run unit and fast integration tests (runs lint stage before)
```bash
Make unit
```
Run integration tests (runs lint and unit stages before)
```bash
make test
```
Remove temporary files such as .venv, .mypy_cache, .pytest_cache etc.
```bash
make clean
```

## Creating project environment

You can create virtual environment using make:

```bash
make install
```

or manually:
```bash
# Create and source virtual Environment
python -m venv .venv
source .venv/bin/active

# Install all requirements and dependencies
pip install .
pip install .[dev]

# Init pre-commit hook
pre-commit install
```

## Preparation of input data
Run input structure creator
```bash
structure-creator --help

Usage: structure-creator [OPTIONS]
Options:
  -i, --input_path PATH     Input data for the creator.  [required]
  -o, --output_path PATH    Path to dump the results.  [required]
  -s, --scenario_name TEXT  Name of the scenario.  [required]
  -h, --n_hours INTEGER     N_HOURS constant.
  -y, --n_years INTEGER     N_YEARS constant.
  --help                    Show this message and exit.
```
#### E.g.

```bash
structure-creator -i pyzefir\resources\structure_creator_resources -o pyzefir\results -s base_scenario -h 8760 -y 20
```

### How structure creator resources directory must look like:
```markdown
.
└── structure_creator_resources/
    ├── lbs/
    │   ├── boiler_coal_new_lkt.xlsx
    │   ├── boiler_gas_lkt.xlsx
    │   └── ...
    ├── scenarios/
    │   └── base_scenario/
    │       ├── fractions/
    │       │   ├── boiler_coal_new_lkt.xlsx
    │       │   ├── boiler_gas_lkt.xlsx
    │       │   └── ...
    │       ├── cost_parameters.xlsx
    │       ├── fuel_parameters.xlsx
    │       ├── generation_fraction.xlsx
    │       ├── n_consumers.xlsx
    │       ├── relative_emission_limits.xlsx
    │       ├── technology_cap_limits.xlsx
    │       ├── technology_type_cap_limits.xlsx
    │       └── yearly_demand.xlsx
    ├── aggregates.xlsx
    ├── configuration.xlsx
    ├── emissions.xlsx
    ├── subsystems.xlsx
    └── transmission_fees.xlsx
```

## Simulation run

1. Prepare `config.ini` file (look at `config_example.ini` file in project directory)

:information_source: The section `create` of `config.ini` file is used for `structure creator` only, so if you're not going
to use `structure-creator` do not add the section.

2. Run `pyzefir`
```bash
pyzefir --help

Options:
  -c, --config PATH         Path to *.ini file.  [required]
  -hcd, --hash-commit-dump  Flag to include hash commit information. (only in
                            development mode)
  --help                    Show this message and exit.
```
#### E.g.

```bash
pyzefir -c pyzefir/config_basic.ini
pyzefir -c pyzefir/config_basic.ini --hash-commit-dump
```

### How pyzefir resources directory must look like:
```markdown

XLSX input
.
└── /pyzefir resources/
    ├── /scenarios/
    │   ├── scenario_1.xlsx
    │   ├── scenario_2.xlsx
    │   └── ...
    ├── capacity_factors.xlsx
    ├── conversion_rate.xlsx
    ├── demand_chunks.xlsx
    ├── fuels.xlsx
    ├── generator_types.xlsx
    ├── initial_state.xlsx
    ├── storage_types.xlsx
    └── structure.xlsx

CSV input

.
└── /pyzefir resources/
    ├── /capacity_factors/
    │   └── Profiles.csv
    ├── /conversion_rate/
    │   ├── HEAT_PUMP.csv
    │   ├── BOILER_COAL.csv
    │   └── ...
    ├── /demand_chunks/
    │   ├── Demand_Chunks.csv
    │   ├── chunk_period_1.csv
    │   ├── chunk_period_2.csv
    │   └── ...
    ├── /demand_types/
    │   ├── family.csv
    │   ├── multifamily.csv
    │   └── ...
    ├── /fuels/
    │   ├── Emission_Per_Unit.csv
    │   └── Energy_Per_Unit.csv
    ├── /generator_types/
    │   ├── Efficiency.csv
    │   ├── Emission_Reduction.csv
    │   ├── Generator_Type_Energy_Carrier.csv
    │   ├── Generator_Type_Energy_Type.csv
    │   ├── Generator_Types.csv
    │   └── Power_Utilization.csv
    ├── /initial_state/
    │   ├── Technology.csv
    │   └── TechnologyStack.csv
    ├── /storage_types/
    │   └── Parameters.csv
    ├── /structure/
    │   ├── Aggregates.csv
    │   ├── Buses.csv
    │   ├── DSR.csv
    │   ├── Emission_Fees_Emission_Types.csv
    │   ├── Emission_Types.csv
    │   ├── Energy_Types.csv
    │   ├── Generator_Binding.csv
    │   ├── Generator_Emission_Fees.csv
    │   ├── Generators.csv
    │   ├── Lines.csv
    │   ├── Power_Reserve.csv
    │   ├── Storages.csv
    │   ├── Technology_Bus.csv
    │   ├── TechnologyStack_Aggregate.csv
    │   ├── TechnologyStack_Buses_out.csv
    │   ├── TechnologyStack_Buses.csv
    │   └── Transmission_Fees.csv
    └── /scenario/
        ├── /scenario_name/
        │   ├── Constants.csv
        │   ├── Cost_Parameters.csv
        │   ├── Curtailment_Cost.csv
        │   ├── Element_Energy_Evolution_Limits.csv
        │   ├── Emission_Fees.csv
        │   ├── Energy_Source_Evolution_Limits.csv
        │   ├── Fractions.csv
        │   ├── Fuel_Availability.csv
        │   ├── Fuel_Prices.csv
        │   ├── Generation_Fraction.csv
        │   ├── N_Consumers.csv
        │   ├── Relative_Emission_Limits.csv
        │   └── Yearly_Demand.csv
        └── /another_scenario_name/
            └── ....
```