from __future__ import print_function
import json, urllib, urllib2, pprint, ast

slack_url = "some hook url"

def send_slack(message):
    message = json.loads(message)
    print("Sending message: {}".format(message))

    # unfurling links in Slack: https://api.slack.com/docs/unfurling
    deployment_link = "<https://{0}.console.aws.amazon.com/codedeploy/home?region={0}#/deployments/{1}|{1}>".format(message['region'], message['deploymentId'])
    application_link = "<https://{0}.console.aws.amazon.com/codedeploy/home?region={0}#/applications/{1}|{1}>".format(message['region'], message['applicationName'])

    formatted_message = "Deployment {0} for project {1} updated with status {2}".format(
            deployment_link,
            application_link,
            message['status'])

    if message['status'] == "CREATED" or message['status'] == "SUCCEEDED":
        color = "good"
    elif message['status'] == "FAILED":
        color = "danger"
    else:
        color = "warning"

    # Slack message attachemnts: https://api.slack.com/docs/attachments
    title = "Deployment {}".format(message['applicationName'], message['status'])
    title_link = "https://{0}.console.aws.amazon.com/codedeploy/home?region={0}#/deployments".format(message['region'])
    attachment = [ {
        "fallback": formatted_message,
        "color": color,
        "title": title,
        "title_link": title_link,
        "text": formatted_message
        } ]
    payload = {
            "attachments": attachment,
            "unfurl_links": "true" }
    headers={'Content-type': 'application/json'}

    try:
        req = urllib2.Request(slack_url, json.dumps(payload), headers)
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print(e.code)
        print(e.read())

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    send_slack(message)
    return message

