#!/usr/bin/env python

import requests
import json
import argparse

def main():
    pipelines_parser = argparse.ArgumentParser(
        description='''
        ** Script to connect the two pipelines with Morty's service account help **
        ''',
        epilog='Author: Aris Boutselis  <aristeidis.boutselis@endclothing.com>')
    pipelines_parser.add_argument('-pass','-p', action='store', dest= 'passw', required=True,
            help="Morty's password that will authenticate the post request to \
            connect the two pipelines.")
    pipelines_parser.add_argument('-b','-branch',action='store',dest='branch',required=True,
            help = "Branch name,  that connector will try to trigger in the payload" )
    pipelines_parser.add_argument('-repo', action= 'store',dest='repo',required=True,
            help = "Repo argument for the pipelines url")
    pipelines_parser.add_argument('-custom',action= 'store_true', default=False, dest='custom',
            help = "Custom argument to invoke an api request in a custom pipeline, default value is False")
    pipelines_parser.add_argument('-selector', action='store',dest='selector',required=False,
            help = "Name of the custom pipeline that you want to trigger")
    pipelines_results = pipelines_parser.parse_args()
    payload = {}
    if pipelines_results.passw:
        url= 'https://api.bitbucket.org/2.0/repositories/endclothing/%s/pipelines/' % pipelines_results.repo
        headers =  {'content-type': 'application/json'}
        if not pipelines_results.custom:
             payload = {'target': {'ref_type': 'branch','type':'pipeline_ref_target','ref_name': pipelines_results.branch}}
        else:
            if pipelines_results.selector:
                payload= {'target':{'selector':{'type':'custom','pattern': pipelines_results.selector},'type':'pipeline_ref_target','ref_name': pipelines_results.branch,'ref_type':'branch'}}
            else:
                print("You need to define the selector's name and add the '-custom' parameter. Exiting..\n")
                pipelines_parser.print_help()
        morty_auth = ('morty-service',pipelines_results.passw)
        req = requests.post(url, data=json.dumps(payload), headers=headers, auth=morty_auth)
        if req.status_code == 201:
            print("Morty is going to trigger a new deployment...")
        else:
            print("Morty can't trigger the deployment. Exiting..")
            print(req.status_code)
            raise SystemExit
if __name__ == '__main__':
    main()
