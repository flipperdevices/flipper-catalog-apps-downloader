import argparse
import os.path

import requests


class FlipperSuccessBuildDownloader:
    parser = argparse.ArgumentParser()
    args = None

    def __init__(self):
        self.parser.add_argument("-o", "--output", help="Output folder", required=True)
        self.parser.add_argument("-a", "--api", help="SDK API", type=str)
        self.parser.add_argument("-t", "--target", help="SDK Target", default='f7', type=str)
        self.parser.add_argument(
            "-hn", "--host", help="Resource hostname", default='https://catalog.flipperzero.one', type=str
        )
        self.parser.set_defaults(func=self.download_bundles)

    def __call__(self):
        self.args = self.parser.parse_args()
        if "func" not in self.args:
            self.parser.error("Choose something to do")
        self.args.func()

    def save_file(self, result_name: str, result: bytes):
        with open(result_name + '.zip', 'wb') as f:
            f.write(result)
        print(f'Saved build for {self.args.target} {self.args.api} into {result_name}.zip')

    def download_bundles(self):
        if not os.path.exists(self.args.output):
            os.mkdir(self.args.output)

        def get_application_versions() -> list:
            application_versions = []
            try:
                applications_response = requests.get(
                    f'{self.args.host}/api/v0/0/application',
                    params={'limit': 500, 'api': self.args.api, 'target': self.args.target},
                )
                applications_response = applications_response.json()
                applications_response = list(
                    filter(
                        lambda x: x['current_version']['current_build']['sdk']['api'] == self.args.api
                        and x['current_version']['current_build']['sdk']['target'] == self.args.target
                        and x['current_version']['status'] == 'READY',
                        applications_response,
                    )
                )
                for application in applications_response:
                    application_version_dict = application['current_version']
                    application_version_dict.update({'alias': application['alias']})
                    application_versions.append(application_version_dict)
            except Exception as ex:
                raise RuntimeError('Failed to get applications') from ex
            return application_versions

        def get_compatible_builds(application_versions: list) -> list:
            try:
                for index, application_version in enumerate(application_versions):
                    print(
                        f'({index}/{len(application_versions)}) Application: {application_version["alias"]}, '
                        f'version: {application_version["name"]}'
                    )
                    application_version_bundle_response = requests.get(
                        f'{self.args.host}/api/v0/0/application/version/{application_version["_id"]}/bundle',
                    )
                    if application_version_bundle_response.status_code != 200:
                        print(f'Bundle not found for {self.args.target} {self.args.api}')
                    else:
                        application_build_file_name = (
                            f'{self.args.output}/app-{application_version["alias"]}-'
                            f'{application_version["name"]}-'
                            f'{self.args.target}-{self.args.api}'
                        )
                        self.save_file(application_build_file_name, application_version_bundle_response.content)
            except Exception as ex:
                raise RuntimeError('Failed to get applications') from ex
            return application_versions

        print('(1/2) Getting all application versions...')
        application_versions = get_application_versions()

        print(f'(2/2) Getting compatible bundles for {len(application_versions)} versions...')
        get_compatible_builds(application_versions)


if __name__ == "__main__":
    FlipperSuccessBuildDownloader()()
