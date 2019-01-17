from os.path import join
from tempfile import mkdtemp
from shutil import rmtree
from chart_inspector import get_exports
import helm, helmfile

class Deployer:
    def install(self, charts, environment):
        chart_paths = self.__fetch(charts)

        for chart_path in chart_paths:
            apply_exports(chart_path, environment)

        print("\nInstalling charts (dry-run)")
        for chart_path in chart_paths:
            install(chart_path, environment, dry_run=True)

        print("\nInstalling charts")
        for chart_path in chart_paths:
            install(chart_path, environment)

    def delete(self, charts, environment):
        chart_paths = self.__fetch(charts)

        for chart_path in chart_paths:
            apply_exports(chart_path, environment)

        print("\nDeleting charts")
        for chart_path in chart_paths:
            delete(chart_path, environment)

    def __enter__(self):
        self.__tempDir = mkdtemp()
        return self

    def __exit__(self ,type, value, traceback):
        rmtree(self.__tempDir)

    def __fetch(self, charts):
        chart_paths = []

        for name, version in charts.items():
            print("Fetching chart " + name + "-" + version)
            chart_paths.append(helm.fetch(name, version, self.__tempDir))

        return chart_paths


def apply_exports(chart_path, environment):
    for key, value in get_exports(chart_path).items():
        if key in environment:
            environment[key] += "," + value
        else:
            environment[key] = value


def install(chart_path, environment, dry_run=False):
    helmfile.charts(environment, join(chart_path, 'helmfile.yaml'), helmArgs='--dry-run' if dry_run else '--force')


def delete(chart_path, environment):
    helmfile.delete(environment, join(chart_path, 'helmfile.yaml'), purge=True)
