import yaml
from requests.auth import HTTPBasicAuth, AuthBase
import requests
from urllib import parse as escape_url
import logging
from requests.models import Response


class RaaSRest:
    """
    Use YAML file to make it easy to use basic auth to access a RaaS from workday. If you don't use yaml often
    you need to start file/section with --- and all related lines under it mast be indented. By default,
    workday.yaml in the same directory as the code calling.

    ---
     account: "Workday User"
     password: "Workday Users Password"
     tenant: "Tenant Name"
     # No ending slash
     base_url: "base URL including but ending at workday.com"
      # optional will use /ccx/service/customreport2 if not specified, no ending slash
     path: "/ccx/service/customreport2"
     # optional will use account or can be provided when getting report.
     report_owner: "Report Owner Default"

     Example:
        from workday_tools_nosrednakram.RaaSRest import RaaSRest
        import json

        # as you can select format to retrieve data It's up to you to manage/convert if needed. The result is returned
        # as a string.

        raas_data = RaaSRest().report('CR_Course_Sections')

        print(type(raas_data))
        # If you use json your returned a dictionary. If you want the data access ['Report_Entry'].
        print(type(json.loads(raas_data)))
        print(type(json.loads(raas_data)['Report_Entry']))
    """

    _core_url: str
    _auth: AuthBase
    _report_owner: str

    def __init__(self,  config_file="workday.yaml"):
        """
        Setup up the url and allows some defaults for path and will store a default report owner if one isn't
        provided in the file. The data is used for the URL called in the report method.
        """
        self.logger = logging.getLogger(__name__)

        def read_config(cf):
            with open(config_file) as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        try:
            cfg = read_config(config_file)
        except FileNotFoundError:
            print("No config file found. Default is workday.yaml, read the documentation.")
            raise

        if 'path' in cfg:
            path = cfg['path'] + '/'
        else:
            path = "/ccx/service/customreport2/"

        if cfg['environment'] == "PROD":
            cfg['base_url'] = cfg['prod_url']
        else:
            cfg['base_url'] = cfg['devel_url']

        self._core_url = cfg['base_url'] + path + cfg['tenant']
        self._auth = HTTPBasicAuth(cfg['account'], cfg['password'])

        if 'report_owner' not in cfg:
            self._report_owner = cfg['account']
        else:
            self._report_owner = cfg['report_owner']

        self.logger.info('RaaSRest initialized')


    def report(self, report, report_owner_param=None, format="json", extra_params=""):
        """
        Pull the specified RaaS report and return the result as a string using REST. You can specify the format
        report owner as well as Provide extra parameters in the extra_params section. Begin extra_params with an
        &.
        """
        if report_owner_param is None:
            report_owner = self._report_owner
        else:
            report_owner = report_owner_param
        report_owner = '/' + escape_url.quote_plus(report_owner) + '/'

        url = self._core_url + report_owner + report + '?format=' + format + extra_params
        try:
            self.logger.error('RaaSRest URL: ' + url)
            response = requests.get(url, auth=self._auth)
            if response.status_code != 200:
                self.logger.error('RaaSRest failed with status code ' + str(response.status_code))
                self.logger.error('RaaSRest response: ' + response.text)
            return response
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error connecting to {self._core_url}")
            the_response = Response()
            the_response.code = "ConnectionError"
            the_response.error_type = "ConnectionError"
            the_response.status_code = 503
            the_response._content = {'data': f'Connection error connecting to {self._core_url}'}
            return the_response
