# Quberneeds

Quberneeds is a small Python script that downloads [Helm charts](https://github.com/kubernetes/helm/blob/master/docs/charts.md) and runs [helmfiles](https://github.com/roboll/helmfile) embedded inside them.

Typically, a `helmfile.yaml` is not placed inside a Helm chart. Instead it is used to declaratively deploy one or more charts.  
However, for use with Quberneeds `helmfile.yaml`s are instead placed inside the chart they deploy (referencing the chart with `./`). Rather than using helmfile to group multiple charts together, here its primary purpose is to map environment variables to Helm values. This is required because Helm itself does not allow templating inside [Values Files](https://github.com/kubernetes/helm/blob/master/docs/chart_template_guide/values_files.md).

## Quberneeds input

Quberneeds takes a JSON file as input. This file lists a set of charts to download and install and a set of environment variables to set. It looks like this:

```json
{
  "charts": {
    "myrepo/mychart": "1.0.0",
    "myrepo/otherchart": "1.0.0"
  },
  "env": {
    "SOME_VAR": "some-value",
    "OTHER_VAR": "other-value"
  }
}
```

## Chart structure

A Helm chart contains a `Chart.yaml` for metadata and a `values.yaml` for configuration in its root directory.  
For use with Quberneeds you also need to place a `helmfile.yaml` here. It could look something like this:

```yaml
releases:
  - name: '{{ requiredEnv "TENANT_ID" }}-myasset'
    namespace: '{{ requiredEnv "TENANT_ID" }}'
    chart: ./

    values:
      - someConfig:
          config1: '{{ requiredEnv "MYASSET_CONFIG1" }}'
          config2: '{{ env "MYASSET_CONFIG2" | default "default-val" }}'
```

As you can see, the `helmfile.yaml` allows you to extend or override the static configuration from `values.yaml` with templated values using environment variables.

## Usage

Quberneeds takes a command (`install` or `delete`) and the path to a JSON file as command-line arguments. It can either be run from Git or using [Zero Install](http://0install.net/) to handle dependencies.

### Run from Git

Clone this Git repository, ensure that `python`, `helmfile` and `helm` are in your `PATH` and then run:

    python quberneeds.py (install|delete) file.json

### Run using Zero Install

Ensure `0install` is in your `PATH` and then run:

    0alias quberneeds http://assets.axoom.cloud/tools/quberneeds.xml
    quberneeds (install|delete) file.json

## Releasing

To package a new release of Quberneeds as a Zero Install feed run:

    0install run http://0install.net/tools/0template.xml quberneeds.xml.template version=0.1
